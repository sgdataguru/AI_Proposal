# Integration & Consumption

## Overview

The Integration & Consumption feature enables external systems and users to access data platform outputs through secure APIs and self-service analytics capabilities.

## Business Value

- Seamless score delivery to CRM and sales tools
- Self-service analytics reducing data engineering bottleneck
- Secure, documented APIs for system integration
- Analyst empowerment with governed data access

## User Stories

| ID | Story | Priority | Phase |
|----|-------|----------|-------|
| [01](./story/01-api-gateway.md) | API Gateway for Score Delivery | High | 1 |
| [02](./story/02-self-service-analytics.md) | Self-Service Analytics Access | Medium | 2 |

## Dependencies

- Data Platform Foundation feature complete
- Lead Scoring feature producing scores
- Lake Formation access control configured
- QuickSight Enterprise license

## Related Architecture Documents

- [Architecture Overview - Consumption Layer](../../architecture/overview.md)
- [Data Flows - Consumption Patterns](../../architecture/data-flows.md)
- [Tech Stack](../../project-context/tech-stack.md)

## Reusable Components

- API Gateway configuration (Terraform)
- Lambda function templates for integration
- Athena workgroup configuration
- QuickSight dataset templates
- OpenAPI specification templates
