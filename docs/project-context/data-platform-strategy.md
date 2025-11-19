# Data Platform Strategy

## Executive Summary

### Business Context
PALO IT e-Commerce faces critical data fragmentation across product, customer, and transaction systems, preventing comprehensive multi-currency, multi-region analytics needed to support $8M in annual revenue across 15+ countries. Manual reporting takes 2-3 days, conflicting metrics undermine decision-making, and geographic performance insights remain invisible.

### Strategic Vision
We will establish a modern cloud-native data platform on Microsoft Azure that consolidates fragmented data sources into a governed, dimensional data warehouse. This platform will enable self-service analytics, multi-currency reporting, and data-driven decision making while reducing report generation from days to minutes. The platform will leverage a medallion architecture pattern with progressive data refinement, API-based ingestion, and managed Azure services to minimize operational complexity.

### Expected Outcomes
- **Single source of truth** eliminating conflicting reports and saving 15+ hours/week in reconciliation
- **Sub-5-minute reporting** replacing 2-3 day manual processes, delivering $80K annual productivity savings
- **Multi-currency analytics** enabling 3-5% revenue growth ($240K-$400K) through geographic optimization
- **Customer segmentation** driving 10-15% repeat purchase improvement ($400K additional revenue)
- **Product portfolio optimization** generating $300K revenue improvement through data-driven decisions

### Strategic Bets
1. **Cloud-native on Azure**: Leverage existing Microsoft enterprise agreement and Azure AD integration vs. multi-cloud complexity
2. **Batch-first architecture**: Daily refresh meets current business needs at 3-5x lower cost than real-time streaming, with architecture allowing future evolution
3. **Dimensional modeling**: Star schema provides business-aligned, performant analytics preferred by SQL/BI-skilled teams over complex data lake patterns

---

## Business Requirements & Strategic Response

### REQ-001: Establish Single Source of Truth for E-Commerce Analytics

**Strategic Approach**: Centralize all e-commerce data (products, customers, orders, geographic reference) in Azure Synapse Analytics using a star schema dimensional model that provides consistent business definitions and enables governed self-service analytics across all departments.

**Key Capabilities**:
- API-based data ingestion from 5 source systems (Fake Store API, Exchange Rates API, REST Countries API)
- Medallion architecture (Bronze → Silver → Gold) for progressive data quality improvement
- Semantic layer in Power BI providing consistent business metrics definitions
- Data lineage tracking showing data origin through transformation to consumption

**Success Criteria**:
- All business reports draw from single Azure Synapse data warehouse
- <5% variance in metrics across teams (Finance, Sales, Marketing)
- 95%+ data quality score (completeness, accuracy, consistency)
- Zero manual spreadsheet-based geographic/currency reference data

**Dependencies**:
- API source connectivity validated (REQ-003)
- Data quality framework operational (REQ-005)
- Azure infrastructure provisioned

**Strategic Rationale**: 
Star schema data warehouse chosen over data lake because: (1) structured analytics with known dimensions is the primary use case, (2) business users need governed, consistent SQL-queryable definitions vs. semi-structured exploration, (3) team has SQL/BI skills vs. big data engineering capabilities, (4) query performance requirements favor dimensional models, (5) complexity and cost are significantly lower for batch-oriented analytics workloads.

---

### REQ-002: Enable Multi-Currency, Multi-Region Analytics

**Strategic Approach**: Implement dual-currency storage pattern where transactions are stored in both original local currency and USD-normalized amounts, with automated daily exchange rate ingestion and point-in-time currency conversion ensuring temporal accuracy for historical analysis.

**Key Capabilities**:
- Daily ingestion of exchange rates from Exchange Rates API (15+ currencies)
- Fact table design storing both local_amount and usd_amount columns
- Date-aligned currency conversion using historical exchange rates
- Geographic dimension hierarchy (Country → Region → Sub-region) enabling drill-down
- Currency dimension tracking exchange rate history and metadata

**Success Criteria**:
- Revenue reportable in both transaction currency and USD
- Currency exchange rate impact quantifiable (variance reporting)
- Geographic drill-down from region to country level functional
- 100% of transactions have valid currency conversion based on transaction date

**Dependencies**:
- Exchange Rates API access and historical data backfill
- dim_location populated from REST Countries API
- fact_sales dimensional model implemented

**Strategic Rationale**:
Dual-currency storage approach avoids runtime conversion complexity and ensures consistent reporting. Storing both currencies eliminates recalculation errors and improves query performance. Daily batch refresh of exchange rates is sufficient (vs. real-time) because business decisions operate on daily/weekly cycles, and historical rate changes don't require intraday precision. Geographic dimension hierarchy enables critical regional analysis for international expansion strategy.

---

### REQ-003: Deliver Product Performance Insights

**Strategic Approach**: Build dimensional model with product hierarchy (Category → Product) and slowly-changing dimension Type 2 tracking for price changes, enabling time-series analysis of product performance across geographic markets with consistent historical comparison.

**Key Capabilities**:
- dim_product with SCD Type 2 for price change tracking over time
- dim_product_category hierarchy for category-level roll-ups
- fact_sales at grain of product × order line enabling detailed analysis
- Product rating dimensions captured for correlation analysis
- Cross-dimensional analysis linking products to geography and customer segments

**Success Criteria**:
- Identify top 20% products driving 80% of revenue
- Track product performance trends over 12-month history
- Compare product performance across countries/regions
- Correlate product ratings with sales volume

**Dependencies**:
- Fake Store API product catalog ingestion
- dim_product and dim_product_category implemented
- fact_sales with product foreign key
- Data synthesis logic for realistic transaction distribution

**Strategic Rationale**:
SCD Type 2 for product dimension enables accurate historical revenue analysis when prices change, critical for understanding performance drivers. Grain at order line level (vs. order level) allows precise product-level metrics while supporting category-level aggregations. The dimensional approach enables intuitive drill-down from category to product that business users expect in BI tools like Power BI.

---

### REQ-004: Understand Customer Behavior and Segmentation

**Strategic Approach**: Create 360-degree customer view through dimensional model linking demographics (dim_customer) to purchase behavior (fact_sales), with derived customer segmentation (New/Regular/VIP) calculated during Gold layer transformation based on purchase frequency and lifetime value.

**Key Capabilities**:
- dim_customer with demographic attributes from User API
- Customer segmentation logic (New: 1-2 orders, Regular: 3-10 orders, VIP: 11+ orders)
- Customer lifetime value (CLV) calculation through aggregated fact_sales
- Cross-category purchase analysis through product-customer joins
- Geographic customer distribution through customer-location joins

**Success Criteria**:
- Customers segmented into New/Regular/VIP tiers with 95%+ accuracy
- Top 20 customers by revenue identifiable
- Cross-category purchase patterns analyzable
- Customer geographic distribution reportable by country/region
- Repeat purchase rate trackable over time

**Dependencies**:
- Fake Store API user data ingestion
- fact_sales with customer foreign key
- Data synthesis creating realistic customer purchase patterns
- dim_location for customer geographic assignment

**Strategic Rationale**:
Customer segmentation in Gold layer (vs. real-time) aligns with daily batch architecture while providing business-critical insights. Segment definitions based on purchase behavior (frequency + value) are actionable for marketing campaigns. Dimensional model enables flexible customer analysis across products, geography, and time without complex joins. The approach supports both aggregate segment analysis and individual customer drill-down.

---

### REQ-005: Improve Operational Efficiency Through Automation

**Strategic Approach**: Implement end-to-end automation through Azure Data Factory orchestration, dbt transformations with built-in testing, and Power BI semantic layer enabling self-service analytics, replacing manual Excel-based reporting with governed, auditable data pipelines.

**Key Capabilities**:
- Azure Data Factory pipelines orchestrating daily data refresh
- Automated API extraction with retry logic and error handling
- dbt transformations with data quality tests at each layer
- Power BI semantic layer providing pre-built measures and KPIs
- Alerting on pipeline failures and data quality violations
- Self-service report building through Power BI with governed datasets

**Success Criteria**:
- Report generation time reduced from 2-3 days to <5 minutes
- Data refresh automated daily with <1% failure rate
- Self-service adoption: 50% of business users accessing dashboards independently
- Zero manual Excel-based geographic or currency calculations
- 15+ hours/week saved across business teams

**Dependencies**:
- Azure Data Factory and dbt Cloud configured
- Data quality framework implemented (Great Expectations or dbt tests)
- Power BI workspace with semantic models deployed
- User training and documentation delivered

**Strategic Rationale**:
Automation through managed services (Azure Data Factory, Power BI) reduces operational burden vs. self-managed orchestration. dbt provides software engineering rigor (version control, testing, documentation) to data transformations. Power BI semantic layer ensures consistent metric definitions while enabling self-service exploration. The approach balances governance (centralized semantic layer) with flexibility (self-service report building).

---

## Data Platform Strategy

### Data Architecture Pattern

**Selected Pattern**: **Medallion Architecture (Bronze → Silver → Gold)**

**Description**:
- **Bronze Layer**: Raw data ingestion from source APIs, stored as-is in Azure Data Lake Gen2 with minimal transformation (schema inference, data type conversion, partition by ingestion date)
- **Silver Layer**: Cleansed and conformed data with validation rules applied, standardized formats, deduplicated records, basic transformations (e.g., JSON parsing, data type corrections)
- **Gold Layer**: Business-aligned dimensional model (star schema) with denormalized, aggregated, and enriched datasets optimized for analytics consumption

**Rationale**:
- **Separation of concerns**: Each layer has clear responsibility (preserve → cleanse → curate) following single responsibility principle
- **Reprocessability**: Preserving raw data in Bronze enables reprocessing if transformation logic changes
- **Incremental complexity**: Progressive refinement matches team skills (start simple, add sophistication over time)
- **Cost optimization**: Hot data in Gold (frequent queries), warm in Silver (occasional reprocessing), cold in Bronze (archival/compliance)
- **Flexibility**: Architecture supports both batch (current) and streaming (future) without redesign

**Implementation Considerations**:
- Zone boundaries enforced through Azure resource groups and access controls
- Each layer stored in separate Azure Data Lake Gen2 containers
- Clear data contracts between layers documented in dbt models
- Lineage tracked through dbt model dependencies and Azure Purview (future)

---

### Data Storage Strategy

**Storage Tiers**:

| Layer | Storage | Format | Access Pattern | Retention | Rationale |
|-------|---------|--------|----------------|-----------|-----------|
| **Bronze** | Azure Data Lake Gen2 (Cool tier) | Parquet (compressed) | Rare (reprocessing only) | 2 years | Preserve source data for compliance and reprocessing at lowest cost |
| **Silver** | Azure Data Lake Gen2 (Hot tier) | Parquet (partitioned by date) | Occasional (troubleshooting, backfills) | 1 year | Cleansed data for ad-hoc analysis and reprocessing |
| **Gold** | Azure Synapse Analytics (dedicated SQL pool) | Columnar (columnstore indexes) | Frequent (daily analytics queries) | 3 years | Optimized for query performance with dimensional model |
| **Semantic** | Power BI Premium | In-memory (aggregations) | Very frequent (user dashboards) | N/A | Sub-second query response for business users |

**Data Lifecycle Management**:
- Automated archival from Hot to Cool/Archive tiers after 90 days (Bronze/Silver)
- Gold layer implements partitioning by date for efficient query pruning
- Historical snapshots maintained for compliance and year-over-year analysis

**Rationale**:
- **Cost optimization**: Tiered storage aligns cost with access patterns (80% savings moving Bronze to Cool tier)
- **Performance**: Gold layer in Synapse with columnstore provides <5 second query performance
- **Scalability**: Data Lake Gen2 scales to petabyte-level if business grows 100x
- **Compliance**: 2-year retention in Bronze meets regulatory requirements for financial data

---

### Data Integration Approach

**Processing Model**: **Daily Batch with Idempotent Pipeline Design**

**Pipeline Architecture**:
1. **Extraction**: Azure Data Factory HTTP connectors to REST APIs with retry logic and rate limiting
2. **Loading**: Parquet files written to Bronze layer (immutable, date-partitioned)
3. **Transformation**: dbt models executing in Synapse, promoting from Bronze → Silver → Gold
4. **Orchestration**: Azure Data Factory master pipeline triggering sequential layer processing

**Key Design Principles**:
- **Idempotency**: All transformations designed to produce identical results when re-run (critical for reprocessing)
- **Incremental processing**: Where possible, process only new/changed data (e.g., new orders since last run)
- **Full refresh for dimensions**: Static/slow-changing data (products, countries) fully replaced daily
- **Watermarking**: Track last successful extraction timestamp to enable incremental loads
- **Graceful degradation**: If one source fails, other sources continue processing

**Schedule**: 
- Daily execution at 2:00 AM local time (low business activity)
- Total runtime target: <2 hours for full refresh
- Data available by 5:00 AM for business users

**Rationale**:
- **Business alignment**: Daily reporting cycle meets current decision-making needs
- **Cost efficiency**: Batch processing 3-5x cheaper than streaming for same data volume
- **Simplicity**: Easier to troubleshoot and maintain vs. complex streaming pipelines
- **Team skills**: Matches SQL/Python skills vs. requiring Spark streaming expertise
- **Future-proof**: Medallion architecture supports adding streaming sources without redesign

---

### Data Modeling Approach

**Selected Approach**: **Star Schema with Slowly Changing Dimensions**

**Dimensional Model Design**:

```
Fact Table:
├── fact_sales (Grain: One row per product per order)
    ├── Measures: quantity, unit_price_usd, unit_price_local, total_amount_usd, total_amount_local, exchange_rate
    ├── Foreign Keys: product_key, customer_key, order_date_key, location_key
    
Dimension Tables:
├── dim_product (SCD Type 2 - track price changes)
    ├── Attributes: product_id, product_name, category, base_price, rating, rating_count, valid_from, valid_to
├── dim_customer (SCD Type 1 - overwrite)
    ├── Attributes: customer_id, name, email, address, phone, segment (New/Regular/VIP)
├── dim_location (SCD Type 1)
    ├── Attributes: country_code, country_name, region, sub_region, capital, currency_code, population
├── dim_date (Static - pre-generated)
    ├── Attributes: date_key, full_date, year, quarter, month, week, day_of_week, is_weekend, is_holiday
├── dim_product_category (Static)
    ├── Attributes: category_id, category_name, category_description
```

**SCD Strategy**:
- **Type 2 for dim_product**: Preserve price history for accurate historical revenue analysis
- **Type 1 for dim_customer**: Overwrite addresses/phones (business doesn't need address history)
- **Type 1 for dim_location**: Country data rarely changes; overwrite if updates occur

**Rationale**:
- **Business alignment**: Dimensional model maps directly to business concepts (products, customers, locations)
- **Query performance**: Star schema optimized for OLAP queries with simple joins
- **User comprehension**: Business users understand dimensional model concepts vs. normalized 3NF
- **BI tool compatibility**: Power BI, Tableau, Looker natively optimized for star schema
- **Incremental complexity**: Start with simple dimensions, add complexity (hierarchies, role-playing dimensions) as needed

---

### Data Quality Strategy

**Quality Dimensions Addressed**:
- **Completeness**: All required fields populated (no critical nulls)
- **Accuracy**: Values match source systems and pass validation rules
- **Consistency**: Related data elements logically coherent (e.g., currency matches country)
- **Timeliness**: Data refreshed within SLA (daily by 5:00 AM)
- **Uniqueness**: No duplicate records (enforced primary keys)
- **Referential Integrity**: All foreign keys resolve to dimension records

**Quality Enforcement Architecture**:

| Layer | Quality Focus | Implementation | Action on Failure |
|-------|---------------|----------------|-------------------|
| **Bronze** | Completeness, Schema | Validate JSON structure, log raw data | Alert, store in quarantine table |
| **Silver** | Accuracy, Consistency | dbt tests (not_null, accepted_values, relationships) | Fail pipeline, alert data engineer |
| **Gold** | Referential Integrity, Business Rules | dbt tests on dimensional model, semantic validation | Fail pipeline, rollback to prior version |

**dbt Testing Framework**:
```yaml
# Example dbt tests for fact_sales
models:
  - name: fact_sales
    tests:
      - dbt_utils.expression_is_true:
          expression: "quantity > 0"
      - dbt_utils.expression_is_true:
          expression: "total_amount_usd >= 0"
    columns:
      - name: product_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_product')
              field: product_key
      - name: customer_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_customer')
              field: customer_key
```

**Data Quality Monitoring**:
- **Dashboard**: Real-time data quality metrics per table (completeness %, test pass rate)
- **Alerting**: Email/Slack alerts on pipeline failures or quality threshold breaches
- **SLA Tracking**: Monitor data freshness (time from source change to Gold availability)

**Rationale**:
- **Shift-left approach**: Catch quality issues early (Bronze/Silver) vs. discovering in dashboards
- **Test-driven development**: dbt tests document data contracts and prevent regressions
- **Fail-fast philosophy**: Better to halt pipeline than propagate bad data to business users
- **Observability**: Data quality dashboard provides transparency into platform health

---

### Data Lineage & Observability

**Lineage Tracking Strategy**:

**Column-Level Lineage** (via dbt):
- Every dbt model documents source → transformation → target
- SQL-level lineage showing which source columns contribute to target columns
- Dependency graphs visualizing data flow across layers

**Operational Lineage** (via Azure Data Factory):
- Pipeline execution logs showing success/failure per activity
- Data movement tracking (source → Bronze → Silver → Gold)
- Execution time per pipeline component for performance tuning

**Business Lineage** (via Azure Purview - future phase):
- Business glossary linking technical tables to business terms
- Impact analysis showing downstream dashboards affected by schema changes
- Data classification (PII, sensitive) for compliance

**Observability Implementation**:

| Component | Metrics Tracked | Alerting Threshold |
|-----------|-----------------|-------------------|
| **API Extraction** | Success rate, latency, error codes | <95% success rate |
| **dbt Transformations** | Model runtime, test pass rate, row counts | >5% row count variance |
| **Synapse Queries** | Query duration, query failures | >10 second average |
| **Power BI Refresh** | Refresh duration, refresh failures | Any failure |

**Rationale**:
- **Troubleshooting**: Lineage enables rapid root cause analysis when data looks incorrect
- **Impact assessment**: Understand downstream effects before making schema changes
- **Compliance**: Document data origins for regulatory audit requirements
- **Performance tuning**: Identify bottlenecks in pipelines through operational metrics

---

### Security & Governance Approach

**Security Layers**:

**1. Network Security**:
- Azure Virtual Network with private endpoints for Synapse, Data Lake, Key Vault
- Network Security Groups restricting inbound traffic to corporate network only
- Azure Firewall for outbound API connections with allowlist
- No public internet access to data assets

**2. Identity & Access Management**:
- Azure AD authentication for all users (SSO with existing Microsoft 365)
- Role-Based Access Control (RBAC) with principle of least privilege:
  - **Data Engineers**: Read/write to Bronze/Silver, read-only to Gold
  - **Business Analysts**: Read-only to Gold, Power BI workspace access
  - **Executives**: Read-only to Power BI dashboards only
- Service principals for pipeline automation (no shared credentials)

**3. Data Encryption**:
- **At Rest**: Azure Storage Service Encryption with Microsoft-managed keys
- **In Transit**: TLS 1.2 for all API connections and internal data movement
- **Sensitive Fields**: Consider dynamic data masking for PII in Synapse (future)

**4. Audit & Compliance**:
- Azure Monitor logs tracking all data access (who, what, when)
- 90-day retention for audit logs (extendable for compliance)
- Quarterly access reviews to validate RBAC assignments
- GDPR compliance through data residency (EU region) and right-to-erasure

**Governance Framework**:

**Data Classification**:
- **Public**: Product catalog, exchange rates
- **Internal**: Aggregated sales metrics, customer segments
- **Confidential**: Individual customer PII (name, email, address)

**Data Stewardship**:
- **Business Owners**: Finance (revenue data), Marketing (customer data), Product (catalog)
- **Data Steward**: Data Platform Lead responsible for quality, lineage, cataloging
- **Technical Owner**: Data Engineering Team responsible for pipelines, infrastructure

**Governance Processes**:
- **Schema Change Management**: All schema changes require business owner approval and impact analysis
- **Access Requests**: Formal ticketing process with business justification
- **Data Retirement**: Automated archival policies, manual approval for deletion

**Rationale**:
- **Regulatory compliance**: GDPR, SOX requirements for data privacy and audit trails
- **Risk mitigation**: Defense-in-depth security layers prevent unauthorized access
- **Trust building**: Transparent governance builds business user confidence in data
- **Operational efficiency**: Clear ownership and processes reduce friction

---

## Technology Approach

### Cloud Platform Rationale

**Selected Platform**: **Microsoft Azure**

**Strategic Reasons**:
1. **Existing Investment**: Enterprise Agreement with favorable pricing, existing Microsoft 365 and Dynamics CRM
2. **Authentication Integration**: Azure AD provides SSO, eliminating separate identity management
3. **Skill Alignment**: Team has SQL Server and .NET experience, natural fit with Azure ecosystem
4. **Regulatory Compliance**: Azure regions in EU and US meet data residency requirements for GDPR
5. **Total Cost of Ownership**: Leveraging existing EA reduces infrastructure costs by ~30% vs. AWS/GCP

**Azure Services Selected**:
- **Azure Synapse Analytics**: Unified analytics platform (data warehouse + pipelines + notebooks)
- **Azure Data Lake Storage Gen2**: Scalable, cost-effective storage for Bronze/Silver layers
- **Azure Data Factory**: Orchestration and API ingestion
- **Power BI Premium**: Enterprise BI with semantic layer and row-level security
- **Azure Key Vault**: Secrets management for API keys and connection strings
- **Azure Monitor**: Logging, alerting, and observability

**Rationale**: Choosing Azure aligns with organizational standards and reduces risk. Managed services (Synapse, ADF, Power BI) minimize operational overhead vs. self-managing Spark clusters or Airflow.

---

### Core Platform Capabilities Needed

**Capabilities Matrix**:

| Capability | Azure Service | Justification |
|------------|---------------|---------------|
| **Data Storage (Bronze/Silver)** | Azure Data Lake Gen2 | Scalable, hierarchical namespace, cost-effective ($0.02/GB/month) |
| **Data Warehouse (Gold)** | Azure Synapse Analytics | Columnar storage, MPP, native Power BI integration |
| **Data Pipelines (Ingestion)** | Azure Data Factory | Managed orchestration, 90+ connectors, serverless |
| **Data Transformation** | dbt Cloud + Synapse | Software engineering rigor (Git, testing, CI/CD) |
| **Analytics & BI** | Power BI Premium | Enterprise BI, semantic layer, mobile apps |
| **Secrets Management** | Azure Key Vault | Centralized secrets, audit logging, HSM-backed |
| **Monitoring & Alerting** | Azure Monitor + Log Analytics | Native integration, KQL queries, dashboards |
| **Data Catalog** | Azure Purview (future) | Data discovery, lineage, governance |

**Preference for Managed Services**:
- **Rationale**: Prefer managed services (ADF, Synapse, Power BI) over self-managed (Airflow, Spark, Superset) to reduce operational burden and focus team on business value vs. infrastructure management.
- **Trade-off**: Slightly higher cost (~20% premium) for managed services justified by reduced engineering time and faster time-to-value.

---

### Integration Patterns

**API Integration Pattern**: **RESTful HTTP with Retry and Circuit Breaker**

**Implementation**:
- Azure Data Factory HTTP Linked Services for API connections
- Retry policy: 3 attempts with exponential backoff (5s, 15s, 45s)
- Circuit breaker: Stop calling API after 5 consecutive failures, alert on-call engineer
- Rate limiting: Respect API provider limits (e.g., 100 requests/minute)
- Authentication: API keys stored in Azure Key Vault, rotated quarterly

**Data Movement Pattern**: **Polybase for Bulk Loading**

**Implementation**:
- Large datasets (fact_sales) loaded from Data Lake to Synapse via Polybase (parallel bulk loading)
- Small datasets (dimensions) loaded via COPY statement
- Partition pruning: Load only new/changed partitions (incremental)

**Avoid Point-to-Point Integrations**:
- All source systems integrate through Bronze layer (hub-and-spoke pattern)
- No direct source → Gold connections (all data flows through medallion layers)
- Rationale: Centralized integration point simplifies troubleshooting and enables reuse

**Standard Protocols**:
- REST APIs for synchronous data extraction
- Event-driven (future): Azure Event Hubs for real-time streaming sources
- File-based (future): Azure Data Share for partner data exchange

**Rationale**: Standard patterns with retry/circuit breaker logic provide resilience. Hub-and-spoke through Bronze layer avoids spaghetti architecture and enables adding sources without disrupting existing pipelines.

---

### Analytics & Reporting Approach

**BI Architecture**: **Semantic Layer with Governed Self-Service**

**Power BI Semantic Layer**:
- Centralized semantic model defining metrics (Total Revenue, AOV, CLV, etc.)
- Pre-built measures with DAX logic (e.g., revenue with currency conversion)
- Row-level security enforcing access control by region/department
- Incremental refresh for large fact tables (only load new data)

**Report Consumption Tiers**:

| Tier | Users | Report Type | Refresh Frequency | Delivery |
|------|-------|-------------|-------------------|----------|
| **Executive** | C-Level (5 users) | Fixed dashboards | Daily 6 AM | Power BI app, mobile |
| **Business Analyst** | Analysts (20 users) | Customizable reports | Daily 6 AM | Power BI workspace |
| **Self-Service** | All users (50+ users) | Ad-hoc exploration | Daily 6 AM | Power BI workspace, export to Excel |
| **Scheduled** | Email distribution lists | PDF reports | Weekly Monday 8 AM | Email attachment |

**Self-Service Guardrails**:
- Users build reports from semantic model (can't write SQL against warehouse directly)
- Pre-defined dimensions and measures ensure consistent calculations
- Ability to export to Excel for offline analysis
- Admin approval required for new calculated measures in semantic layer

**Rationale**: Semantic layer balances governance (consistent metrics) with flexibility (self-service exploration). Power BI Premium provides enterprise-scale performance with security. Tiered consumption model right-sizes access for different user needs.

---

### Infrastructure as Code

**Selected Approach**: **Terraform for Azure Infrastructure**

**IaC Scope**:
- Azure resource groups, subscriptions, regions
- Azure Synapse workspace, SQL pools, Spark pools
- Azure Data Lake Gen2 accounts, containers, folder structure
- Azure Data Factory pipelines and linked services
- Azure Key Vault and secrets (excluding sensitive values)
- Azure Monitor log analytics workspaces and alert rules
- Role assignments and RBAC policies

**Implementation Strategy**:
```
infra/
├── terraform/
│   ├── modules/
│   │   ├── synapse/          # Reusable Synapse module
│   │   ├── data_lake/        # Data Lake Gen2 module
│   │   ├── data_factory/     # ADF module
│   │   └── monitoring/       # Azure Monitor module
│   ├── environments/
│   │   ├── dev/              # Dev environment variables
│   │   ├── prod/             # Prod environment variables
│   ├── main.tf               # Root module
│   ├── variables.tf
│   └── outputs.tf
└── scripts/
    ├── deploy-dev.sh
    └── deploy-prod.sh
```

**CI/CD Integration**:
- Terraform state stored in Azure Storage with state locking
- GitHub Actions workflow: terraform plan on PR, terraform apply on merge to main
- Manual approval required for production deployments
- Drift detection running daily to catch manual changes

**Version Control**:
- All infrastructure definitions in Git
- Semantic versioning for Terraform modules (v1.0.0, v1.1.0)
- Immutable infrastructure: Replace resources vs. in-place updates

**Rationale**: Terraform provides declarative infrastructure definitions with version control, repeatability, and environment parity. Azure-native Bicep considered but rejected due to team's existing Terraform experience. GitHub Actions provides free CI/CD for infrastructure deployments.

---

## Strategic Decision Framework

### Decision D-001: Real-time vs. Batch Data Processing

**Decision Point**: What data processing model should anchor the platform architecture?

**Options Considered**:

1. **Real-time streaming (Event-driven)**:
   - **Pros**: Sub-second latency, supports real-time use cases, modern architecture
   - **Cons**: High complexity (Kafka, Spark Streaming), 3-5x higher cost, requires specialized skills, longer time-to-value (3-6 months)
   - **Cost**: ~$10K/month infrastructure + $50K additional implementation

2. **Micro-batch (5-15 min refresh)**:
   - **Pros**: Near-real-time, balances complexity and freshness
   - **Cons**: Still complex orchestration, unclear business value vs. daily refresh
   - **Cost**: ~$6K/month infrastructure + $30K additional implementation

3. **Daily batch (Scheduled overnight)**:
   - **Pros**: Simple orchestration, cost-effective, matches current business cycle, team skills align
   - **Cons**: No intraday insights, cannot support real-time use cases
   - **Cost**: ~$3K/month infrastructure, baseline implementation cost

**Recommended Strategy**: **Daily batch initially, with architecture that allows future streaming adoption**

**Decision Criteria**:
- **Business requirement**: Current reporting needs operate on daily/weekly cycles (no real-time use cases identified)
- **Team skills**: Team has SQL/Python skills; no Spark streaming experience
- **Cost constraints**: Batch is 3x less expensive than streaming ($3K vs. $10K/month)
- **Time to value**: Batch operational in 4-6 weeks vs. 3-6 months for streaming
- **Risk**: Streaming adds significant complexity and failure modes

**Decision Timing**: Confirm during Phase 1 after validating business requirements with stakeholders. Revisit if real-time personalization or fraud detection use cases emerge in future.

**Reversibility**: **Two-way door decision** - Medallion architecture supports adding streaming sources without redesigning batch pipelines. Can introduce Azure Event Hubs + Stream Analytics for specific real-time use cases while keeping daily batch for core reporting.

---

### Decision D-002: Build vs. Buy for Data Transformation

**Decision Point**: Should we build custom Python transformations or use a transformation framework?

**Options Considered**:

1. **Custom Python scripts**:
   - **Pros**: Maximum flexibility, no licensing cost, team knows Python
   - **Cons**: No built-in testing, lineage, documentation; reinventing wheel; maintenance burden
   - **Cost**: $0 licensing, higher long-term engineering cost

2. **dbt (Data Build Tool)**:
   - **Pros**: SQL-based (team skill match), built-in testing/lineage/docs, open-source, strong community, CI/CD integration
   - **Cons**: $100/month for dbt Cloud (optional), SQL-only (no Python UDFs in free version)
   - **Cost**: $1,200/year for dbt Cloud, lower engineering cost

3. **Azure Synapse Notebooks (PySpark)**:
   - **Pros**: Native Azure integration, supports Python and Scala
   - **Cons**: More complex than SQL, overkill for structured data, higher learning curve
   - **Cost**: Compute costs ~$5K/year

**Recommended Strategy**: **dbt Cloud for Silver and Gold transformations**

**Decision Criteria**:
- **Team skills**: Team strong in SQL, matches dbt's SQL-first approach
- **Software engineering rigor**: dbt provides testing, documentation, version control out-of-box
- **Maintenance**: dbt's modular design reduces technical debt vs. monolithic Python scripts
- **Cost**: $1,200/year dbt Cloud cost easily justified by reduced engineering time
- **Ecosystem**: Large dbt community and pre-built packages (dbt-utils, dbt-expectations)

**Decision Timing**: Implement dbt in Phase 1 for Silver/Gold transformations. Bronze layer remains simple ADF copy activities (no transformation).

**Reversibility**: **One-way door with low switching cost** - dbt models are portable SQL; could migrate to alternative if needed, but unlikely given strong ecosystem fit.

---

### Decision D-003: Azure Synapse Dedicated SQL Pool vs. Serverless SQL Pool

**Decision Point**: Which Synapse SQL engine should host the Gold layer data warehouse?

**Options Considered**:

1. **Dedicated SQL Pool (formerly SQL Data Warehouse)**:
   - **Pros**: Predictable performance, optimized for large queries, columnstore indexes, query result caching
   - **Cons**: Always-on cost even when idle (~$1,500/month minimum for DW100c), requires capacity planning
   - **Cost**: $1,500 - $3,000/month (DW100c - DW500c)

2. **Serverless SQL Pool (on-demand)**:
   - **Pros**: Pay-per-query ($5/TB scanned), no idle cost, automatic scaling
   - **Cons**: Higher cost for frequent queries, slower performance for complex joins, no query result caching
   - **Cost**: Highly variable; estimated $800/month for expected query volume

3. **Hybrid approach**:
   - **Pros**: Best of both worlds - dedicated pool for Gold star schema, serverless for Bronze/Silver ad-hoc queries
   - **Cons**: Slightly more complex to manage
   - **Cost**: $1,500/month + $200/month serverless usage = $1,700/month

**Recommended Strategy**: **Dedicated SQL Pool (DW100c) for Gold layer**

**Decision Criteria**:
- **Query patterns**: 50+ daily dashboard refreshes favor dedicated pool with result caching
- **Performance SLA**: <5 second query performance requires columnstore indexes and compute resources
- **Cost predictability**: Fixed cost easier to budget vs. variable serverless charges
- **Business hours**: 24/7 global operations mean queries occur around the clock (no long idle periods)

**Decision Timing**: Implement dedicated pool in Phase 1. Can scale up to DW200c or DW500c in Phase 2 if query volume increases.

**Reversibility**: **Two-way door with data migration cost** - Can switch between dedicated and serverless, but requires reloading data and updating connection strings. Cost to switch ~1 week engineering time.

---

### Decision D-004: Power BI vs. Tableau for Business Intelligence

**Decision Point**: Which BI tool should provide self-service analytics and dashboards?

**Options Considered**:

1. **Power BI Premium**:
   - **Pros**: Native Azure integration, existing Microsoft 365 SSO, lower cost, familiar to team, mobile apps
   - **Cons**: Less flexible than Tableau for advanced visualizations, weaker geospatial capabilities
   - **Cost**: $5,000/month (P1 capacity for 100 users)

2. **Tableau**:
   - **Pros**: Superior visualization flexibility, excellent geospatial mapping, strong market presence
   - **Cons**: Higher cost, separate authentication system, less Azure-native integration
   - **Cost**: $70/user/month × 100 users = $7,000/month (Creator licenses)

3. **Open-source (Apache Superset, Metabase)**:
   - **Pros**: $0 licensing cost, customizable
   - **Cons**: Self-managed, limited support, lack of enterprise features (RLS, semantic layer), higher engineering burden
   - **Cost**: $0 licensing, ~$30K/year engineering overhead

**Recommended Strategy**: **Power BI Premium**

**Decision Criteria**:
- **Existing ecosystem**: Microsoft 365 and Azure AD already deployed; Power BI leverages SSO
- **Cost**: $5K/month vs. $7K/month for Tableau (29% savings)
- **Team skills**: Finance team already uses Excel; Power BI's Excel-like DAX syntax familiar
- **Azure integration**: Native Synapse connector, automatic refresh, Azure Monitor integration
- **Mobile access**: Power BI mobile apps for executives (critical requirement)

**Decision Timing**: Implement Power BI in Phase 1. Can export data to Tableau later if specific use cases require advanced geospatial (e.g., precision mapping).

**Reversibility**: **Two-way door** - Semantic layer can be accessed by multiple BI tools. Could add Tableau for specific use cases while keeping Power BI as primary tool. Cost to switch ~2 weeks for report migration.

---

### Decision D-005: Data Quality Testing Framework

**Decision Point**: How should we implement automated data quality testing?

**Options Considered**:

1. **Great Expectations (Python framework)**:
   - **Pros**: Comprehensive testing library, rich documentation, profiling capabilities, open-source
   - **Cons**: Python dependency, additional infrastructure (Jupyter notebooks), learning curve
   - **Cost**: $0 (open-source)

2. **dbt Tests (SQL-based)**:
   - **Pros**: Native integration with dbt transformations, SQL-based (team skill match), lightweight, version-controlled
   - **Cons**: Less comprehensive than Great Expectations, limited statistical tests
   - **Cost**: $0 (included with dbt Core/Cloud)

3. **Azure Data Factory Data Quality (preview)**:
   - **Pros**: Native Azure integration, no separate tool
   - **Cons**: Limited functionality, preview status (not production-ready)
   - **Cost**: $0 (included with ADF)

**Recommended Strategy**: **dbt Tests for Silver/Gold layers, basic validation in ADF for Bronze**

**Decision Criteria**:
- **Simplicity**: dbt tests integrated directly into transformation code (single workflow)
- **Team skills**: SQL-based tests match team capabilities
- **Coverage**: dbt tests cover 80% of requirements (not_null, unique, relationships, accepted_values, custom SQL)
- **Deployment**: Tests run automatically in CI/CD pipeline; no separate infrastructure
- **Cost**: $0 incremental cost

**Decision Timing**: Implement dbt tests starting Phase 1. Revisit Great Expectations in Phase 3 if advanced statistical testing (distribution tests, anomaly detection) required.

**Reversibility**: **Two-way door** - Can add Great Expectations alongside dbt tests without replacing them. Complementary tools.

---

## Summary

This Data Platform Strategy provides a comprehensive blueprint for PALO IT e-Commerce's data modernization initiative. The strategy:

✅ **Aligns with business objectives**: Every business requirement has a clear strategic response with success criteria  
✅ **Makes pragmatic technology choices**: Azure-native, managed services, batch-first architecture matching team skills and cost constraints  
✅ **Balances governance and flexibility**: Semantic layer provides consistent metrics while enabling self-service exploration  
✅ **Enables scalability**: Medallion architecture and cloud-native services support 10x growth without redesign  
✅ **Minimizes risk**: Daily batch processing reduces complexity; proven technologies reduce implementation risk  
✅ **Delivers incremental value**: Phased approach delivers business value every 6-8 weeks  

**Next Steps**:
1. Review and validate strategy with business stakeholders (CFO, CMO, CTO)
2. Proceed to detailed architecture design (component specifications, network diagrams)
3. Generate user stories from strategic requirements
4. Establish development environment and begin Phase 1 implementation

**Related Documents**:
- [Value Delivery Roadmap](./value-delivery-roadmap.md) - Implementation phasing and value sequencing
- [Risk & Constraint Register](./risk-constraint-register.md) - Comprehensive risk assessment and mitigation strategies
- [Business Case](./business-case.md) - Original business requirements and objectives
- [Tech Stack](./tech-stack.md) - Technology constraints and preferences
