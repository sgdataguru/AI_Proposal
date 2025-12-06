# 02 - Self-Service Analytics Access

## 📝 Description

As a **Business Analyst**, I want self-service access to curated datasets through Amazon Athena so that I can run ad-hoc queries and build reports without requiring data engineering support for every analysis.

## 🎯 Acceptance Criteria

### 1. Athena Access
- Athena workgroup configured per team
- Query results storage with lifecycle
- Query cost controls (data scan limits)
- Saved queries library for common patterns

### 2. Dataset Access
- Access to Gold zone analytics tables:
  - lead_scores
  - lead_features (non-PII)
  - aggregated reports
- Pre-built views for common analyses
- Documentation for table schemas

### 3. QuickSight Integration
- Athena as data source in QuickSight
- Pre-built SPICE datasets for common reports
- Scheduled refresh for dashboards
- Row-level security where applicable

### 4. Governance
- Access controlled via Lake Formation
- Query logging for audit
- No access to Bronze/Silver without approval
- PII columns masked or excluded

## 🔒 Technical Constraints

- Queries run against S3 via Athena
- Cost monitoring per workgroup
- No direct S3 access for analysts
- All queries logged in CloudTrail

## 📦 Dependencies

- Lake Formation Access Control (Data Governance Story 01)
- Gold zone populated with analytics data
- Glue Catalog with table metadata
- QuickSight Enterprise license

## ✅ Tasks

### Athena Setup
- ⬜ Create analyst workgroup with cost controls
- ⬜ Configure query results S3 location
- ⬜ Set up data scan limits
- ⬜ Create saved queries library

### View Development
- ⬜ Create analyst-friendly views over Gold tables
- ⬜ Document view definitions and usage
- ⬜ Implement PII masking in views
- ⬜ Set up view refresh automation

### QuickSight Configuration
- ⬜ Connect Athena as data source
- ⬜ Create SPICE datasets for common reports
- ⬜ Configure scheduled refresh
- ⬜ Set up user groups for access control

### Training & Documentation
- ⬜ Create SQL query guide for analysts
- ⬜ Document available tables and columns
- ⬜ Create sample queries for common analyses
- ⬜ Conduct training session for analysts

### Validation
- ⬜ Test analyst access to approved tables
- ⬜ Verify denied access to restricted tables
- ⬜ Validate cost controls function correctly
- ⬜ Test QuickSight dashboard refresh

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Self-service adoption | 50% of routine analyses self-served |
| Query success rate | >95% queries complete successfully |
| Support ticket reduction | 30% fewer data request tickets |
| User satisfaction | Analyst NPS >7 |

## 🔗 Related Documents

- [Data Flows - Consumption Layer](../../../architecture/data-flows.md)
- [Security & Governance - Access Patterns](../../../architecture/security-governance.md)
- [Tech Stack - QuickSight](../../../project-context/tech-stack.md)

## 📚 Relevant Context

### Strategic Alignment
This story enables the "governed, discoverable, and high-quality data accessible across the organization" vision per [Data Platform Strategy §1.2](../../../architecture/data-platform-strategy.md). Self-service analytics supports Strategic Bet #1 by expanding access after curated, governed analytics are established.

### Architecture Context
- **Consumption Layer**: Athena provides SQL access to Gold zone per [Data Flows §6](../../../architecture/data-flows.md)
- **Access Control**: Lake Formation policies govern what analysts can query per [Security & Governance §2.5](../../../architecture/security-governance.md)
- **BI Integration**: QuickSight connected to Athena with SPICE datasets for common reports per [Architecture Overview §2.2](../../../architecture/overview.md)

### Timeline & Milestones
- Foundation established in **Phase 1** but full capability in **Phase 2** per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Phase 2 deliverable: "Curated Data Mart - Self-service access to governed client metrics" (Week 24)
- Phase 3 expands: "Self-service analytics capabilities" with experimentation framework

### Key Risks & Constraints
- **R05 (High)**: Low frontline adoption - provide training, sample queries, and simple interfaces ([Risk Register](../../../architecture/risk-constraint-register.md))
- Analysts restricted to Gold zone per governance policies
- PII columns masked or excluded for analyst access
- Query cost controls required per workgroup

### Access Patterns by Persona
Per [Data Flows §6.2](../../../architecture/data-flows.md) and [Security & Governance §2.4](../../../architecture/security-governance.md):
| Persona | Access Method | Data Scope | Governance |
|---------|---------------|------------|------------|
| Data Scientist | SageMaker, Athena | Silver/Gold | Lake Formation |
| Business Analyst | QuickSight, Athena | Gold only | Read-only |
| Data Engineer | Glue Console, Athena | All zones | Admin role |

### Analytics Enablement
Per [Data Platform Strategy §4.4](../../../architecture/data-platform-strategy.md):
- **Semantic Layer**: Curated datasets with business-friendly naming
- **Pre-built Metrics**: Common KPIs and aggregations available
- **Self-service Controls**: Governed sandbox with access controls

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon Athena** for ad-hoc SQL queries against S3
- **Amazon QuickSight** for dashboards and SPICE datasets
- **AWS Lake Formation** for fine-grained access control
- **AWS Glue Data Catalog** for table metadata and schema documentation
- **Amazon CloudWatch** for query logging and cost monitoring
