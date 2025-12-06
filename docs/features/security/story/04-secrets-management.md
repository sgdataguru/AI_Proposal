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
