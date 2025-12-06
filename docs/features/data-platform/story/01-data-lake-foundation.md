# 01 - Data Lake Foundation Setup

## 📝 Description

As a **Data Engineer**, I want to establish the foundational S3-based data lake with Bronze/Silver/Gold zones so that the platform can support progressive data refinement with clear data lineage and governance controls from inception.

## 🎯 Acceptance Criteria

### 1. S3 Bucket Structure
- S3 buckets created with proper naming convention following environment prefix (dev/uat/prod)
- Three storage zones established:
  - Bronze (raw/) - for source data preservation
  - Silver (curated/) - for cleansed and conformed data
  - Gold (analytics/) - for business-aligned aggregated data
- Additional zones created for:
  - features/ - ML feature store data
  - models/ - ML model artifacts
  - outputs/ - scoring and report outputs

### 2. Storage Configuration
- S3 Standard storage class applied for active data (last 90 days)
- S3 Intelligent-Tiering configured for historical data with variable access patterns
- S3 Glacier configured for compliance archives (>1 year)
- Lifecycle policies implemented:
  - Bronze: S3 Standard → IA (90d) → Glacier (1y)
  - Silver: S3 Standard → IA (180d)
  - Gold: S3 Standard → IA (1y)

### 3. Partitioning Strategy
- Time-based partitioning implemented (year/month/day for raw, dt for curated)
- Partition keys documented for each table type
- Parquet format used as default for analytics data
- Snappy compression enabled

### 4. Encryption & Security
- SSE-KMS encryption enabled for all buckets
- Bucket versioning enabled
- Public access blocked
- VPC endpoints configured for private access

## 🔒 Technical Constraints

- All infrastructure must be defined as Terraform code (IaC)
- AWS Mumbai region (ap-south-1) required for data residency compliance
- Must integrate with AWS Lake Formation for access control
- Bucket keys must be Customer Managed Keys (CMK)

## 📦 Dependencies

- AWS Organizations account structure
- VPC with private subnets configured
- KMS keys provisioned
- IAM roles for data platform team

## ✅ Tasks

### Infrastructure (Terraform)
- ⬜ Create S3 bucket module with zone configuration
- ⬜ Configure lifecycle policies per zone
- ⬜ Set up KMS key for data encryption
- ⬜ Configure bucket policies for VPC endpoint access
- ⬜ Enable access logging to audit bucket

### Governance Setup
- ⬜ Register buckets with Lake Formation
- ⬜ Create Glue Data Catalog database per zone
- ⬜ Document partition strategy in architecture docs

### Validation
- ⬜ Verify encryption at rest
- ⬜ Test lifecycle policy transitions
- ⬜ Validate VPC endpoint connectivity
- ⬜ Confirm Lake Formation registration

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Data ingestion success | Zone structure supports batch loads |
| Governance compliance | 100% buckets under Lake Formation control |
| Cost optimization | Lifecycle policies reducing storage costs by 30% after 6 months |

## 🔗 Related Documents

- [Architecture Overview](../../../architecture/overview.md)
- [Data Platform Strategy](../../../architecture/data-platform-strategy.md)
- [Data Flows](../../../architecture/data-flows.md)
