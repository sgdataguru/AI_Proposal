# 02 - Glue Data Catalog and Schema Management

## 📝 Description

As a **Data Engineer**, I want to set up AWS Glue Data Catalog with schema discovery and versioning so that all data assets are discoverable, documented, and maintain consistent schemas across the platform.

## 🎯 Acceptance Criteria

### 1. Database Structure
- Glue databases created for each zone:
  - `raw_db` for Bronze zone tables
  - `curated_db` for Silver zone tables
  - `analytics_db` for Gold zone tables
  - `features_db` for ML feature tables
- Database naming convention follows `{env}_{zone}_db` pattern

### 2. Table Registration
- Crawler configured for automatic schema discovery
- Initial tables registered:
  - raw_db: leads, campaigns, outcomes
  - curated_db: leads, campaigns, outcomes (conformed)
  - analytics_db: lead_scores, lead_features, reports
- Schema versioning enabled for tracking changes

### 3. Metadata Management
- Business glossary tags applied to tables
- Data classification tags (PII, Confidential, Internal) configured
- Table descriptions and column comments documented
- Data owner and steward tags assigned

### 4. Search and Discovery
- Tables searchable by name, tags, and description
- Column-level search enabled
- Integration with Lake Formation for access control metadata

## 🔒 Technical Constraints

- Glue Catalog must be encrypted with KMS
- Crawler schedules must not conflict with ETL jobs
- Schema evolution must be backward compatible
- All catalog changes logged for audit

## 📦 Dependencies

- S3 Data Lake Foundation (Story 01)
- Lake Formation configured
- IAM roles for Glue service
- KMS keys for catalog encryption

## ✅ Tasks

### Infrastructure (Terraform)
- ⬜ Create Glue databases per zone
- ⬜ Configure Glue crawlers for each data source
- ⬜ Set up crawler schedules (off-peak hours)
- ⬜ Enable Glue Data Catalog encryption

### Schema Management
- ⬜ Define initial table schemas for leads data
- ⬜ Define initial table schemas for campaign data
- ⬜ Define initial table schemas for outcome data
- ⬜ Configure schema versioning

### Metadata Enrichment
- ⬜ Create tag taxonomy (classification, ownership, sensitivity)
- ⬜ Apply tags to existing tables
- ⬜ Document column-level business definitions
- ⬜ Set up data steward assignments

### Validation
- ⬜ Verify crawler discovers new data correctly
- ⬜ Test schema evolution with sample data changes
- ⬜ Validate tag-based search functionality
- ⬜ Confirm audit logging for catalog changes

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Table registration | 100% of data assets cataloged |
| Metadata completeness | All tables have descriptions and owners |
| Schema accuracy | Crawler discovers schema correctly on first run |
| Discovery time | Users find relevant data in <30 seconds |

## 🔗 Related Documents

- [Architecture Overview](../../../architecture/overview.md)
- [Data Platform Strategy - Data Catalog](../../../architecture/data-platform-strategy.md#36-data-lineage-catalog--observability)
- [Security & Governance](../../../architecture/security-governance.md)

## 📚 Relevant Context

### Strategic Alignment
This story implements the "Governed, discoverable, and high-quality data accessible across the organization" vision from [Data Platform Strategy §1.2](../../../architecture/data-platform-strategy.md). The Glue Catalog serves as the central metadata repository enabling data discovery and schema management.

### Architecture Context
- **Catalog Integration**: Glue Catalog integrated with Lake Formation for access control metadata per [Architecture Overview §3.4](../../../architecture/overview.md)
- **Schema Management**: Schema versioning and evolution support per [Data Platform Strategy §3.6](../../../architecture/data-platform-strategy.md)
- **Data Lineage**: Column-level lineage tracking via Glue per [Data Platform Strategy §3.6](../../../architecture/data-platform-strategy.md)

### Timeline & Milestones
- Part of **Phase 1** "Data Platform Foundation Setup" (Weeks 2-4) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M2: Platform Foundation** (Week 4) - Data catalog operational
- Supports future self-service: Phase 2 delivers "Curated Data Mart" for analyst access (Week 24)

### Key Risks & Constraints
- **A17**: Assumes data quality is sufficient - catalog metadata enables quality tracking per dataset ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C04**: All infrastructure must be defined as Terraform code
- Crawler schedules must not conflict with ETL jobs (operational constraint)
- Schema evolution must be backward compatible

### Database Structure
Per [Data Platform Strategy §3.2](../../../architecture/data-platform-strategy.md):
| Database | Zone | Initial Tables |
|----------|------|----------------|
| raw_db | Bronze | leads, campaigns, outcomes |
| curated_db | Silver | leads, campaigns, outcomes (conformed) |
| analytics_db | Gold | lead_scores, lead_features, reports |
| features_db | Features | lead_features, model_features |

### Metadata & Governance Tags
Per [Security & Governance §5.3](../../../architecture/security-governance.md):
- **Data Classification**: PII, Confidential, Internal, Public
- **Ownership**: Data Steward, Technical Owner, Business Owner
- **Sensitivity**: Tags for Lake Formation column-level security

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **AWS Glue Data Catalog** for schema discovery and versioning
- **AWS Glue Crawlers** for automatic schema detection
- **AWS Lake Formation** for access control metadata integration
- **AWS KMS** for catalog encryption
- **Terraform** for infrastructure as code
