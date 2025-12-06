# Risk & Constraint Register

**Document Owner:** Program Management / Risk Office  
**Last Updated:** December 2024  
**Status:** Active  
**Review Frequency:** Monthly (risks), Quarterly (assumptions/constraints)  
**Related Documents:** [Data Platform Strategy](./data-platform-strategy.md) | [Value Delivery Roadmap](./value-delivery-roadmap.md)

---

## 1. Overview

### 1.1 Purpose

This document provides a centralized register of risks, assumptions, and constraints affecting the AI-led data platform transformation. It serves as a living document to:

- Track identified risks with impact, likelihood, and mitigation strategies
- Document assumptions that underpin delivery planning
- Record constraints that bound solution design and delivery
- Enable proactive risk management and informed decision-making

### 1.2 Ownership

| Role | Responsibility |
|------|----------------|
| **Risk Owner** | Accountable for managing specific risks; ensures mitigations are implemented |
| **Program Manager** | Maintains the register; coordinates risk reviews; escalates as needed |
| **Steering Committee** | Reviews high-impact risks; approves mitigation investments; makes go/no-go decisions |
| **Technical Leads** | Identify technical risks; implement technical mitigations |
| **Business Sponsors** | Identify business risks; validate assumptions; confirm constraints |

### 1.3 Monitoring Frequency

| Category | Review Frequency | Forum |
|----------|------------------|-------|
| High-Impact Risks | Weekly | Program Status Meeting |
| All Risks | Monthly | Risk Review Meeting |
| Assumptions | Monthly | Program Status Meeting |
| Constraints | Quarterly | Architecture Review |

### 1.4 Links to Strategy

This register directly supports:
- **[Data Platform Strategy](./data-platform-strategy.md):** Informs strategic decisions and architecture choices
- **[Value Delivery Roadmap](./value-delivery-roadmap.md):** Identifies dependencies and phase-gate considerations
- **[Business Case](../project-context/business-case.md):** Validates assumptions and risk mitigations

---

## 2. Risk Register

### 2.1 Risk Scoring Matrix

| | **Low Impact (1)** | **Medium Impact (2)** | **High Impact (3)** |
|---|---|---|---|
| **High Likelihood (3)** | Medium (3) | High (6) | Critical (9) |
| **Medium Likelihood (2)** | Low (2) | Medium (4) | High (6) |
| **Low Likelihood (1)** | Low (1) | Low (2) | Medium (3) |

**Risk Score = Likelihood × Impact**
- **Critical (7-9):** Immediate escalation; mitigation required before proceeding
- **High (5-6):** Active management; mitigation plan required
- **Medium (3-4):** Monitor; mitigation strategies defined
- **Low (1-2):** Accept; monitor periodically

---

### 2.2 Risk Table

| ID | Risk Category | Risk Description | Likelihood (1-3) | Impact (1-3) | Score | Mitigation Strategy | Owner | Phase Affected | Status |
|----|---------------|------------------|------------------|--------------|-------|---------------------|-------|----------------|--------|
| **R01** | Data Quality | Historical lead data has significant gaps or quality issues, reducing model accuracy | 3 | 3 | 9 (Critical) | Focus on high-signal features first; define data quality remediation backlog; implement quality checks in ingestion; establish minimum data quality thresholds | Data Lead | Phase 1 | Active |
| **R02** | Business Alignment | Activation definition ambiguity leads to misaligned model training and invalid success measurement | 3 | 3 | 9 (Critical) | Lock definition in Week 1 with business sign-off; document in glossary; validate against historical outcomes; create test cases | Product Owner | Phase 1 | Active |
| **R03** | Integration | CRM integration delays block value realization and adoption | 2 | 3 | 6 (High) | Start with secure CSV/flat-file integration for PoC; parallel track API development; identify fallback integration points | Tech Lead | Phase 1-2 | Active |
| **R04** | Timeline | Insufficient time for full uplift measurement within PoC period | 3 | 2 | 6 (High) | Track leading indicators (contact rate, meeting bookings); design measurement for directional lift; plan for extended measurement post-PoC | Program Manager | Phase 1 | Active |
| **R05** | Adoption | Low frontline (RM/sales) adoption of AI-generated prioritization | 2 | 3 | 6 (High) | Co-design priority bands with RMs; keep UI simple; provide training; establish champion network; measure and address feedback | Business Lead | Phase 1-2 | Active |
| **R06** | Technical Complexity | Feature engineering complexity exceeds available skills/time | 2 | 2 | 4 (Medium) | Start with proven features from industry patterns; leverage SageMaker built-in capabilities; phased feature complexity | ML Lead | Phase 1-2 | Active |
| **R07** | Security | Data breach or unauthorized access to sensitive lead/client data | 1 | 3 | 3 (Medium) | Implement Lake Formation fine-grained access; KMS encryption; audit logging; least privilege IAM; regular security reviews | Security Lead | All Phases | Active |
| **R08** | Vendor Lock-in | Over-reliance on AWS-specific services limits future flexibility | 2 | 2 | 4 (Medium) | Use open formats (Parquet, Iceberg) where possible; document portability requirements; maintain abstraction layers for critical components | Architecture Lead | All Phases | Active |
| **R09** | Compliance | Model decisions lack sufficient explainability for regulatory requirements | 2 | 3 | 6 (High) | Implement SHAP/LIME for top drivers; document model decisions; human-in-the-loop for threshold setting; compliance review of explainability outputs | ML Lead + Compliance | Phase 1-2 | Active |
| **R10** | Scalability | Platform cannot handle increased data volumes as more sources are integrated | 2 | 2 | 4 (Medium) | Design for scale from start; use auto-scaling services; implement partitioning strategies; load test before Phase 2+ | Platform Lead | Phase 2-4 | Planned |
| **R11** | Data Drift | Model performance degrades over time due to changing data patterns | 3 | 2 | 6 (High) | Implement SageMaker Model Monitor; define drift thresholds; automated alerting; establish retraining triggers and cadence | ML Lead | Phase 2+ | Planned |
| **R12** | Resource Availability | Key team members unavailable, causing knowledge gaps or delays | 2 | 2 | 4 (Medium) | Cross-training; documentation standards; identify backup resources; stagger critical deliverables | Program Manager | All Phases | Active |
| **R13** | Scope Creep | Expanding requirements within phases delay delivery and dilute focus | 2 | 2 | 4 (Medium) | Strict change control; phase scope lock at planning; separate backlog for future enhancements | Product Owner | All Phases | Active |
| **R14** | Third-Party Dependencies | External system owners (CRM, marketing) don't prioritize integration work | 2 | 3 | 6 (High) | Early stakeholder engagement; escalation paths defined; document integration requirements early; executive sponsorship | Program Manager | Phase 1-3 | Active |
| **R15** | Data Privacy | PII handling does not meet evolving regulatory requirements | 1 | 3 | 3 (Medium) | Data classification at ingestion; encryption and masking standards; privacy impact assessment; regular compliance reviews | Compliance + Data Lead | All Phases | Active |

---

### 2.3 Risk Heat Map

```
                    Impact
                 Low   Med   High
              ┌─────┬─────┬─────┐
        High  │     │ R04 │R01  │
              │     │     │R02  │
   Likelihood ├─────┼─────┼─────┤
        Med   │     │R06  │R03  │
              │R12  │R08  │R05  │
              │R13  │R10  │R09  │
              │     │     │R11  │
              │     │     │R14  │
              ├─────┼─────┼─────┤
        Low   │     │     │R07  │
              │     │     │R15  │
              └─────┴─────┴─────┘
```

---

## 3. Assumptions

### 3.1 Delivery Assumptions

| ID | Assumption | Impact if Invalid | Validation Approach |
|----|------------|-------------------|---------------------|
| **A01** | Nuvama will provide access to lead and outcome data within the first two weeks of each phase | Delays data preparation and model training | Data access agreements signed before phase start |
| **A02** | Business definitions for activation and lead scoring criteria will be agreed in Week 1 | Invalid model training and success measurement | Formal sign-off process with business stakeholders |
| **A03** | SME availability for weekly reviews throughout the project | Delays in decision-making and validation | Confirmed calendar commitments from sponsors |
| **A04** | One integration endpoint (CRM or activation list) will be agreed and prioritized early | Delays value realization from scoring | Early integration planning meetings |
| **A05** | The core delivery team will remain stable throughout each phase | Knowledge loss and ramp-up delays | Resource commitments from functional managers |
| **A06** | AWS cloud infrastructure can be provisioned within standard timelines (1-2 weeks) | Delays platform foundation setup | Pre-approved infrastructure requests |
| **A07** | Historical data covers at least 6-12 months of lead activity and outcomes | Insufficient training data for models | Data profiling in discovery phase |
| **A08** | Lead volume and patterns during pilot are representative of normal operations | Pilot results may not generalize | Statistical validation of pilot cohort |

### 3.2 Business Assumptions

| ID | Assumption | Impact if Invalid | Validation Approach |
|----|------------|-------------------|---------------------|
| **A09** | Business processes can accommodate AI-driven prioritization without major changes | Change management overhead increases | Process mapping and impact assessment |
| **A10** | RMs and sales teams are willing to adopt AI-generated lead priorities | Low utilization of delivered capabilities | Change management and training planning |
| **A11** | Conversion improvement from better prioritization will be measurable within 3-6 months | ROI validation delayed | Define leading indicators alongside lagging metrics |
| **A12** | The lead scoring use case is representative of future AI product needs | Patterns may not transfer to future products | Explicit documentation of reusable components |
| **A13** | Budget is available for cloud infrastructure and tooling for all defined phases | Scope reduction or phase delays | Budget confirmation before each phase |
| **A14** | Regulatory requirements for AI explainability are understood and stable | Rework needed if requirements change | Compliance consultation and documentation |

### 3.3 Technical Assumptions

| ID | Assumption | Impact if Invalid | Validation Approach |
|----|------------|-------------------|---------------------|
| **A15** | AWS services (SageMaker, Glue, Lake Formation) meet functional requirements | Alternative tooling needed | Proof of concept validation |
| **A16** | Batch processing (daily) meets business latency requirements for Phase 1 | Architecture changes needed | Business sign-off on SLA requirements |
| **A17** | Data quality is sufficient for meaningful model training with targeted remediation | Model accuracy compromised | Data profiling and quality assessment |
| **A18** | CRM system supports the planned integration approach (API or file-based) | Alternative integration patterns needed | Technical discovery with CRM team |
| **A19** | Network connectivity between cloud and on-premise systems is available | Delays in data ingestion | Infrastructure assessment |
| **A20** | Team has sufficient AWS ML/data engineering skills or can acquire them quickly | Training overhead and delays | Skills assessment and training plan |

---

## 4. Constraints

### 4.1 Technical Constraints

| ID | Constraint | Impact on Solution | Mitigation/Accommodation |
|----|------------|-------------------|--------------------------|
| **C01** | Primary cloud provider is AWS | Limits technology choices to AWS ecosystem or compatible tools | Design for AWS-first but maintain abstraction where critical |
| **C02** | Data must remain in India (AWS Mumbai region) for regulatory compliance | Limits region choices; may impact some service availability | Validate service availability in ap-south-1 |
| **C03** | Production systems require VPC isolation and private connectivity | No direct public internet access for data pipelines | VPC endpoints for AWS services; private subnets |
| **C04** | All infrastructure must be defined as code (Terraform) | Manual configuration not permitted | IaC patterns established early; team training if needed |
| **C05** | Model explainability is required for all production models | Limits model complexity; requires explainability tooling | Factor SHAP/LIME into model selection criteria |
| **C06** | Real-time scoring is out of scope for Phase 1 | Batch-only architecture in initial release | Design for streaming-readiness without implementing |

### 4.2 Budget Constraints

| ID | Constraint | Impact on Solution | Mitigation/Accommodation |
|----|------------|-------------------|--------------------------|
| **C07** | PoC budget is fixed; production budget requires Phase 1 success | Limited experimentation in PoC | Focus on highest-value features; defer nice-to-haves |
| **C08** | Cloud cost optimization is required from Phase 2 onwards | Infrastructure choices must consider cost | Reserved instances; spot for training; lifecycle policies |
| **C09** | No additional headcount; must use existing team capacity | Limits parallel work streams | Phased delivery; prioritization; selective outsourcing |

### 4.3 Regulatory Constraints

| ID | Constraint | Impact on Solution | Mitigation/Accommodation |
|----|------------|-------------------|--------------------------|
| **C10** | PII data handling must comply with Indian data protection regulations | Encryption, access controls, audit logging required | Compliance-first architecture; Lake Formation policies |
| **C11** | Model decisions affecting customers must be auditable | Logging and traceability infrastructure required | Scoring logs retained; model versioning |
| **C12** | Data retention policies must be enforced | Lifecycle management required | S3 lifecycle policies; documented retention periods |
| **C13** | Access to production data requires formal approval process | May slow down development/debugging | Masked/synthetic data for non-production; formal access requests |

### 4.4 Timeline Constraints

| ID | Constraint | Impact on Solution | Mitigation/Accommodation |
|----|------------|-------------------|--------------------------|
| **C14** | Phase 1 PoC must demonstrate value within 5 weeks | Limits scope; requires fast iteration | Minimal viable scope; pre-built patterns; focused deliverables |
| **C15** | Phase 1 production launch targeted within 12 weeks | Tight timeline for full production-ready deployment | Prioritization; parallel workstreams; scope management |
| **C16** | Business review cycles require 1-week lead time | Built-in delay for approvals | Front-load review-dependent items; scheduled review slots |

### 4.5 Organizational Constraints

| ID | Constraint | Impact on Solution | Mitigation/Accommodation |
|----|------------|-------------------|--------------------------|
| **C17** | CRM system changes require coordination with IT operations | Integration timeline dependent on IT capacity | Early engagement; clear requirements; escalation path |
| **C18** | Marketing system access requires separate approval process | May delay Phase 3 data access | Initiate approval process in Phase 2 |
| **C19** | Cross-functional teams have competing priorities | Resource availability may be limited | Executive sponsorship; documented commitments; escalation |
| **C20** | Change management for RM adoption requires sales leadership buy-in | Adoption risk if not secured | Early engagement; champion program; visible executive support |

---

## 5. Risk Monitoring & Review

### 5.1 Monitoring Cadence

| Activity | Frequency | Owner | Participants |
|----------|-----------|-------|--------------|
| Risk status update | Weekly | Risk Owners | Individual |
| Risk review meeting | Monthly | Program Manager | Project team + Risk Owners |
| Steering Committee risk report | Monthly | Program Manager | Steering Committee |
| Assumption validation | Monthly | Product Owner | Business + Technical leads |
| Constraint review | Quarterly | Architecture Lead | Architecture Board |

### 5.2 Escalation Process

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Risk Escalation Flow                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    Risk Identified
          │
          ▼
    ┌─────────────┐
    │ Risk Owner  │──── Low/Medium Risk ────► Monitor & Mitigate
    │ Assessment  │                           (Weekly update)
    └─────────────┘
          │
          │ High Risk
          ▼
    ┌─────────────┐
    │ Program     │──── Mitigation Defined ──► Implement & Track
    │ Manager     │                            (Weekly review)
    └─────────────┘
          │
          │ Critical Risk / Mitigation Failing
          ▼
    ┌─────────────┐
    │ Steering    │──── Decision Required ───► Approve mitigation /
    │ Committee   │                            Adjust scope/timeline
    └─────────────┘
          │
          │ Enterprise Impact
          ▼
    ┌─────────────┐
    │ Executive   │──── Strategic Decision ──► Program direction
    │ Sponsor     │
    └─────────────┘
```

### 5.3 Risk Response Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Avoid** | Eliminate the risk by changing approach | High-impact risks where alternatives exist |
| **Mitigate** | Reduce likelihood or impact | Most common; default for medium+ risks |
| **Transfer** | Shift risk to third party (insurance, vendor) | Where external parties better positioned |
| **Accept** | Acknowledge and monitor | Low risks; risks with acceptable residual impact |
| **Escalate** | Elevate decision to higher authority | When mitigation requires authority beyond team |

### 5.4 Key Risk Indicators (KRIs)

| KRI | Threshold | Action Trigger |
|-----|-----------|----------------|
| Data quality score | <90% | Escalate to Data Lead |
| Model accuracy decline | >5% from baseline | Trigger retraining review |
| Integration test failures | >10% | Technical investigation |
| Stakeholder engagement score | <3/5 | Change management intervention |
| Timeline variance | >10% | Scope/resource review |
| Budget variance | >10% | Financial review with Steering Committee |

---

## 6. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | December 2024 | Program Team | Initial version |

---

## Appendix A: Risk Assessment Template

**For new risks, complete the following:**

```
Risk ID:          R##
Category:         [Data Quality | Technical | Timeline | Security | Compliance | 
                   Adoption | Integration | Scalability | Resource | Scope]
Description:      [Clear description of the risk event]
Likelihood:       [1-Low, 2-Medium, 3-High]
Impact:           [1-Low, 2-Medium, 3-High]
Score:            [Likelihood × Impact]
Mitigation:       [Specific actions to reduce likelihood or impact]
Owner:            [Person accountable for managing this risk]
Phase Affected:   [Phase 1, 2, 3, 4, or All]
Status:           [Active | Planned | Closed | Accepted]
Date Identified:  [YYYY-MM-DD]
Target Resolution:[YYYY-MM-DD or "Ongoing"]
```

## Appendix B: References

- [Data Platform Strategy](./data-platform-strategy.md)
- [Value Delivery Roadmap](./value-delivery-roadmap.md)
- [Business Case](../project-context/business-case.md)
- [Technology Stack](../project-context/tech-stack.md)
