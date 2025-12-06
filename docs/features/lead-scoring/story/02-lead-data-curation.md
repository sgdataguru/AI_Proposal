# 02 - Lead Data Curation Pipeline

## 📝 Description

As a **Data Analyst**, I want lead data to be cleansed, deduplicated, and conformed to a standard schema in the Silver zone so that I can trust the data quality for analysis and model training.

## 🎯 Acceptance Criteria

### 1. Data Quality Transformations
- Deduplication based on lead_id (keep most recent)
- Null handling:
  - Required fields: reject if null
  - Optional fields: apply default values or flags
- Data type casting to standard types
- Date normalization to ISO 8601 format

### 2. Schema Conformance
- Standard lead schema applied:
  - lead_id (string, PK)
  - lead_source (string, enum)
  - lead_channel (string, enum)
  - acquisition_date (timestamp)
  - contact_email (string, masked in non-prod)
  - contact_phone (string, masked in non-prod)
  - engagement_score (decimal)
  - lead_status (string, enum)
  - last_updated (timestamp)
- Schema version tracked in Glue Catalog

### 3. Data Quality Scoring
- Quality score computed per batch:
  - Completeness score (% non-null required fields)
  - Validity score (% records passing business rules)
  - Uniqueness score (% unique records)
- Quality metrics logged to CloudWatch
- Quality dashboard updated

### 4. Output to Silver Zone
- Data written to `s3://bucket/curated/leads/dt=YYYY-MM-DD/`
- Parquet format with Snappy compression
- Glue Catalog table updated automatically

## 🔒 Technical Constraints

- PII masking applied in non-production environments
- Transformation logic version-controlled
- Failed records routed to quarantine with reason codes
- Processing must be idempotent (re-runnable)

## 📦 Dependencies

- Lead Data Ingestion (Lead Scoring Story 01)
- Glue ETL Framework (Data Platform Story 03)
- Data quality rules defined with business

## ✅ Tasks

### Transformation Development
- ⬜ Implement deduplication logic
- ⬜ Create null handling functions
- ⬜ Build schema conformance mapper
- ⬜ Implement date normalization

### Data Quality
- ⬜ Define completeness rules for lead data
- ⬜ Define validity rules (enum values, formats)
- ⬜ Implement quality scoring function
- ⬜ Create quarantine routing logic

### Pipeline Integration
- ⬜ Create Glue job for Bronze-to-Silver transformation
- ⬜ Integrate with Airflow DAG
- ⬜ Set up data quality metrics export
- ⬜ Configure quality alerts

### Validation
- ⬜ Test with known data quality issues
- ⬜ Verify deduplication accuracy
- ⬜ Confirm PII masking in non-prod
- ⬜ Validate quality scores against manual review

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Data quality pass rate | >95% records passing all checks |
| Deduplication accuracy | 100% duplicates removed |
| Processing latency | Complete within 1 hour of Bronze load |
| Quality score tracking | Scores available for each batch |

## 🔗 Related Documents

- [Data Flows Architecture](../../../architecture/data-flows.md)
- [Data Platform Strategy - Data Quality](../../../architecture/data-platform-strategy.md#35-data-quality-controls)
- [Security & Governance - Data Classification](../../../architecture/security-governance.md)
