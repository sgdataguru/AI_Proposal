# Data Sources Summary

## Overview
This document summarizes the public API data sources that will be used to build the PALO IT e-Commerce data platform demonstration.

## Selected APIs

### 1. Fake Store API
**Purpose**: Primary e-commerce data (products, customers, orders)  
**URL**: https://fakestoreapi.com/  
**Cost**: Free, no API key required  

**Endpoints Used**:
- `GET /products` - 20 products across 4 categories
- `GET /products/categories` - 4 categories (electronics, jewelery, men's clothing, women's clothing)
- `GET /users` - ~10 user profiles with address and contact info
- `GET /carts` - Shopping cart/order data with product-user associations

**Why This Works**:
- Provides realistic e-commerce product catalog
- Includes customer demographic data
- Contains transaction/order data for fact table
- Product ratings provide additional analytical dimension

---

### 2. Exchange Rates API
**Purpose**: Currency conversion and multi-currency analytics  
**URL**: https://exchangeratesapi.io/ or https://api.exchangerate-api.com/  
**Cost**: Free tier available  

**Endpoints Used**:
- `GET /latest` - Current exchange rates
- `GET /v4/history/{date}` - Historical rates for specific dates

**Currencies to Track**:
USD (base), EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN, BRL, ZAR, SGD, SEK, NOK

**Why This Works**:
- Enables multi-currency revenue reporting (key requirement)
- Historical data allows proper temporal alignment with transactions
- Free tier sufficient for demo purposes
- Real-world exchange rate fluctuations add authenticity

---

### 3. REST Countries API
**Purpose**: Geographic reference data and country demographics  
**URL**: https://restcountries.com/  
**Cost**: Free, no API key required  

**Endpoints Used**:
- `GET /v3.1/all` - All countries with full details
- `GET /v3.1/alpha/{code}` - Individual country by code

**Data Retrieved**:
- Country names, codes (ISO 2/3)
- Regions and sub-regions
- Population, capital, area
- Currencies per country
- Timezones
- Languages

**Why This Works**:
- Provides dimension table for geographic analysis (critical requirement)
- Enables country/region hierarchy for drill-down
- Population data allows per-capita analysis
- Currency mapping validates transaction currency logic

---

## Data Synthesis Strategy

Since the APIs provide limited transaction volume, we'll synthesize realistic data:

### Transaction Generation (12 Months Historical)
- **Volume**: ~3,000 orders/month = 36,000 total orders
- **Distribution**: 
  - 70% customers: 1-2 orders (New segment)
  - 25% customers: 3-10 orders (Regular segment)
  - 5% customers: 11+ orders (VIP segment)
- **Patterns**:
  - Seasonal trends (Q4 spike)
  - Weekly patterns (weekend boost)
  - Random variation to avoid artificial patterns

### Geographic Assignment
- Map customers to countries based on real e-commerce market distribution
- Assign appropriate currencies based on country
- Ensure all major regions represented

### Product Selection Logic
- 1-5 products per order (realistic mix)
- Category affinity (e.g., jewelry + women's clothing correlation)
- Price-conscious behavior by region

### Currency Application
- Transaction currency based on customer country
- Historical exchange rates aligned with order dates
- Handle multi-currency consistently

---

## Dimensional Model Support

### Fact Table: fact_sales
**Grain**: One row per product per order  
**Measures**: quantity, unit_price_usd, unit_price_local, total_amount_usd, total_amount_local, exchange_rate

**Source Mapping**:
- **Base data**: Fake Store API (carts)
- **Currency conversion**: Exchange Rates API
- **Geographic context**: REST Countries API

### Dimension Tables

#### dim_product
**Source**: Fake Store API `/products`  
**SCD Type**: Type 2 (track price changes)  
**Attributes**: product_id, product_name, category, description, base_price, rating_average, rating_count

#### dim_customer
**Source**: Fake Store API `/users`  
**SCD Type**: Type 1  
**Attributes**: customer_id, name, email, phone, address, username

#### dim_location
**Source**: REST Countries API  
**SCD Type**: Type 1  
**Attributes**: country_code, country_name, region, sub_region, capital, currency_code, population, timezone

#### dim_date
**Source**: Generated  
**Attributes**: date_id, full_date, year, quarter, month, week, day_of_week, is_weekend

---

## Key Analytics Enabled

With these three API sources, we can demonstrate:

✅ **Product Performance**: Revenue and units by product/category  
✅ **Geographic Analysis**: Sales by country, region with drill-down  
✅ **Multi-Currency Reporting**: Revenue in local currency + USD normalization  
✅ **Customer Segmentation**: New/Regular/VIP based on purchase behavior  
✅ **Time-Series Analysis**: Trends, seasonality, YoY comparisons  
✅ **Cross-Dimensional**: Product performance by geography, customer value by region  
✅ **Currency Impact**: How exchange rates affect revenue reporting  

---

## API Limitations & Mitigations

| Limitation | Mitigation Strategy |
|------------|---------------------|
| Limited products (20) | Focus on category-level analysis; emphasize that this is representative |
| Few users (~10 in API) | Synthesize customer base to ~1,000 for realistic segmentation |
| Limited transaction history | Generate 12 months of synthetic transactions with realistic patterns |
| No real-time data | Daily batch refresh acceptable for demo; show architecture for streaming |
| No inventory data | Remove inventory KPIs from business case; focus on sales analytics |
| No marketing channel data | Remove CAC/channel metrics; focus on product/geo/customer dimensions |

---

## Data Quality Considerations

**From APIs**:
- Product data: Clean, structured, reliable
- User data: Some inconsistency in address formatting
- Cart data: May need deduplication logic
- Exchange rates: High quality, authoritative source
- Country data: Very high quality, standardized

**Validation Rules**:
- All product IDs must exist in dim_product
- All customer IDs must exist in dim_customer
- All country codes must exist in dim_location
- All dates must exist in dim_date
- Exchange rates must be > 0
- Quantities and prices must be positive
- No null values in key/required fields

---

## Next Steps

1. ✅ Validate API access and response formats
2. ✅ Design ETL pipeline architecture
3. ✅ Implement data extraction layer
4. ✅ Build data synthesis logic
5. ✅ Create dimensional model in data warehouse
6. ✅ Develop transformation scripts
7. ✅ Load and validate data
8. ✅ Build dashboards

---

**Last Updated**: October 8, 2025  
**Status**: Ready for implementation
