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

## 📚 Relevant Context

### Strategic Alignment
This story implements the API-first integration paradigm per [Data Platform Strategy §4.3](../../../architecture/data-platform-strategy.md), enabling system integration with CRM and other applications. The API layer supports **REQ-003: Scalable Multi-Channel Support** by providing programmatic access to scores.

### Architecture Context
- **Integration Pattern**: API Gateway → Lambda → S3/Athena/DynamoDB per [Architecture Overview §3.5](../../../architecture/overview.md)
- **Consumption Layer**: Part of the platform's consumption architecture delivering scores to external systems per [Data Flows §6](../../../architecture/data-flows.md)
- **API Response Pattern**: JSON format with leadId, score, scoreBand, topDrivers, modelVersion, scoreDate per [Data Flows §6.3](../../../architecture/data-flows.md)

### Timeline & Milestones
- Phase 1: CSV/file-based integration during PoC (Weeks 4-5)
- Phase 2: API-based real-time push per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Supports milestone **M5: Integration Live** (Week 9)

### Key Risks & Constraints
- **R03 (High)**: CRM integration delays - CSV fallback ensures value realization even if API delayed ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R14 (High)**: External system owners may not prioritize integration - API Gateway reduces dependency on CRM team
- **C15**: Phase 1 production launch within 12 weeks - API enables faster iteration than CRM-side changes

### Security Requirements
Per [Security & Governance §3.3](../../../architecture/security-governance.md):
- **Authentication**: API key authentication with rate limiting
- **Encryption**: TLS 1.2+ required for all API calls
- **Network**: HTTPS only, IP allowlisting option available
- **Audit**: All API requests logged to CloudWatch and S3

### Integration Patterns
Per [Architecture Overview §3.5](../../../architecture/overview.md):
| Pattern | Use Case |
|---------|----------|
| API (Outbound) | Lambda → External API for CRM score delivery |
| API (Inbound) | API Gateway → Lambda → S3 for real-time event capture |
| Batch File | S3 drop → Glue trigger for legacy systems |

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon API Gateway** for REST API management
- **AWS Lambda** for backend processing
- **Amazon Athena** or **DynamoDB** for score retrieval (depending on latency requirements)
- **AWS WAF** for API protection (optional)
- **Amazon CloudWatch** for request metrics and logging
- **Terraform** for infrastructure as code

---

## Implementation Plan

### 1. Feature Overview

**Goal:** Set up an API Gateway that delivers lead scores to external systems via secure, documented APIs, enabling CRM and other applications to retrieve scores programmatically.

**Primary User Role:** Integration Engineer

**Business Value:** Provides >99.9% API availability with <500ms response latency, enabling real-time score access for CRM and other systems.

### 2. Component Analysis & Reuse Strategy

#### Existing Components
| Component | Location | Reuse Decision |
|-----------|----------|----------------|
| Score Output | Lead Scoring Story 05 | **REUSE** - Data source |
| VPC Infrastructure | Security Story 01 | **REUSE** - Lambda VPC |
| CloudWatch | Shared Infrastructure | **REUSE** - Logging |

#### New Components Required
| Component | Purpose | Priority |
|-----------|---------|----------|
| REST API | API Gateway definition | High |
| Lambda Functions | Score retrieval logic | High |
| API Documentation | OpenAPI spec | High |
| DynamoDB Cache | Low-latency retrieval | Medium |

### 3. Affected Files

#### Infrastructure (Terraform)
| File Path | Action | Description |
|-----------|--------|-------------|
| `infra/modules/api-gateway/main.tf` | [CREATE] | API Gateway module |
| `infra/modules/api-gateway/routes.tf` | [CREATE] | API routes |
| `infra/modules/api-gateway/lambda.tf` | [CREATE] | Lambda integrations |

#### Lambda Functions
| File Path | Action | Description |
|-----------|--------|-------------|
| `src/lambda/get_lead_score/handler.py` | [CREATE] | Single lead score |
| `src/lambda/batch_scores/handler.py` | [CREATE] | Batch scores |
| `src/lambda/latest_scores/handler.py` | [CREATE] | Latest run summary |

#### Documentation
| File Path | Action | Description |
|-----------|--------|-------------|
| `docs/api/openapi-spec.yaml` | [CREATE] | OpenAPI specification |
| `docs/api/integration-guide.md` | [CREATE] | Integration guide |

### 4. Component Breakdown

#### 4.1 API Endpoints

| Endpoint | Method | Description | Latency Target |
|----------|--------|-------------|----------------|
| `/leads/{leadId}/score` | GET | Single lead score | <500ms |
| `/leads/scores/batch` | POST | Multiple lead scores | <2s |
| `/scores/latest` | GET | Latest scoring run summary | <500ms |

#### 4.2 Response Schema

```json
{
  "leadId": "L12345",
  "score": 0.87,
  "scoreBand": "Hot",
  "topDrivers": [
    {"feature": "engagement_score", "contribution": 0.35},
    {"feature": "recency_days", "contribution": 0.28},
    {"feature": "channel_quality", "contribution": 0.22}
  ],
  "modelVersion": "v1.2",
  "scoreDate": "2024-12-01"
}
```

### 5. Implementation Steps

#### Phase 1: API Development (Week 8-9)
- [ ] **Step 1.1:** Create OpenAPI specification
- [ ] **Step 1.2:** Implement GET /leads/{leadId}/score Lambda
- [ ] **Step 1.3:** Implement POST /leads/scores/batch Lambda
- [ ] **Step 1.4:** Implement GET /scores/latest Lambda

#### Phase 2: API Gateway Setup (Week 9)
- [ ] **Step 2.1:** Create API Gateway REST API
- [ ] **Step 2.2:** Configure API key authentication
- [ ] **Step 2.3:** Set up rate limiting (1000 req/min)
- [ ] **Step 2.4:** Configure CORS headers

#### Phase 3: Documentation & Testing (Week 9-10)
- [ ] **Step 3.1:** Generate Swagger documentation
- [ ] **Step 3.2:** Create integration guide
- [ ] **Step 3.3:** Test API endpoints
- [ ] **Step 3.4:** Load test for performance

### 6. Dependencies & Prerequisites

| Dependency | Source | Status |
|------------|--------|--------|
| Batch Scoring Pipeline | Lead Scoring Story 05 | Required |
| VPC with private subnets | Security Story 01 | Required |
| Lambda execution role | Shared Infrastructure | Required |
