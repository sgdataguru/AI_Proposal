# Data Platform Architecture Overview

**Document Owner:** Data Platform Team  
**Last Updated:** December 2024  
**Status:** Active  
**Related Documents:** [Data Platform Strategy](./data-platform-strategy.md) | [Data Flows](./data-flows.md) | [Security & Governance](./security-governance.md)

---

## 1. Executive Summary

Nuvama Financial's Data Platform is a modern, cloud-based infrastructure designed to enable AI-driven revenue transformation. The platform establishes the foundation for a trusted AI product ecosystem, starting with AI Lead Scoring and scaling to support Portfolio Review, Campaign Intelligence, Client 360, IFA Portal AI, and RM Co-Pilot capabilities.

### 1.1 Platform Vision

The platform delivers:

- **Governed, discoverable, and high-quality data** accessible across the organization
- **AI-first revenue transformation** with embedded governance-by-design
- **Scalable, auditable, and compliant infrastructure** aligned with Indian financial services regulatory requirements
- **Reusable patterns** for rapid deployment of new AI products

### 1.2 Key Outcomes

| Outcome | Target |
|---------|--------|
| Improved lead conversion | 15-25% uplift for prioritized leads |
| RM productivity gains | 20-30% increase in leads processed |
| Data freshness | Daily batch refresh (evolving to near-real-time) |
| Audit compliance | 100% traceability of data access and model decisions |
| New AI use case deployment | 50% time reduction after Phase 1 |

---

## 2. High-Level Logical Architecture

### 2.1 Architecture Diagram

```mermaid
graph TB
    subgraph "Data Sources"
        CRM[CRM System]
        CAMP[Campaign Platform]
        TRADE[Trading Systems]
        MF[Mutual Fund Data]
        PMS[PMS Data]
        PARTNER[Partner Portal]
    end

    subgraph "Ingestion Layer"
        GLUE_ING[AWS Glue ETL Jobs]
        KINESIS[Amazon Kinesis<br/>Future: Streaming]
        SFTP[SFTP/S3 Transfer]
    end

    subgraph "Storage Layer - Data Lake"
        subgraph "Bronze Zone"
            RAW[Raw Data<br/>S3: raw/]
        end
        subgraph "Silver Zone"
            CURATED[Curated Data<br/>S3: curated/]
        end
        subgraph "Gold Zone"
            ANALYTICS[Analytics Data<br/>S3: analytics/]
            FEATURES[Feature Store<br/>S3: features/]
            MODELS[Model Artifacts<br/>S3: models/]
        end
    end

    subgraph "Processing Layer"
        GLUE_PROC[AWS Glue<br/>Data Processing]
        EMR[Amazon EMR<br/>Heavy Processing]
        SAGEMAKER[Amazon SageMaker<br/>ML Training]
    end

    subgraph "Governance & Catalog"
        LAKE_FORM[AWS Lake Formation]
        GLUE_CAT[AWS Glue Data Catalog]
        KMS[AWS KMS<br/>Encryption]
    end

    subgraph "Orchestration"
        MWAA[Amazon MWAA<br/>Managed Airflow]
        STEP[AWS Step Functions]
    end

    subgraph "ML Platform"
        SM_STUDIO[SageMaker Studio]
        SM_PIPE[SageMaker Pipelines]
        SM_REG[Model Registry]
        SM_BATCH[Batch Transform]
        SM_MON[Model Monitor]
    end

    subgraph "Consumption Layer"
        API_GW[API Gateway + Lambda]
        QUICKSIGHT[Amazon QuickSight]
        ATHENA[Amazon Athena]
    end

    subgraph "Integration Targets"
        CRM_OUT[CRM Priority View]
        SALES[Inside Sales Tools]
        DASHBOARDS[Business Dashboards]
    end

    subgraph "Observability"
        CLOUDWATCH[Amazon CloudWatch]
        CLOUDTRAIL[AWS CloudTrail]
        CONFIG[AWS Config]
    end

    %% Data Source Connections
    CRM --> GLUE_ING
    CAMP --> GLUE_ING
    TRADE --> GLUE_ING
    MF --> SFTP
    PMS --> SFTP
    PARTNER --> KINESIS

    %% Ingestion to Storage
    GLUE_ING --> RAW
    KINESIS --> RAW
    SFTP --> RAW

    %% Storage Flow
    RAW --> GLUE_PROC
    GLUE_PROC --> CURATED
    CURATED --> GLUE_PROC
    GLUE_PROC --> ANALYTICS
    GLUE_PROC --> FEATURES

    %% Heavy Processing
    CURATED --> EMR
    EMR --> FEATURES

    %% ML Training
    FEATURES --> SAGEMAKER
    SAGEMAKER --> MODELS
    SM_PIPE --> SM_REG
    SM_REG --> SM_BATCH
    SM_BATCH --> ANALYTICS

    %% Governance
    LAKE_FORM --> RAW
    LAKE_FORM --> CURATED
    LAKE_FORM --> ANALYTICS
    GLUE_CAT --> LAKE_FORM
    KMS --> RAW
    KMS --> CURATED
    KMS --> ANALYTICS

    %% Orchestration
    MWAA --> GLUE_ING
    MWAA --> GLUE_PROC
    MWAA --> SM_PIPE
    STEP --> SM_BATCH

    %% Consumption
    ANALYTICS --> API_GW
    ANALYTICS --> QUICKSIGHT
    ANALYTICS --> ATHENA
    API_GW --> CRM_OUT
    API_GW --> SALES
    QUICKSIGHT --> DASHBOARDS

    %% Observability
    CLOUDWATCH --> GLUE_PROC
    CLOUDWATCH --> SAGEMAKER
    CLOUDTRAIL --> LAKE_FORM
```

### 2.2 Architecture Layers

| Layer | Purpose | Key Components |
|-------|---------|----------------|
| **Data Sources** | External systems providing data | CRM, Campaign Platform, Trading, MF, PMS, Partner Portal |
| **Ingestion** | Data acquisition and landing | AWS Glue ETL, Kinesis (future), SFTP/S3 |
| **Storage** | Persistent data storage with zones | Amazon S3 (Bronze/Silver/Gold zones) |
| **Processing** | Data transformation and enrichment | AWS Glue, Amazon EMR |
| **Governance** | Access control, catalog, encryption | Lake Formation, Glue Catalog, KMS |
| **Orchestration** | Workflow management | Amazon MWAA, Step Functions |
| **ML Platform** | Model development and deployment | SageMaker (Studio, Pipelines, Registry) |
| **Consumption** | Data access and delivery | API Gateway, QuickSight, Athena |
| **Observability** | Monitoring and audit | CloudWatch, CloudTrail, Config |

---

## 3. Major Components and Relationships

### 3.1 Data Lake Foundation

The platform uses Amazon S3 as the foundation with a **Medallion Architecture** (Bronze → Silver → Gold):

| Zone | Purpose | Data Characteristics |
|------|---------|---------------------|
| **Bronze (Raw)** | Ingestion layer | Source data preserved as-is; minimal transformation; full audit trail |
| **Silver (Curated)** | Cleansed & conformed | Deduplicated, validated, standardized schemas; business-ready structure |
| **Gold (Analytics)** | Business-aligned | Aggregated, modeled for specific use cases; dimensional models; feature stores |

### 3.2 Data Processing Engine

```mermaid
graph LR
    subgraph "ETL Processing"
        A[AWS Glue Jobs] --> B[PySpark/Python]
        B --> C[Data Quality Checks]
        C --> D[Schema Validation]
    end
    
    subgraph "Heavy Processing"
        E[Amazon EMR] --> F[Spark Clusters]
        F --> G[Feature Engineering]
    end
    
    subgraph "ML Processing"
        H[SageMaker] --> I[Training Jobs]
        I --> J[Model Artifacts]
    end
```

**Primary Processing:** AWS Glue for standard ETL workloads with built-in data quality  
**Heavy Processing:** Amazon EMR for large-scale feature engineering when required  
**ML Processing:** Amazon SageMaker for model training, validation, and deployment

### 3.3 ML Platform

The machine learning platform supports the full ML lifecycle:

| Component | Purpose | Phase |
|-----------|---------|-------|
| **SageMaker Studio** | Development environment, notebooks, EDA | All phases |
| **SageMaker Training** | Managed training jobs with tracking | All phases |
| **SageMaker Feature Store** | Centralized feature management | Phase 2+ |
| **SageMaker Pipelines** | CI/CD for ML workflows | Phase 1 (Production) |
| **Model Registry** | Version control and lifecycle management | Phase 1 (Production) |
| **Batch Transform** | Scheduled batch scoring | Phase 1 |
| **Model Monitor** | Drift detection and alerts | Phase 2+ |

### 3.4 Governance Framework

```mermaid
graph TB
    subgraph "Data Governance"
        A[AWS Lake Formation]
        B[Data Catalog]
        C[Access Policies]
        D[Column-Level Security]
    end
    
    subgraph "Security Controls"
        E[AWS KMS]
        F[IAM Roles]
        G[VPC Isolation]
        H[Secrets Manager]
    end
    
    subgraph "Audit & Compliance"
        I[CloudTrail]
        J[Config Rules]
        K[Access Logs]
    end
    
    A --> B
    A --> C
    A --> D
    E --> A
    F --> A
    I --> A
```

### 3.5 Integration Architecture

| Integration Type | Pattern | Use Case |
|------------------|---------|----------|
| **Batch File** | S3 drop → Glue trigger | Legacy system data |
| **SFTP** | AWS Transfer Family | Partner data exchange |
| **API (Inbound)** | API Gateway → Lambda → S3 | Real-time event capture |
| **API (Outbound)** | Lambda → External API | CRM score delivery |
| **Database** | Glue JDBC connections | Direct database extraction |

---

## 4. Key Design Principles

### 4.1 Core Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Governance-First** | Security and compliance embedded from design | Lake Formation policies, encryption at rest/transit |
| **Cloud-Native** | Leverage managed services for reliability | AWS managed services reduce operational overhead |
| **Scalable by Design** | Architecture supports growth without rework | Auto-scaling services, partitioning strategies |
| **Observable** | Full visibility into platform health | CloudWatch metrics, alerts, dashboards |
| **Cost-Efficient** | Optimize spend without compromising capability | Right-sizing, lifecycle policies, reserved capacity |
| **Batch-First, Streaming-Ready** | Start simple, evolve as needed | Architecture designed to add streaming without major rework |

### 4.2 Data Principles

| Principle | Application |
|-----------|-------------|
| **Single Source of Truth** | S3 data lake as canonical source |
| **Immutable Raw Data** | Bronze zone preserves original data |
| **Progressive Refinement** | Data quality improves through zones |
| **Schema Evolution** | Glue Catalog manages schema versions |
| **Lineage Tracking** | Column-level lineage via Glue |

### 4.3 Security Principles

| Principle | Application |
|-----------|-------------|
| **Least Privilege** | IAM roles with minimal required permissions |
| **Defense in Depth** | Multiple security layers (network, identity, encryption) |
| **Encryption Everywhere** | KMS encryption at rest, TLS in transit |
| **Audit Everything** | CloudTrail logging for all API actions |
| **Data Classification** | Tag-based classification and handling |

---

## 5. Architectural Decisions

### 5.1 Key Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Cloud Provider** | AWS | Aligns with organizational preference; mature ML/data services; India region availability |
| **Architecture Pattern** | Medallion (Bronze/Silver/Gold) | Progressive refinement; clear lineage; governance-friendly |
| **Processing Paradigm** | Batch-first with streaming readiness | Meets initial SLAs; lower complexity; clear upgrade path |
| **Storage Format** | Parquet with Iceberg (future) | Open format; cost-effective; supports diverse access patterns |
| **ML Platform** | Amazon SageMaker | Integrated with AWS ecosystem; managed MLOps; governance features |
| **Orchestration** | Amazon MWAA (Airflow) | Open-source based; rich ecosystem; team familiarity |
| **Data Governance** | AWS Lake Formation | Fine-grained access; catalog integration; audit support |

### 5.2 Trade-offs Acknowledged

| Decision | Trade-off | Mitigation |
|----------|-----------|------------|
| AWS-only | Vendor lock-in risk | Open formats (Parquet); abstraction layers where critical |
| Batch-first | No real-time initially | Architecture supports streaming addition |
| Managed services | Less customization | Reduces operational burden; predictable costs |
| Lake Formation | Learning curve | Training plan; phased rollout |

---

## 6. Component Interaction Patterns

### 6.1 Daily Lead Scoring Pipeline

```mermaid
sequenceDiagram
    participant CRM as CRM System
    participant S3Raw as S3 Bronze
    participant Glue as AWS Glue
    participant S3Cur as S3 Silver
    participant S3Feat as Feature Store
    participant SM as SageMaker
    participant S3Out as S3 Gold
    participant API as API Gateway
    participant CRMOut as CRM Priority View

    Note over CRM,CRMOut: Daily Lead Scoring Pipeline
    
    CRM->>S3Raw: Export leads (daily)
    S3Raw->>Glue: Trigger ETL job
    Glue->>Glue: Data quality checks
    Glue->>S3Cur: Store curated leads
    S3Cur->>Glue: Feature engineering
    Glue->>S3Feat: Store features
    S3Feat->>SM: Batch transform job
    SM->>SM: Score leads
    SM->>S3Out: Store scores
    S3Out->>API: Trigger delivery
    API->>CRMOut: Push priority scores
```

### 6.2 Model Training Pipeline

```mermaid
sequenceDiagram
    participant DS as Data Scientist
    participant Studio as SageMaker Studio
    participant S3Feat as Feature Store
    participant Train as Training Job
    participant Reg as Model Registry
    participant Approve as Approval
    participant Deploy as Batch Transform

    Note over DS,Deploy: Model Training Pipeline
    
    DS->>Studio: Develop model code
    Studio->>S3Feat: Access training features
    Studio->>Train: Submit training job
    Train->>Train: Train model
    Train->>Reg: Register model version
    Reg->>Approve: Request approval
    Approve->>Reg: Approve model
    Reg->>Deploy: Deploy to production
```

---

## 7. Environment Strategy

### 7.1 Environment Overview

| Environment | Purpose | Characteristics |
|-------------|---------|-----------------|
| **Dev/Experiment** | Exploration, prototyping | Cost-controlled, rapid iteration, masked data |
| **Test/UAT** | Validation, integration testing | Production-like config, synthetic data |
| **Production** | Live workloads | Full security, governance, monitoring |

### 7.2 AWS Account Structure

```mermaid
graph TB
    subgraph "AWS Organizations"
        ROOT[Management Account]
        
        subgraph "Workload Accounts"
            DEV[Dev Account]
            UAT[UAT Account]
            PROD[Production Account]
        end
        
        subgraph "Shared Services"
            SEC[Security Account]
            LOG[Logging Account]
            NET[Network Account]
        end
    end
    
    ROOT --> DEV
    ROOT --> UAT
    ROOT --> PROD
    ROOT --> SEC
    ROOT --> LOG
    ROOT --> NET
```

---

## 8. Future Evolution

### 8.1 Platform Evolution Path

| Phase | Capability Addition | Architecture Impact |
|-------|---------------------|---------------------|
| **Phase 1** | Lead Scoring | Foundation established |
| **Phase 2** | Portfolio Review | Multi-domain data model; continuous training |
| **Phase 3** | Campaign Intelligence | A/B testing framework; Client 360 foundation |
| **Phase 4** | Partner AI | Real-time scoring option; enterprise MLOps |

### 8.2 Technology Evolution

| Current | Future | Trigger |
|---------|--------|---------|
| Batch processing | Streaming (Kinesis) | Real-time business requirement |
| Parquet format | Apache Iceberg | ACID requirements, time travel needs |
| QuickSight | Enterprise BI integration | Organizational BI consolidation |
| CSV integration | Full API integration | CRM API readiness |

---

## 9. References

- [Data Platform Strategy](./data-platform-strategy.md)
- [Data Flows](./data-flows.md)
- [Security & Governance](./security-governance.md)
- [Component Specifications](../../infra/docs/architecture/component-specifications.md)
- [Network & Security Details](../../infra/docs/architecture/network-security.md)
- [Operations Guide](../../infra/docs/architecture/operations.md)
- [Technology Stack](../project-context/tech-stack.md)
- [Business Case](../project-context/business-case.md)
