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
