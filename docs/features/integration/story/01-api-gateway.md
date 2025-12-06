# 01 - API Gateway for Score Delivery

## 📝 Description

As an **Integration Engineer**, I want to set up an API Gateway that can deliver lead scores to external systems so that CRM and other applications can retrieve scores via secure, documented APIs.

## 🎯 Acceptance Criteria

### 1. API Design
- RESTful API endpoints:
  - GET /leads/{leadId}/score - Get single lead score
  - POST /leads/scores/batch - Get multiple lead scores
  - GET /scores/latest - Get latest scoring run summary
- Response format:
  ```json
  {
    "leadId": "L12345",
    "score": 0.87,
    "scoreBand": "Hot",
    "topDrivers": [...],
    "modelVersion": "v1.2",
    "scoreDate": "2024-12-01"
  }
  ```
- API versioning (v1, v2)

### 2. Security
- API key authentication
- Rate limiting (1000 requests/minute)
- Request logging
- IP allowlisting option
- HTTPS only (TLS 1.2+)

### 3. Documentation
- OpenAPI/Swagger specification
- Example requests/responses
- Error code documentation
- Integration guide

### 4. Monitoring
- Request metrics (count, latency, errors)
- Usage tracking per API key
- CloudWatch alarms for errors
- Access logging to S3

## 🔒 Technical Constraints

- Lambda functions for backend processing
- Data sourced from Gold zone via Athena or DynamoDB cache
- Response latency <500ms for single lead
- Must support CORS for web clients

## 📦 Dependencies

- Batch Scoring Pipeline (Lead Scoring Story 05)
- VPC with private subnets
- Lambda execution role
- CloudWatch for monitoring

## ✅ Tasks

### API Development
- ⬜ Create OpenAPI specification
- ⬜ Implement GET /leads/{leadId}/score Lambda
- ⬜ Implement POST /leads/scores/batch Lambda
- ⬜ Implement GET /scores/latest Lambda

### API Gateway Setup
- ⬜ Create API Gateway REST API
- ⬜ Configure API key authentication
- ⬜ Set up rate limiting
- ⬜ Configure CORS headers

### Infrastructure (Terraform)
- ⬜ Create API Gateway resources
- ⬜ Configure Lambda integrations
- ⬜ Set up CloudWatch logging
- ⬜ Create WAF rules (optional)

### Documentation
- ⬜ Generate Swagger documentation
- ⬜ Create integration guide
- ⬜ Document error codes
- ⬜ Create example code snippets

### Validation
- ⬜ Test API endpoints with sample data
- ⬜ Verify rate limiting works
- ⬜ Test authentication flow
- ⬜ Load test for performance

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| API availability | >99.9% uptime |
| Response latency | <500ms p95 for single lead |
| Error rate | <0.1% of requests |
| Documentation completeness | All endpoints documented |

## 🔗 Related Documents

- [Architecture Overview - Integration](../../../architecture/overview.md)
- [Data Flows - Consumption Layer](../../../architecture/data-flows.md)
- [Security & Governance](../../../architecture/security-governance.md)
