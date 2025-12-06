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

---

## Implementation Plan

### 1. Feature Overview

**Goal:** Provide self-service access to curated datasets through Amazon Athena so business analysts can run ad-hoc queries and build reports without requiring data engineering support.

**Primary User Role:** Business Analyst

**Business Value:** Enables 50% of routine analyses to be self-served, reducing data request tickets by 30% and accelerating time-to-insight.

### 2. Component Analysis & Reuse Strategy

#### Existing Components
| Component | Location | Reuse Decision |
|-----------|----------|----------------|
| Gold Zone Data | Data Platform Story 01 | **REUSE** - Query target |
| Lake Formation | Data Governance Story 01 | **REUSE** - Access control |
| QuickSight | Lead Scoring Story 07 | **EXTEND** - Analyst access |

#### New Components Required
| Component | Purpose | Priority |
|-----------|---------|----------|
| Athena Workgroups | Team-based cost control | High |
| Analyst Views | Simplified data access | High |
| Query Library | Common query patterns | Medium |
| Training Materials | User enablement | Medium |

### 3. Affected Files

#### Infrastructure (Terraform)
| File Path | Action | Description |
|-----------|--------|-------------|
| `infra/modules/athena-workgroup/main.tf` | [CREATE] | Workgroup module |
| `infra/modules/athena-workgroup/cost-controls.tf` | [CREATE] | Cost limits |

#### SQL Views
| File Path | Action | Description |
|-----------|--------|-------------|
| `src/analytics/views/analyst_lead_scores.sql` | [CREATE] | Lead scores view |
| `src/analytics/views/analyst_conversion.sql` | [CREATE] | Conversion view |
| `src/analytics/queries/common_queries.sql` | [CREATE] | Query library |

#### Documentation
| File Path | Action | Description |
|-----------|--------|-------------|
| `docs/analytics/self-service-guide.md` | [CREATE] | User guide |
| `docs/analytics/table-dictionary.md` | [CREATE] | Table documentation |

### 4. Component Breakdown

#### 4.1 Workgroup Configuration

| Workgroup | Team | Data Scan Limit | Query Timeout |
|-----------|------|-----------------|---------------|
| analyst-workgroup | Business Analysts | 100 GB/day | 30 minutes |
| datascience-workgroup | Data Scientists | 500 GB/day | 2 hours |

#### 4.2 Analyst-Friendly Views

```sql
-- Simplified lead scores view (PII masked)
CREATE OR REPLACE VIEW analyst_lead_scores AS
SELECT 
    lead_id,
    score_value,
    score_band,
    model_version,
    score_date,
    -- PII columns excluded
    lead_source,
    lead_channel,
    acquisition_date
FROM analytics_db.lead_scores
WHERE score_date >= DATE_SUB(CURRENT_DATE, 90);
```

### 5. Implementation Steps

#### Phase 1: Athena Setup (Week 16-18)
- [ ] **Step 1.1:** Create analyst workgroup with cost controls
- [ ] **Step 1.2:** Configure query results S3 location
- [ ] **Step 1.3:** Set up data scan limits
- [ ] **Step 1.4:** Create saved queries library

#### Phase 2: View Development (Week 18-20)
- [ ] **Step 2.1:** Create analyst-friendly views over Gold tables
- [ ] **Step 2.2:** Document view definitions and usage
- [ ] **Step 2.3:** Implement PII masking in views
- [ ] **Step 2.4:** Set up view refresh automation

#### Phase 3: Training & Documentation (Week 20-22)
- [ ] **Step 3.1:** Create SQL query guide for analysts
- [ ] **Step 3.2:** Document available tables and columns
- [ ] **Step 3.3:** Create sample queries for common analyses
- [ ] **Step 3.4:** Conduct training session for analysts

### 6. Dependencies & Prerequisites

| Dependency | Source | Status |
|------------|--------|--------|
| Lake Formation Access Control | Data Governance Story 01 | Required |
| Gold zone populated | Lead Scoring Story 05 | Required |
| Glue Catalog | Data Platform Story 02 | Required |
| QuickSight Enterprise | Infrastructure | Required |
