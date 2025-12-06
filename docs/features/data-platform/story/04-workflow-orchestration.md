# 04 - Workflow Orchestration with Amazon MWAA

## 📝 Description

As a **Data Engineer**, I want to set up Amazon MWAA (Managed Airflow) for workflow orchestration so that data pipelines and ML workflows can be scheduled, monitored, and managed with dependencies in a unified interface.

## 🎯 Acceptance Criteria

### 1. MWAA Environment
- MWAA environment provisioned in private VPC
- Environment class sized appropriately (mw1.small for dev, mw1.medium for prod)
- Airflow version 2.x configured
- Web server accessible via VPN/private access

### 2. DAG Structure
- Standard DAG templates created for:
  - Daily lead data ingestion pipeline
  - Bronze-to-Silver transformation workflow
  - Feature engineering pipeline
  - ML scoring pipeline
- DAGs organized by domain (data, ml, integration)
- Common utility operators for Glue, SageMaker, S3

### 3. Scheduling & Dependencies
- Cron-based scheduling for daily batch jobs
- Cross-DAG dependencies via sensors
- SLA monitoring configured
- Backfill capability for historical reruns

### 4. Monitoring & Alerting
- Airflow metrics exported to CloudWatch
- Task failure alerts via SNS/email
- DAG run history retained for 30 days
- Custom dashboard for pipeline health

## 🔒 Technical Constraints

- MWAA must run in private subnets
- No public endpoint for web server
- IAM roles for Airflow execution with least privilege
- DAG code version-controlled in Git, synced to S3

## 📦 Dependencies

- VPC with private subnets and NAT gateway
- S3 bucket for DAG storage
- Glue jobs created (Story 03)
- IAM roles for Airflow execution

## ✅ Tasks

### Infrastructure (Terraform)
- ⬜ Create MWAA environment with VPC configuration
- ⬜ Configure S3 bucket for DAGs and plugins
- ⬜ Set up IAM execution role for Airflow
- ⬜ Configure security groups for MWAA

### DAG Development
- ⬜ Create lead ingestion DAG
- ⬜ Create transformation pipeline DAG
- ⬜ Create feature engineering DAG
- ⬜ Create ML scoring DAG
- ⬜ Implement common operators module

### Monitoring
- ⬜ Configure CloudWatch metrics export
- ⬜ Set up SNS alerts for task failures
- ⬜ Create Airflow health dashboard
- ⬜ Define SLA for critical pipelines

### Validation
- ⬜ Test DAG execution end-to-end
- ⬜ Verify cross-DAG dependencies work
- ⬜ Test backfill for historical dates
- ⬜ Confirm alerting on failures

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| DAG success rate | >99% scheduled runs complete |
| SLA adherence | >95% jobs complete within SLA |
| Pipeline visibility | All runs visible in Airflow UI |
| Alert response time | Failures notified within 5 minutes |

## 🔗 Related Documents

- [Architecture Overview](../../../architecture/overview.md)
- [Data Platform Strategy - Orchestration](../../../architecture/data-platform-strategy.md)
- [Operations Guide](../../../../infra/docs/architecture/operations.md)

## 📚 Relevant Context

### Strategic Alignment
This story implements the orchestration layer supporting all data and ML workflows per [Data Platform Strategy §4.1](../../../architecture/data-platform-strategy.md). MWAA (Managed Airflow) was selected per Decision 5 for its open-source foundation, managed infrastructure, rich ecosystem, and team familiarity.

### Architecture Context
- **Orchestration Layer**: MWAA manages ETL pipelines, ML workflows, and integration jobs per [Architecture Overview §2.2](../../../architecture/overview.md)
- **Multi-step Workflows**: Coordinates Glue ETL → Feature Engineering → SageMaker Pipelines → Score Delivery per [Data Flows §2.2](../../../architecture/data-flows.md)
- **Integration with ML**: Triggers SageMaker Batch Transform for daily scoring per [Architecture Overview §6.1](../../../architecture/overview.md)

### Timeline & Milestones
- Part of **Phase 1** foundation, supports "Integration & Pilot Launch" (Weeks 8-10) per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Target: >99% DAG success rate, >95% SLA adherence
- Critical for achieving "Scores available by 6 AM daily" SLA

### Key Risks & Constraints
- **R04 (High)**: Timeline pressure - MWAA setup required early to support pipeline testing ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C03**: Production systems require VPC isolation - MWAA must run in private subnets
- **C04**: All infrastructure defined as Terraform code
- DAG code version-controlled in Git, synced to S3

### Platform Health Metrics
Per [Data Platform Strategy §6.1](../../../architecture/data-platform-strategy.md):
| Metric | Target |
|--------|--------|
| Data pipeline success rate | >99% |
| Data freshness SLA adherence | >95% |
| Mean time to recover (MTTR) | <4 hours |

### Orchestration Decision Rationale
Per [Data Platform Strategy Decision 5](../../../architecture/data-platform-strategy.md):
- **Selected**: Amazon MWAA (Managed Airflow)
- **Pros**: Open-source based, managed infrastructure, rich ecosystem, team familiarity
- **Cons**: Higher cost than Step Functions for simple workflows
- **Reversibility**: Medium - DAG code portable to other Airflow deployments

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon MWAA** for multi-step pipeline orchestration
- **AWS Step Functions** as lightweight alternative for deterministic workflows
- **Amazon CloudWatch** for Airflow metrics export
- **Amazon SNS** for task failure alerts
- **Amazon S3** for DAG storage and plugins
- **Terraform** for infrastructure as code
