---
description: Rules and guidelines for Terraform Development
globs: infra/**/*
alwaysApply: false
stage: Deployment & DevOps
subcategory: subcategory-cloud-platforms
rule_name: terraform-cloud
rule_version: latest
---

# Terraform General Rules

You are an expert in Terraform and Infrastructure as Code (IaC) for cloud platforms such as AWS, Azure, and GCP.

## Key Principles

- Write concise, well-structured Terraform code with accurate examples.
- Organize infrastructure resources into reusable modules.
- Use versioned modules and provider version locks to ensure consistent deployments.
- Avoid hardcoded values; always use variables for flexibility.
- Structure files into logical sections: main configuration, variables, outputs, and modules.

## Terraform Best Practices

- Use remote backends (e.g., S3, Azure Blob, GCS) for state management.
- Enable state locking and use encryption for security.
- Utilize workspaces for environment separation (e.g., dev, staging, prod).
- Organize resources by service or application domain.
- Always run `terraform fmt` and `terraform validate` to catch errors early.
- Use linting tools such as `tflint` or `terrascan`.
- Store sensitive information in Vault, AWS Secrets Manager, or Azure Key Vault.

## State Management and Handling

- Use `terraform state` commands (mv, rm, list) to manage resources in the state.
- Run `terraform refresh` to ensure state reflects the current infrastructure.
- Monitor state consistency and fix drift issues.
- Implement rollback mechanisms and plan approval workflows for production.
- Ensure backup strategies are in place for state files.
- Use Terraform Cloud or Terraform Enterprise for advanced collaboration.

## Error Handling and Validation

- Use validation rules for variables to prevent incorrect input values.
- Handle edge cases using conditional expressions and `null` checks.
- Use `depends_on` to manage explicit dependencies when needed.

## Module Guidelines

- Split code into reusable modules to avoid duplication.
- Use outputs from modules to pass information between configurations.
- Version control modules and follow semantic versioning.
- Document module usage with examples and clearly define inputs/outputs.

## Security Practices

- Avoid hardcoding sensitive values; use Vault or environment variables.
- Ensure encryption for storage and communication.
- Define access controls and security groups for each cloud resource.
- Follow cloud provider-specific security guidelines.

## Performance Optimization

- Use resource targeting (`-target`) to speed up resource-specific changes.
- Cache Terraform provider plugins locally.
- Limit the use of `count` or `for_each` when not necessary.

## Testing and CI/CD Integration

- Integrate Terraform with CI/CD pipelines to automate testing and deployment.
- Run `terraform plan` in CI pipelines to catch issues before applying changes.
- Use tools like `terratest` to write unit tests for Terraform modules.
- Set up automated tests for critical infrastructure paths.

## Key Conventions

1. Lock provider versions to avoid breaking changes.
2. Use tagging for resources to ensure tracking and cost management.
3. Define resources in a modular, reusable way.
4. Document your code and configurations with `README.md` files.

## Directory Structure and Project Organization

- Use a modular directory structure:

  ```
  infra/
  ├── components/                # Logical infrastructure components
  │   ├── networking/            # Network infrastructure (VPC, subnets, gateways)
  │   │   ├── main.tf
  │   │   ├── variables.tf
  │   │   └── outputs.tf
  │   ├── compute/              # Computing resources (EC2, EKS, ECS)
  │   │   ├── main.tf
  │   │   ├── variables.tf
  │   │   └── outputs.tf
  │   ├── storage/              # Storage resources (S3, EBS, EFS)
  │   │   ├── main.tf
  │   │   ├── variables.tf
  │   │   └── outputs.tf
  │   └── database/             # Database resources (RDS, DynamoDB)
  │       ├── main.tf
  │       ├── variables.tf
  │       └── outputs.tf
  ├── environments/             # Environment-specific configurations
  │   ├── dev/
  │   │   ├── terraform.tfvars  # Base environment variables
  │   │   ├── networking.tfvars # Network-specific variables for dev
  │   │   ├── compute.tfvars    # Compute-specific variables for dev
  │   │   └── backend.tf        # Dev backend configuration
  │   ├── staging/
  │   └── prod/
  ├── modules/                  # Reusable modules
  │   ├── vpc/
  │   ├── eks/
  │   └── rds/
  ├── global/                   # Global resources (IAM, Route53)
  │   ├── main.tf
  │   ├── variables.tf
  │   └── outputs.tf
  ├── docs/                     # Contains infrastructure documents
  ├── main.tf                   # Root module that imports components
  ├── variables.tf              # Common variables
  ├── outputs.tf                # Common outputs
  ├── providers.tf              # Provider configuration
  └── versions.tf               # Version constraints
  ```

- For coordinating components, use a root module that references each component:

  ```hcl
  # main.tf
  module "networking" {
    source = "./components/networking"

    vpc_cidr        = var.vpc_cidr
    subnet_cidrs    = var.subnet_cidrs
    environment     = var.environment
  }

  module "compute" {
    source = "./components/compute"

    vpc_id          = module.networking.vpc_id
    subnet_ids      = module.networking.subnet_ids
    instance_type   = var.instance_type
    environment     = var.environment

    depends_on = [module.networking]
  }

  module "database" {
    source = "./components/database"

    vpc_id          = module.networking.vpc_id
    subnet_ids      = module.networking.database_subnet_ids
    instance_class  = var.db_instance_class
    environment     = var.environment

    depends_on = [module.networking]
  }
  ```

- Apply environment-specific configurations using variable files:

  ```bash
  # Apply dev environment configuration
  terraform apply -var-file=environments/dev/terraform.tfvars -var-file=environments/dev/networking.tfvars -var-file=environments/dev/compute.tfvars

  # Apply prod environment configuration
  terraform apply -var-file=environments/prod/terraform.tfvars -var-file=environments/prod/networking.tfvars -var-file=environments/prod/compute.tfvars
  ```

## Component Management

- For targeted creation or modification of specific components:

  ```bash
  # Create or update only the networking component
  terraform apply -target=module.networking -var-file=environments/dev/terraform.tfvars -var-file=environments/dev/networking.tfvars
  ```

- For safely removing components:

  1. **Targeted destruction** (preferred method):

     ```bash
     # Destroy only the database component
     terraform destroy -target=module.database -var-file=environments/dev/terraform.tfvars

     # After successful destruction, remove or comment out the module from main.tf
     ```

  2. **Module removal with state management**:

     ```bash
     # First remove or comment out the module from main.tf
     # Then list all resources in that module
     terraform state list | grep module.database

     # For each resource listed, remove it from state
     terraform state rm module.database.aws_db_instance.main
     terraform state rm module.database.aws_db_subnet_group.main
     # etc.
     ```

- Always run `terraform plan` before any apply or destroy operation to confirm the expected changes:
  ```bash
  # Preview what would be destroyed
  terraform plan -destroy -target=module.database -var-file=environments/dev/terraform.tfvars
  ```

## Initialization and Backend Configuration

- Use a backend configuration file for cleaner environment switching:

  ```bash
  # Initialize with backend config
  terraform init -backend-config=environments/dev/backend.tf

  # Switch to production environment
  terraform init -reconfigure -backend-config=environments/prod/backend.tf
  ```

  Where `environments/dev/backend.tf` might contain:

  ```hcl
  # backend.tf
  terraform {
    backend "s3" {
      bucket         = "my-terraform-state"
      key            = "environments/dev/terraform.tfstate"
      region         = "us-west-2"
      dynamodb_table = "terraform-locks"
      encrypt        = true
    }
  }
  ```

## Variable Handling

- Pass individual variables via command line:

  ```bash
  # Override specific variables during apply
  terraform apply \
    -var="environment=dev" \
    -var="region=us-east-1" \
    -var="instance_type=t3.medium" \
    -var-file=environments/dev/terraform.tfvars
  ```

- Pass sensitive variables via environment variables:

  ```bash
  export TF_VAR_db_password="supersecretpassword"
  export TF_VAR_aws_access_key="AKIAIOSFODNN7EXAMPLE"

  # Apply without exposing sensitive data in command line
  terraform apply -var-file=environments/dev/terraform.tfvars
  ```

- Combine variable files with specific overrides:
  ```bash
  # Use base configuration but override specific settings
  terraform apply \
    -var-file=environments/dev/terraform.tfvars \
    -var-file=environments/dev/networking.tfvars \
    -var="vpc_cidr=10.1.0.0/16" \
    -var="enable_vpn=true"
  ```

## Module Structure Guidelines

- For each module, follow this structure:

  1. `main.tf`: Primary resource definitions
  2. `variables.tf`: Input parameters with descriptions and validation rules
  3. `outputs.tf`: Return values from the module
  4. `README.md`: Module documentation

- Use descriptive names for resources with a consistent naming pattern

## Terraform Version Management

- Pin Terraform versions using version constraints
- Use tfenv or asdf for managing multiple Terraform versions locally
- Pin Terraform versions in CI/CD environments

## Drift Detection and Remediation

- Implement scheduled drift detection in CI/CD pipelines
- Create drift remediation processes
- Use tagging to identify resources managed by Terraform

## Import Strategies

- Import existing resources into Terraform management using `terraform import`
- Document imported resources with comments

## Cost Optimization

- Implement resource tagging for cost allocation
- Use cost estimation in CI/CD workflows with tools like Infracost
- Implement lifecycle policies for resource management
- Use conditional resource creation based on environment

## Secrets Management

- Integrate with external secrets managers (Vault, AWS Secrets Manager, Azure Key Vault)
- Set up secrets rotation policies
- Never store sensitive values in Terraform code or state

## Team Collaboration

- Implement pull request workflows for infrastructure changes
- Document code review guidelines
- Generate documentation with terraform-docs
- Define CODEOWNERS for critical infrastructure components

## Compliance and Security Scanning

- Integrate security scanning tools (tfsec, checkov, terrascan)
- Implement compliance-as-code patterns
- Use policy-as-code tools to enforce rules
- Create security baseline modules