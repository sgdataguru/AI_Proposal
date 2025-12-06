# Component Specifications

**Document Owner:** Platform Engineering Team  
**Last Updated:** December 2024  
**Status:** Active  
**Related Documents:** [Architecture Overview](../../../docs/architecture/overview.md) | [Network Security](./network-security.md) | [Operations](./operations.md)

---

## 1. Overview

This document provides detailed specifications for each infrastructure component in the Nuvama Data Platform. For each component, it covers purpose, technology rationale, configuration requirements, scalability considerations, dependencies, and cost implications.

---

## 2. Storage Components

### 2.1 Amazon S3 - Data Lake

#### Purpose and Functionality

Amazon S3 serves as the foundation of the data lake, providing:
- Centralized storage for all data assets (raw, curated, analytics)
- Foundation for the Medallion Architecture (Bronze/Silver/Gold zones)
- Storage for ML model artifacts and feature stores
- Archive storage for compliance and audit requirements

#### Technology Choice and Rationale

| Criteria | S3 Advantage |
|----------|--------------|
| **Durability** | 99.999999999% (11 9's) durability |
| **Scalability** | Unlimited storage, automatic scaling |
| **Cost** | Pay-per-use, lifecycle policies reduce costs |
| **Integration** | Native integration with all AWS analytics services |
| **Security** | KMS encryption, Lake Formation integration, access logging |

**Alternatives Considered:**
- Azure Blob Storage - Not aligned with AWS-first strategy
- HDFS - Higher operational overhead, less cost-effective

#### Configuration Requirements

```hcl
# S3 Bucket Configuration
resource "aws_s3_bucket" "data_lake" {
  bucket = "nuvama-data-platform-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = "data-platform"
    CostCenter  = "data-analytics"
  }
}

# Versioning
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.data_platform.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}
```

**Bucket Structure:**

| Prefix | Purpose | Lifecycle |
|--------|---------|-----------|
| `raw/` | Bronze zone - raw ingested data | Standard → IA (90d) → Glacier (1y) |
| `curated/` | Silver zone - cleansed data | Standard → IA (180d) |
| `analytics/` | Gold zone - business-ready data | Standard → IA (1y) |
| `features/` | ML feature store | Standard (1y retention) |
| `models/` | Model artifacts | Standard (indefinite) |
| `outputs/` | Scoring outputs | Standard → IA (90d) |
| `temp/` | Temporary processing | Expire after 7 days |
| `audit/` | Audit logs | Glacier after 90d, 7y retention |

#### Scalability Considerations

| Aspect | Design |
|--------|--------|
| **Throughput** | S3 auto-scales; no pre-provisioning needed |
| **Partitioning** | Date-based partitioning for query efficiency |
| **Request Rate** | Prefix distribution to avoid hot partitions |
| **Transfer** | S3 Transfer Acceleration for large uploads |

#### Dependencies and Integration Points

| Dependency | Purpose |
|------------|---------|
| AWS KMS | Encryption key management |
| Lake Formation | Fine-grained access control |
| Glue Data Catalog | Metadata management |
| VPC Endpoints | Private network access |
| CloudTrail | Access logging |

#### Cost Implications

| Cost Component | Estimate (Monthly) | Optimization |
|----------------|-------------------|--------------|
| Storage (Standard) | $0.023/GB | Lifecycle policies |
| Storage (IA) | $0.0125/GB | Auto-transition |
| Storage (Glacier) | $0.004/GB | Archive old data |
| PUT requests | $0.005/1000 | Batch operations |
| GET requests | $0.0004/1000 | Efficient queries |
| Data transfer (out) | $0.09/GB | VPC endpoints |

**Estimated Monthly Cost:** $500-2,000 (Phase 1), scaling with data volume

---

### 2.2 AWS Glue Data Catalog

#### Purpose and Functionality

- Central metadata repository for all data assets
- Schema management and version tracking
- Integration with query engines (Athena, Spark)
- Foundation for data discovery and governance

#### Technology Choice and Rationale

| Criteria | Glue Catalog Advantage |
|----------|------------------------|
| **Integration** | Native to AWS analytics stack |
| **Hive Compatible** | Works with existing tools |
| **Serverless** | No infrastructure management |
| **Lake Formation** | Fine-grained access via LF policies |

#### Configuration Requirements

```hcl
# Glue Database
resource "aws_glue_catalog_database" "bronze" {
  name        = "bronze_${var.environment}"
  description = "Raw data zone"
  
  location_uri = "s3://${aws_s3_bucket.data_lake.id}/raw/"
}

resource "aws_glue_catalog_database" "silver" {
  name        = "silver_${var.environment}"
  description = "Curated data zone"
  
  location_uri = "s3://${aws_s3_bucket.data_lake.id}/curated/"
}

resource "aws_glue_catalog_database" "gold" {
  name        = "gold_${var.environment}"
  description = "Analytics data zone"
  
  location_uri = "s3://${aws_s3_bucket.data_lake.id}/analytics/"
}
```

#### Cost Implications

| Cost Component | Rate | Notes |
|----------------|------|-------|
| Storage | $1.00/100K objects/month | First million free |
| Requests | $1.00/million requests | First million free |

**Estimated Monthly Cost:** $50-200

---

## 3. Processing Components

### 3.1 AWS Glue - ETL Processing

#### Purpose and Functionality

- Batch ETL for data ingestion and transformation
- Data quality checks and validation
- Schema discovery and evolution
- Serverless processing at scale

#### Technology Choice and Rationale

| Criteria | Glue Advantage |
|----------|----------------|
| **Serverless** | No cluster management |
| **Auto-scaling** | Scales to workload |
| **PySpark/Python** | Flexible development |
| **Data Quality** | Built-in DQ rules |
| **Cost** | Pay per job run |

**Alternatives Considered:**
- EMR - Higher complexity, better for very large scale
- Databricks - Higher cost, more features than needed for Phase 1

#### Configuration Requirements

```hcl
# Glue Job for Lead Ingestion
resource "aws_glue_job" "ingest_leads" {
  name     = "ingest-leads-${var.environment}"
  role_arn = aws_iam_role.glue_role.arn
  
  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
  
  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.scripts.id}/etl/ingest_leads.py"
    python_version  = "3"
  }
  
  default_arguments = {
    "--job-language"          = "python"
    "--job-bookmark-option"   = "job-bookmark-enable"
    "--enable-metrics"        = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--additional-python-modules" = "great_expectations"
    "--TempDir"               = "s3://${aws_s3_bucket.data_lake.id}/temp/"
  }
  
  timeout = 120  # minutes
  
  execution_property {
    max_concurrent_runs = 1
  }
}
```

**Job Configurations:**

| Job Type | Worker Type | Workers | Timeout | Use Case |
|----------|-------------|---------|---------|----------|
| Ingestion | G.1X | 2-5 | 60 min | Daily data loads |
| Transformation | G.1X | 3-10 | 120 min | Heavy transformations |
| Feature Engineering | G.2X | 5-10 | 180 min | ML feature computation |
| Data Quality | G.1X | 2 | 30 min | Quality validation |

#### Scalability Considerations

| Aspect | Design |
|--------|--------|
| **Horizontal** | Increase number of workers |
| **Vertical** | Use G.2X for memory-intensive jobs |
| **Concurrency** | Configure max concurrent runs |
| **Auto-scaling** | Glue auto-scales within worker count |

#### Dependencies and Integration Points

| Dependency | Purpose |
|------------|---------|
| S3 | Source and target storage |
| Glue Catalog | Metadata management |
| IAM | Job execution role |
| KMS | Encryption |
| CloudWatch | Logging and metrics |
| Lake Formation | Data access control |

#### Cost Implications

| Cost Component | Rate | Notes |
|----------------|------|-------|
| DPU-hour (ETL) | $0.44 | G.1X = 1 DPU, G.2X = 2 DPU |
| Data Catalog | Included | See Catalog section |
| Development Endpoint | $0.44/DPU-hour | Use notebooks instead |

**Estimated Monthly Cost:** $200-800 (Phase 1)

---

### 3.2 Amazon EMR (Optional - Heavy Processing)

#### Purpose and Functionality

- Large-scale data processing when Glue insufficient
- Complex feature engineering workloads
- Spark-based ML training pipelines
- Ad-hoc big data analysis

#### Technology Choice and Rationale

| Criteria | EMR Advantage |
|----------|---------------|
| **Scale** | Massive cluster capacity |
| **Flexibility** | Full Spark/Hadoop control |
| **Performance** | Optimized for large datasets |
| **Cost** | Spot instances, auto-termination |

#### Configuration Requirements

```hcl
# EMR Cluster for Heavy Processing
resource "aws_emr_cluster" "processing" {
  name          = "data-platform-processing-${var.environment}"
  release_label = "emr-6.15.0"
  applications  = ["Spark", "Hadoop", "Hive"]
  
  ec2_attributes {
    subnet_id                         = var.private_subnet_id
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr.arn
  }
  
  master_instance_group {
    instance_type = "m5.xlarge"
  }
  
  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2
    
    ebs_config {
      size = 100
      type = "gp3"
    }
  }
  
  auto_termination_policy {
    idle_timeout = 3600  # 1 hour
  }
  
  configurations_json = jsonencode([
    {
      Classification = "spark-defaults"
      Properties = {
        "spark.dynamicAllocation.enabled" = "true"
      }
    }
  ])
}
```

#### Cost Implications

| Instance Type | On-Demand | Spot (est.) | Use Case |
|---------------|-----------|-------------|----------|
| m5.xlarge | $0.192/hr | $0.06/hr | Core nodes |
| m5.2xlarge | $0.384/hr | $0.12/hr | Heavy processing |
| r5.xlarge | $0.252/hr | $0.08/hr | Memory-intensive |

**Estimated Monthly Cost:** $300-1,500 (when used)

---

## 4. Machine Learning Components

### 4.1 Amazon SageMaker

#### Purpose and Functionality

- ML model development (SageMaker Studio)
- Automated training pipelines (SageMaker Pipelines)
- Model versioning and approval (Model Registry)
- Batch inference (Batch Transform)
- Model monitoring (Model Monitor)

#### Technology Choice and Rationale

| Criteria | SageMaker Advantage |
|----------|---------------------|
| **Integration** | Native AWS data integration |
| **MLOps** | Built-in CI/CD for ML |
| **Governance** | Model Registry, lineage |
| **Managed** | Reduced operational overhead |
| **Flexibility** | Custom or built-in algorithms |

**Alternatives Considered:**
- Databricks MLflow - Higher cost, more complex setup
- Kubeflow - High operational overhead
- Open-source stack - Lack of governance features

#### Configuration Requirements

**SageMaker Domain:**

```hcl
resource "aws_sagemaker_domain" "data_platform" {
  domain_name = "data-platform-${var.environment}"
  auth_mode   = "IAM"
  vpc_id      = var.vpc_id
  subnet_ids  = var.private_subnet_ids
  
  default_user_settings {
    execution_role = aws_iam_role.sagemaker_execution.arn
    
    security_groups = [aws_security_group.sagemaker.id]
    
    kernel_gateway_app_settings {
      default_resource_spec {
        instance_type       = "ml.t3.medium"
        sagemaker_image_arn = var.sagemaker_image_arn
      }
    }
    
    jupyter_server_app_settings {
      default_resource_spec {
        instance_type = "system"
      }
    }
  }
  
  default_space_settings {
    execution_role = aws_iam_role.sagemaker_execution.arn
  }
}
```

**Model Registry:**

```hcl
resource "aws_sagemaker_model_package_group" "lead_scoring" {
  model_package_group_name        = "lead-scoring-models"
  model_package_group_description = "Lead scoring model versions"
}
```

#### Component Specifications

| Component | Purpose | Instance Type | Notes |
|-----------|---------|---------------|-------|
| **Studio** | Development | ml.t3.medium | Notebooks, EDA |
| **Training** | Model training | ml.m5.xlarge+ | Auto-scaling |
| **Processing** | Data processing | ml.m5.xlarge | Feature engineering |
| **Batch Transform** | Batch inference | ml.m5.large | Daily scoring |
| **Model Monitor** | Drift detection | ml.m5.large | Scheduled |

#### Scalability Considerations

| Aspect | Design |
|--------|--------|
| **Training** | Use spot instances, distributed training |
| **Inference** | Batch transform scales horizontally |
| **Processing** | SageMaker Processing job auto-scaling |
| **Notebooks** | On-demand instance types |

#### Dependencies and Integration Points

| Dependency | Purpose |
|------------|---------|
| S3 | Training data, model artifacts |
| IAM | Execution roles |
| VPC | Network isolation |
| KMS | Model encryption |
| CloudWatch | Metrics and logs |
| ECR | Custom containers |

#### Cost Implications

| Component | Cost | Notes |
|-----------|------|-------|
| Studio (ml.t3.medium) | $0.05/hr | On-demand |
| Training (ml.m5.xlarge) | $0.23/hr | Use Spot (~70% savings) |
| Batch Transform (ml.m5.large) | $0.115/hr | Per-transform |
| Model Monitor | $0.015/hr + data | Per-endpoint monitored |
| Processing | $0.115/hr | ml.m5.large |

**Estimated Monthly Cost:** $500-1,500 (Phase 1)

---

## 5. Orchestration Components

### 5.1 Amazon MWAA (Managed Airflow)

#### Purpose and Functionality

- Workflow orchestration for data pipelines
- ML pipeline coordination
- Dependency management between jobs
- Scheduling and monitoring

#### Technology Choice and Rationale

| Criteria | MWAA Advantage |
|----------|----------------|
| **Open Source** | Standard Airflow, portable DAGs |
| **Managed** | No infrastructure management |
| **Integration** | AWS service operators |
| **Scalability** | Auto-scaling workers |
| **Ecosystem** | Rich plugin ecosystem |

**Alternatives Considered:**
- Step Functions - Less flexible for complex DAGs
- Self-managed Airflow - Higher operational overhead
- Prefect - Less mature AWS integration

#### Configuration Requirements

```hcl
resource "aws_mwaa_environment" "data_platform" {
  name              = "data-platform-${var.environment}"
  airflow_version   = "2.8.1"
  environment_class = "mw1.small"  # Phase 1
  
  source_bucket_arn = aws_s3_bucket.airflow.arn
  dag_s3_path       = "dags/"
  
  execution_role_arn = aws_iam_role.mwaa_execution.arn
  
  network_configuration {
    security_group_ids = [aws_security_group.mwaa.id]
    subnet_ids         = var.private_subnet_ids
  }
  
  logging_configuration {
    dag_processing_logs {
      enabled   = true
      log_level = "INFO"
    }
    scheduler_logs {
      enabled   = true
      log_level = "INFO"
    }
    task_logs {
      enabled   = true
      log_level = "INFO"
    }
    webserver_logs {
      enabled   = true
      log_level = "INFO"
    }
    worker_logs {
      enabled   = true
      log_level = "INFO"
    }
  }
  
  airflow_configuration_options = {
    "core.default_timezone" = "Asia/Kolkata"
  }
  
  max_workers = 10
  min_workers = 1
}
```

#### Environment Classes

| Class | Scheduler | Workers | Use Case |
|-------|-----------|---------|----------|
| mw1.small | 1 | 1-10 | Development, Phase 1 |
| mw1.medium | 2 | 1-20 | Production, Phase 2+ |
| mw1.large | 2 | 1-50 | Heavy workloads |

#### Dependencies and Integration Points

| Dependency | Purpose |
|------------|---------|
| S3 | DAG storage, logs |
| VPC | Network isolation |
| IAM | Execution role |
| Glue | ETL job triggers |
| SageMaker | ML pipeline triggers |

#### Cost Implications

| Environment Class | Base Cost/hr | Workers/hr |
|-------------------|--------------|------------|
| mw1.small | $0.49 | $0.035/worker |
| mw1.medium | $0.98 | $0.035/worker |
| mw1.large | $1.96 | $0.035/worker |

**Estimated Monthly Cost:** $400-800 (Phase 1)

---

### 5.2 AWS Step Functions (Alternative/Complement)

#### Purpose and Functionality

- Serverless workflow orchestration
- Simple, deterministic pipelines
- Visual workflow designer
- Native AWS service integration

#### Configuration Requirements

```hcl
resource "aws_sfn_state_machine" "lead_scoring" {
  name     = "lead-scoring-pipeline-${var.environment}"
  role_arn = aws_iam_role.step_functions.arn
  
  definition = jsonencode({
    StartAt = "StartGlueJob"
    States = {
      StartGlueJob = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = {
          JobName = aws_glue_job.ingest_leads.name
        }
        Next = "StartBatchTransform"
      }
      StartBatchTransform = {
        Type     = "Task"
        Resource = "arn:aws:states:::sagemaker:createTransformJob.sync"
        Parameters = {
          "TransformJobName.$" = "States.Format('lead-scoring-{}', $$.Execution.Name)"
          ModelName            = var.model_name
        }
        End = true
      }
    }
  })
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| State transitions | $0.025 per 1000 |
| Express workflows | $1.00 per million requests |

**Estimated Monthly Cost:** $50-150

---

## 6. Analytics and Consumption Components

### 6.1 Amazon Athena

#### Purpose and Functionality

- Serverless SQL queries on S3 data
- Ad-hoc data exploration
- Dashboard data source
- Data validation queries

#### Configuration Requirements

```hcl
resource "aws_athena_workgroup" "data_platform" {
  name = "data-platform-${var.environment}"
  
  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true
    
    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.id}/results/"
      
      encryption_configuration {
        encryption_option = "SSE_KMS"
        kms_key_arn       = aws_kms_key.data_platform.arn
      }
    }
    
    engine_version {
      selected_engine_version = "Athena engine version 3"
    }
  }
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| Data scanned | $5.00 per TB |
| Savings (compressed/partitioned) | Up to 90% reduction |

**Estimated Monthly Cost:** $100-500

---

### 6.2 Amazon QuickSight

#### Purpose and Functionality

- Business intelligence dashboards
- Lead scoring visualization
- Performance monitoring
- Self-service analytics

#### Configuration Requirements

| Setting | Value | Notes |
|---------|-------|-------|
| Edition | Enterprise | SPICE, row-level security |
| Authentication | IAM Identity Center | Federated access |
| Data Sources | Athena, S3 | Via Lake Formation |
| SPICE Capacity | 10 GB initial | Scale as needed |

#### Cost Implications

| Component | Cost |
|-----------|------|
| Author (Enterprise) | $24/user/month |
| Reader | $0.30/session (max $5/month) |
| SPICE | $0.38/GB/month |

**Estimated Monthly Cost:** $200-500 (Phase 1)

---

## 7. Integration Components

### 7.1 Amazon API Gateway

#### Purpose and Functionality

- REST API for score delivery
- Integration with CRM systems
- Secure external access
- Rate limiting and throttling

#### Configuration Requirements

```hcl
resource "aws_api_gateway_rest_api" "scores" {
  name        = "lead-scores-api-${var.environment}"
  description = "API for lead score delivery"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.scores.id
  rest_api_id   = aws_api_gateway_rest_api.scores.id
  stage_name    = "v1"
  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      responseLength = "$context.responseLength"
    })
  }
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| REST API requests | $3.50 per million |
| Data transfer | $0.09/GB |
| Caching | $0.02-$3.80/hr |

**Estimated Monthly Cost:** $50-200

---

### 7.2 AWS Lambda

#### Purpose and Functionality

- Serverless compute for integrations
- Event-driven processing
- API backend
- File processing triggers

#### Configuration Requirements

```hcl
resource "aws_lambda_function" "score_delivery" {
  function_name = "score-delivery-${var.environment}"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "handler.main"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 256
  
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }
  
  tracing_config {
    mode = "Active"
  }
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| Requests | $0.20 per million |
| Duration | $0.0000166667/GB-second |
| Free tier | 1M requests, 400K GB-seconds/month |

**Estimated Monthly Cost:** $50-150

---

## 8. Security Components

### 8.1 AWS KMS

#### Purpose and Functionality

- Encryption key management
- Data encryption at rest
- Key rotation and audit

#### Configuration Requirements

```hcl
resource "aws_kms_key" "data_platform" {
  description             = "Data Platform encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM policies"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow service usage"
        Effect = "Allow"
        Principal = {
          Service = [
            "s3.amazonaws.com",
            "glue.amazonaws.com",
            "sagemaker.amazonaws.com"
          ]
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey*"
        ]
        Resource = "*"
      }
    ]
  })
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| Key storage | $1.00/key/month |
| Key usage | $0.03 per 10,000 requests |

**Estimated Monthly Cost:** $10-50

---

### 8.2 AWS Lake Formation

#### Purpose and Functionality

- Fine-grained data access control
- Column and row-level security
- Cross-account data sharing
- Data catalog permissions

#### Configuration Requirements

```hcl
resource "aws_lakeformation_permissions" "analyst_gold" {
  principal   = aws_iam_role.analyst.arn
  permissions = ["SELECT", "DESCRIBE"]
  
  table {
    database_name = aws_glue_catalog_database.gold.name
    wildcard      = true
  }
}

resource "aws_lakeformation_permissions" "data_engineer_all" {
  principal   = aws_iam_role.data_engineer.arn
  permissions = ["ALL"]
  
  database {
    name = aws_glue_catalog_database.bronze.name
  }
}
```

#### Cost Implications

Lake Formation is included with other AWS services (no additional charge).

---

## 9. Observability Components

### 9.1 Amazon CloudWatch

#### Purpose and Functionality

- Centralized logging
- Metrics and dashboards
- Alerting and alarms
- Log insights queries

#### Configuration Requirements

```hcl
# Log Groups
resource "aws_cloudwatch_log_group" "glue" {
  name              = "/aws/glue/jobs/${var.environment}"
  retention_in_days = 90
  kms_key_id        = aws_kms_key.data_platform.arn
}

# Alarms
resource "aws_cloudwatch_metric_alarm" "glue_job_failure" {
  alarm_name          = "glue-job-failure-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "glue.driver.aggregate.numFailedTasks"
  namespace           = "Glue"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Glue job has failed tasks"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

#### Cost Implications

| Cost Component | Rate |
|----------------|------|
| Log ingestion | $0.50/GB |
| Log storage | $0.03/GB |
| Metrics | $0.30/metric/month (first 10K) |
| Alarms | $0.10/alarm/month |
| Dashboards | $3.00/dashboard/month |

**Estimated Monthly Cost:** $100-300

---

## 10. Cost Summary

### Phase 1 Estimated Monthly Costs

| Component | Low Estimate | High Estimate |
|-----------|--------------|---------------|
| S3 Storage | $500 | $2,000 |
| Glue Catalog | $50 | $200 |
| Glue ETL | $200 | $800 |
| SageMaker | $500 | $1,500 |
| MWAA | $400 | $800 |
| Athena | $100 | $500 |
| QuickSight | $200 | $500 |
| API Gateway + Lambda | $100 | $350 |
| KMS | $10 | $50 |
| CloudWatch | $100 | $300 |
| **Total** | **$2,160** | **$7,000** |

### Cost Optimization Strategies

1. **Reserved Capacity:** SageMaker savings plans for predictable workloads
2. **Spot Instances:** Use for SageMaker training, EMR processing
3. **Lifecycle Policies:** Auto-transition data to cheaper storage tiers
4. **Right-sizing:** Monitor usage and adjust instance types
5. **Workgroup Limits:** Set Athena scan limits per workgroup
6. **Scheduling:** Auto-stop development resources off-hours

---

## 11. References

- [Architecture Overview](../../../docs/architecture/overview.md)
- [Network Security](./network-security.md)
- [Operations Guide](./operations.md)
- [Data Platform Strategy](../../../docs/architecture/data-platform-strategy.md)
