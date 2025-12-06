# 01 - VPC and Network Security Configuration

## 📝 Description

As a **Security Engineer**, I want to configure VPC with private subnets and VPC endpoints so that all data platform components operate in network isolation without public internet exposure.

## 🎯 Acceptance Criteria

### 1. VPC Architecture
- VPC created with CIDR block appropriate for scale
- Subnet configuration:
  - Public subnets for NAT Gateway (outbound only)
  - Private subnets for data workloads
  - Isolated subnets for databases (future)
- Multi-AZ deployment for high availability
- Route tables configured for traffic isolation

### 2. VPC Endpoints
- Gateway endpoints:
  - S3 (for data lake access)
- Interface endpoints:
  - Glue
  - SageMaker (API, Runtime, Studio)
  - KMS
  - Secrets Manager
  - CloudWatch Logs
  - ECR (for containers)

### 3. Security Groups
- sg-glue: Self-reference for Glue jobs
- sg-sagemaker: Self-reference for SageMaker
- sg-lambda: Outbound HTTPS only
- sg-endpoints: HTTPS from private subnets
- sg-emr: Spark communication ports

### 4. Network ACLs
- Restrictive inbound rules
- Allowlist for required protocols only
- Logging enabled for denied traffic

## 🔒 Technical Constraints

- No public IP addresses for data workloads
- All AWS service access via VPC endpoints
- NAT Gateway only for external dependencies
- Private DNS enabled for endpoints

## 📦 Dependencies

- AWS account provisioned
- IP address allocation planned
- VPN/Direct Connect for corporate access (optional)
- KMS for encryption

## ✅ Tasks

### VPC Setup
- ⬜ Create VPC with CIDR block
- ⬜ Create public and private subnets across AZs
- ⬜ Configure NAT Gateway in public subnet
- ⬜ Set up route tables

### VPC Endpoints
- ⬜ Create S3 gateway endpoint
- ⬜ Create Glue interface endpoint
- ⬜ Create SageMaker endpoints
- ⬜ Create KMS and Secrets Manager endpoints
- ⬜ Create CloudWatch Logs endpoint

### Security Groups
- ⬜ Create and configure sg-glue
- ⬜ Create and configure sg-sagemaker
- ⬜ Create and configure sg-lambda
- ⬜ Create and configure sg-endpoints

### Network ACLs
- ⬜ Configure restrictive NACL rules
- ⬜ Enable VPC Flow Logs
- ⬜ Set up flow log analysis

### Validation
- ⬜ Test Glue job connectivity via endpoints
- ⬜ Test SageMaker connectivity
- ⬜ Verify no public internet access from private subnets
- ⬜ Validate VPC Flow Logs capture traffic

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Network isolation | Zero public exposure for data workloads |
| Endpoint coverage | All required AWS services accessible via VPC |
| Flow log coverage | 100% VPC traffic logged |
| Security group compliance | All resources tagged with appropriate SGs |

## 🔗 Related Documents

- [Network Security Details](../../../../infra/docs/architecture/network-security.md)
- [Security & Governance Architecture](../../../architecture/security-governance.md)
- [Component Specifications](../../../../infra/docs/architecture/component-specifications.md)
