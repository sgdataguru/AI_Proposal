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

## 📚 Relevant Context

### Strategic Alignment
This story operationalizes **REQ-001: Lead Prioritisation Intelligence** by delivering daily automated scoring to frontline teams. The batch scoring pipeline implements the "Minimum Viable AI Product" stage from the [Business Case](../../../project-context/business-case.md): "Scheduled batch scoring, CRM integration, Basic dashboard."

### Architecture Context
- **Daily Lead Scoring Pipeline**: Follows the sequence diagram in [Architecture Overview §6.1](../../../architecture/overview.md): Features → SageMaker Batch Transform → Gold Zone → API Gateway → CRM
- **Batch-First Strategy**: Per [Data Platform Strategy §3.3](../../../architecture/data-platform-strategy.md), batch processing meets initial business SLAs with lower complexity
- **Score Storage**: Outputs to Gold zone at `s3://bucket/analytics/lead_scores/` per [Data Flows §5.3](../../../architecture/data-flows.md)

### Timeline & Milestones
- Part of **Phase 1** "Integration & Pilot Launch" (Weeks 8-10) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M5: Integration Live** (Week 9) - Scoring pipeline operational
- SLA: Scores available by 6 AM daily (data freshness requirement per Strategy §1.3)

### Key Risks & Constraints
- **R04 (High)**: Insufficient time for full uplift measurement - track leading indicators (contact rate, meeting bookings) during pilot ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R11 (High)**: Model performance degradation over time - implement score distribution monitoring as early warning
- **C14**: Phase 1 PoC must demonstrate value within 5 weeks - scoring pipeline is critical path
- **C15**: Production launch targeted within 12 weeks - pipeline reliability >99% required

### Platform Health Metrics
Per [Data Platform Strategy §6.1](../../../architecture/data-platform-strategy.md):
- Data pipeline success rate: >99%
- Data freshness SLA adherence: >95%
- Mean time to recover (MTTR): <4 hours

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **SageMaker Batch Transform** for daily/hourly scoring with predictable cost
- **SageMaker Model Registry** for retrieving approved model versions
- **Amazon MWAA / Step Functions** for workflow orchestration
- **Amazon CloudWatch** for pipeline monitoring and SLA tracking
- **Amazon S3** for score output storage (Gold zone)
