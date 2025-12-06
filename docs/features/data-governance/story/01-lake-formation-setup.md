# 01 - Lake Formation Access Control Setup

## 📝 Description

As a **Platform Administrator**, I want to configure AWS Lake Formation with fine-grained access controls so that data access is governed at the table and column level, ensuring users can only access data they are authorized to see.

## 🎯 Acceptance Criteria

### 1. Lake Formation Configuration
- Lake Formation enabled as the data governance layer
- Data locations registered (S3 buckets for all zones)
- Glue Data Catalog integrated with Lake Formation
- IAM role for Lake Formation administration created

### 2. Permission Model
- Role-based access implemented:
  - DataScientistRole: Read Silver/Gold zones
  - DataEngineerRole: Read/Write all zones
  - AnalystRole: Read Gold zone only
  - ServiceRole: Read specific tables only
- Table-level permissions configured
- Column-level security for PII fields

### 3. Access Grants
- Permissions granted to IAM roles, not users directly
- Grant inheritance configured appropriately
- Database CREATE permissions restricted
- Table ALTER/DROP permissions limited to admins

### 4. PII Protection
- Sensitive columns identified and tagged
- Column-level masking configured for non-prod
- Data classification tags applied
- Access to PII requires additional approval

## 🔒 Technical Constraints

- Permissions must not break existing ETL jobs
- Changes logged in CloudTrail
- Permission changes require approval workflow
- Cannot use IAM policies to bypass Lake Formation

## 📦 Dependencies

- S3 Data Lake Foundation (Data Platform Story 01)
- Glue Data Catalog (Data Platform Story 02)
- IAM roles defined for each persona
- Data classification completed

## ✅ Tasks

### Lake Formation Setup
- ⬜ Enable Lake Formation on AWS account
- ⬜ Register S3 data locations
- ⬜ Configure Lake Formation administrators
- ⬜ Set up audit logging

### Permission Configuration
- ⬜ Create permission grants for DataScientistRole
- ⬜ Create permission grants for DataEngineerRole
- ⬜ Create permission grants for AnalystRole
- ⬜ Create permission grants for ServiceRole

### Column-Level Security
- ⬜ Tag PII columns in Glue Catalog
- ⬜ Configure column-level permissions
- ⬜ Set up data masking for non-prod
- ⬜ Test PII access restrictions

### Validation
- ⬜ Test access for each role type
- ⬜ Verify denied access returns proper errors
- ⬜ Validate audit logging captures access attempts
- ⬜ Confirm ETL jobs still function with new permissions

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Permission coverage | 100% tables under Lake Formation control |
| Access accuracy | Zero unauthorized data access incidents |
| Audit completeness | All access attempts logged |
| Role adoption | All users accessing data via defined roles |

## 🔗 Related Documents

- [Security & Governance Architecture](../../../architecture/security-governance.md)
- [Data Platform Strategy - Governance](../../../architecture/data-platform-strategy.md#37-security-compliance--governance)
- [Network Security Details](../../../../infra/docs/architecture/network-security.md)

## 📚 Relevant Context

### Strategic Alignment
This story implements the **Data Governance** pillar of the three-pillar AI Governance approach per [Business Case](../../../project-context/business-case.md). Lake Formation access control is foundational to Strategic Bet #1: "Prioritize curated, governed analytics over raw data exploration in Phase 1" - ensuring data quality, building trust, and reducing risk of misinterpretation.

### Architecture Context
- **Governance Framework**: Lake Formation serves as the central data governance layer per [Architecture Overview §3.4](../../../architecture/overview.md)
- **Access Control Model**: Fine-grained permissions at table and column level with data classification tags per [Security & Governance §2.5](../../../architecture/security-governance.md)
- **RBAC Implementation**: Role-based access for DataScientist, DataEngineer, Analyst, and Service roles

### Timeline & Milestones
- Part of **Phase 1 Foundation** (Weeks 1-12) - core to "Data Platform Foundation Setup" (Weeks 2-4) per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M2: Platform Foundation** (Week 4) - Governance framework active
- Success criteria: 100% buckets under Lake Formation control, Zero unauthorized access incidents

### Key Risks & Constraints
- **R07 (Medium)**: Data breach or unauthorized access risk - Lake Formation fine-grained access controls are primary mitigation ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C10**: PII data handling must comply with Indian data protection regulations - encryption, access controls, audit logging required
- **C13**: Access to production data requires formal approval process
- **A01**: Assumes Nuvama will provide data access within first two weeks

### Data Classification
Per [Security & Governance §5.3](../../../architecture/security-governance.md):
- **Restricted**: PII fields (customer names, contact info) - enhanced controls, masking
- **Confidential**: Lead data, scores, features - encryption, access control
- **Internal**: Aggregated reports, dashboards - access logging

### Permission Matrix
Per [Security & Governance §2.5](../../../architecture/security-governance.md):
| Principal | Database | Operations |
|-----------|----------|------------|
| DataScientistRole | curated, analytics | SELECT |
| DataEngineerRole | All | ALL |
| AnalystRole | analytics | SELECT (non-PII) |
| ServiceRole | analytics (lead_scores) | SELECT |

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **AWS Lake Formation** for fine-grained access controls
- **AWS Glue Data Catalog** for metadata management and classification tags
- **AWS IAM** for role-based access control
- **AWS CloudTrail** for audit logging of all access attempts
