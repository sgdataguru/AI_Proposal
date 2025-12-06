# 04 - Workflow Orchestration with Amazon MWAA

## 📝 Description

As a **Data Engineer**, I want to set up Amazon MWAA (Managed Airflow) for workflow orchestration so that data pipelines and ML workflows can be scheduled, monitored, and managed with dependencies in a unified interface.

## 🎯 Acceptance Criteria

### 1. MWAA Environment
- MWAA environment provisioned in private VPC
- Environment class sized appropriately (mw1.small for dev, mw1.medium for prod)
- Airflow version 2.x configured
- Web server accessible via VPN/private access

### 2. DAG Structure
- Standard DAG templates created for:
  - Daily lead data ingestion pipeline
  - Bronze-to-Silver transformation workflow
  - Feature engineering pipeline
  - ML scoring pipeline
- DAGs organized by domain (data, ml, integration)
- Common utility operators for Glue, SageMaker, S3

### 3. Scheduling & Dependencies
- Cron-based scheduling for daily batch jobs
- Cross-DAG dependencies via sensors
- SLA monitoring configured
- Backfill capability for historical reruns

### 4. Monitoring & Alerting
- Airflow metrics exported to CloudWatch
- Task failure alerts via SNS/email
- DAG run history retained for 30 days
- Custom dashboard for pipeline health

## 🔒 Technical Constraints

- MWAA must run in private subnets
- No public endpoint for web server
- IAM roles for Airflow execution with least privilege
- DAG code version-controlled in Git, synced to S3

## 📦 Dependencies

- VPC with private subnets and NAT gateway
- S3 bucket for DAG storage
- Glue jobs created (Story 03)
- IAM roles for Airflow execution

## ✅ Tasks

### Infrastructure (Terraform)
- ⬜ Create MWAA environment with VPC configuration
- ⬜ Configure S3 bucket for DAGs and plugins
- ⬜ Set up IAM execution role for Airflow
- ⬜ Configure security groups for MWAA

### DAG Development
- ⬜ Create lead ingestion DAG
- ⬜ Create transformation pipeline DAG
- ⬜ Create feature engineering DAG
- ⬜ Create ML scoring DAG
- ⬜ Implement common operators module

### Monitoring
- ⬜ Configure CloudWatch metrics export
- ⬜ Set up SNS alerts for task failures
- ⬜ Create Airflow health dashboard
- ⬜ Define SLA for critical pipelines

### Validation
- ⬜ Test DAG execution end-to-end
- ⬜ Verify cross-DAG dependencies work
- ⬜ Test backfill for historical dates
- ⬜ Confirm alerting on failures

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| DAG success rate | >99% scheduled runs complete |
| SLA adherence | >95% jobs complete within SLA |
| Pipeline visibility | All runs visible in Airflow UI |
| Alert response time | Failures notified within 5 minutes |

## 🔗 Related Documents

- [Architecture Overview](../../../architecture/overview.md)
- [Data Platform Strategy - Orchestration](../../../architecture/data-platform-strategy.md)
- [Operations Guide](../../../../infra/docs/architecture/operations.md)
