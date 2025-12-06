# Data Platform Strategy

**Document Owner:** Data Platform Team  
**Last Updated:** December 2024  
**Status:** Active  
**Related Documents:** [Value Delivery Roadmap](./value-delivery-roadmap.md) | [Risk & Constraint Register](./risk-constraint-register.md)

---

## 1. Executive Summary

### 1.1 Business Context

Nuvama Financial operates in a rapidly evolving wealth and investment landscape in India, with a growing ecosystem of Relationship Managers (RMs), Independent Financial Advisors (IFAs), and partners. As documented in the [Business Case](../project-context/business-case.md), the organization faces several critical challenges:

**Current Pain Points:**
- **Lead Prioritisation Is Not Predictive**: Leads are treated similarly despite varying intent levels, resulting in missed high-potential opportunities and inefficient RM/telesales time allocation.
- **Limited Closed-Loop Learning**: Lead outcomes are not systematically fed back into models or strategy, causing fragmented campaign and sales performance insights.
- **Scaling Constraints Across Channels**: Expansion of partner ecosystems and digital funnels increases manual effort for lead nurturing.

**Business Drivers:**
- Increasing client activation and expanding wallet share
- Improving advisor productivity
- Enabling scalable partner-assisted growth
- Diversifying acquisition channels while maintaining conversion efficiency

### 1.2 Strategic Vision

The target state is a **modern, cloud-based data platform** that bridges business needs with technical capabilities, enabling:

- **Governed, discoverable, and high-quality data** accessible across the organization
- **AI-first revenue transformation** starting with Lead Scoring and scaling to Portfolio Review, Campaign Intelligence, Client 360, IFA Portal AI, and RM Co-Pilot
- **Embedded data quality and observability** from inception
- **Scalable, auditable, and compliant infrastructure** aligned with financial services regulatory requirements in India

This platform will serve as the **foundation for a trusted AI product ecosystem**, establishing standards, data foundations, operating controls, and measurable value needed to scale confidently.

### 1.3 Expected Outcomes

| Outcome | KPI | Target |
|---------|-----|--------|
| Improved decision-making speed | Time-to-insight for lead prioritisation | Reduce from days to hours |
| Reduced reporting latency | Data freshness for scoring models | Daily batch refresh (moving to near-real-time) |
| Increased activation efficiency | Lead conversion rate for prioritised leads | 15-25% improvement over baseline |
| RM productivity gains | Leads processed per RM per day | 20-30% increase |
| Regulatory compliance | Audit readiness for data access/usage | 100% traceability |
| Reusable AI patterns | Time to deploy new AI use cases | 50% reduction after Phase 1 |

### 1.4 Strategic Bets

1. **Prioritize curated, governed analytics over raw data exploration in Phase 1**  
   *Rationale:* Ensures data quality, builds trust, and reduces risk of misinterpretation before expanding self-service capabilities.

2. **Prefer managed, cloud-native services for platform reliability and agility**  
   *Rationale:* Reduces operational overhead, leverages AWS expertise, and enables faster iteration with built-in governance features.

3. **Embed data quality and observability from inception**  
   *Rationale:* Prevents technical debt accumulation and establishes trust in AI outputs from the first deployment.

---

## 2. Business Requirements & Strategic Response

### REQ-001: Lead Prioritisation Intelligence

| Attribute | Description |
|-----------|-------------|
| **Requirement ID** | REQ-001 |
| **Statement** | Enable predictive lead scoring to identify high-intent leads early and boost conversion probability. |
| **Strategic Approach** | Build AI Lead Scoring as the foundation product with governance-by-design, establishing patterns for future AI products. |
| **Key Capabilities** | Lead score (probability/index), Priority bands (Hot/Warm/Cold), Top driver explainability, CRM integration |
| **Success Criteria** | 15-25% improvement in conversion rate for prioritised leads; RM adoption rate >80% |
| **Dependencies** | CRM/lead system access, Historical lead data (6-12 months), Business definition of "activation" |
| **Rationale** | Lead scoring requires narrower data scope than full Client 360, produces fast measurable outcomes, and introduces AI to frontline teams in a low-friction way. |

### REQ-002: Closed-Loop Learning System

| Attribute | Description |
|-----------|-------------|
| **Requirement ID** | REQ-002 |
| **Statement** | Systematically capture and feed lead outcomes back into models and strategy. |
| **Strategic Approach** | Implement feedback loops with outcome tracking, model retraining pipelines, and performance dashboards. |
| **Key Capabilities** | Outcome capture automation, Model retraining triggers, Performance drift monitoring, A/B testing framework |
| **Success Criteria** | Model performance degradation detected within 7 days; Automated retraining cycle <30 days |
| **Dependencies** | Sales outcome data access, CRM integration, Model versioning infrastructure |
| **Rationale** | Continuous learning ensures models stay relevant as market conditions and customer behaviors evolve. |

### REQ-003: Scalable Multi-Channel Support

| Attribute | Description |
|-----------|-------------|
| **Requirement ID** | REQ-003 |
| **Statement** | Support lead nurturing and prioritisation across expanding partner ecosystems and digital funnels without proportional increase in manual effort. |
| **Strategic Approach** | Build a unified data layer supporting multiple lead sources with standardized processing and scoring. |
| **Key Capabilities** | Multi-source data ingestion, Channel-agnostic scoring, Partner portal integration readiness, API-first architecture |
| **Success Criteria** | New channel onboarding time <2 weeks; Processing capacity scales with volume without manual intervention |
| **Dependencies** | Partner data agreements, API standards documentation, Channel attribution logic |
| **Rationale** | Scalability is essential as Nuvama expands its digital and partner-assisted growth channels. |

### REQ-004: AI Governance & Compliance

| Attribute | Description |
|-----------|-------------|
| **Requirement ID** | REQ-004 |
| **Statement** | Establish governance-first AI product standards with embedded controls, transparency, and monitoring. |
| **Strategic Approach** | Implement three-pillar governance: Data Governance, Model Governance, and Operational Governance. |
| **Key Capabilities** | Data ownership/access controls, Model explainability, Version tracking, Drift monitoring, Audit logs |
| **Success Criteria** | 100% auditability of scoring decisions; Zero compliance incidents; Explainability available for every score band |
| **Dependencies** | Compliance/infosec sign-off, RACI definition, Governance tooling selection |
| **Rationale** | Financial services require robust governance; this also builds internal trust and enables scaling to higher-risk models. |

---

## 3. Data Platform Strategy

### 3.1 Architecture Pattern Selection

**Selected Pattern:** Medallion Architecture (Bronze → Silver → Gold)

| Layer | Purpose | Data Characteristics |
|-------|---------|---------------------|
| **Bronze (Raw)** | Ingestion layer | Source data preserved as-is; minimal transformation; full audit trail |
| **Silver (Curated)** | Cleansed & conformed | Deduplicated, validated, standardized schemas; business-ready structure |
| **Gold (Analytics)** | Business-aligned | Aggregated, modeled for specific use cases; dimensional models; feature stores |

**Rationale for Medallion Architecture:**
- **Progressive data refinement** aligns with governance-first approach
- **Clear data lineage** from source to consumption
- **Separation of concerns** enables parallel development across layers
- **Industry-proven pattern** in financial services analytics platforms
- **Supports both batch and streaming** ingestion patterns

**Alternative Considered:** Hub-and-Spoke (rejected for Phase 1 due to higher complexity for initial use case)

### 3.2 Data Storage Tiers & Zones

```
┌─────────────────────────────────────────────────────────────────┐
│                        Amazon S3 Data Lake                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Raw Zone      │  Curated Zone   │      Analytics Zone          │
│   (Bronze)      │   (Silver)      │         (Gold)               │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ raw/leads/      │ curated/leads/  │ analytics/lead_scores/       │
│ raw/crm/        │ curated/crm/    │ analytics/features/          │
│ raw/campaigns/  │ curated/        │ analytics/reports/           │
│ raw/outcomes/   │   campaigns/    │ models/                      │
│                 │ curated/        │ outputs/                     │
│                 │   outcomes/     │                              │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

**Storage Strategy:**
- **S3 Standard**: Active/recent data (last 90 days)
- **S3 Intelligent-Tiering**: Historical data with variable access patterns
- **S3 Glacier**: Long-term audit/compliance archives (>1 year)

### 3.3 Batch vs. Streaming Strategy

**Phase 1 Position:** Batch-First with Streaming Readiness

| Pattern | Use Case | Timeline |
|---------|----------|----------|
| **Batch (Daily)** | Lead scoring, Model training, Reporting | Phase 1-2 |
| **Micro-batch (Hourly)** | High-priority lead alerts, Drift monitoring | Phase 2 |
| **Near-Real-Time** | Event-driven scoring, Campaign triggers | Phase 3+ |

**Rationale:**
- Batch processing meets initial business requirements (daily lead prioritisation)
- Lower operational complexity for PoC and early production
- Architecture designed to accommodate streaming (Kinesis) when business justifies real-time scoring
- Cost-effective starting point with clear upgrade path

### 3.4 Data Modeling Strategy

**Approach:** Business-Aligned Dimensional Models

**Core Principles:**
1. **Fact tables** for measurable events (leads, interactions, conversions, scores)
2. **Dimension tables** for descriptive attributes (lead source, channel, product, time)
3. **Slowly Changing Dimensions (SCD Type 2)** for tracking historical changes
4. **Conformed dimensions** across use cases for consistent reporting

**Initial Dimensional Model (Lead Scoring):**

| Table Type | Table Name | Key Attributes |
|------------|------------|----------------|
| Fact | fact_lead_scores | lead_id, score_date, score_value, score_band, model_version |
| Fact | fact_lead_interactions | lead_id, interaction_date, interaction_type, channel |
| Fact | fact_lead_outcomes | lead_id, outcome_date, outcome_type, conversion_flag |
| Dimension | dim_lead | lead_id, source, channel, acquisition_date, attributes |
| Dimension | dim_time | date_key, day, week, month, quarter, year |
| Dimension | dim_campaign | campaign_id, campaign_name, campaign_type, start_date |
| Dimension | dim_model | model_id, model_version, training_date, status |

### 3.5 Data Quality Controls

**Data Quality Framework:**

| Dimension | Check Type | Frequency | Action on Failure |
|-----------|------------|-----------|-------------------|
| **Completeness** | Null/missing value counts | Every load | Alert + quarantine if >5% |
| **Uniqueness** | Duplicate detection | Every load | Deduplicate + log |
| **Validity** | Schema conformance, data types | Every load | Reject invalid records |
| **Accuracy** | Business rule validation | Daily | Flag for review |
| **Timeliness** | Data freshness monitoring | Hourly | Alert if stale >6 hours |
| **Consistency** | Cross-source reconciliation | Weekly | Investigation trigger |

**Implementation:**
- AWS Glue Data Quality for automated checks
- Custom validation rules in transformation jobs
- Quality scores tracked per dataset in metadata catalog

### 3.6 Data Lineage, Catalog & Observability

**Data Catalog:** AWS Glue Data Catalog
- Schema discovery and versioning
- Business glossary integration
- Search and discovery for data assets

**Data Lineage:**
- Column-level lineage tracking via Glue
- Visual lineage dashboards
- Impact analysis for change management

**Observability Stack:**
- **Pipeline Monitoring:** Amazon CloudWatch (logs, metrics, alarms)
- **Data Quality Dashboards:** Amazon QuickSight
- **Model Performance:** SageMaker Model Monitor
- **Cost Tracking:** AWS Cost Explorer with tagged resources

### 3.7 Security, Compliance & Governance

**Security Architecture:**

| Layer | Control | Implementation |
|-------|---------|----------------|
| **Identity** | Role-based access control | AWS IAM with least privilege |
| **Data Access** | Fine-grained permissions | AWS Lake Formation |
| **Encryption** | At-rest and in-transit | AWS KMS (SSE-S3), TLS 1.2+ |
| **Secrets** | Credential management | AWS Secrets Manager |
| **Network** | Private connectivity | VPC endpoints, private subnets |
| **Audit** | Complete activity logging | AWS CloudTrail |

**Compliance Positioning:**
- Data residency in India (AWS Mumbai region)
- PII handling with encryption and access controls
- Audit logs retained for regulatory requirements
- Data retention policies aligned with business needs

**Governance Model:**
- **Data Stewards:** Business ownership of data domains
- **Platform Team:** Technical governance and standards
- **Compliance:** Oversight and audit readiness
- **RACI Matrix:** Defined for all data assets and processes

---

## 4. Technology Approach

### 4.1 Cloud Strategy

**Primary Cloud Provider:** Amazon Web Services (AWS)

**Rationale (from [Tech Stack](../project-context/tech-stack.md)):**
- Aligns with Nuvama's preference for unified, scalable cloud foundation
- Strong native capabilities for ML experimentation and governed model deployment
- Mature ecosystem for financial services controls
- Enables phased maturity from fast PoC to production scale

**Environment Strategy:**
| Environment | Purpose | Key Characteristics |
|-------------|---------|---------------------|
| **Dev/Experiment** | Exploration, prototyping | Cost-controlled, rapid iteration, masked data |
| **Test/UAT** | Validation, integration testing | Production-like config, synthetic data |
| **Production** | Live workloads | Full security, governance, monitoring |

### 4.2 Platform Capabilities

**Core Data Platform Services:**
- **Storage:** Amazon S3 (data lake foundation)
- **Processing:** AWS Glue (ETL), Amazon EMR (heavy processing)
- **Catalog:** AWS Glue Data Catalog
- **Governance:** AWS Lake Formation
- **ML Platform:** Amazon SageMaker (Studio, Pipelines, Model Registry)
- **Orchestration:** Amazon MWAA (Managed Airflow)
- **Analytics:** Amazon QuickSight

### 4.3 Integration Paradigms

**API-First Design:**
- RESTful APIs for system integration (API Gateway + Lambda)
- Event-driven patterns for asynchronous workflows (EventBridge)
- Secure file exchange for legacy systems (SFTP/S3)

**Loose Coupling Principles:**
- Service boundaries aligned with business capabilities
- Message-based communication where appropriate
- Schema registry for contract management

**Initial Integration Points:**
| System | Integration Pattern | Phase |
|--------|---------------------|-------|
| CRM | Priority view / API push | Phase 1 |
| Inside Sales Tools | Daily activation list (CSV/API) | Phase 1 |
| Campaign Platform | Audience segment sync | Phase 2 |
| Partner Portal | API integration | Phase 3 |

### 4.4 Analytics Enablement

**Semantic/Business Layer:**
- Curated datasets with business-friendly naming
- Pre-built metrics and KPIs
- Self-service access controls (governed sandbox)

**BI Strategy:**
- Amazon QuickSight for initial dashboards
- Integration path to enterprise BI tools if required
- Embedded analytics for operational users

### 4.5 Infrastructure as Code (IaC)

**Approach:** Terraform as primary IaC tool

**Principles:**
- All infrastructure defined as code
- Environment parity through parameterization
- Version-controlled infrastructure changes
- Automated testing of infrastructure changes

**Repository Structure (Aligned with [Terraform Guidelines](../..)):**
```
infra/
├── components/         # Logical infrastructure components
│   ├── networking/     # VPC, subnets, security groups
│   ├── storage/        # S3 buckets, lifecycle policies
│   ├── data-platform/  # Glue, Lake Formation, EMR
│   └── ml-platform/    # SageMaker resources
├── environments/       # Environment-specific configs
│   ├── dev/
│   ├── uat/
│   └── prod/
└── modules/           # Reusable Terraform modules
```

---

## 5. Strategic Decision Framework

### Decision 1: Architecture Pattern

| Aspect | Details |
|--------|---------|
| **Decision** | Which architecture pattern best supports our data platform needs? |
| **Options Evaluated** | 1. Medallion (Bronze/Silver/Gold) 2. Hub-and-Spoke 3. Data Mesh 4. Traditional EDW |
| **Recommended** | Medallion Architecture |
| **Pros** | Progressive refinement, clear lineage, governance-friendly, proven in financial services |
| **Cons** | Potential data duplication across zones, requires discipline in zone definitions |
| **Criteria** | Governance alignment, scalability, implementation complexity, team capability fit |
| **Reversibility** | Medium - Core pattern difficult to change, but implementation details adjustable |

### Decision 2: Batch vs. Streaming

| Aspect | Details |
|--------|---------|
| **Decision** | What data processing paradigm should we adopt? |
| **Options Evaluated** | 1. Batch-only 2. Streaming-first 3. Lambda (batch + stream) 4. Batch-first with streaming readiness |
| **Recommended** | Batch-first with streaming readiness |
| **Pros** | Lower complexity for Phase 1, cost-effective, meets current business SLAs, upgrade path clear |
| **Cons** | Won't support real-time use cases initially |
| **Criteria** | Business latency requirements, operational complexity, cost, team skills |
| **Reversibility** | High - Architecture supports streaming addition without major rework |

### Decision 3: Storage Pattern

| Aspect | Details |
|--------|---------|
| **Decision** | What storage architecture should underpin the data lake? |
| **Options Evaluated** | 1. S3 only (open formats) 2. S3 + Redshift 3. S3 + Athena 4. Lake house (Delta/Iceberg) |
| **Recommended** | S3 with Parquet/Iceberg formats, Athena for ad-hoc queries |
| **Pros** | Open formats avoid lock-in, cost-effective, scales well, supports diverse access patterns |
| **Cons** | Requires careful partitioning strategy, limited ACID without Iceberg |
| **Criteria** | Cost, flexibility, query performance, vendor independence |
| **Reversibility** | High - Format choices can evolve, Redshift can be added if needed |

### Decision 4: ML Platform

| Aspect | Details |
|--------|---------|
| **Decision** | What ML platform should support model development and deployment? |
| **Options Evaluated** | 1. SageMaker 2. Open-source stack (MLflow + Kubeflow) 3. Databricks MLflow 4. Vertex AI |
| **Recommended** | Amazon SageMaker |
| **Pros** | Integrated with AWS ecosystem, managed MLOps capabilities, strong governance features |
| **Cons** | Some vendor lock-in, costs can scale with usage |
| **Criteria** | Integration with data platform, governance capabilities, team skills, time-to-value |
| **Reversibility** | Medium - Model code portable, but pipeline/registry integration requires rework |

### Decision 5: Orchestration Tool

| Aspect | Details |
|--------|---------|
| **Decision** | What workflow orchestration tool should manage data and ML pipelines? |
| **Options Evaluated** | 1. Amazon MWAA (Managed Airflow) 2. AWS Step Functions 3. Apache Airflow (self-managed) 4. Prefect |
| **Recommended** | Amazon MWAA |
| **Pros** | Open-source based (Airflow), managed infrastructure, rich ecosystem, team familiarity |
| **Cons** | Higher cost than Step Functions for simple workflows |
| **Criteria** | Pipeline complexity needs, operational overhead, team skills, extensibility |
| **Reversibility** | Medium - DAG code portable to other Airflow deployments |

---

## 6. Success Metrics & Governance

### 6.1 Platform Health Metrics

| Metric | Target | Measurement Frequency |
|--------|--------|----------------------|
| Data pipeline success rate | >99% | Daily |
| Data freshness SLA adherence | >95% | Daily |
| Platform availability | >99.5% | Monthly |
| Mean time to recover (MTTR) | <4 hours | Per incident |
| Data quality score | >95% | Weekly |

### 6.2 Business Value Metrics

Tracked in coordination with [Value Delivery Roadmap](./value-delivery-roadmap.md):
- Lead conversion improvement
- RM productivity gains
- Time-to-insight reduction
- Model accuracy/performance

### 6.3 Review Cadence

| Review Type | Frequency | Participants |
|-------------|-----------|--------------|
| Platform health review | Weekly | Platform team |
| Data quality review | Weekly | Data stewards + Platform |
| Architecture review | Monthly | Tech leads + Architecture |
| Strategic alignment review | Quarterly | Leadership + Business |

---

## Appendix A: Glossary

See [Glossary](../project-context/glossary.md) for standard terminology definitions.

## Appendix B: References

- [Business Case](../project-context/business-case.md)
- [Technology Stack](../project-context/tech-stack.md)
- [Value Delivery Roadmap](./value-delivery-roadmap.md)
- [Risk & Constraint Register](./risk-constraint-register.md)
