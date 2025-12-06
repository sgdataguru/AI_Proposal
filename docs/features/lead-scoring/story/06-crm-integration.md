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

## 📚 Relevant Context

### Strategic Alignment
This story delivers the final step of **REQ-001: Lead Prioritisation Intelligence** - getting scores into the hands of RMs and sales teams. Per [Business Case](../../../project-context/business-case.md), one integration endpoint (CRM priority view OR daily activation list OR campaign audience segment) must be agreed early to enable value realization.

### Architecture Context
- **Integration Pattern**: CRM Integration follows the score delivery flow in [Data Flows §6.4](../../../architecture/data-flows.md): Gold Zone → Lambda → API Gateway → CRM System
- **Phased Approach**: Phase 1 uses CSV/flat-file integration; Phase 2 adds API-based real-time push per [Architecture Overview §3.5](../../../architecture/overview.md)
- **API Design**: RESTful APIs via API Gateway + Lambda for system integration per [Data Platform Strategy §4.3](../../../architecture/data-platform-strategy.md)

### Timeline & Milestones
- Part of **Phase 1** "Integration & Pilot Launch" (Weeks 8-10) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M5: Integration Live** (Week 9) - CRM integration active with sales teams using priority lists
- Success criteria: >80% RM adoption of priority lists

### Key Risks & Constraints
- **R03 (High)**: CRM integration delays block value realization - mitigate by starting with secure CSV/flat-file integration for PoC, parallel track API development ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R05 (High)**: Low frontline adoption of AI-generated prioritization - co-design priority bands with RMs, keep UI simple, provide training
- **R14 (High)**: External system owners may not prioritize integration work - early stakeholder engagement, executive sponsorship
- **C17**: CRM system changes require coordination with IT operations

### Integration Targets
Per [Architecture Overview §3.5](../../../architecture/overview.md), initial integration points for Phase 1:
- **CRM**: Priority view / API push
- **Inside Sales Tools**: Daily activation list (CSV/API)

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon API Gateway + AWS Lambda** for API-based CRM ingestion
- **SFTP/secure file delivery** for CSV-based integration in early phases
- **AWS Secrets Manager** for CRM credential storage
- **Amazon S3** for secure file exchange
- **Amazon CloudWatch** for delivery monitoring and alerting
