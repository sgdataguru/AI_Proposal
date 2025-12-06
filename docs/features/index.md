# Features Index

## Overview

This directory contains INVEST-compliant user stories for the Nuvama Data Platform, organized by feature area. Each story represents a vertically-sliced, value-driven increment that can be independently developed and delivered.

## Feature Areas

| Feature | Description | Stories | Phase |
|---------|-------------|---------|-------|
| [Data Platform](./data-platform/index.md) | Core data lake infrastructure, ETL framework, orchestration | 4 | 1 |
| [Lead Scoring](./lead-scoring/index.md) | AI-powered lead prioritization and scoring | 7 | 1 |
| [Data Governance](./data-governance/index.md) | Access control, data quality, model governance | 4 | 1-2 |
| [Integration](./integration/index.md) | API delivery, self-service analytics | 2 | 1-2 |
| [Security](./security/index.md) | Network security, encryption, audit logging | 4 | 1 |

## Story Summary

### Total Stories: 21

#### By Priority
- **High Priority:** 17 stories
- **Medium Priority:** 4 stories

#### By Phase
- **Phase 1 (Foundation):** 19 stories
- **Phase 2 (Core Analytics):** 2 stories

## Story Format

Each user story follows the INVEST criteria and includes:

- 📝 **Description** - User story in "As a... I want... so that..." format
- 🎯 **Acceptance Criteria** - Numbered requirements with details
- 🔒 **Technical Constraints** - Architecture and implementation boundaries
- 📦 **Dependencies** - Prerequisites and related stories
- ✅ **Tasks** - Implementation checklist grouped by layer
- 📊 **Success Metrics** - Measurable outcomes

## Delivery Roadmap Alignment

Stories are aligned with the [Value Delivery Roadmap](../architecture/value-delivery-roadmap.md):

### Phase 1: Foundation & AI Lead Scoring (Weeks 1-12)
- Data Platform Foundation stories (4)
- Lead Scoring stories (7)
- Security stories (4)
- Data Governance stories (3)
- Integration story (1)

### Phase 2: Core Analytics (Weeks 13-24)
- Drift Detection story
- Self-Service Analytics story

## Related Documents

- [Data Platform Strategy](../architecture/data-platform-strategy.md)
- [Value Delivery Roadmap](../architecture/value-delivery-roadmap.md)
- [Risk & Constraint Register](../architecture/risk-constraint-register.md)
- [Architecture Overview](../architecture/overview.md)
- [Business Case](../project-context/business-case.md)

## Reusable Components Across Features

| Component | Source Feature | Reusability |
|-----------|----------------|-------------|
| S3 bucket Terraform module | Data Platform | All features needing storage |
| Glue job templates | Data Platform | Any ETL pipeline |
| Airflow DAG templates | Data Platform | Any orchestrated workflow |
| Lake Formation policies | Data Governance | All data access |
| Model governance artifacts | Data Governance | Any ML model |
| API Gateway configuration | Integration | Any API endpoint |
| VPC and security groups | Security | All AWS resources |
| KMS key policies | Security | All encryption needs |
