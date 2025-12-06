# Preferred Technology Stack (AWS) – AI Lead Scoring (Experiment → Production)

## Cloud Platform

### Primary Cloud Provider: **Amazon Web Services (AWS)**

**Rationale**:
- Aligns with Nuvama’s preference for a unified, scalable cloud foundation for AI and data products.
- Strong native capabilities for **ML experimentation, governed model deployment, and secure data access**.
- Mature ecosystem for **financial services** controls: encryption, audit logging, fine-grained IAM, and policy-as-code.
- Enables phased maturity:
  - **Fast PoC builds**
  - **Controlled production rollout**
  - **Reusable blueprint** for Portfolio Review, Campaign Intelligence, Client 360, IFA Portal AI, and RM Co-Pilot.

---

## Environment Strategy

### Two Dedicated AWS Environments

1. **Experiment / PoC Environment**
   - Lightweight, cost-controlled, rapid iteration.
   - Designed for **data exploration, feature engineering, and model prototyping**.
   - Uses anonymised or masked datasets where feasible.

2. **Production Environment**
   - Enforces **security, governance, reliability, and monitoring**.
   - Supports stable batch scoring and integration into CRM/activation workflows.
   - Designed for scale and auditability.

**Recommended account setup**:
- Use **AWS Organizations** with separate accounts:
  - **Dev/Experiment**
  - **Test/UAT**
  - **Production**
- Centralised security and billing guardrails.

---

## Core Data Stack (Both Environments)

### Storage & Data Lake
- **Amazon S3**
  - Single source of truth for:
    - Raw leads data
    - Enriched features
    - Scoring outputs
    - Model artefacts
  - Folder convention:
    - `raw/`, `curated/`, `features/`, `models/`, `outputs/`

### Metadata & Governance
- **AWS Glue Data Catalog**
  - Registers datasets and schema versions.
- **AWS Lake Formation**
  - Fine-grained access controls for sensitive data.

### Processing
- **AWS Glue (ETL)**
  - Batch extraction and transformation.
- **Amazon EMR (optional)**
  - For heavier feature engineering at scale.

---

## Machine Learning Stack

### Experiment / PoC ML Tooling
- **Amazon SageMaker Studio**
  - Notebooks for exploration, EDA, and feature prototyping.
- **SageMaker Training Jobs**
  - Automated training runs with tracked parameters.
- **SageMaker Feature Store (optional for PoC)**
  - Useful if early standardisation of reusable lead features is desired.

**Why this works for a 5-week PoC**:
- Enables rapid build-test cycles.
- Minimal infrastructure overhead.
- Easy migration path to production-grade workflows.

---

### Production ML Tooling
- **Amazon SageMaker Pipelines**
  - Reproducible and versioned ML workflows:
    - Ingest → Feature build → Train → Evaluate → Approve.
- **SageMaker Model Registry**
  - Controls model versioning and lifecycle:
    - `Staging` → `Approved` → `Archived`.
- **SageMaker Batch Transform**
  - Recommended for Lead Scoring:
    - Daily/hourly scoring jobs with predictable cost.
- **SageMaker Model Monitor (optional initially)**
  - Drift and data quality monitoring.

---

## Orchestration & Integration

### Workflow Orchestration
- **Amazon MWAA (Managed Airflow)**
  - Preferred for multi-step pipelines across data + ML.
- **AWS Step Functions**
  - Lightweight alternative for deterministic batch workflows.

### API / System Integration
- **Amazon API Gateway + AWS Lambda**
  - If CRM supports API-based ingestion of scores.
- **SFTP/secure file delivery**
  - For CSV-based integration in early phases.
- **Amazon EventBridge (optional)**
  - For event-driven triggers later.

---

## Security & Compliance Baseline

### Identity & Access
- **AWS IAM**
  - Least privilege with role-based access for:
    - Data engineers
    - Data scientists
    - Platform admins
    - Business users

### Secrets
- **AWS Secrets Manager**
  - CRM credentials, API tokens.

### Encryption
- **AWS KMS**
  - Encryption at rest for S3, Glue, SageMaker.
- TLS for data in transit.

### Audit & Monitoring
- **AWS CloudTrail**
  - Full audit logs for API actions.
- **Amazon CloudWatch**
  - Logs, metrics, alarms for pipelines and batch jobs.
- **AWS Config**
  - Policy compliance checks (optional but recommended).

---

## Observability & Analytics

### Dashboards
- **Amazon QuickSight**
  - PoC dashboards:
    - Lead volume
    - Score band distribution
    - Early activation indicators
  - Can be replaced/extended with existing enterprise BI later.

---

## CI/CD & Infrastructure as Code

### Code & Pipelines
- **AWS CodeCommit / GitHub (as preferred)**
- **AWS CodeBuild + CodePipeline**
  - Automated deployment of:
    - Data jobs
    - SageMaker pipelines
    - Lambda/APIs

### IaC
- **Terraform or AWS CloudFormation**
  - Repeatable environment builds and audit-ready infrastructure.

---

## Recommended Tech Stack Summary (At-a-Glance)

### Experiment / PoC (Week 1–5)
- **S3** (raw/curated/features)
- **Glue** (ETL jobs)
- **SageMaker Studio** (notebooks)
- **SageMaker Training** (model builds)
- **QuickSight** (PoC reporting)
- **CloudWatch + CloudTrail**
- Simple integration via **CSV export** or **Lambda**

### Production (Post-PoC Scale)
- **S3 + Lake Formation + Glue Catalog**
- **SageMaker Pipelines**
- **Model Registry**
- **Batch Transform**
- **MWAA / Step Functions**
- **API Gateway + Lambda** (if moving to API-based CRM ingest)
- **KMS, Secrets Manager**
- **CloudWatch, CloudTrail, Config**
- **CodePipeline + Terraform/CloudFormation**

---

## Why This Stack Is Ideal for Lead Scoring First

- **Fast to start** with minimal setup.
- **Governance-friendly** via registry, approvals, and audit logs.
- **Scales cleanly** to future AI levers:
  - Portfolio Review Engine
  - Campaign Intelligence
  - Client 360° Data Lake
  - IFA / Partner Portal AI
  - RM AI Co-Pilot

---

## Optional Future Enhancements

- **Real-time scoring**
  - **Kinesis + Lambda + SageMaker Endpoints**
- **Unified Client 360**
  - S3-based lake + curated layers, with stronger Lake Formation policies.
- **Advanced experimentation**
  - A/B testing frameworks and uplift models embedded into Campaign Intelligence.

---

**Document type:** Preferred Technology Stack  
**Use case focus:** AI Lead Scoring & Activation (Experiment → Production)  
**Cloud standard:** AWS
