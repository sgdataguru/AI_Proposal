# Data Flows Architecture

**Document Owner:** Data Platform Team  
**Last Updated:** December 2025  
**Status:** Active  
**Related Documents:** [Architecture Overview](./overview.md) | [Security & Governance](./security-governance.md) | [Data Platform Strategy](./data-platform-strategy.md)

---

## 1. Overview

This document describes the end-to-end data flows within the Nuvama Data Platform, covering ingestion patterns, transformation pipelines, storage strategies, and consumption layers. The platform implements a Medallion Architecture with batch-first processing, designed to support AI-led revenue transformation.

---

## 2. End-to-End Data Flow Diagrams

### 2.1 High-Level Data Flow

```mermaid
flowchart LR
    subgraph Sources["Data Sources"]
        S1[CRM/Lead Systems]
        S2[Campaign Platform]
        S3[Trading Systems]
        S4[Portfolio Data]
        S5[Partner Portal]
    end
    
    subgraph Ingestion["Ingestion Layer"]
        I1[Batch ETL]
        I2[File Transfer]
        I3[Event Stream]
    end
    
    subgraph Storage["Data Lake - S3"]
        subgraph Bronze["Bronze Zone"]
            B1[Raw Leads]
            B2[Raw Campaigns]
            B3[Raw Trades]
            B4[Raw Portfolio]
        end
        
        subgraph Silver["Silver Zone"]
            SV1[Curated Leads]
            SV2[Curated Campaigns]
            SV3[Curated Portfolio]
        end
        
        subgraph Gold["Gold Zone"]
            G1[Lead Scores]
            G2[Features]
            G3[Reports]
            G4[Model Outputs]
        end
    end
    
    subgraph Processing["Processing"]
        P1[Data Quality]
        P2[Transformation]
        P3[Feature Eng.]
        P4[ML Scoring]
    end
    
    subgraph Consumption["Consumption"]
        C1[CRM Integration]
        C2[BI Dashboards]
        C3[APIs]
        C4[Analytics]
    end
    
    S1 --> I1
    S2 --> I1
    S3 --> I2
    S4 --> I2
    S5 --> I3
    
    I1 --> B1
    I1 --> B2
    I2 --> B3
    I2 --> B4
    I3 --> B1
    
    B1 --> P1
    B2 --> P1
    B3 --> P1
    B4 --> P1
    
    P1 --> P2
    P2 --> SV1
    P2 --> SV2
    P2 --> SV3
    
    SV1 --> P3
    SV2 --> P3
    SV3 --> P3
    
    P3 --> G2
    G2 --> P4
    P4 --> G1
    P4 --> G4
    
    G1 --> C1
    G1 --> C2
    G3 --> C2
    G4 --> C3
    SV1 --> C4
```

### 2.2 Lead Scoring Data Flow (Phase 1)

```mermaid
flowchart TB
    subgraph Sources["Source Systems"]
        CRM[CRM System]
        CAMP[Campaign Platform]
        OUTCOME[Sales Outcomes]
    end
    
    subgraph Ingestion["Daily Ingestion - AWS Glue"]
        EXT_LEADS[Extract Leads]
        EXT_CAMP[Extract Campaigns]
        EXT_OUT[Extract Outcomes]
    end
    
    subgraph Bronze["Bronze Zone - S3"]
        RAW_LEADS[s3://bucket/raw/leads/]
        RAW_CAMP[s3://bucket/raw/campaigns/]
        RAW_OUT[s3://bucket/raw/outcomes/]
    end
    
    subgraph DQ["Data Quality - AWS Glue DQ"]
        DQ_CHECK[Quality Checks]
        DQ_QUARANTINE[Quarantine Zone]
        DQ_LOG[Quality Logs]
    end
    
    subgraph Transform["Transformation - AWS Glue"]
        DEDUP[Deduplication]
        CONFORM[Schema Conformance]
        ENRICH[Data Enrichment]
    end
    
    subgraph Silver["Silver Zone - S3"]
        CUR_LEADS[s3://bucket/curated/leads/]
        CUR_CAMP[s3://bucket/curated/campaigns/]
        CUR_OUT[s3://bucket/curated/outcomes/]
    end
    
    subgraph Features["Feature Engineering"]
        FEAT_ENG[Feature Pipeline]
        FEAT_STORE[s3://bucket/features/lead_features/]
    end
    
    subgraph ML["ML Scoring - SageMaker"]
        BATCH[Batch Transform]
        MODEL[Lead Scoring Model]
    end
    
    subgraph Gold["Gold Zone - S3"]
        SCORES[s3://bucket/analytics/lead_scores/]
        REPORTS[s3://bucket/analytics/reports/]
    end
    
    subgraph Output["Integration Output"]
        API[API Gateway]
        CRM_UPDATE[CRM Priority View]
        DASH[QuickSight Dashboard]
    end
    
    CRM --> EXT_LEADS
    CAMP --> EXT_CAMP
    OUTCOME --> EXT_OUT
    
    EXT_LEADS --> RAW_LEADS
    EXT_CAMP --> RAW_CAMP
    EXT_OUT --> RAW_OUT
    
    RAW_LEADS --> DQ_CHECK
    RAW_CAMP --> DQ_CHECK
    RAW_OUT --> DQ_CHECK
    
    DQ_CHECK -->|Pass| DEDUP
    DQ_CHECK -->|Fail| DQ_QUARANTINE
    DQ_CHECK --> DQ_LOG
    
    DEDUP --> CONFORM
    CONFORM --> ENRICH
    
    ENRICH --> CUR_LEADS
    ENRICH --> CUR_CAMP
    ENRICH --> CUR_OUT
    
    CUR_LEADS --> FEAT_ENG
    CUR_CAMP --> FEAT_ENG
    CUR_OUT --> FEAT_ENG
    
    FEAT_ENG --> FEAT_STORE
    
    FEAT_STORE --> BATCH
    MODEL --> BATCH
    
    BATCH --> SCORES
    SCORES --> REPORTS
    
    SCORES --> API
    API --> CRM_UPDATE
    REPORTS --> DASH
```

---

## 3. Data Ingestion Patterns

### 3.1 Ingestion Pattern Overview

| Pattern | Description | Use Case | Frequency | Technology |
|---------|-------------|----------|-----------|------------|
| **Batch ETL** | Scheduled extraction and load | CRM, Campaign data | Daily/Hourly | AWS Glue |
| **File Drop** | File-based data transfer | Legacy systems, Partner data | As available | S3 + Lambda trigger |
| **SFTP Transfer** | Secure file exchange | External partners | Scheduled | AWS Transfer Family |
| **Database Extract** | Direct database connection | Transactional systems | Daily | Glue JDBC |
| **API Polling** | REST API extraction | Modern systems | Scheduled | Lambda + EventBridge |
| **Event Streaming** | Real-time event capture | Future: Portal events | Continuous | Kinesis (Phase 3+) |

### 3.2 Batch Ingestion Flow

```mermaid
sequenceDiagram
    participant Source as Source System
    participant Glue as AWS Glue Job
    participant S3Raw as S3 Bronze
    participant Catalog as Glue Catalog
    participant CW as CloudWatch
    
    Note over Source,CW: Scheduled Batch Ingestion (Daily)
    
    Glue->>Source: Connect via JDBC/API
    Source-->>Glue: Return data
    Glue->>Glue: Apply extraction logic
    Glue->>Glue: Convert to Parquet
    Glue->>S3Raw: Write to Bronze zone
    Glue->>Catalog: Update table metadata
    Glue->>CW: Log metrics & status
    
    alt Success
        CW->>CW: Log success
    else Failure
        CW->>CW: Trigger alert
    end
```

### 3.3 File Drop Ingestion Flow

```mermaid
sequenceDiagram
    participant Ext as External System
    participant S3Land as S3 Landing Zone
    participant Lambda as Lambda Trigger
    participant Glue as AWS Glue Job
    participant S3Raw as S3 Bronze
    participant SNS as SNS Notification
    
    Note over Ext,SNS: Event-Driven File Ingestion
    
    Ext->>S3Land: Upload file (CSV/JSON)
    S3Land->>Lambda: S3 event trigger
    Lambda->>Lambda: Validate file format
    Lambda->>Glue: Start Glue job
    Glue->>S3Land: Read file
    Glue->>Glue: Transform to Parquet
    Glue->>S3Raw: Write to Bronze
    Glue->>S3Land: Move file to processed/
    Glue->>SNS: Send completion notification
```

### 3.4 Real-Time Streaming (Future State)

```mermaid
flowchart LR
    subgraph Sources["Event Sources"]
        WEB[Web Events]
        APP[App Events]
        PARTNER[Partner API]
    end
    
    subgraph Streaming["Kinesis Streaming"]
        KDS[Kinesis Data Streams]
        KDF[Kinesis Data Firehose]
    end
    
    subgraph Processing["Stream Processing"]
        LAMBDA[Lambda Processing]
        KDA[Kinesis Analytics]
    end
    
    subgraph Storage["Storage"]
        S3RT[S3 Real-time Zone]
        S3BATCH[S3 Bronze Zone]
    end
    
    WEB --> KDS
    APP --> KDS
    PARTNER --> KDS
    
    KDS --> LAMBDA
    KDS --> KDF
    KDS --> KDA
    
    LAMBDA --> S3RT
    KDF --> S3BATCH
    KDA --> S3RT
```

---

## 4. Data Transformation and Processing Pipeline

### 4.1 Processing Stages

```mermaid
flowchart TB
    subgraph Stage1["Stage 1: Landing"]
        L1[Raw File/Extract]
        L2[Format Validation]
        L3[File Cataloging]
    end
    
    subgraph Stage2["Stage 2: Quality"]
        Q1[Completeness Check]
        Q2[Uniqueness Check]
        Q3[Validity Check]
        Q4[Consistency Check]
    end
    
    subgraph Stage3["Stage 3: Curation"]
        C1[Deduplication]
        C2[Type Casting]
        C3[Null Handling]
        C4[Schema Conformance]
    end
    
    subgraph Stage4["Stage 4: Enrichment"]
        E1[Reference Lookup]
        E2[Derived Fields]
        E3[Business Rules]
    end
    
    subgraph Stage5["Stage 5: Feature Engineering"]
        F1[Aggregations]
        F2[Time Windows]
        F3[Categorical Encoding]
        F4[Feature Scaling]
    end
    
    L1 --> L2 --> L3
    L3 --> Q1 --> Q2 --> Q3 --> Q4
    Q4 --> C1 --> C2 --> C3 --> C4
    C4 --> E1 --> E2 --> E3
    E3 --> F1 --> F2 --> F3 --> F4
```

### 4.2 Data Quality Framework

| Dimension | Check Type | Threshold | Action on Failure |
|-----------|------------|-----------|-------------------|
| **Completeness** | Null/missing value counts | >5% nulls in key fields | Alert + quarantine records |
| **Uniqueness** | Duplicate detection on key | Any duplicates | Deduplicate + log |
| **Validity** | Data type validation | Any type mismatch | Reject invalid records |
| **Accuracy** | Business rule validation | Per-rule threshold | Flag for review |
| **Timeliness** | Data freshness | >6 hours stale | Alert operations |
| **Consistency** | Cross-source reconciliation | >1% variance | Investigation trigger |

### 4.3 Transformation Rules by Zone

#### Bronze to Silver Transformations

| Transformation | Description | Implementation |
|----------------|-------------|----------------|
| **Deduplication** | Remove duplicate records | Glue DynamicFrame dedupe |
| **Type Casting** | Standardize data types | Schema mapping |
| **Null Handling** | Apply default values or flags | Coalesce functions |
| **Date Normalization** | Standardize date formats | Date parsing functions |
| **Schema Conformance** | Apply target schema | Glue schema evolution |
| **Data Masking** | Mask sensitive fields for non-prod | Lake Formation masking |

#### Silver to Gold Transformations

| Transformation | Description | Implementation |
|----------------|-------------|----------------|
| **Aggregation** | Compute summary metrics | GroupBy operations |
| **Joins** | Combine related datasets | Broadcast joins for dimensions |
| **Calculations** | Derived business metrics | UDF functions |
| **Pivoting** | Reshape data for analysis | Pivot operations |
| **Feature Computation** | ML-ready feature vectors | Feature engineering pipeline |

### 4.4 ETL Job Configuration

```mermaid
flowchart LR
    subgraph Config["Job Configuration"]
        CATALOG[Glue Catalog]
        PARAMS[Job Parameters]
        CONN[Connections]
    end
    
    subgraph Runtime["Job Runtime"]
        WORKERS[Worker Nodes]
        DPU[Data Processing Units]
        TIMEOUT[Timeout Settings]
    end
    
    subgraph Output["Job Output"]
        TARGET[Target Tables]
        METRICS[Job Metrics]
        BOOKMARKS[Job Bookmarks]
    end
    
    CATALOG --> WORKERS
    PARAMS --> WORKERS
    CONN --> WORKERS
    
    WORKERS --> TARGET
    WORKERS --> METRICS
    WORKERS --> BOOKMARKS
```

**Standard Job Parameters:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Worker Type | G.1X / G.2X | Based on data volume |
| Number of Workers | 2-10 (auto-scaling) | Scale with data |
| Job Timeout | 2-4 hours | Prevent runaway jobs |
| Job Bookmark | Enabled | Incremental processing |
| Retry Attempts | 3 | Handle transient failures |

---

## 5. Data Storage Strategy

### 5.1 Storage Tier Overview

```mermaid
flowchart TB
    subgraph Hot["Hot Storage (S3 Standard)"]
        H1[Active Data<br/>Last 90 days]
        H2[Frequent Access]
        H3[Low Latency Queries]
    end
    
    subgraph Warm["Warm Storage (S3 IA)"]
        W1[Recent Historical<br/>90 days - 1 year]
        W2[Periodic Access]
        W3[Analytics Workloads]
    end
    
    subgraph Cold["Cold Storage (S3 Glacier)"]
        C1[Archive Data<br/>> 1 year]
        C2[Compliance/Audit]
        C3[Rare Access]
    end
    
    Hot -->|Lifecycle Rule| Warm
    Warm -->|Lifecycle Rule| Cold
```

### 5.2 Storage Configuration by Zone

| Zone | Storage Class | Lifecycle Policy | Encryption | Versioning |
|------|---------------|------------------|------------|------------|
| **Bronze** | S3 Standard → IA (90d) → Glacier (1y) | 7 year retention | SSE-KMS | Enabled |
| **Silver** | S3 Standard → IA (180d) | 3 year retention | SSE-KMS | Enabled |
| **Gold** | S3 Standard → IA (1y) | 2 year retention | SSE-KMS | Enabled |
| **Features** | S3 Standard | 1 year retention | SSE-KMS | Enabled |
| **Models** | S3 Standard | Indefinite | SSE-KMS | Enabled |

### 5.3 Partitioning Strategy

```
s3://data-platform-bucket/
├── raw/
│   └── leads/
│       └── year=2024/
│           └── month=12/
│               └── day=01/
│                   └── data.parquet
├── curated/
│   └── leads/
│       └── dt=2024-12-01/
│           └── part-00000.parquet
├── analytics/
│   └── lead_scores/
│       └── score_date=2024-12-01/
│           └── model_version=v1.2/
│               └── scores.parquet
└── features/
    └── lead_features/
        └── snapshot_date=2024-12-01/
            └── features.parquet
```

**Partition Keys by Table:**

| Table | Partition Keys | Rationale |
|-------|----------------|-----------|
| Raw Leads | year, month, day | Time-based ingestion |
| Curated Leads | dt (date) | Daily processing |
| Lead Scores | score_date, model_version | Track by scoring run |
| Features | snapshot_date | Point-in-time features |
| Outcomes | outcome_date | Time-series analysis |

### 5.4 File Format Standards

| Format | Use Case | Compression | Benefits |
|--------|----------|-------------|----------|
| **Parquet** | Analytics, ML | Snappy | Columnar, efficient queries |
| **JSON** | Raw ingestion | GZIP | Schema flexibility |
| **CSV** | Legacy integration | GZIP | Compatibility |
| **Avro** | Schema evolution | Snappy | Schema in file |

---

## 6. Data Access Patterns and Consumption Layers

### 6.1 Consumption Architecture

```mermaid
flowchart TB
    subgraph Gold["Gold Zone - S3"]
        SCORES[Lead Scores]
        REPORTS[Aggregated Reports]
        FEATURES[Feature Store]
    end
    
    subgraph Access["Access Layer"]
        ATHENA[Amazon Athena<br/>Ad-hoc SQL]
        REDSHIFT[Redshift Spectrum<br/>Future: Complex Analytics]
        API[API Gateway + Lambda<br/>Application Integration]
        DIRECT[Direct S3 Access<br/>ML Training]
    end
    
    subgraph Consumers["Consumers"]
        QUICKSIGHT[QuickSight<br/>Dashboards]
        CRM[CRM System<br/>Priority Lists]
        ANALYSTS[Business Analysts<br/>Self-Service]
        ML[ML Training<br/>SageMaker]
    end
    
    SCORES --> ATHENA
    SCORES --> API
    REPORTS --> ATHENA
    FEATURES --> DIRECT
    
    ATHENA --> QUICKSIGHT
    ATHENA --> ANALYSTS
    API --> CRM
    DIRECT --> ML
```

### 6.2 Access Patterns by Persona

| Persona | Access Method | Data Scope | Governance |
|---------|---------------|------------|------------|
| **Data Scientist** | SageMaker Studio, Athena | All zones (dev), Silver/Gold (prod) | Lake Formation policies |
| **Data Engineer** | Glue Console, Athena | All zones | Admin IAM role |
| **Business Analyst** | QuickSight, Athena | Gold zone only | Read-only Lake Formation |
| **Application** | API Gateway | Specific datasets | Service account |
| **External System** | SFTP/API | Defined exports | Limited scope |

### 6.3 Query Patterns

#### Ad-hoc Analytics (Athena)

```sql
-- Example: Lead score distribution query
SELECT 
    score_band,
    COUNT(*) as lead_count,
    AVG(score_value) as avg_score
FROM analytics.lead_scores
WHERE score_date = DATE '2024-12-01'
GROUP BY score_band
ORDER BY avg_score DESC;
```

#### API Response Pattern

```json
{
  "leadId": "L12345",
  "score": 0.87,
  "scoreBand": "Hot",
  "topDrivers": [
    {"feature": "engagement_score", "contribution": 0.35},
    {"feature": "recency_days", "contribution": 0.28},
    {"feature": "channel_quality", "contribution": 0.22}
  ],
  "modelVersion": "v1.2",
  "scoreDate": "2024-12-01"
}
```

### 6.4 Integration Patterns

#### CRM Integration Flow

```mermaid
sequenceDiagram
    participant Gold as Gold Zone (S3)
    participant Lambda as Lambda Function
    participant API as API Gateway
    participant CRM as CRM System
    
    Note over Gold,CRM: Score Delivery to CRM
    
    Gold->>Lambda: S3 event (new scores)
    Lambda->>Lambda: Format priority list
    Lambda->>API: POST /scores/batch
    API->>CRM: Batch update scores
    CRM-->>API: Acknowledge
    API-->>Lambda: Success response
    Lambda->>Gold: Update delivery status
```

#### Batch Export Pattern

```mermaid
flowchart LR
    subgraph Export["Export Pipeline"]
        ATHENA[Athena Query]
        S3OUT[S3 Output]
        TRANSFER[AWS Transfer]
    end
    
    subgraph External["External Consumption"]
        SFTP[SFTP Server]
        EMAIL[Email Notification]
    end
    
    ATHENA -->|CTAS| S3OUT
    S3OUT --> TRANSFER
    TRANSFER --> SFTP
    TRANSFER --> EMAIL
```

---

## 7. Data Lineage and Metadata

### 7.1 Lineage Tracking

```mermaid
flowchart LR
    subgraph Source["Source Lineage"]
        S1[CRM.leads]
        S2[Campaign.interactions]
        S3[Sales.outcomes]
    end
    
    subgraph Bronze["Bronze Lineage"]
        B1[raw.leads]
        B2[raw.interactions]
        B3[raw.outcomes]
    end
    
    subgraph Silver["Silver Lineage"]
        C1[curated.leads]
        C2[curated.interactions]
        C3[curated.outcomes]
    end
    
    subgraph Gold["Gold Lineage"]
        G1[analytics.lead_features]
        G2[analytics.lead_scores]
    end
    
    S1 -->|ETL Job: ingest_leads| B1
    S2 -->|ETL Job: ingest_interactions| B2
    S3 -->|ETL Job: ingest_outcomes| B3
    
    B1 -->|ETL Job: curate_leads| C1
    B2 -->|ETL Job: curate_interactions| C2
    B3 -->|ETL Job: curate_outcomes| C3
    
    C1 -->|Pipeline: feature_engineering| G1
    C2 -->|Pipeline: feature_engineering| G1
    C3 -->|Pipeline: feature_engineering| G1
    
    G1 -->|SageMaker: batch_scoring| G2
```

### 7.2 Metadata Management

| Metadata Type | Storage | Purpose |
|---------------|---------|---------|
| **Technical Metadata** | Glue Data Catalog | Schema, partitions, statistics |
| **Operational Metadata** | CloudWatch Logs | Job runs, errors, metrics |
| **Business Metadata** | Data Catalog Tags | Ownership, classification, glossary |
| **Lineage Metadata** | Glue Lineage | Data flow tracking |
| **Quality Metadata** | S3 + Athena | Quality scores, issues |

---

## 8. Performance Optimization

### 8.1 Query Optimization

| Technique | Application | Impact |
|-----------|-------------|--------|
| **Partitioning** | Time-based queries | 10-100x faster |
| **Columnar Format** | Analytics queries | 50-90% less data scan |
| **Compression** | All storage | 3-5x storage reduction |
| **Predicate Pushdown** | Filter operations | Reduced data transfer |
| **Bucketing** | Join operations | Faster joins |

### 8.2 Pipeline Optimization

| Technique | Application | Benefit |
|-----------|-------------|---------|
| **Incremental Processing** | Daily loads | Process only new data |
| **Job Bookmarks** | Glue ETL | Track processed data |
| **Parallel Processing** | Large datasets | Scale horizontally |
| **Broadcast Joins** | Dimension tables | Efficient small table joins |
| **Caching** | Repeated queries | Faster response |

---

## 9. References

- [Architecture Overview](./overview.md)
- [Security & Governance](./security-governance.md)
- [Data Platform Strategy](./data-platform-strategy.md)
- [Component Specifications](../../infra/docs/architecture/component-specifications.md)
- [Operations Guide](../../infra/docs/architecture/operations.md)
