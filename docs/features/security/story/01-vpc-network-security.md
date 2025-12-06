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

## 📚 Relevant Context

### Strategic Alignment
This story implements the "Defense in Depth" security principle per [Security & Governance §1.1](../../../architecture/security-governance.md), establishing network isolation as the foundation for all platform security. Network security enables compliance with financial services regulatory requirements in India.

### Architecture Context
- **Network Architecture**: VPC with public/private subnet separation per [Security & Governance §4.1](../../../architecture/security-governance.md)
- **VPC Endpoints**: Gateway endpoints for S3, interface endpoints for Glue, SageMaker, KMS, Secrets Manager, CloudWatch per [Security & Governance §4.1](../../../architecture/security-governance.md)
- **Zero Public Exposure**: All data workloads run in private subnets with no public IP addresses

### Timeline & Milestones
- Part of **Phase 1** foundation infrastructure (Weeks 2-4) per [Value Delivery Roadmap](../../../architecture/value-delivery-roadmap.md)
- Critical dependency: All other platform components require VPC infrastructure
- Target: Zero public exposure for data workloads, 100% VPC traffic logged

### Key Risks & Constraints
- **C02**: Data must remain in AWS Mumbai region (ap-south-1) - validates VPC placement ([Risk Register](../../../architecture/risk-constraint-register.md))
- **C03**: Production systems require VPC isolation and private connectivity
- **C04**: All infrastructure must be defined as Terraform code
- **A19**: Assumes network connectivity between cloud and on-premise systems is available

### Security Groups
Per [Security & Governance §4.2](../../../architecture/security-governance.md):
| Security Group | Purpose | Key Rules |
|----------------|---------|-----------|
| sg-glue | Glue jobs | Self-reference, HTTPS to endpoints |
| sg-sagemaker | SageMaker workloads | Self-reference, HTTPS to endpoints |
| sg-lambda | Lambda functions | Outbound HTTPS only |
| sg-endpoints | VPC endpoints | HTTPS from private subnets |
| sg-emr | EMR clusters | Self-reference, Spark ports |

### VPC Endpoints Required
Per [Security & Governance §4.1](../../../architecture/security-governance.md):
- **Gateway**: S3 (data lake access)
- **Interface**: Glue, SageMaker (API, Runtime, Studio), KMS, Secrets Manager, CloudWatch Logs, ECR

### Technology Stack
Per [Tech Stack](../../../project-context/tech-stack.md):
- **Amazon VPC** with multi-AZ deployment
- **NAT Gateway** in public subnets for outbound access
- **VPC Endpoints** for private AWS service access
- **VPC Flow Logs** for network traffic monitoring
- **AWS Network ACLs** for additional traffic filtering
- **Terraform** for infrastructure as code
