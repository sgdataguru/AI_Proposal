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
