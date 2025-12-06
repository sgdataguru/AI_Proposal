# AI Lead Scoring

## Overview

The AI Lead Scoring feature delivers a machine learning solution that predicts lead conversion probability, enabling RMs and inside sales teams to prioritize high-intent leads for improved activation efficiency.

## Business Value

- 15-25% improvement in lead conversion rate for prioritized leads
- 20-30% increase in RM productivity
- Reduction in time-to-prioritization from days to hours
- Foundation for future AI products (Portfolio Review, Campaign Intelligence)

## User Stories

| ID | Story | Priority | Phase |
|----|-------|----------|-------|
| [01](./story/01-lead-data-ingestion.md) | Lead Data Ingestion Pipeline | High | 1 |
| [02](./story/02-lead-data-curation.md) | Lead Data Curation Pipeline | High | 1 |
| [03](./story/03-feature-engineering.md) | Feature Engineering Pipeline for Lead Scoring | High | 1 |
| [04](./story/04-model-training.md) | Lead Scoring Model Training Pipeline | High | 1 |
| [05](./story/05-batch-scoring.md) | Batch Scoring Pipeline | High | 1 |
| [06](./story/06-crm-integration.md) | CRM Integration for Score Delivery | High | 1 |
| [07](./story/07-performance-dashboard.md) | Lead Scoring Performance Dashboard | Medium | 1 |

## Dependencies

- Data Platform Foundation feature complete
- CRM data access approved
- Historical lead and outcome data (6-12 months)
- Business definition of "activation" confirmed

## Related Architecture Documents

- [Business Case](../../project-context/business-case.md)
- [Value Delivery Roadmap](../../architecture/value-delivery-roadmap.md)
- [Architecture Overview - ML Platform](../../architecture/overview.md)

## Reusable Components

- Feature engineering pipeline template
- SageMaker training pipeline template
- Batch scoring configuration
- CRM integration pattern
- Model governance artifacts (model card template)
