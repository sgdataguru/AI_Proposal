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

## 📚 Relevant Context

### Strategic Alignment
This story establishes the foundational infrastructure for Strategic Bet #1: "Prioritize curated, governed analytics over raw data exploration in Phase 1" per [Data Platform Strategy](../../../architecture/data-platform-strategy.md). The S3 data lake serves as the "Single Source of Truth" for all downstream analytics and ML workloads.

### Architecture Context
- **Medallion Architecture**: Bronze/Silver/Gold zone structure per [Architecture Overview §3.1](../../../architecture/overview.md) and [Data Platform Strategy §3.1](../../../architecture/data-platform-strategy.md)
- **Storage Strategy**: S3 Standard → Intelligent-Tiering → Glacier lifecycle per [Data Platform Strategy §3.2](../../../architecture/data-platform-strategy.md)
- **Integration with Lake Formation**: S3 buckets registered for fine-grained access control per governance requirements

### Timeline & Milestones
- Part of **Phase 1** "Data Platform Foundation Setup" (Weeks 2-4) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M2: Platform Foundation** (Week 4) - Data lake operational
- Success criteria: Zone structure supports batch loads, 100% buckets under Lake Formation control

### Key Risks & Constraints
- **C02**: Data must remain in AWS Mumbai region (ap-south-1) for regulatory compliance ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C04**: All infrastructure must be defined as Terraform code (IaC)
- **A06**: AWS cloud infrastructure can be provisioned within standard timelines (1-2 weeks)
- Security: Encryption at rest (SSE-KMS), VPC endpoints for private access, bucket versioning enabled

### Storage Zone Configuration
Per [Data Platform Strategy §3.2](../../../architecture/data-platform-strategy.md):
| Zone | Purpose | Lifecycle Policy |
|------|---------|------------------|
| Bronze (raw/) | Source data preserved | S3 Standard → IA (90d) → Glacier (1y) |
| Silver (curated/) | Cleansed, conformed | S3 Standard → IA (180d) |
| Gold (analytics/) | Business-aligned | S3 Standard → IA (1y) |
| Features | ML feature store | S3 Standard (1 year retention) |
| Models | ML artifacts | S3 Standard (indefinite) |

### File Format & Partitioning
Per [Data Flows §5.3-5.4](../../../architecture/data-flows.md):
- **Default format**: Parquet with Snappy compression for analytics
- **Partitioning**: Time-based (year/month/day for raw, dt for curated)
- **Versioning**: Enabled on all buckets for recovery and audit

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon S3** as single source of truth
- **AWS Lake Formation** for registration and access control
- **AWS Glue Data Catalog** for database-per-zone metadata
- **AWS KMS** with Customer Managed Keys (CMK) for encryption
- **Terraform** for infrastructure as code
