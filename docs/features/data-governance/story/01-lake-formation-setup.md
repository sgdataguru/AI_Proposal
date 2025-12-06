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
