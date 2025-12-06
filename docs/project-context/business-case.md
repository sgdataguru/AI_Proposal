# Business Case: AI Lead Scoring as the Foundation for Nuvama’s Revenue AI Roadmap (India)

## Executive Summary

Nuvama Financial will kickstart its AI-led revenue transformation with a **Lead Scoring & Activation** product designed with **AI governance-by-design**. This first model will establish the standards, data foundations, operating controls, and measurable value needed to scale confidently into higher-complexity revenue levers: **AI Portfolio Review Engine**, **AI Campaign Intelligence**, **Client 360° Data Lake**, **IFA/Partner Portal AI**, and finally an **RM AI Co-Pilot**.

This phased approach ensures Nuvama captures quick revenue impact early while building a trusted, compliant, and scalable AI product ecosystem aligned with financial services expectations in India.

---

## Company Background (Context for this Proposal)

**Nuvama Financial** is a leading wealth and investment firm in India with a growing ecosystem across RMs, IFAs, and partners. The business depends heavily on increasing client activation, expanding wallet share, improving advisor productivity, and enabling scalable partner-assisted growth.

As acquisition channels diversify and volume of leads increases, the current prioritisation approach—typically rule-based, manual, or experience-driven—limits conversion efficiency and makes consistent performance difficult to scale across teams.

---

## Current Challenges

### 1. Lead Prioritisation Is Not Predictive
- Leads are often treated similarly despite varying intent levels.
- High-potential leads can be missed or contacted too late.
- RM and telesales time is spent disproportionately on low-intent prospects.

### 2. Limited Closed-Loop Learning
- Lead outcomes are not systematically fed back into models or strategy.
- Campaign and sales performance insights are fragmented.

### 3. Scaling Constraints Across Channels
- As Nuvama expands partner ecosystems and digital funnels, the manual effort required to support lead nurturing rises sharply.

---

## Business Objectives

### Primary Objectives (Phase 1: Lead Scoring)

1. **Increase Activation Efficiency**
   - Identify high-intent leads early and boost conversion probability.
2. **Optimise RM & Inside Sales Focus**
   - Provide priority queues and clear next steps.
3. **Establish Governance-First AI Product Standard**
   - Build the first AI model with embedded controls, transparency, and monitoring.
4. **Create a Reusable AI Pattern**
   - Make Lead Scoring the template for future revenue AI products.

---

## Proposed Roadmap (Sequenced Value Build)

1. **AI Lead Scoring & Activation (Foundation Product)**
   - Build the first revenue AI model that prioritises high-intent leads and triggers focused activation actions.
   - This becomes the **governance + data + deployment blueprint** for everything else.

2. **AI Portfolio Review Engine**
   - After lead flows are optimised, shift to **existing client growth** by generating portfolio diagnostics that prompt timely upsell and rebalancing opportunities.

3. **AI Campaign Intelligence**
   - Use learnings from lead conversion signals and portfolio behaviours to optimise **product, timing, and channel** for higher ROI.

4. **Client 360° Data Lake**
   - Consolidate trading, MF, PMS, CRM, and engagement data for a unified truth layer.
   - Enables high-trust personalisation at scale.

5. **AI Upgrade for IFA / Partner Portal**
   - Equip IFAs and partners with automated product comparisons, proposals, and client insights.
   - Reduces RM dependency and creates a scalable partner revenue engine.
   - **Core problem solved:** Partners bring business, but without AI support the load shifts back to RMs and doesn’t scale.

6. **RM / Advisor AI Co-Pilot**
   - With governance, data, and model infrastructure proven, introduce a co-pilot with summaries, churn alerts, next-best actions, and compliant call scripts.

---

## Why Lead Scoring First (Strategic Rationale)

Lead scoring is the most practical starting point because it:
- Requires **narrower data scope** than a full Client 360 build.
- Produces **fast, measurable outcomes**.
- Introduces AI to frontline teams in a low-friction way.
- Allows Nuvama to establish **AI governance patterns** before higher-risk, higher-complexity models.

---

## Product Scope for Lead Scoring (Initial)

### In Scope
- One priority lead segment (e.g., digital acquisition or one key campaign type).
- Historical lead + engagement + outcome data (e.g., 6–12 months, subject to availability).
- Creation of:
  - Lead score (probability/index)
  - Priority bands (Hot/Warm/Cold)
  - Simple explainability (top drivers)
- One integration path:
  - CRM priority view **or**
  - Daily activation list for inside sales **or**
  - Campaign audience segment
- Baseline vs. pilot measurement plan.

### Out of Scope (for first release)
- Full enterprise Client 360.
- Real-time scoring.
- Multi-product optimisation across all segments.
- Enterprise-grade MLOps maturity (will be phased in).

---

## AI Governance by Design (Lead Scoring)

This first AI product will be implemented with embedded controls:

### 1. Data Governance
- Clear data ownership, access roles, and approved sources.
- Documented data definitions:
  - “Lead,” “Activation,” “High-intent signals.”
- Data quality checks:
  - Completeness, duplication, bias hotspots.

### 2. Model Governance
- Explainability minimum standard:
  - Top 5 drivers per score band.
- Human-in-the-loop controls:
  - Business review of band thresholds.
- Versioning:
  - Model versions tracked with change rationale.

### 3. Operational Governance
- Monitoring:
  - Drift checks and performance tracking.
- Auditability:
  - Reproducible scoring logs for sample decisions.
- Escalation:
  - Defined process for model performance degradation.

---

## 5-Week PoC Plan (Lead Scoring)

### Week 1 – Discovery & Metric Lock
- Confirm:
  - Lead type
  - Activation definition
  - Pilot cohort
  - KPIs
- Data access + sampling.
- Baseline performance captured.

### Week 2 – Data Prep & Feature Build
- Data profiling and cleansing.
- Feature engineering:
  - Source, channel, engagement, recency, frequency.
- Initial baseline model.

### Week 3 – Model Iteration & Governance Review
- Tune model and define:
  - Scoring bands.
  - Explainability outputs.
- Review with business + risk/ops stakeholders.

### Week 4 – Integration & Pilot Launch
- Implement scoring pipeline (batch).
- Push results into CRM/activation workflow.
- Start small pilot.

### Week 5 – Measurement & Scale Blueprint
- Compare:
  - Hot vs. non-Hot leading indicators.
- Final PoC report with:
  - Uplift signals.
  - Governance artefacts.
  - Recommendation for Phase 1 production rollout.

---

## Experiment → Production-Ready Path (Lead Scoring)

1. **Experiment**
   - Prototype model using historical data.
   - Validate directional lift.

2. **Pilot**
   - Limited cohort, parallel run.
   - Human validation of ranking quality.

3. **Minimum Viable AI Product**
   - Scheduled batch scoring.
   - CRM integration.
   - Basic dashboard.

4. **Governed Production**
   - Defined RACI.
   - Model versioning + change control.
   - Drift monitoring.

5. **Scaled AI Platform Pattern**
   - The same blueprint applied to:
     - Portfolio Review
     - Campaign Intelligence
     - IFA Portal AI
     - RM Co-Pilot

---

## Assumptions

- Nuvama will provide:
  - Access to lead and outcome data.
  - Business definitions for activation.
  - SME availability for weekly reviews.
- One integration endpoint is agreed early.

---

## Dependencies

- CRM / lead system owners.
- Marketing / campaign data owners.
- Data platform and cloud infrastructure support.
- Compliance/infosec alignment for data access.

---

## Top Risks & Mitigations

1. **Activation definition ambiguity**
   - *Mitigation:* Lock definition in Week 1 with business sign-off.

2. **Data quality gaps**
   - *Mitigation:* Focus on high-signal features first; define a remediation backlog.

3. **Integration delays**
   - *Mitigation:* Start with secure CSV/flat-file integration for PoC.

4. **Insufficient time for full uplift measurement**
   - *Mitigation:* Track leading indicators (contact rate, meeting bookings).

5. **Low frontline adoption**
   - *Mitigation:* Co-design priority bands with RMs; keep UI simple.

---

## Value Proposition

### Business Value
- Higher activation efficiency through smarter prioritisation.
- Better RM productivity with focused lead queues.
- Faster revenue impact with controlled risk.

### Technical Value
- A reusable AI product pattern.
- Governance foundation ahead of more complex models.
- Scalable architecture aligned to future Client 360 adoption.

---

## What This Enables Next

**Lead Scoring becomes the foundation** for structured scaling:

- **Portfolio Review** applies the same governance + scoring pattern to existing client assets and sales-trigger alerts.
- **Campaign Intelligence** uses lead/portfolio signals to optimise product, timing and channel.
- **Client 360° Data Lake** consolidates data for trusted personalisation and next-best-action strategies.
- **IFA Portal AI** extends insights to partners so RMs don’t become the bottleneck.
- **RM Co-Pilot** is introduced safely after trust, data quality and model governance are proven.

---

**Prepared for:** Nuvama Financial (India)  
**Use case focus:** AI Lead Scoring & Activation as Phase 1 of a multi-lever Revenue AI roadmap  
**Document type:** Business Case (Proposal-ready narrative)
