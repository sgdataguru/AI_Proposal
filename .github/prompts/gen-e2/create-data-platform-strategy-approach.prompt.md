# Data Platform Strategy & Approach Prompt

## Role and Purpose

You are an expert data platform architect tasked with creating a **Data Platform Strategy & Approach document** that will serve as the foundational strategic reference for all downstream activities including:
- Detailed technical architecture design
- User story creation and backlog prioritization
- Technology selection and evaluation
- Implementation planning and phasing
- Risk management and mitigation strategies

This strategic document bridges business objectives with technical execution, defining both the "what" and "why" at a high level, while providing clear direction on "how" we'll achieve business goals through data platform capabilities.

## Context and Inputs

You have access to the following project context:

1. **Business Case** (`docs/project-context/business-case.md`)
   - Business objectives and success criteria
   - Current challenges and pain points
   - Expected business outcomes and KPIs
   - Stakeholder requirements

2. **Technology Stack** (`docs/project-context/tech-stack.md`) [if available]
   - Preferred cloud platforms and services
   - Existing technology constraints
   - Organizational capabilities and preferences

## Scope and Boundaries

**In Scope (Strategic):**
- Business requirement alignment and solution strategy
- High-level solution approach and architectural patterns
- Strategic technology decisions (e.g., cloud data warehouse vs. data lake, batch vs. streaming)
- Data platform principles and design philosophy
- Core capabilities and their rationale
- Key architectural principles and patterns
- Implementation phasing and value delivery roadmap
- Major decision points, trade-offs, and alternatives
- Risk landscape and strategic mitigations

**Out of Scope (Tactical):**
- Detailed technical specifications or configurations
- Specific code implementations or scripts
- Detailed data models and schema definitions (come during architecture phase)
- Specific Azure/AWS resource naming conventions or sizing
- Detailed cost estimates or line-item pricing
- Operational runbooks or deployment procedures

## Deliverables

### 1. Data Platform Strategy & Approach Document

Create a comprehensive strategic document with the following structure:

#### 1.1 Executive Summary
- **Business Context**: Problem statement and current state recap (2-3 sentences)
- **Strategic Vision**: Proposed solution approach and target state (3-4 sentences)
- **Expected Outcomes**: Key benefits and measurable business impacts
- **Strategic Bets**: 2-3 key decisions or directions that define this strategy

#### 1.2 Business Requirements & Strategic Response
For each business objective identified in the business case, provide:
- **Requirement ID & Statement**: Clear reference to business case requirement
- **Strategic Approach**: High-level solution strategy (2-4 sentences)
- **Key Capabilities**: Primary platform capabilities required (e.g., data ingestion, storage, transformation)
- **Success Criteria**: How we'll measure that this requirement is met
- **Dependencies**: Other requirements or capabilities this depends on
- **Strategic Rationale**: Why this approach best serves business objectives (consider alternatives briefly)

Example format:
```
**REQ-001: Establish Single Source of Truth**
- Strategic Approach: Centralize data in cloud data warehouse using dimensional model to enable consistent, governed analytics across the organization
- Key Capabilities: Data ingestion, staging layer, curated data warehouse, business semantic layer
- Success Criteria: All business reports draw from single data warehouse; <5% variance in metrics across teams
- Dependencies: Data source connectivity (REQ-003), data quality framework (REQ-005)
- Strategic Rationale: Data warehouse pattern chosen over data lake because (1) structured analytics is primary use case, (2) business users need governed, consistent definitions, (3) team has SQL/BI skills vs. big data engineering skills
```

#### 1.3 Data Platform Strategy
- **Data Architecture Pattern**: Hub-and-spoke, medallion/lakehouse, data mesh, etc.
  - Consider: Separation of concerns, scalability, and maintainability
  - Apply: Single responsibility principle for data zones/layers
- **Data Storage Strategy**: Where different types of data will be stored and why
  - Consider: Hot/warm/cold data tiers based on access patterns
  - Apply: Zone-based architecture (raw → cleansed → curated → consumption)
- **Data Integration Approach**: Batch vs. streaming, orchestration philosophy
  - Consider: Idempotency and reprocessability of data pipelines
  - Apply: ELT over ETL where possible for flexibility
- **Data Modeling Approach**: Star schema, Data Vault, wide tables, etc.
  - Consider: Query performance, business user understanding, and change management
  - Apply: Business-aligned dimensional models for analytics
- **Data Quality Strategy**: How data quality will be ensured
  - Consider: Data quality dimensions (completeness, accuracy, consistency, timeliness)
  - Apply: Quality checks at ingestion, transformation, and consumption layers
- **Data Lineage & Observability**: How data flow and quality will be tracked
  - Consider: End-to-end data lineage, data cataloging, and metadata management
  - Apply: Instrumentation for monitoring, alerting, and SLA tracking
- **Security & Governance Approach**: High-level security and compliance strategy
  - Consider: Data classification, access control, encryption, and audit logging
  - Apply: Principle of least privilege, data masking/anonymization where needed

#### 1.4 Technology Approach
Note: Keep this high-level. Specific services will be chosen during architecture phase.
- **Cloud Platform Rationale**: Why this cloud provider fits the requirements
  - Consider: Existing investments, team skills, regulatory requirements, cost model
- **Core Platform Capabilities Needed**: Storage, compute, orchestration, etc.
  - Consider: Managed services vs. self-managed (prefer managed for operational simplicity)
  - Apply: Cloud-native services that reduce undifferentiated heavy lifting
- **Integration Patterns**: How systems will connect
  - Consider: API-first design, loose coupling, event-driven where appropriate
  - Apply: Standard protocols (REST, messaging) and avoid point-to-point integrations
- **Analytics & Reporting Approach**: BI tools, self-service analytics strategy
  - Consider: Semantic layer for business logic, governed self-service
  - Apply: Single version of truth through curated data products
- **Infrastructure as Code**: How infrastructure will be defined and deployed
  - Consider: Version control, repeatability, and environment parity
  - Apply: Declarative infrastructure definitions (Terraform, ARM, Bicep)

#### 1.5 Implementation Strategy & Phasing
Recommend 2-4 phases that progressively build capability while delivering business value:
- **Phase Name & Strategic Objectives**: What will be delivered and why
- **Key Capabilities**: Features and capabilities included in this phase
- **Business Value & Outcomes**: Specific measurable outcomes stakeholders will see
- **Strategic Enablers**: What this phase enables for future phases
- **Dependencies & Prerequisites**: What must be in place first

**Strategic Phasing Principles:**
- **Value First**: Start with **high-value, low-complexity** use cases that prove platform value early (crawl-walk-run)
- **End-to-End**: Deliver **working vertical slices** rather than horizontal infrastructure layers
- **Foundation Early**: Include **observability, security, and governance** from Phase 1—technical debt is expensive
- **Learn and Adapt**: Early phases validate assumptions and inform later phases
- **Measurable Progress**: Each phase delivers **tangible business outcomes**, not just technical milestones

Example:
```
Phase 1: Foundation & Core Analytics (Weeks 1-4)
- Objectives: Establish basic infrastructure, ingest core data sources
- Capabilities: Product and sales reporting by country
- Value: Answer "What are our top products by region?"
- Prerequisites: Cloud environment setup, API access confirmed
```

### 2. Risks and Mitigation Strategies

Provide a risk register with:

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy | Owner Role |
|---------|-----------------|------------|--------|---------------------|------------|
| R-001 | Data source API rate limits | Medium | High | Implement caching layer... | Data Engineer |

Include risks related to:
- **Data quality and availability**: Source system reliability, data freshness, completeness
- **Technical complexity and skill gaps**: Team learning curve, new technology adoption
- **Timeline and resource constraints**: Scope creep, dependency delays, resource availability
- **Integration challenges**: API changes, connectivity issues, data format inconsistencies
- **Security and compliance concerns**: Data privacy, access control, regulatory requirements
- **Scalability and performance**: Data volume growth, query performance, cost escalation
- **Vendor lock-in**: Over-reliance on proprietary services, migration complexity
- **Data drift**: Schema evolution, semantic changes in source systems

### 3. Assumptions and Constraints

Clearly document:

#### Assumptions
- What you're assuming about project scope, resources, or environment
- Data availability and quality assumptions
- Skill and capability assumptions
- Timeline assumptions

#### Constraints
- Known technical limitations
- Budget or resource constraints (if mentioned)
- Regulatory or compliance requirements
- Timeline constraints
- Existing technology constraints

### 4. Strategic Decision Framework

For major strategic decisions identified in the approach:
- **Decision Point**: What strategic choice needs to be made
- **Options Considered**: 2-3 viable alternatives with pros/cons
- **Recommended Strategy**: Your strategic recommendation
- **Decision Criteria**: Business and technical factors that should drive the decision
- **Decision Timing**: What information or validation is needed before committing
- **Reversibility**: How easily this decision can be changed later (one-way vs. two-way door)

Example:
```
Decision Point: Real-time vs. Batch Data Processing
Options: (1) Real-time streaming, (2) Micro-batch (5-15 min), (3) Daily batch
Recommended: Daily batch initially, with architecture allowing future streaming
Criteria: Business requirement urgency, cost, complexity, data volumes
When to Decide: After validating business requirements for data freshness
```

## Strategic Principles to Guide Your Strategy

When developing your strategy and approach, ensure alignment with these core data platform principles:

### Architectural Principles
- **Layered Data Refinement**: Establish clear zones for progressive data quality improvement (e.g., raw → cleansed → curated)
- **Preserve the Past**: Retain source data in its original form; enable reprocessing and historical analysis
- **Design for Change**: Anticipate schema evolution and changing business requirements without breaking existing consumers
- **Repeatability & Reliability**: Ensure data processes are deterministic and can be safely re-executed

### Strategic Patterns
- **Choose the Right Pattern**: Select architectural patterns (medallion, data mesh, hub-and-spoke) based on organizational structure, data volumes, and team capabilities
- **Minimize Complexity**: Start with simpler patterns; evolve to advanced patterns only when requirements clearly justify the additional complexity
- **Balance Batch and Real-time**: Align processing approach with actual business needs for data freshness vs. cost and complexity trade-offs

### Operational Foundation
- **Built-in Observability**: Plan for monitoring, alerting, and troubleshooting from day one—not as an afterthought
- **Data Quality by Design**: Embed quality validation throughout the data flow; fail fast to prevent bad data propagation
- **Cost-Conscious**: Consider data lifecycle management, storage tiers, and compute efficiency in the approach
- **Testability**: Design for automated testing at each layer—data pipelines are code and deserve software engineering rigor

### Governance & Trust
- **Discoverable Data**: Plan for data cataloging and metadata management to enable self-service analytics
- **Security by Default**: Apply least-privilege access, data classification, and audit logging as foundational requirements
- **Lineage & Transparency**: Enable users to understand data origins, transformations, and quality for informed decision-making

### Scalability Considerations
- **Scale Up and Out**: Design for both increasing data volumes and growing number of consumers
- **Performance Patterns**: Consider partitioning strategies, incremental processing, and caching philosophy appropriate to query patterns
- **Avoid Premature Optimization**: Focus on critical paths; don't over-engineer for theoretical scale problems

## Quality Criteria

A high-quality Data Platform Strategy & Approach document should:

✅ **Business-Aligned** - Every business requirement has a clear strategic response
✅ **Strategic Yet Actionable** - Provides clear direction without prescribing detailed implementation
✅ **Well-Justified** - Includes clear rationale linking business needs to technical approach
✅ **Trade-off Aware** - Shows consideration of alternatives and explicit decision-making
✅ **Appropriately Abstract** - Focus on capabilities and patterns over specific tools (some specificity is OK given constraints)
✅ **Realistic & Pragmatic** - Considers organizational capabilities, constraints, and maturity
✅ **Value-Sequenced** - Shows logical implementation phases with clear business value
✅ **Risk-Conscious** - Identifies strategic risks, dependencies, and mitigation approaches
✅ **Enables Downstream Work** - Provides sufficient foundation for architecture design and story writing
✅ **Principle-Based** - Applies relevant industry patterns and architectural principles
✅ **Future-Oriented** - Considers evolution, scalability, and long-term platform vision
✅ **Decision-Transparent** - Documents key strategic decisions, alternatives considered, and rationale

## Output Format

Provide your response as a well-structured markdown document that can be saved as `docs/project-context/data-platform-strategy-approach.md` and serve as the authoritative strategic reference throughout the project lifecycle.

This document should be:
- **Comprehensive yet concise** - Cover all strategic elements without unnecessary detail
- **Scannable** - Use clear headings, bullets, and tables for easy navigation
- **Professional** - Written for technical and business stakeholders alike
- **Referenceable** - Each section should stand alone and be easily cited in downstream documents