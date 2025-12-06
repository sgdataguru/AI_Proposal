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
