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
