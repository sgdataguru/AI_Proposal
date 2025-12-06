# 06 - CRM Integration for Score Delivery

## 📝 Description

As a **Relationship Manager**, I want lead scores and priority bands delivered to the CRM system so that I can see which leads to contact first and understand why they are prioritized, enabling me to focus my time on high-potential prospects.

## 🎯 Acceptance Criteria

### 1. Score Delivery
- Daily scores pushed to CRM priority view
- Integration supports:
  - Phase 1: CSV file delivery via secure channel
  - Phase 2: API-based real-time push
- Scores visible in CRM lead record within 1 hour of generation

### 2. CRM Display
- Lead score visible on lead record
- Priority band (Hot/Warm/Cold) displayed with visual indicator
- Top 3 drivers shown for context
- Score date/freshness indicated
- Link to detailed explainability if available

### 3. Priority Lists
- Daily activation list generated:
  - Hot leads for immediate follow-up
  - Warm leads for scheduled nurturing
- Lists sortable by score within band
- Assignment to RMs/teams based on rules
- List export capability for offline work

### 4. Audit Trail
- All score deliveries logged
- CRM update confirmations captured
- Failed deliveries trigger retry with alerting
- Score history maintained for trend analysis

## 🔒 Technical Constraints

- CRM credentials stored in Secrets Manager
- API calls must be rate-limited per CRM requirements
- PII handling compliant with data protection policies
- Integration must not impact CRM performance

## 📦 Dependencies

- Batch Scoring Pipeline (Lead Scoring Story 05)
- CRM system API access or file drop location
- API Gateway configured (for API integration)
- Lambda functions for integration logic

## ✅ Tasks

### CSV Integration (Phase 1)
- ⬜ Define CSV schema for score delivery
- ⬜ Create Lambda function for CSV generation
- ⬜ Set up secure file transfer (SFTP or S3)
- ⬜ Configure delivery notification

### API Integration (Phase 2)
- ⬜ Design API payload for score updates
- ⬜ Create Lambda function for batch API calls
- ⬜ Implement rate limiting and retry logic
- ⬜ Configure API Gateway endpoint

### CRM Configuration
- ⬜ Create custom fields for score/band/drivers
- ⬜ Design priority list view
- ⬜ Configure visual indicators for bands
- ⬜ Set up team assignment rules

### Monitoring
- ⬜ Create delivery success dashboard
- ⬜ Set up alerts for delivery failures
- ⬜ Configure audit logging
- ⬜ Implement delivery reconciliation

### Validation
- ⬜ Test CSV delivery end-to-end
- ⬜ Verify scores appear correctly in CRM
- ⬜ Validate priority list functionality
- ⬜ Test failure recovery scenarios

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Delivery success rate | >99% daily deliveries successful |
| CRM availability | Scores visible within 1 hour of generation |
| RM adoption | >80% RMs using priority lists daily |
| Data accuracy | 100% scores match source after delivery |

## 🔗 Related Documents

- [Data Flows Architecture](../../../architecture/data-flows.md)
- [Architecture Overview - Integration](../../../architecture/overview.md)
- [Business Case - Integration Path](../../../project-context/business-case.md)
