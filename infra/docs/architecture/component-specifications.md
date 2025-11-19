# Component Specifications

## Overview

This document provides detailed technical specifications for each component of the PALO IT e-Commerce data platform, including configuration parameters, scaling characteristics, dependencies, and cost implications.

---

## Data Ingestion Layer

### Azure Data Factory

**Purpose**: Orchestrate data extraction from APIs, coordinate pipeline execution, and manage data movement between layers.

**Service Tier**: Standard (Pay-as-you-go)

**Configuration Specifications**:
```yaml
resource_name: "palo-ecommerce-adf"
location: "East US"
sku: "Standard"
public_network_enabled: false
managed_virtual_network_enabled: true

identity:
  type: "SystemAssigned"  # Managed Identity for Azure service authentication

git_configuration:
  account_name: "palo-it"
  repository_name: "ecommerce-data-platform"
  collaboration_branch: "main"
  root_folder: "/adf"
  type: "GitHub"

integration_runtime:
  - name: "AutoResolveIntegrationRuntime"
    type: "Managed"
    location: "East US"
    compute_type: "General"
    core_count: 8
    time_to_live_minutes: 10
  
  - name: "VNetIntegrationRuntime"
    type: "Managed"
    virtual_network_enabled: true
    subnet_id: "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/palo-ecommerce-vnet/subnets/integration-subnet"
```

**Linked Services**:

1. **Data Lake Linked Service**
```json
{
  "name": "AzureDataLakeGen2",
  "type": "AzureBlobFS",
  "typeProperties": {
    "url": "https://paloecommercedatalake.dfs.core.windows.net",
    "authenticationType": "SystemAssignedManagedIdentity"
  }
}
```

2. **Synapse Linked Service**
```json
{
  "name": "AzureSynapseAnalytics",
  "type": "AzureSqlDW",
  "typeProperties": {
    "connectionString": "Server=palo-ecommerce-synapse.sql.azuresynapse.net;Database=gold_db;",
    "authenticationType": "SystemAssignedManagedIdentity"
  }
}
```

3. **Key Vault Linked Service**
```json
{
  "name": "AzureKeyVault",
  "type": "AzureKeyVault",
  "typeProperties": {
    "baseUrl": "https://palo-ecommerce-kv.vault.azure.net/",
    "authenticationType": "SystemAssignedManagedIdentity"
  }
}
```

**Pipeline Specifications**:

**Master Pipeline: `daily_data_refresh`**
```yaml
trigger:
  type: "Schedule"
  schedule:
    frequency: "Day"
    interval: 1
    start_time: "2024-01-01T02:00:00Z"
    time_zone: "Eastern Standard Time"

activities:
  - name: "Extract_API_Data"
    type: "ForEach"
    items: ["products", "users", "countries", "exchange_rates"]
    is_sequential: false
    batch_count: 4
    activities:
      - name: "HTTP_Extract"
        type: "Copy"
        policy:
          timeout: "0:05:00"
          retry: 3
          retry_interval_in_seconds: 30
  
  - name: "Synthesize_Transactions"
    type: "ExecutePipeline"
    depends_on: ["Extract_API_Data"]
    
  - name: "Run_dbt_Bronze_to_Silver"
    type: "CustomActivity"
    depends_on: ["Synthesize_Transactions"]
    command: "dbt run --models tag:silver"
    
  - name: "Run_dbt_Silver_to_Gold"
    type: "CustomActivity"
    depends_on: ["Run_dbt_Bronze_to_Silver"]
    command: "dbt run --models tag:gold"
    
  - name: "Run_dbt_Tests"
    type: "CustomActivity"
    depends_on: ["Run_dbt_Silver_to_Gold"]
    command: "dbt test"
    
  - name: "Refresh_PowerBI"
    type: "WebActivity"
    depends_on: ["Run_dbt_Tests"]
    method: "POST"
    url: "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
```

**Scalability Considerations**:
- **Parallel Execution**: Up to 4 concurrent API extractions
- **Integration Runtime**: Auto-scale from 8 to 32 cores based on workload
- **Data Movement Units (DMU)**: Start with 4 DMUs, increase to 32 for large file copies

**Cost Estimation**:
- **Pipeline orchestration**: $1 per 1,000 activity runs = ~$30/month (1,000 activities)
- **Data movement**: $0.25 per DMU-hour = ~$120/month (480 DMU-hours)
- **Integration runtime**: $0.25 per vCore-hour = ~$350/month (1,400 vCore-hours)
- **Total**: ~$500/month

**Dependencies**:
- Azure Data Lake Gen2 (write access to Bronze layer)
- Azure Key Vault (read access to secrets)
- External APIs (Fake Store API, Exchange Rates API, REST Countries API)
- dbt Cloud or dbt Core (for transformation execution)

**Monitoring & Alerts**:
```yaml
alerts:
  - name: "Pipeline Failure"
    condition: "Pipeline status == Failed"
    severity: "High"
    action: "Email data-engineering-team@palo-it.com"
  
  - name: "Long Running Pipeline"
    condition: "Pipeline duration > 2 hours"
    severity: "Medium"
    action: "Email data-platform-lead@palo-it.com"
  
  - name: "Data Quality Test Failure"
    condition: "dbt test status == Failed"
    severity: "High"
    action: "Email + Slack #data-quality-alerts"
```

**Risk Mitigation** (addresses R-001, R-004, R-018):
- Retry logic with exponential backoff for API failures
- Schema validation before writing to Bronze layer
- Network connectivity tests during pipeline initialization
- Quarantine table for failed records (manual review)

---

## Storage Layer

### Azure Data Lake Gen2

**Purpose**: Scalable, cost-optimized storage for Bronze and Silver layers with hierarchical namespace support.

**Service Tier**: 
- Bronze: Cool tier (rare access)
- Silver: Hot tier (frequent access)

**Configuration Specifications**:
```yaml
resource_name: "paloecommercedatalake"
location: "East US"
account_kind: "StorageV2"
account_tier: "Standard"
replication_type: "LRS"  # Locally Redundant Storage
hierarchical_namespace_enabled: true
public_network_access: "Disabled"
min_tls_version: "TLS1_2"
allow_blob_public_access: false

blob_properties:
  versioning_enabled: true
  change_feed_enabled: true
  delete_retention_policy:
    enabled: true
    days: 30
  container_delete_retention_policy:
    enabled: true
    days: 30

containers:
  - name: "bronze"
    access_tier: "Cool"
    public_access: "None"
  
  - name: "silver"
    access_tier: "Hot"
    public_access: "None"

lifecycle_management_policies:
  - name: "ArchiveBronze"
    filters:
      blob_types: ["blockBlob"]
      prefix_match: ["bronze/"]
    actions:
      base_blob:
        tier_to_cool:
          days_after_modification_greater_than: 90
        tier_to_archive:
          days_after_modification_greater_than: 365
  
  - name: "CoolSilver"
    filters:
      blob_types: ["blockBlob"]
      prefix_match: ["silver/"]
    actions:
      base_blob:
        tier_to_cool:
          days_after_modification_greater_than: 90
        delete:
          days_after_modification_greater_than: 365
```

**Storage Hierarchy**:
```
paloecommercedatalake/
├── bronze/
│   ├── products_raw/
│   │   └── ingestion_date=YYYY-MM-DD/
│   ├── users_raw/
│   │   └── ingestion_date=YYYY-MM-DD/
│   ├── exchange_rates_raw/
│   │   └── effective_date=YYYY-MM-DD/
│   ├── countries_raw/
│   └── transactions_raw/
│       └── order_date=YYYY-MM-DD/
└── silver/
    ├── products_clean/
    │   └── business_date=YYYY-MM-DD/
    ├── customers_clean/
    │   └── business_date=YYYY-MM-DD/
    ├── exchange_rates_clean/
    │   └── effective_date=YYYY-MM-DD/
    ├── locations_clean/
    └── orders_clean/
        └── order_date=YYYY-MM-DD/
```

**Access Control (ACLs)**:
```yaml
acl_configuration:
  - path: "/bronze"
    permissions:
      - principal: "data-factory-managed-identity"
        access: "rwx"  # Read, write, execute
      - principal: "data-engineers"
        access: "rwx"
      - principal: "bi-developers"
        access: "---"  # No access
  
  - path: "/silver"
    permissions:
      - principal: "data-factory-managed-identity"
        access: "rwx"
      - principal: "data-engineers"
        access: "rwx"
      - principal: "bi-developers"
        access: "r-x"  # Read and execute only
```

**Performance Characteristics**:
- **Throughput**: Up to 60 Gbps egress, 40 Gbps ingress
- **IOPS**: Up to 20,000 read IOPS, 20,000 write IOPS
- **Latency**: <10ms for Hot tier, <100ms for Cool tier
- **Scalability**: Exabyte-scale storage capacity

**Cost Estimation**:
- **Storage (Hot tier - Silver)**: $0.018/GB/month × 100 GB = $1.80/month
- **Storage (Cool tier - Bronze)**: $0.010/GB/month × 400 GB = $4.00/month
- **Transactions (read)**: $0.0004 per 10,000 = ~$5/month
- **Data egress**: $0.087/GB × 50 GB = ~$4.35/month
- **Total**: ~$15/month (scales with data volume)

**Scalability Roadmap**:
- Year 1: 500 GB total
- Year 2: 2 TB (4x growth)
- Year 3: 8 TB (4x growth)
- Year 5: 50 TB (6x growth)

**Dependencies**:
- Azure Virtual Network (private endpoints)
- Azure Key Vault (optional: customer-managed encryption keys)
- Azure Data Factory (read/write access)

**Risk Mitigation** (addresses R-028, R-031):
- Lifecycle policies automate tier transitions (cost optimization)
- Soft delete enabled (30-day recovery window for accidental deletions)
- Versioning enabled (recover from accidental overwrites)
- Cost alerts configured at $50/month threshold

---

## Processing Layer

### Azure Synapse Analytics (Dedicated SQL Pool)

**Purpose**: High-performance data warehouse hosting Gold layer dimensional model with columnar storage and query optimization.

**Service Tier**: Dedicated SQL Pool (formerly SQL Data Warehouse)

**Configuration Specifications**:
```yaml
workspace_name: "palo-ecommerce-synapse"
location: "East US"
managed_virtual_network: true
public_network_access: "Disabled"

sql_pool:
  name: "gold_pool"
  sku:
    name: "DW100c"
    capacity: 100  # Data Warehouse Units (DWU)
  collation: "SQL_Latin1_General_CP1_CI_AS"
  max_size_bytes: 263882790666240  # 240 TB max
  create_mode: "Default"
  
  auto_pause:
    enabled: true
    delay_in_minutes: 60  # Pause after 1 hour of inactivity
  
  auto_scale:
    enabled: false  # Manual scaling for cost control
    min_capacity: 100
    max_capacity: 500

firewall_rules:
  - name: "AllowPowerBI"
    start_ip_address: "0.0.0.0"
    end_ip_address: "0.0.0.0"  # Power BI service tag
  
  - name: "AllowDataFactory"
    start_ip_address: "0.0.0.0"
    end_ip_address: "0.0.0.0"  # Azure services

private_endpoints:
  - name: "synapse-sql-pe"
    subnet_id: "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/palo-ecommerce-vnet/subnets/data-subnet"
    private_dns_zone_id: "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/privateDnsZones/privatelink.sql.azuresynapse.net"

transparent_data_encryption:
  status: "Enabled"
  encryption_protector: "ServiceManaged"  # Or CustomerManaged for CMK

azure_ad_authentication:
  enabled: true
  admin_login: "data-platform-admins"
  admin_object_id: "{AAD_group_object_id}"
```

**Database Schema**:
```sql
-- Gold database
CREATE DATABASE gold_db;
GO

USE gold_db;
GO

-- Schema organization
CREATE SCHEMA gold AUTHORIZATION dbo;
GO

-- Resource class for data loading
CREATE WORKLOAD GROUP DataLoadWorkload
WITH (
  MIN_PERCENTAGE_RESOURCE = 40,
  CAP_PERCENTAGE_RESOURCE = 80,
  REQUEST_MIN_RESOURCE_GRANT_PERCENT = 10
);
GO

-- Workload classifier for dbt service principal
CREATE WORKLOAD CLASSIFIER DataLoadClassifier
WITH (
  WORKLOAD_GROUP = 'DataLoadWorkload',
  MEMBERNAME = 'dbt-service-principal',
  IMPORTANCE = HIGH
);
GO
```

**Performance Optimization**:

**Columnstore Indexes**:
```sql
-- Fact table with clustered columnstore
CREATE TABLE gold.fact_sales (
    sales_key BIGINT IDENTITY(1,1) NOT NULL,
    -- ... columns ...
) WITH (
    CLUSTERED COLUMNSTORE INDEX,
    DISTRIBUTION = HASH(customer_key),  -- Distribute by frequently joined key
    PARTITION (order_date_key RANGE RIGHT FOR VALUES (
        20240101, 20240201, 20240301, 20240401, 20240501, 20240601,
        20240701, 20240801, 20240901, 20241001, 20241101, 20241201
    ))
);
```

**Distribution Strategy**:
- **Fact tables**: HASH distribution on frequently joined dimension key (customer_key)
- **Large dimensions**: REPLICATE distribution (dim_date, dim_product_category)
- **Small dimensions**: ROUND_ROBIN (default)

**Partitioning Strategy**:
- **fact_sales**: Monthly partitions on order_date_key (12 partitions per year)
- **Partition switching**: Enables fast historical data archival

**Statistics Maintenance**:
```sql
-- Auto-create statistics (enabled by default)
ALTER DATABASE gold_db SET AUTO_CREATE_STATISTICS ON;
ALTER DATABASE gold_db SET AUTO_UPDATE_STATISTICS ON;

-- Manual statistics for critical columns
CREATE STATISTICS stat_customer_key ON gold.fact_sales (customer_key) WITH FULLSCAN;
CREATE STATISTICS stat_product_key ON gold.fact_sales (product_key) WITH FULLSCAN;
CREATE STATISTICS stat_order_date_key ON gold.fact_sales (order_date_key) WITH FULLSCAN;
```

**Scalability Considerations**:
- **Current**: DW100c (1,000 DWU) = $1,500/month
- **Growth Path**: Scale to DW500c (5,000 DWU) = $7,500/month as query concurrency increases
- **Scaling Operation**: 5-10 minutes downtime, scripted via Azure CLI

**Cost Estimation**:
```yaml
compute_cost:
  sku: "DW100c"
  hourly_rate: 2.04  # USD per hour (East US)
  monthly_runtime: 720 hours  # 24/7 operation
  auto_pause_savings: 40%  # Pause during nights/weekends
  effective_monthly_cost: 1500 * 0.6 = $900/month

storage_cost:
  data_size_gb: 50  # Gold layer only
  rate_per_gb: 0.10  # USD per GB per month
  monthly_cost: $5/month

backup_cost:
  snapshot_storage: 50 GB * 0.02 = $1/month
  retention: 30 days

total_monthly_cost: ~$906/month
```

**Dependencies**:
- Azure Data Lake Gen2 (PolyBase external tables for Bronze/Silver access)
- Azure Key Vault (connection string storage)
- Azure Virtual Network (private endpoints)
- dbt (transformation execution)

**Monitoring & Alerts**:
```yaml
metrics:
  - name: "DWU Percentage"
    threshold: 80%
    action: "Alert data engineer to consider scaling"
  
  - name: "Failed Queries"
    threshold: 5% failure rate
    action: "Email + Slack alert"
  
  - name: "Long Running Queries"
    threshold: 300 seconds
    action: "Log for performance tuning"
  
  - name: "Storage Used"
    threshold: 200 GB (80% of initial 240 GB allocation)
    action: "Alert platform admin"
```

**Risk Mitigation** (addresses R-028, R-029, R-030, R-032):
- Auto-pause reduces costs during off-hours (40% savings)
- Partitioning enables efficient query pruning (10x performance improvement)
- Columnstore indexes optimized for analytical queries (<5 second response)
- Cost alerts prevent budget overruns

---

### dbt (Data Build Tool)

**Purpose**: Software engineering framework for SQL transformations with testing, documentation, and version control.

**Deployment Option**: dbt Cloud (managed service)

**Configuration Specifications**:
```yaml
dbt_cloud_account:
  account_name: "palo-it-ecommerce"
  plan: "Team"  # $100/developer/month
  users: 5  # Data engineers

project:
  name: "ecommerce-data-platform"
  dbt_version: "1.7.0"
  
  connection:
    type: "synapse"
    host: "palo-ecommerce-synapse.sql.azuresynapse.net"
    database: "gold_db"
    schema: "gold"
    authentication: "ServicePrincipal"
    client_id: "{{env_var('DBT_SP_CLIENT_ID')}}"
    client_secret: "{{env_var('DBT_SP_CLIENT_SECRET')}}"
    tenant_id: "{{env_var('DBT_TENANT_ID')}}"

  target_configs:
    dev:
      schema: "gold_dev"
      threads: 4
    
    prod:
      schema: "gold"
      threads: 8
```

**Project Structure**:
```
dbt_project/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── bronze/  # Source definitions
│   │   ├── _sources.yml
│   │   └── schema.yml
│   ├── silver/  # Cleansing transformations
│   │   ├── products_clean.sql
│   │   ├── customers_clean.sql
│   │   ├── exchange_rates_clean.sql
│   │   ├── locations_clean.sql
│   │   ├── orders_clean.sql
│   │   └── schema.yml
│   └── gold/  # Dimensional model
│       ├── dim_product.sql
│       ├── dim_customer.sql
│       ├── dim_location.sql
│       ├── dim_date.sql
│       ├── dim_product_category.sql
│       ├── fact_sales.sql
│       └── schema.yml
├── tests/
│   ├── generic/  # Reusable test templates
│   └── singular/  # Custom SQL tests
├── macros/  # Reusable SQL functions
│   ├── currency_conversion.sql
│   └── scd_type2_merge.sql
├── seeds/  # Static reference data
│   └── product_categories.csv
└── docs/
    └── overview.md
```

**Model Example (dim_product with SCD Type 2)**:
```sql
-- models/gold/dim_product.sql
{{ config(
    materialized='incremental',
    unique_key='product_key',
    on_schema_change='fail',
    tags=['gold', 'dimension']
) }}

WITH source_data AS (
    SELECT
        product_id,
        product_name,
        category,
        description,
        base_price,
        rating,
        rating_count,
        business_date AS valid_from
    FROM {{ ref('products_clean') }}
    {% if is_incremental() %}
    WHERE business_date > (SELECT MAX(valid_from) FROM {{ this }})
    {% endif %}
),

current_records AS (
    SELECT *
    FROM {{ this }}
    WHERE is_current = TRUE
),

detect_changes AS (
    SELECT
        s.*,
        c.product_key,
        CASE
            WHEN c.product_key IS NULL THEN 'INSERT'
            WHEN s.base_price != c.base_price THEN 'UPDATE'
            ELSE 'NO_CHANGE'
        END AS change_type
    FROM source_data s
    LEFT JOIN current_records c ON s.product_id = c.product_id
),

-- Expire old records
expired_records AS (
    SELECT
        product_key,
        product_id,
        product_name,
        category,
        description,
        base_price,
        rating,
        rating_count,
        valid_from,
        DATEADD(day, -1, CURRENT_DATE) AS valid_to,
        FALSE AS is_current
    FROM current_records
    WHERE product_id IN (
        SELECT product_id FROM detect_changes WHERE change_type = 'UPDATE'
    )
),

-- Insert new/updated records
new_records AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY product_id) + 
            (SELECT COALESCE(MAX(product_key), 0) FROM {{ this }}) AS product_key,
        product_id,
        product_name,
        category,
        description,
        base_price,
        rating,
        rating_count,
        valid_from,
        CAST('9999-12-31' AS DATE) AS valid_to,
        TRUE AS is_current
    FROM detect_changes
    WHERE change_type IN ('INSERT', 'UPDATE')
)

SELECT * FROM expired_records
UNION ALL
SELECT * FROM new_records
```

**Testing Framework**:
```yaml
# models/gold/schema.yml
version: 2

models:
  - name: fact_sales
    description: "Sales fact table at order line grain"
    
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [order_id, order_line_number]
      - dbt_utils.recency:
          datepart: day
          field: created_at
          interval: 1
    
    columns:
      - name: sales_key
        description: "Surrogate key for fact table"
        tests:
          - unique
          - not_null
      
      - name: product_key
        description: "Foreign key to dim_product"
        tests:
          - not_null
          - relationships:
              to: ref('dim_product')
              field: product_key
      
      - name: total_amount_usd
        description: "Total order line amount in USD"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0.01
              max_value: 100000.00
```

**Execution Schedule** (via dbt Cloud):
```yaml
job:
  name: "Daily Prod Refresh"
  schedule:
    cron: "0 2 * * *"  # 2:00 AM daily
    timezone: "America/New_York"
  
  commands:
    - "dbt deps"  # Install packages
    - "dbt seed"  # Load static reference data
    - "dbt run --models tag:silver"  # Bronze → Silver
    - "dbt run --models tag:gold"    # Silver → Gold
    - "dbt test"  # Run all tests
    - "dbt docs generate"  # Update documentation
  
  notifications:
    on_failure:
      - email: "data-engineering-team@palo-it.com"
      - slack: "#data-quality-alerts"
```

**Cost Estimation**:
- **dbt Cloud Team Plan**: $100/developer/month × 5 developers = $500/month
- **Alternative (dbt Core)**: Free (self-hosted on Azure VM or Container Instances)
  - Azure VM: Standard_D2s_v3 (2 vCPUs, 8 GB RAM) = $70/month
  - Container Instances: ~$30/month for scheduled runs

**Dependencies**:
- Azure Synapse Analytics (transformation execution)
- Azure Data Lake Gen2 (source data in Silver layer)
- GitHub (version control for dbt project)
- Azure Key Vault (service principal credentials)

**Risk Mitigation** (addresses R-008, R-011):
- 2-day dbt training for data engineering team
- Naming conventions enforce consistent model structure
- Code review required for all dbt model PRs
- DAG visualization identifies circular dependencies

---

## Consumption Layer

### Power BI Premium

**Purpose**: Self-service analytics platform with governed semantic layer, interactive dashboards, and row-level security.

**Service Tier**: Power BI Premium P1 capacity

**Configuration Specifications**:
```yaml
capacity:
  name: "PALO_IT_ECOMMERCE"
  sku: "P1"
  v_cores: 8
  memory_gb: 25
  max_memory_per_dataset_gb: 25
  backend_v_cores: 8

workspace:
  - name: "E-Commerce Analytics - Production"
    capacity: "PALO_IT_ECOMMERCE"
    access:
      admins: ["data-platform-admins", "bi-developers"]
      viewers: ["business-executives", "business-finance", "business-marketing", "business-sales"]
  
  - name: "E-Commerce Analytics - Development"
    capacity: "PALO_IT_ECOMMERCE"
    access:
      admins: ["data-platform-admins"]
      members: ["bi-developers", "data-engineers"]

semantic_model:
  name: "Ecommerce_Data_Model"
  source:
    type: "DirectQuery"  # Or Import for smaller datasets
    connection:
      server: "palo-ecommerce-synapse.sql.azuresynapse.net"
      database: "gold_db"
      authentication: "ServicePrincipal"
  
  refresh_schedule:
    type: "Automatic"
    frequency: "Daily"
    time: "04:00"  # After pipeline completion
    timezone: "Eastern Standard Time"
    notify_on_failure: true
  
  incremental_refresh:
    enabled: true
    archive_partition: 3 years
    refresh_partition: 13 months  # Current month + 12 months history
    detect_data_changes: true

row_level_security:
  roles:
    - name: "Executive"
      filter: "[Segment] IN (\"new\", \"regular\", \"vip\")"
      members: ["business-executives"]
    
    - name: "RegionalManager"
      filter: "[Region] = USERPRINCIPALNAME()"
      members: ["business-regional-managers"]
    
    - name: "SalesRep"
      filter: "[SalesRepEmail] = USERPRINCIPALNAME()"
      members: ["business-sales"]
```

**Semantic Layer Measures (DAX)**:
```dax
// Key Performance Indicators

Total Revenue = 
SUMX(
    fact_sales,
    fact_sales[total_amount_usd]
)

Total Orders = 
DISTINCTCOUNT(fact_sales[order_id])

Average Order Value = 
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)

Customer Lifetime Value = 
CALCULATE(
    [Total Revenue],
    ALL(dim_date)  -- Ignore date filter for LTV
)

Revenue Growth % = 
VAR CurrentPeriodRevenue = [Total Revenue]
VAR PreviousPeriodRevenue = 
    CALCULATE(
        [Total Revenue],
        DATEADD(dim_date[full_date], -1, YEAR)
    )
RETURN
DIVIDE(
    CurrentPeriodRevenue - PreviousPeriodRevenue,
    PreviousPeriodRevenue,
    0
)

Customer Retention Rate = 
VAR CustomersLastMonth = 
    CALCULATE(
        DISTINCTCOUNT(fact_sales[customer_key]),
        DATEADD(dim_date[full_date], -1, MONTH)
    )
VAR ReturnCustomers = 
    CALCULATE(
        DISTINCTCOUNT(fact_sales[customer_key]),
        FILTER(
            fact_sales,
            fact_sales[customer_key] IN CustomersLastMonth
        )
    )
RETURN
DIVIDE(ReturnCustomers, CustomersLastMonth, 0)
```

**Dashboard Specifications**:

| Dashboard | Purpose | Key Metrics | Audience | Refresh Frequency |
|-----------|---------|-------------|----------|-------------------|
| **Executive Overview** | High-level business health | Total Revenue, Orders, Customers, YoY Growth | C-level, VPs | Daily (4 AM) |
| **Sales Performance** | Sales trends and targets | Revenue by Region, Top Products, Sales Rep Performance | Sales Team | Daily (4 AM) |
| **Product Analytics** | Product portfolio insights | Product Revenue, Category Mix, Rating Trends | Product Team | Daily (4 AM) |
| **Customer Insights** | Customer behavior analysis | Customer Segments, LTV, Retention Rate | Marketing Team | Daily (4 AM) |
| **Geographic Performance** | Multi-region analysis | Revenue by Country, Currency Impact, Regional Growth | Finance, Sales | Daily (4 AM) |
| **Financial Reporting** | Compliance-ready financials | Revenue by Currency, Exchange Rate Variance, Monthly Close | Finance Team | Daily (4 AM) |
| **Operational Metrics** | Pipeline health monitoring | Data Freshness, Pipeline Success Rate, Query Performance | Data Engineering | Hourly |

**Performance Optimization**:
- **Aggregations**: Pre-aggregate fact_sales at month/category grain for fast executive dashboards
- **Incremental Refresh**: Load only current month + 12 months (reduces refresh time from 40 min to 10 min)
- **DirectQuery**: Use for large datasets; Import mode for dimension tables
- **Composite Models**: Combine Import (dimensions) + DirectQuery (facts) for best performance

**Cost Estimation**:
```yaml
power_bi_premium:
  sku: "P1"
  v_cores: 8
  monthly_cost: $4,995/month
  
  capacity_planning:
    current_users: 100
    datasets: 7 (one per dashboard)
    refresh_per_day: 1
    query_concurrency: 20
    headroom: 40%  # Avoid capacity throttling

alternative_pro_licensing:
  pro_licenses: 100 users × $10/user = $1,000/month
  note: "Premium more cost-effective above 50 users"
```

**Dependencies**:
- Azure Synapse Analytics (data source)
- Azure Key Vault (service principal credentials)
- Microsoft Entra ID (user authentication, RLS)
- Azure Monitor (refresh failure alerting)

**Risk Mitigation** (addresses R-010, R-021, R-029, R-034):
- Semantic layer design started in Week 4 (parallel with Gold layer development)
- Phased user rollout (5 → 15 → 50 → 100 users) validates adoption before full Premium commitment
- Incremental refresh reduces dashboard load times to <5 seconds
- Refresh failure alerts via Azure Monitor (email + Slack)

---

## Governance & Operations

### Azure Key Vault

**Purpose**: Centralized secrets management for API keys, connection strings, and service principal credentials.

**Service Tier**: Standard (no Premium HSM required for current use case)

**Configuration Specifications**:
```yaml
resource_name: "palo-ecommerce-kv"
location: "East US"
sku_name: "standard"
enabled_for_deployment: false
enabled_for_disk_encryption: false
enabled_for_template_deployment: true
enable_soft_delete: true
soft_delete_retention_days: 90
enable_purge_protection: true
public_network_access: "Disabled"

network_acls:
  bypass: "AzureServices"
  default_action: "Deny"
  ip_rules: []  # No public IP access
  virtual_network_subnet_ids:
    - "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/palo-ecommerce-vnet/subnets/data-subnet"

access_policies:
  - tenant_id: "{tenant_id}"
    object_id: "{data-factory-managed-identity}"
    secret_permissions: ["Get", "List"]
  
  - tenant_id: "{tenant_id}"
    object_id: "{powerbi-service-principal}"
    secret_permissions: ["Get"]
  
  - tenant_id: "{tenant_id}"
    object_id: "{data-platform-admins-group}"
    secret_permissions: ["Get", "List", "Set", "Delete", "Backup", "Restore", "Recover", "Purge"]
    key_permissions: ["Get", "List", "Create", "Delete", "Update", "Import", "Backup", "Restore", "Recover", "Purge"]
    certificate_permissions: ["Get", "List", "Create", "Delete", "Update", "Import", "Backup", "Restore", "Recover", "Purge", "ManageContacts", "ManageIssuers", "GetIssuers", "ListIssuers", "SetIssuers", "DeleteIssuers"]
```

**Secrets Stored**:
```yaml
secrets:
  - name: "exchangeratesapi-key"
    value: "{api_key}"
    content_type: "text/plain"
    expires_on: "2025-12-31"
    tags:
      purpose: "Exchange Rates API authentication"
      rotation: "annual"
  
  - name: "synapse-admin-password"
    value: "{strong_password}"
    content_type: "text/plain"
    expires_on: "2025-03-31"
    tags:
      purpose: "Synapse SQL admin login"
      rotation: "quarterly"
  
  - name: "powerbi-sp-secret"
    value: "{client_secret}"
    content_type: "text/plain"
    expires_on: "2025-01-14"
    tags:
      purpose: "Power BI service principal authentication"
      rotation: "quarterly"
  
  - name: "dbt-sp-secret"
    value: "{client_secret}"
    content_type: "text/plain"
    expires_on: "2025-04-14"
    tags:
      purpose: "dbt service principal authentication"
      rotation: "semi-annual"
```

**Secret Rotation Automation**:
```yaml
# Azure Function for automated secret rotation
function_app:
  name: "SecretRotationFunction"
  trigger: "TimerTrigger"
  schedule: "0 0 1 * *"  # Monthly check
  
  logic:
    - Check secret expiration dates
    - If expires within 30 days:
        - Notify platform admin via email
        - Log rotation reminder to Azure Monitor
    - If expires within 7 days:
        - Escalate alert (email + Slack)
        - Create incident ticket
```

**Cost Estimation**:
- **Key Vault operations**: $0.03 per 10,000 transactions = ~$3/month
- **Secret storage**: $0/month (first 10,000 secrets free)
- **Total**: ~$3/month

**Dependencies**:
- Azure Virtual Network (private endpoint)
- Microsoft Entra ID (access policies)
- Azure Monitor (secret access logging)

**Risk Mitigation** (addresses R-023):
- Git pre-commit hooks detect secrets in code (prevent accidental exposure)
- Soft delete + purge protection prevent accidental secret deletion
- Access logging tracks which service principals accessed which secrets
- Expiration dates enforce regular rotation

---

### Azure Monitor

**Purpose**: Centralized logging, monitoring, and alerting for all data platform components.

**Service Tier**: Pay-as-you-go (Log Analytics workspace)

**Configuration Specifications**:
```yaml
log_analytics_workspace:
  name: "palo-ecommerce-logs"
  location: "East US"
  sku: "PerGB2018"
  retention_in_days: 90
  daily_quota_gb: 10
  internet_ingestion_enabled: false
  internet_query_enabled: false

diagnostic_settings:
  - resource: "Azure Data Factory"
    logs:
      - category: "PipelineRuns"
        enabled: true
        retention_days: 90
      - category: "ActivityRuns"
        enabled: true
        retention_days: 90
      - category: "TriggerRuns"
        enabled: true
        retention_days: 90
    metrics:
      - category: "AllMetrics"
        enabled: true
        retention_days: 90
  
  - resource: "Azure Synapse Analytics"
    logs:
      - category: "SQLSecurityAuditEvents"
        enabled: true
        retention_days: 730  # 2 years for compliance
      - category: "DmsWorkers"
        enabled: true
        retention_days: 90
      - category: "ExecRequests"
        enabled: true
        retention_days: 90
    metrics:
      - category: "AllMetrics"
        enabled: true
        retention_days: 90
  
  - resource: "Azure Data Lake Gen2"
    logs:
      - category: "StorageRead"
        enabled: true
        retention_days: 90
      - category: "StorageWrite"
        enabled: true
        retention_days: 90
    metrics:
      - category: "Transaction"
        enabled: true
        retention_days: 90
  
  - resource: "Azure Key Vault"
    logs:
      - category: "AuditEvent"
        enabled: true
        retention_days: 730  # 2 years for compliance
    metrics:
      - category: "AllMetrics"
        enabled: true
        retention_days: 90
```

**Alert Rules**:
```yaml
alerts:
  - name: "Pipeline Failure - Critical"
    resource: "Azure Data Factory"
    condition: "PipelineRuns | where Status == 'Failed'"
    severity: "Critical"
    frequency: "5 minutes"
    action_group: "data-engineering-team"
    notification:
      - email: "data-engineering-team@palo-it.com"
      - sms: "+1-555-0100"
      - slack: "#data-pipeline-alerts"
  
  - name: "Data Quality Test Failure"
    resource: "Azure Data Factory"
    condition: "ActivityRuns | where ActivityName contains 'dbt_test' and Status == 'Failed'"
    severity: "High"
    frequency: "5 minutes"
    action_group: "data-quality-team"
  
  - name: "High Query Failure Rate"
    resource: "Azure Synapse Analytics"
    condition: "ExecRequests | summarize FailureRate = countif(Status == 'Failed') / count() | where FailureRate > 0.05"
    severity: "Medium"
    frequency: "15 minutes"
    action_group: "data-engineering-team"
  
  - name: "Cost Budget Alert"
    resource: "Subscription"
    condition: "Cost exceeds 80% of monthly budget ($10,000)"
    severity: "High"
    frequency: "Daily"
    action_group: "finance-team"
  
  - name: "Storage Capacity Warning"
    resource: "Azure Data Lake Gen2"
    condition: "Storage used > 400 GB (80% of expected 500 GB)"
    severity: "Medium"
    frequency: "Daily"
    action_group: "platform-admins"
```

**Dashboard (Azure Workbook)**:
```yaml
workbook_name: "Data Platform Health Dashboard"

sections:
  - title: "Pipeline Execution"
    visualizations:
      - type: "Time Chart"
        query: "PipelineRuns | summarize count() by bin(TimeGenerated, 1h), Status"
      - type: "Grid"
        query: "PipelineRuns | where Status == 'Failed' | project TimeGenerated, PipelineName, ErrorMessage | order by TimeGenerated desc"
  
  - title: "Data Quality"
    visualizations:
      - type: "Metric"
        query: "ActivityRuns | where ActivityName contains 'dbt_test' | summarize SuccessRate = countif(Status == 'Succeeded') * 100.0 / count()"
      - type: "Grid"
        query: "ActivityRuns | where ActivityName contains 'dbt_test' and Status == 'Failed' | project TimeGenerated, ActivityName, ErrorMessage | order by TimeGenerated desc"
  
  - title: "Query Performance"
    visualizations:
      - type: "Time Chart"
        query: "ExecRequests | summarize avg(TotalElapsedTime) by bin(TimeGenerated, 1h)"
      - type: "Grid"
        query: "ExecRequests | where TotalElapsedTime > 30000 | project TimeGenerated, Command, TotalElapsedTime, RowCount | order by TotalElapsedTime desc"
  
  - title: "Cost Tracking"
    visualizations:
      - type: "Metric"
        query: "AzureCosts | summarize sum(Cost) by ServiceName"
      - type: "Time Chart"
        query: "AzureCosts | summarize sum(Cost) by bin(Date, 1d)"
```

**Cost Estimation**:
- **Log ingestion**: $2.76/GB × 5 GB/day × 30 days = $414/month
- **Log retention (90 days)**: Included in ingestion cost
- **Extended retention (2 years for compliance)**: $0.12/GB × 100 GB = $12/month
- **Alert evaluations**: $0.10 per alert × 10 alerts × 30 days = $30/month
- **Total**: ~$456/month

**Dependencies**:
- All Azure resources (diagnostic logs sent to Log Analytics)
- Action Groups (email, SMS, Slack notifications)
- Azure Workbooks (dashboard visualization)

**Risk Mitigation** (addresses R-014, R-027):
- Proactive alerting detects issues before business impact
- 2-year audit log retention meets SOX compliance requirements
- Cost tracking prevents budget overruns (R-032)
- Performance metrics identify optimization opportunities (R-029, R-030)

---

## Related Documents

- [Architecture Overview](../../docs/architecture/overview.md)
- [Data Flows](../../docs/architecture/data-flows.md)
- [Security & Governance](../../docs/architecture/security-governance.md)
- [Network Security](./network-security.md)
- [Operations Guide](./operations.md)
