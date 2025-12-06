# 04 - Lead Scoring Model Training Pipeline

## 📝 Description

As a **Data Scientist**, I want to train a machine learning model that predicts lead conversion probability so that high-intent leads can be prioritized for RM outreach and improve activation efficiency.

## 🎯 Acceptance Criteria

### 1. Model Development
- Model trained using SageMaker Training Jobs
- Algorithm selection documented (XGBoost, LightGBM, or similar)
- Hyperparameter tuning performed
- Cross-validation used for robust evaluation
- Training data covers 6-12 months of historical leads

### 2. Model Output
- Score: Conversion probability (0-1)
- Priority bands:
  - Hot: Probability > 0.7
  - Warm: Probability 0.4-0.7
  - Cold: Probability < 0.4
- Thresholds configurable by business

### 3. Explainability
- SHAP values computed for feature importance
- Top 5 drivers per prediction available
- Global feature importance documented
- Model card created with:
  - Model purpose and limitations
  - Training data description
  - Performance metrics
  - Bias considerations

### 4. Model Registry
- Model registered in SageMaker Model Registry
- Model versioning with change rationale
- Status workflow: Staging → Approved → Archived
- Model artifacts stored in S3 with versioning

## 🔒 Technical Constraints

- Training must use only historical data (no future leakage)
- Model must produce consistent results (set random seeds)
- Training jobs must run in VPC
- Model size must support batch inference latency

## 📦 Dependencies

- Feature Engineering Pipeline (Lead Scoring Story 03)
- Outcome data for training labels
- SageMaker Studio configured
- Model Registry set up

## ✅ Tasks

### Model Development
- ⬜ Prepare training dataset with features and labels
- ⬜ Split data into train/validation/test sets
- ⬜ Train baseline model
- ⬜ Perform hyperparameter tuning
- ⬜ Evaluate model on test set

### Explainability
- ⬜ Compute SHAP values for test set
- ⬜ Create feature importance visualization
- ⬜ Generate model card documentation
- ⬜ Review explainability with business stakeholders

### Model Registry
- ⬜ Create model package group in SageMaker
- ⬜ Register trained model with metadata
- ⬜ Define approval workflow
- ⬜ Document model versioning process

### Pipeline Integration
- ⬜ Create SageMaker Pipeline for training
- ⬜ Integrate with Airflow for scheduling
- ⬜ Set up model evaluation metrics export
- ⬜ Configure alerts for training failures

### Validation
- ⬜ Validate model accuracy on holdout set
- ⬜ Review predictions with business SMEs
- ⬜ Confirm explainability meets requirements
- ⬜ Test model approval workflow

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Model accuracy | AUC > 0.70 on test set |
| Precision at Hot | >50% conversion rate for Hot leads |
| Lift | 2x+ lift for Hot vs. random |
| Explainability | Top 5 drivers available for all predictions |

## 🔗 Related Documents

- [Architecture Overview - ML Platform](../../../architecture/overview.md)
- [Security & Governance - Model Governance](../../../architecture/security-governance.md)
- [Business Case - AI Governance](../../../project-context/business-case.md)

## 📚 Relevant Context

### Strategic Alignment
This story delivers the core AI capability for **REQ-001: Lead Prioritisation Intelligence**, establishing the "governance + data + deployment blueprint" that will be reused for Portfolio Review, Campaign Intelligence, and future AI products per [Business Case](../../../project-context/business-case.md). Model training implements the three-pillar AI Governance approach: Data Governance, Model Governance, and Operational Governance.

### Architecture Context
- **ML Platform**: Uses Amazon SageMaker (Studio, Training, Pipelines, Registry) per [Architecture Overview §3.3](../../../architecture/overview.md)
- **Model Registry**: SageMaker Model Registry for version control and lifecycle management (Staging → Approved → Archived)
- **Explainability**: SHAP/LIME required for top driver analysis per [Business Case - AI Governance](../../../project-context/business-case.md)

### Timeline & Milestones
- Part of **Phase 1** "Model Development & Governance Review" (Weeks 5-8) per [Value Delivery Roadmap §3.1](../../../architecture/value-delivery-roadmap.md)
- Target milestone: **M3: PoC Model Ready** (Week 5) - Lead scoring model validated with directional lift
- Success criteria: AUC > 0.70, model deployed to production with governance artifacts approved

### Key Risks & Constraints
- **R09 (High)**: Model decisions must have sufficient explainability for regulatory requirements - implement SHAP/LIME, document decisions, human-in-the-loop for threshold setting ([Risk Register](../../../architecture/risk-constraint-register.md))
- **R02 (Critical)**: Activation definition ambiguity - lock definition in Week 1 with business sign-off for valid training labels
- **A07**: Assumes historical data covers at least 6-12 months of lead activity and outcomes
- **C05**: Model explainability required - limits model complexity to interpretable approaches

### Model Governance Framework
Per [Security & Governance §7](../../../architecture/security-governance.md):
- **Approval Workflow**: Technical Review → Business Review → Compliance Review → Production Approval
- **Model Documentation**: Model card required with purpose, training data, performance metrics, bias considerations
- **Lineage Tracking**: SageMaker Lineage for Features → Model → Predictions traceability

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon SageMaker Studio** for development environment and notebooks
- **SageMaker Training Jobs** for managed training with tracked parameters
- **SageMaker Model Registry** for version control and approval workflow
- **SageMaker Pipelines** for reproducible ML workflows (production phase)
