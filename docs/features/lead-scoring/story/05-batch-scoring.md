# 05 - Batch Scoring Pipeline

## 📝 Description

As an **Operations Manager**, I want lead scores to be generated automatically on a daily basis so that RMs and inside sales teams have fresh prioritization data every morning to guide their outreach activities.

## 🎯 Acceptance Criteria

### 1. Scoring Pipeline
- Daily batch scoring using SageMaker Batch Transform
- Scores generated for all active leads
- Pipeline triggered after feature engineering completes
- Processing handles millions of leads efficiently

### 2. Score Output
- Scores written to `s3://bucket/analytics/lead_scores/score_date=YYYY-MM-DD/model_version=X.Y/`
- Output includes:
  - lead_id
  - score_value (probability)
  - score_band (Hot/Warm/Cold)
  - top_drivers (JSON array of top 5 features)
  - model_version
  - score_timestamp
- Scores registered in Glue Catalog analytics_db.lead_scores

### 3. Score Quality
- Score distribution validated against expected ranges
- Anomaly detection for unusual score patterns
- Score statistics logged (mean, percentiles, band distribution)
- Alerts for unexpected changes in score distribution

### 4. SLA Compliance
- Scoring complete by 6 AM daily
- End-to-end pipeline from ingestion to scores < 4 hours
- Status updates logged throughout pipeline
- Dashboard showing pipeline progress

## 🔒 Technical Constraints

- Use approved model version from Model Registry
- Scoring must match training-time feature logic
- Batch Transform must run in VPC
- Scores encrypted at rest

## 📦 Dependencies

- Feature Engineering Pipeline (Lead Scoring Story 03)
- Model Training Pipeline (Lead Scoring Story 04)
- Approved model in Model Registry
- Airflow orchestration (Data Platform Story 04)

## ✅ Tasks

### Pipeline Development
- ⬜ Create SageMaker Batch Transform configuration
- ⬜ Implement feature retrieval for active leads
- ⬜ Configure model version retrieval from registry
- ⬜ Set up score output formatting

### Quality Assurance
- ⬜ Implement score distribution validation
- ⬜ Create anomaly detection rules
- ⬜ Set up score statistics logging
- ⬜ Configure alerts for distribution anomalies

### Orchestration
- ⬜ Create Airflow DAG for scoring pipeline
- ⬜ Configure dependencies on feature engineering
- ⬜ Set up SLA monitoring
- ⬜ Create status notification workflow

### Validation
- ⬜ Test end-to-end scoring pipeline
- ⬜ Verify score output schema
- ⬜ Validate SLA compliance
- ⬜ Test recovery from partial failures

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Pipeline success rate | >99% daily scoring runs complete |
| SLA adherence | Scores available by 6 AM 95% of time |
| Score coverage | 100% active leads scored |
| Processing throughput | Handle 1M+ leads in <1 hour |

## 🔗 Related Documents

- [Architecture Overview - ML Platform](../../../architecture/overview.md)
- [Data Flows Architecture](../../../architecture/data-flows.md)
- [Value Delivery Roadmap - Phase 1](../../../architecture/value-delivery-roadmap.md)
