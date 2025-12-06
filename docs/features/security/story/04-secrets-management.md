# 04 - Secrets Management

## 📝 Description

As a **DevOps Engineer**, I want to configure AWS Secrets Manager for secure credential storage so that database passwords, API keys, and other secrets are never hardcoded and are automatically rotated.

## 🎯 Acceptance Criteria

### 1. Secret Storage
- All credentials stored in Secrets Manager
- Secrets organized by environment and service:
  - /prod/data-platform/crm-credentials
  - /prod/data-platform/api-keys
  - /dev/data-platform/...
- Secret versioning enabled
- Secret descriptions documented

### 2. Access Control
- IAM policies for secret access
- Least privilege per service/role
- Cross-account access via resource policies (if needed)
- No direct console access in production

### 3. Rotation Configuration
- Automatic rotation for supported secrets
- Rotation schedule: 30-90 days based on secret type
- Rotation Lambda functions configured
- Rotation testing in non-prod

### 4. Integration
- Application retrieval via SDK
- Caching for performance
- Glue connections use Secrets Manager
- Lambda environment variables reference secrets

## 🔒 Technical Constraints

- Secrets encrypted with KMS CMK
- No plaintext secrets in code or configs
- Rotation must not cause service disruption
- Secret access logged in CloudTrail

## 📦 Dependencies

- KMS keys for encryption
- IAM roles for services
- VPC endpoint for Secrets Manager
- Lambda for rotation functions

## ✅ Tasks

### Secret Setup
- ⬜ Create secrets for CRM credentials
- ⬜ Create secrets for API keys
- ⬜ Create secrets for database connections
- ⬜ Configure secret naming convention

### Access Configuration
- ⬜ Create IAM policies for secret access
- ⬜ Configure Glue connections with secrets
- ⬜ Update Lambda functions to use secrets
- ⬜ Remove any hardcoded credentials

### Rotation Setup
- ⬜ Create rotation Lambda for database secrets
- ⬜ Configure rotation schedules
- ⬜ Test rotation in dev environment
- ⬜ Document rotation procedures

### Monitoring
- ⬜ Set up alerts for rotation failures
- ⬜ Monitor secret access patterns
- ⬜ Create dashboard for secret health
- ⬜ Configure expiration warnings

### Validation
- ⬜ Verify all credentials use Secrets Manager
- ⬜ Test secret rotation end-to-end
- ⬜ Validate access controls
- ⬜ Confirm no plaintext secrets in codebase

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Secret coverage | 100% credentials in Secrets Manager |
| Rotation compliance | All secrets rotated per policy |
| Access audit | All secret access logged |
| Zero hardcoded credentials | No secrets in code or configs |

## 🔗 Related Documents

- [Security & Governance Architecture](../../../architecture/security-governance.md)
- [Tech Stack - Security](../../../project-context/tech-stack.md)
- [Operations Guide](../../../../infra/docs/architecture/operations.md)

## 📚 Relevant Context

### Strategic Alignment
This story implements secure credential management per the "Secrets" control in [Data Platform Strategy §3.7](../../../architecture/data-platform-strategy.md). Secrets Manager enables secure CRM integration and external system connectivity required for Lead Scoring value delivery.

### Architecture Context
- **Security Layer**: AWS Secrets Manager integrated with IAM and VPC endpoints per [Security & Governance §2](../../../architecture/security-governance.md)
- **Integration Pattern**: Glue connections and Lambda functions retrieve credentials from Secrets Manager per [Data Flows §3.2](../../../architecture/data-flows.md)
- **Encryption**: Secrets encrypted with KMS CMK per [Security & Governance §3](../../../architecture/security-governance.md)

### Timeline & Milestones
- Part of **Phase 1** foundation infrastructure (Weeks 2-4) per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Required before CRM integration (Lead Scoring Story 06)
- Target: 100% credentials in Secrets Manager, zero hardcoded secrets

### Key Risks & Constraints
- **R03 (High)**: CRM integration requires secure credential storage ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R07 (Medium)**: Data breach risk - Secrets Manager prevents credential exposure
- **C03**: VPC endpoint required for Secrets Manager access from private subnets
- Rotation must not cause service disruption (operational constraint)

### Secret Organization
Recommended naming convention per story requirements:
- `/prod/data-platform/crm-credentials` - CRM system access
- `/prod/data-platform/api-keys` - External API keys
- `/dev/data-platform/...` - Development environment secrets

### Security Integration Points
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Glue Jobs**: Use Secrets Manager for CRM/database credentials
- **Lambda Functions**: Reference secrets via environment variables
- **SageMaker**: Access training data connections securely

### Rotation Requirements
- Database secrets: 30-90 day rotation cycle
- API keys: Based on external system requirements
- Rotation Lambda functions configured for supported secret types
- Rotation tested in non-prod before production enablement

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **AWS Secrets Manager** for credential storage and rotation
- **AWS KMS** CMK for secret encryption
- **AWS Lambda** for custom rotation functions
- **AWS CloudTrail** for secret access audit logging
- **Amazon CloudWatch** for rotation failure alerts
- **Terraform** for secret and policy management as code
