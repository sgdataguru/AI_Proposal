# 03 - Model Governance and Registry

## 📝 Description

As a **ML Engineer**, I want a model governance framework with versioning, approval workflows, and lineage tracking so that all models in production are documented, approved, and auditable for compliance requirements.

## 🎯 Acceptance Criteria

### 1. Model Registry
- SageMaker Model Registry configured
- Model Package Groups created for each use case
- Model versioning with semantic versioning (vX.Y.Z)
- Model metadata captured:
  - Training data version
  - Hyperparameters
  - Performance metrics
  - Training timestamp

### 2. Approval Workflow
- Multi-stage approval process:
  - Technical Review (ML Lead)
  - Business Review (Product Owner)
  - Compliance Review (if required)
  - Production Approval (Platform Lead)
- Approval status: Pending → Approved → Rejected → Archived
- Approval audit trail maintained

### 3. Model Documentation
- Model card required for each model version:
  - Model purpose and use case
  - Training data description
  - Performance metrics and limitations
  - Bias and fairness considerations
  - Operational requirements
- Documentation linked to model artifact

### 4. Model Lineage
- Training data lineage tracked
- Feature → Model → Prediction lineage
- Model version history maintained
- Rollback capability to previous versions

## 🔒 Technical Constraints

- Only approved models can be deployed to production
- Model artifacts encrypted with KMS
- All approvals logged for audit
- Manual override requires additional approval

## 📦 Dependencies

- Model Training Pipeline (Lead Scoring Story 04)
- SageMaker Studio configured
- IAM roles for model approvers
- S3 bucket for model artifacts

## ✅ Tasks

### Registry Setup
- ⬜ Create Model Package Group for lead scoring
- ⬜ Configure model artifact storage
- ⬜ Set up model versioning schema
- ⬜ Create model metadata template

### Approval Workflow
- ⬜ Define approval roles and permissions
- ⬜ Create Step Functions workflow for approvals
- ⬜ Set up approval notifications
- ⬜ Implement approval audit logging

### Documentation
- ⬜ Create model card template
- ⬜ Implement model card validation
- ⬜ Link documentation to model registry
- ⬜ Set up documentation review process

### Lineage Tracking
- ⬜ Configure SageMaker Lineage
- ⬜ Create lineage visualization
- ⬜ Implement rollback procedures
- ⬜ Document lineage query patterns

### Validation
- ⬜ Test approval workflow end-to-end
- ⬜ Verify model cannot be deployed without approval
- ⬜ Validate audit trail completeness
- ⬜ Test rollback to previous version

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Model documentation | 100% models have complete model cards |
| Approval compliance | 100% production models are approved |
| Audit completeness | All model decisions traceable |
| Rollback capability | Can rollback within 15 minutes |

## 🔗 Related Documents

- [Security & Governance - Model Governance](../../../architecture/security-governance.md)
- [Architecture Overview - ML Platform](../../../architecture/overview.md)
- [Business Case - AI Governance](../../../project-context/business-case.md)

## 📚 Relevant Context

### Strategic Alignment
This story implements the **Model Governance** pillar of the three-pillar AI Governance approach per [Business Case](../../../project-context/business-case.md). Lead Scoring establishes the model governance patterns that will be reused for Portfolio Review, Campaign Intelligence, IFA Portal AI, and RM Co-Pilot.

### Architecture Context
- **Model Registry**: SageMaker Model Registry for version control and lifecycle management per [Architecture Overview §3.3](../../../architecture/overview.md)
- **Approval Workflow**: Multi-stage approval process (Technical → Business → Compliance → Production) per [Security & Governance §7.2](../../../architecture/security-governance.md)
- **Lineage Tracking**: SageMaker Lineage for Features → Model → Predictions traceability

### Timeline & Milestones
- Part of **Phase 1** "Model Development & Governance Review" (Weeks 5-8) and "Governance Artifacts" (Week 12) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Success criteria: Governance artifacts reviewed and approved by compliance
- Supports Phase 1 deliverable: "Governance Artifacts - Model documentation, RACI, audit controls"

### Key Risks & Constraints
- **R09 (High)**: Model decisions lack sufficient explainability for regulatory requirements - implement SHAP/LIME, document decisions, compliance review ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C05**: Model explainability required for all production models - limits model complexity
- **C11**: Model decisions affecting customers must be auditable - logging and traceability required
- **A14**: Assumes regulatory requirements for AI explainability are understood and stable

### Model Governance Framework
Per [Security & Governance §7](../../../architecture/security-governance.md):
- **Version Control**: Semantic versioning (vX.Y.Z) with change rationale
- **Model Card Requirements**: Purpose, training data, performance metrics, bias considerations, limitations
- **Approval Status Flow**: Pending → Approved → Rejected → Archived
- **Rollback Capability**: Can rollback within 15 minutes

### Business Case Governance Requirements
Per [Business Case - AI Governance](../../../project-context/business-case.md):
- **Explainability minimum**: Top 5 drivers per score band
- **Human-in-the-loop**: Business review of band thresholds
- **Versioning**: Model versions tracked with change rationale
- **Auditability**: Reproducible scoring logs for sample decisions

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **SageMaker Model Registry** for version control and approval workflow
- **SageMaker Pipelines** for reproducible ML workflows
- **SageMaker Lineage** for training data and prediction lineage
- **AWS Step Functions** for approval workflow automation
- **AWS CloudTrail** for audit logging of all model operations

---

## Implementation Plan

### 1. Feature Overview

**Goal:** Establish a model governance framework with versioning, approval workflows, and lineage tracking to ensure all production models are documented, approved, and auditable.

**Primary User Role:** ML Engineer

**Business Value:** Ensures 100% production models are approved with complete audit trails, supporting regulatory compliance and enabling safe scaling to future AI products.

### 2. Component Analysis & Reuse Strategy

#### Existing Components
| Component | Location | Reuse Decision |
|-----------|----------|----------------|
| Model Training | Lead Scoring Story 04 | **INTEGRATE** - Registry integration |
| SageMaker Studio | Infrastructure | **REUSE** - Governance UI |
| CloudTrail | Security Story 03 | **REUSE** - Audit logging |

#### New Components Required
| Component | Purpose | Priority |
|-----------|---------|----------|
| Model Package Group | Registry organization | High |
| Approval Workflow | Multi-stage approvals | High |
| Model Card Template | Governance documentation | High |
| Lineage Configuration | Traceability | Medium |

### 3. Affected Files

#### Infrastructure (Terraform)
| File Path | Action | Description |
|-----------|--------|-------------|
| `infra/modules/model-registry/main.tf` | [CREATE] | Registry module |
| `infra/modules/model-registry/approval.tf` | [CREATE] | Approval workflow |
| `infra/modules/model-registry/iam.tf` | [CREATE] | Approver roles |

#### Documentation Templates
| File Path | Action | Description |
|-----------|--------|-------------|
| `docs/ml/templates/model-card-template.md` | [CREATE] | Model card template |
| `docs/ml/templates/approval-checklist.md` | [CREATE] | Approval checklist |

### 4. Component Breakdown

#### 4.1 Approval Workflow

```
Model Trained → Register in Registry
                      ↓
            Technical Review (ML Lead)
                      ↓
            Business Review (Product Owner)
                      ↓
            Compliance Review (if required)
                      ↓
            Production Approval (Platform Lead)
                      ↓
                Approved → Deploy
```

#### 4.2 Model Card Requirements

| Section | Content |
|---------|---------|
| Model Purpose | Use case and business context |
| Training Data | Dataset description and version |
| Performance Metrics | AUC, precision, recall, lift |
| Limitations | Known constraints and biases |
| Bias & Fairness | Fairness analysis results |
| Operational Requirements | Infrastructure needs |

### 5. Implementation Steps

#### Phase 1: Registry Setup (Week 6)
- [ ] **Step 1.1:** Create Model Package Group for lead scoring
- [ ] **Step 1.2:** Configure model artifact storage
- [ ] **Step 1.3:** Set up model versioning schema (vX.Y.Z)
- [ ] **Step 1.4:** Create model metadata template

#### Phase 2: Approval Workflow (Week 6-7)
- [ ] **Step 2.1:** Define approval roles and permissions
- [ ] **Step 2.2:** Create Step Functions workflow for approvals
- [ ] **Step 2.3:** Set up approval notifications
- [ ] **Step 2.4:** Implement approval audit logging

#### Phase 3: Documentation & Lineage (Week 7-8)
- [ ] **Step 3.1:** Create model card template
- [ ] **Step 3.2:** Configure SageMaker Lineage
- [ ] **Step 3.3:** Implement rollback procedures
- [ ] **Step 3.4:** Test approval workflow end-to-end

### 6. Dependencies & Prerequisites

| Dependency | Source | Status |
|------------|--------|--------|
| Model Training Pipeline | Lead Scoring Story 04 | Required |
| SageMaker Studio | Infrastructure | Required |
| IAM roles for approvers | Shared Infrastructure | Required |
