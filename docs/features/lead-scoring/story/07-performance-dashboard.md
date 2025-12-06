# 07 - Lead Scoring Performance Dashboard

## 📝 Description

As a **Sales Manager**, I want a dashboard showing lead score distribution, conversion tracking, and model performance so that I can monitor the effectiveness of AI-driven prioritization and make data-driven decisions about team focus.

## 🎯 Acceptance Criteria

### 1. Score Distribution View
- Daily score band distribution (Hot/Warm/Cold counts)
- Score distribution histogram
- Trend over time (weekly/monthly)
- Comparison against baseline period

### 2. Conversion Tracking
- Conversion rate by score band
- Lead funnel visualization (scored → contacted → converted)
- Time-to-conversion by band
- A/B comparison vs. non-scored leads (pilot)

### 3. Model Performance Metrics
- Actual vs. predicted conversion rates
- Precision/recall at each band threshold
- Lift chart showing model value
- Feature importance summary

### 4. Operational Metrics
- Pipeline health indicators (success/failure)
- Data freshness (last score update time)
- Coverage metrics (% leads scored)
- Alert status summary

## 🔒 Technical Constraints

- Dashboard built with Amazon QuickSight
- Data sourced from Gold zone (Athena queries)
- Refresh frequency: Daily (automated)
- Access controlled by IAM/QuickSight groups

## 📦 Dependencies

- Batch Scoring Pipeline (Lead Scoring Story 05)
- CRM Integration (Lead Scoring Story 06)
- Outcome data available for conversion tracking
- QuickSight configured with data source access

## ✅ Tasks

### Data Preparation
- ⬜ Create aggregated reporting tables in Gold zone
- ⬜ Define conversion join logic with CRM outcomes
- ⬜ Build Athena views for dashboard queries
- ⬜ Set up incremental refresh for reports

### Dashboard Development
- ⬜ Create score distribution visualizations
- ⬜ Build conversion funnel analysis
- ⬜ Implement model performance charts
- ⬜ Add operational health indicators

### Access Control
- ⬜ Define dashboard access groups
- ⬜ Configure row-level security if needed
- ⬜ Set up scheduled refresh
- ⬜ Create alert rules for KPI deviations

### Documentation
- ⬜ Document metric definitions
- ⬜ Create user guide for dashboard
- ⬜ Define interpretation guidelines
- ⬜ Train sales managers on dashboard use

### Validation
- ⬜ Verify metrics match source data
- ⬜ Test refresh automation
- ⬜ Validate access control rules
- ⬜ Gather user feedback on usability

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Dashboard availability | >99.5% uptime |
| Data freshness | Metrics updated by 7 AM daily |
| User adoption | 100% of sales managers access weekly |
| Metric accuracy | Metrics match source within 0.1% |

## 🔗 Related Documents

- [Architecture Overview - Analytics](../../../architecture/overview.md)
- [Value Delivery Roadmap - Success Criteria](../../../architecture/value-delivery-roadmap.md)
- [Tech Stack - QuickSight](../../../project-context/tech-stack.md)

## 📚 Relevant Context

### Strategic Alignment
This story enables measurement of **REQ-001: Lead Prioritisation Intelligence** success criteria per [Business Case](../../../project-context/business-case.md). The dashboard supports the "Closed-Loop Learning System" (REQ-002) by systematically tracking lead outcomes and feeding performance insights back into strategy.

### Architecture Context
- **Analytics Layer**: Dashboard queries Gold zone via Amazon Athena per [Data Flows §6](../../../architecture/data-flows.md)
- **BI Platform**: Amazon QuickSight for dashboards with Athena as data source per [Architecture Overview §2.2](../../../architecture/overview.md)
- **Consumption Pattern**: Self-service access to governed datasets per [Data Platform Strategy §4.4](../../../architecture/data-platform-strategy.md)

### Timeline & Milestones
- Part of **Phase 1** "Measurement, Optimization & Scale Blueprint" (Weeks 10-12) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M6: Phase 1 Go-Live** (Week 12) - Performance dashboard operational
- Dashboard enables Week 5 PoC report: "Uplift signals, Governance artefacts, Recommendation for Phase 1 production rollout"

### Success Metrics Alignment
Per [Value Delivery Roadmap §3.1.3](../../../architecture/value-delivery-roadmap.md), the dashboard tracks:
- Lead conversion improvement: 15-25% uplift for Hot leads vs. baseline
- RM productivity: 20-30% more leads processed/day
- Time-to-prioritization: Reduce from manual (days) to automated (daily)
- Governance compliance: 100% auditability of scoring decisions

### Key Risks & Constraints
- **R04 (High)**: Insufficient time for full uplift measurement - dashboard should track leading indicators (contact rate, meeting bookings) alongside lagging metrics ([Risk Register](../../../architecture/risk-constraint-register.md))
- **A11**: Assumes conversion improvement will be measurable within 3-6 months - define leading indicators alongside lagging metrics
- Dashboard must support A/B comparison for pilot cohort vs. non-scored leads

### Observability Stack
Per [Data Platform Strategy §3.6](../../../architecture/data-platform-strategy.md):
- **Pipeline Monitoring**: Amazon CloudWatch (logs, metrics, alarms)
- **Data Quality Dashboards**: Amazon QuickSight
- **Model Performance**: SageMaker Model Monitor metrics integration

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon QuickSight** for PoC dashboards (lead volume, score distribution, activation indicators)
- **Amazon Athena** for ad-hoc queries against Gold zone
- **AWS Glue Data Catalog** for table metadata and schema documentation
- **Amazon CloudWatch** for operational metrics (pipeline health, data freshness)
