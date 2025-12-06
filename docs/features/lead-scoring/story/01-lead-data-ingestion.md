# 01 - Lead Data Ingestion Pipeline

## 📝 Description

As a **Data Engineer**, I want to build an automated pipeline to ingest lead data from the CRM system into the data lake's Bronze zone so that lead information is available for scoring and analytics on a daily basis.

## 🎯 Acceptance Criteria

### 1. Data Extraction
- Daily automated extraction from CRM system
- Support for both full load (initial) and incremental load (daily)
- Extraction captures:
  - Lead demographic information
  - Lead source and channel data
  - Lead engagement signals
  - Lead status and timestamps
- Data format: CSV/JSON from CRM, converted to Parquet for storage

### 2. Bronze Zone Landing
- Data lands in `s3://bucket/raw/leads/year=YYYY/month=MM/day=DD/`
- Original data preserved without transformation
- File-level metadata captured (extraction timestamp, source system, record count)
- Duplicate file detection to prevent re-processing

### 3. Initial Quality Checks
- Record count validation against source
- Schema validation (expected columns present)
- Basic completeness check (non-null lead_id)
- Quarantine zone for malformed files

### 4. Integration Pattern
- Phase 1: SFTP/S3 file drop integration (CSV)
- Phase 2 readiness: API-based extraction via Lambda
- Trigger: S3 event notification or scheduled Glue job
- Retry logic for transient failures

## 🔒 Technical Constraints

- CRM credentials stored in Secrets Manager
- Extraction must not impact CRM performance (off-peak hours)
- PII fields encrypted at rest
- All extractions logged for audit trail

## 📦 Dependencies

- S3 Data Lake Foundation (Data Platform Story 01)
- Glue ETL Framework (Data Platform Story 03)
- CRM system data access approved
- Network connectivity to CRM (VPN/Direct Connect)

## ✅ Tasks

### Data Extraction
- ⬜ Document CRM data schema and extraction fields
- ⬜ Create extraction script (SFTP download or API call)
- ⬜ Implement incremental extraction logic (timestamp-based)
- ⬜ Configure scheduling for off-peak hours

### Pipeline Development
- ⬜ Create Glue job for CSV-to-Parquet conversion
- ⬜ Implement S3 event trigger for file processing
- ⬜ Add file validation and quarantine logic
- ⬜ Set up extraction metrics logging

### Infrastructure
- ⬜ Configure AWS Transfer Family for SFTP (if needed)
- ⬜ Create Lambda trigger for S3 events
- ⬜ Set up CloudWatch alarms for extraction failures
- ⬜ Store CRM credentials in Secrets Manager

### Validation
- ⬜ Test full load extraction
- ⬜ Test incremental extraction
- ⬜ Verify data in Bronze zone matches source
- ⬜ Confirm audit logging captures all operations

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Extraction reliability | >99% daily extractions successful |
| Data freshness | Lead data available by 6 AM daily |
| Record accuracy | 100% records extracted vs. source count |
| Processing time | Extraction completes within 30 minutes |

## 🔗 Related Documents

- [Data Flows Architecture](../../../architecture/data-flows.md)
- [Business Case - Lead Scoring](../../../project-context/business-case.md)
- [Value Delivery Roadmap - Phase 1](../../../architecture/value-delivery-roadmap.md)

## 📚 Relevant Context

### Strategic Alignment
This story directly supports **REQ-001: Lead Prioritisation Intelligence** from the [Data Platform Strategy](../../../architecture/data-platform-strategy.md), which establishes lead scoring as the foundation product with governance-by-design. The business case positions lead data ingestion as critical infrastructure for the "Experiment → Production" path outlined in the 5-week PoC plan.

### Architecture Context
- **Medallion Architecture**: Data lands in the Bronze (raw) zone as the first stage of progressive refinement ([Architecture Overview §3.1](../../../architecture/overview.md))
- **Ingestion Patterns**: Supports both Batch ETL and File Drop patterns as defined in [Data Flows §3](../../../architecture/data-flows.md)
- **Storage Strategy**: Uses S3 Standard for active data with lifecycle transitions to IA (90 days) and Glacier (1 year) per [Data Platform Strategy §3.2](../../../architecture/data-platform-strategy.md)

### Timeline & Milestones
- Part of **Phase 1 Foundation** (Weeks 1-12) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M2: Platform Foundation** (Week 4) - Data lake operational
- Daily lead data availability by 6 AM supports the Phase 1 SLA requirement

### Key Risks & Constraints
- **R01 (Critical)**: Historical lead data quality gaps may impact model accuracy - mitigate by implementing quality checks in ingestion ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R03 (High)**: CRM integration delays - start with CSV/file-based integration per mitigation strategy
- **C02**: Data must remain in AWS Mumbai region (ap-south-1) for regulatory compliance
- **C04**: All infrastructure must be defined as Terraform code

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **AWS Glue** for batch ETL extraction and transformation
- **Amazon S3** for Bronze zone storage (`raw/leads/`)
- **AWS Transfer Family** for SFTP integration if required
- **AWS Secrets Manager** for CRM credential storage
