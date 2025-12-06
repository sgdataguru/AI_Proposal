# 02 - Encryption and Key Management

## 📝 Description

As a **Security Engineer**, I want to configure AWS KMS for encryption key management so that all data at rest and in transit is encrypted with customer-managed keys and proper key rotation.

## 🎯 Acceptance Criteria

### 1. KMS Key Structure
- Customer Managed Keys (CMK) created per environment
- Key hierarchy:
  - Master key per environment (dev/uat/prod)
  - Data encryption keys generated per service
  - S3 bucket keys enabled for performance
- Key aliases for easy reference

### 2. Encryption Coverage
- S3 buckets: SSE-KMS with bucket keys
- Glue Data Catalog: KMS encryption
- SageMaker: KMS for volumes and artifacts
- CloudWatch Logs: KMS encryption
- Secrets Manager: Automatic KMS encryption

### 3. Key Policies
- Key administrators cannot use keys
- Key users cannot administer keys
- Service principals granted via key policies
- Cross-account access via grants only
- All key usage logged

### 4. Key Rotation
- Automatic annual rotation enabled
- Rotation documented in key policy
- Previous key versions retained for decryption
- Rotation tested and validated

## 🔒 Technical Constraints

- Keys must reside in AWS Mumbai region (ap-south-1)
- No key material import (AWS-managed material)
- Multi-region keys not required initially
- Key deletion requires 7-30 day waiting period

## 📦 Dependencies

- AWS account with KMS access
- IAM roles for key administration
- Service principals identified

## ✅ Tasks

### Key Creation
- ⬜ Create CMK for dev environment
- ⬜ Create CMK for uat environment
- ⬜ Create CMK for prod environment
- ⬜ Configure key aliases

### Key Policies
- ⬜ Define key administrator policy
- ⬜ Define key user policy
- ⬜ Grant service principals access
- ⬜ Configure audit logging

### Service Integration
- ⬜ Configure S3 bucket encryption with KMS
- ⬜ Configure Glue Catalog encryption
- ⬜ Configure SageMaker encryption
- ⬜ Configure CloudWatch Logs encryption

### Key Rotation
- ⬜ Enable automatic key rotation
- ⬜ Document rotation procedures
- ⬜ Test decryption after rotation
- ⬜ Set up rotation monitoring

### Validation
- ⬜ Verify all data encrypted at rest
- ⬜ Test TLS in transit (TLS 1.2+)
- ⬜ Validate key usage logging in CloudTrail
- ⬜ Test key rotation process

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Encryption coverage | 100% data encrypted at rest and in transit |
| Key policy compliance | All keys follow least privilege policy |
| Rotation compliance | All production keys rotate annually |
| Audit completeness | All key operations logged |

## 🔗 Related Documents

- [Security & Governance - Encryption](../../../architecture/security-governance.md)
- [Data Platform Strategy - Security](../../../architecture/data-platform-strategy.md#37-security-compliance--governance)
- [Network Security Details](../../../../infra/docs/architecture/network-security.md)
