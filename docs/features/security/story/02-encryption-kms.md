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

## 📚 Relevant Context

### Strategic Alignment
This story implements the "Encryption Everywhere" security principle per [Security & Governance §1.1](../../../architecture/security-governance.md). KMS encryption enables compliance with Indian data protection regulations and financial services audit requirements.

### Architecture Context
- **Encryption Architecture**: Customer Managed Keys (CMK) per environment with key hierarchy per [Security & Governance §3.1](../../../architecture/security-governance.md)
- **Encryption at Rest**: SSE-KMS for S3, Glue Catalog, SageMaker, CloudWatch Logs per [Security & Governance §3.2](../../../architecture/security-governance.md)
- **Encryption in Transit**: TLS 1.2+ for all communications per [Security & Governance §3.3](../../../architecture/security-governance.md)

### Timeline & Milestones
- Part of **Phase 1** foundation infrastructure (Weeks 2-4) per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Required before any data is stored in the platform
- Target: 100% data encrypted at rest and in transit

### Key Risks & Constraints
- **R07 (Medium)**: Data breach risk - KMS encryption is primary mitigation for data at rest ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C10**: PII data handling must comply with Indian data protection regulations
- **C02**: Keys must reside in AWS Mumbai region (ap-south-1)
- Key deletion requires 7-30 day waiting period (AWS constraint)

### Encryption Coverage
Per [Security & Governance §3.2](../../../architecture/security-governance.md):
| Service | Encryption Method | Key Type | Rotation |
|---------|-------------------|----------|----------|
| S3 | SSE-KMS with bucket keys | Customer Managed | Annual |
| Glue Data Catalog | KMS encryption | Customer Managed | Annual |
| SageMaker | KMS for volumes/artifacts | Customer Managed | Annual |
| CloudWatch Logs | KMS encryption | Customer Managed | Annual |
| Secrets Manager | KMS encryption | AWS Managed | Automatic |

### Key Policy Principles
Per [Security & Governance §3.4](../../../architecture/security-governance.md):
- Separate keys per environment (dev, uat, prod)
- Key administrators cannot use keys
- Key users cannot administer keys
- Cross-account access via grants (not policies)
- All key usage logged in CloudTrail

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **AWS KMS** with Customer Managed Keys
- **AWS CloudTrail** for key usage audit logging
- **Terraform** for key and policy management as code
- TLS 1.2+ enforced on all S3 bucket policies

---

## Implementation Plan

### 1. Feature Overview

**Goal:** Configure AWS KMS for encryption key management to ensure all data at rest and in transit is encrypted with customer-managed keys and proper key rotation.

**Primary User Role:** Security Engineer

**Business Value:** Achieves 100% encryption coverage at rest and in transit, enabling compliance with Indian data protection regulations and financial services audit requirements.

### 2. Component Analysis & Reuse Strategy

#### Existing Components
| Component | Location | Reuse Decision |
|-----------|----------|----------------|
| AWS Account | Infrastructure | **REUSE** - KMS target |

#### New Components Required
| Component | Purpose | Priority |
|-----------|---------|----------|
| CMK per Environment | Master encryption keys | Critical |
| Key Policies | Access control for keys | Critical |
| Service Integrations | S3, Glue, SageMaker encryption | High |
| Key Rotation | Annual automatic rotation | High |

### 3. Affected Files

#### Infrastructure (Terraform)
| File Path | Action | Description |
|-----------|--------|-------------|
| `infra/modules/kms/main.tf` | [CREATE] | KMS module |
| `infra/modules/kms/key-policy.tf` | [CREATE] | Key policies |
| `infra/modules/kms/aliases.tf` | [CREATE] | Key aliases |
| `infra/components/security/kms.tf` | [CREATE] | KMS component |

### 4. Component Breakdown

#### 4.1 Key Hierarchy

```
Organization
├── Dev Account
│   └── CMK: alias/dev-data-platform
├── UAT Account
│   └── CMK: alias/uat-data-platform
└── Prod Account
    └── CMK: alias/prod-data-platform
```

#### 4.2 Encryption Coverage

| Service | Encryption Type | Key |
|---------|----------------|-----|
| S3 | SSE-KMS with bucket keys | CMK |
| Glue Data Catalog | KMS encryption | CMK |
| SageMaker | KMS for volumes/artifacts | CMK |
| CloudWatch Logs | KMS encryption | CMK |
| Secrets Manager | KMS encryption | AWS Managed |

#### 4.3 Key Policy Principles

- Separate keys per environment
- Key administrators cannot use keys
- Key users cannot administer keys
- All key usage logged in CloudTrail

### 5. Implementation Steps

#### Phase 1: Key Creation (Week 2)
- [ ] **Step 1.1:** Create CMK for dev environment
- [ ] **Step 1.2:** Create CMK for uat environment
- [ ] **Step 1.3:** Create CMK for prod environment
- [ ] **Step 1.4:** Configure key aliases

#### Phase 2: Key Policies (Week 2-3)
- [ ] **Step 2.1:** Define key administrator policy
- [ ] **Step 2.2:** Define key user policy
- [ ] **Step 2.3:** Grant service principals access
- [ ] **Step 2.4:** Configure audit logging

#### Phase 3: Service Integration (Week 3)
- [ ] **Step 3.1:** Configure S3 bucket encryption with KMS
- [ ] **Step 3.2:** Configure Glue Catalog encryption
- [ ] **Step 3.3:** Configure SageMaker encryption
- [ ] **Step 3.4:** Configure CloudWatch Logs encryption

#### Phase 4: Rotation & Validation (Week 3-4)
- [ ] **Step 4.1:** Enable automatic key rotation
- [ ] **Step 4.2:** Test decryption after rotation
- [ ] **Step 4.3:** Verify all data encrypted at rest
- [ ] **Step 4.4:** Test TLS in transit (TLS 1.2+)

### 6. Dependencies & Prerequisites

| Dependency | Source | Status |
|------------|--------|--------|
| AWS account with KMS access | Infrastructure | Required |
| IAM roles for key administration | Shared Infrastructure | Required |
