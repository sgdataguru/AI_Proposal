-- Purpose: Test bronze to silver transformation for lead data
-- Prerequisites: None (uses CTE test data)
-- Expected: Clean, normalized lead data with standardized formats
-- How to run: Execute this query in your SQL environment (Synapse, BigQuery, etc.)
--
-- Example test demonstrating data transformation SQL logic

WITH bronze_lead_data AS (
    -- Simulated raw data from bronze layer
    SELECT 
        'L001' as lead_id,
        'JOHN.DOE@EXAMPLE.COM' as email,  -- Mixed case
        'Acme Corp' as company_name,
        '2024-01-15T10:30:00Z' as ingested_at,
        'active' as status,
        '{"source": "web_form", "campaign": "Q1_2024"}' as metadata_json
    UNION ALL
    SELECT 
        'L002',
        'jane.smith@example.com',
        'Tech Inc',
        '2024-01-16T14:20:00Z',
        'active',
        '{"source": "webinar", "campaign": "Q1_2024"}'
    UNION ALL
    SELECT 
        'L003',
        'bob.jones@COMPANY.COM  ',  -- Trailing spaces
        NULL,  -- Missing company
        '2024-01-17T09:15:00Z',
        'inactive',
        '{"source": "email", "campaign": "Q4_2023"}'
    UNION ALL
    SELECT 
        'L004',
        'invalid-email',  -- Invalid format
        'Demo Co',
        '2024-01-18T16:45:00Z',
        'pending',
        NULL  -- Missing metadata
),

silver_lead_data AS (
    -- Transformation logic
    SELECT 
        lead_id,
        LOWER(TRIM(email)) as email_normalized,
        CASE 
            WHEN email LIKE '%_@_%.__%' THEN TRUE 
            ELSE FALSE 
        END as email_valid,
        COALESCE(company_name, 'Unknown') as company_name,
        CAST(ingested_at AS TIMESTAMP) as ingested_timestamp,
        UPPER(status) as status_standardized,
        metadata_json,
        CURRENT_TIMESTAMP as transformed_at
    FROM bronze_lead_data
)

-- Output transformed data
SELECT 
    lead_id,
    email_normalized,
    email_valid,
    company_name,
    ingested_timestamp,
    status_standardized,
    metadata_json,
    -- Add data quality flags
    CASE 
        WHEN email_valid = FALSE THEN 'INVALID_EMAIL'
        WHEN company_name = 'Unknown' THEN 'MISSING_COMPANY'
        ELSE 'OK'
    END as data_quality_flag
FROM silver_lead_data
ORDER BY lead_id;

-- Expected output verification:
-- 
-- | lead_id | email_normalized       | email_valid | company_name | status_standardized | data_quality_flag |
-- |---------|------------------------|-------------|--------------|---------------------|-------------------|
-- | L001    | john.doe@example.com   | TRUE        | Acme Corp    | ACTIVE              | OK                |
-- | L002    | jane.smith@example.com | TRUE        | Tech Inc     | ACTIVE              | OK                |
-- | L003    | bob.jones@company.com  | TRUE        | Unknown      | INACTIVE            | MISSING_COMPANY   |
-- | L004    | invalid-email          | FALSE       | Demo Co      | PENDING             | INVALID_EMAIL     |

-- Test Assertions (to validate manually):
-- 1. ✅ All emails should be lowercase and trimmed
-- 2. ✅ Email validation should flag 'invalid-email' as FALSE
-- 3. ✅ NULL company names should be replaced with 'Unknown'
-- 4. ✅ Status should be uppercase
-- 5. ✅ Data quality flags should identify issues
