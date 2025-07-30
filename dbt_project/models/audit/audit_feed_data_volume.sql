SELECT
    CURRENT_DATE AS audit_date,
    COUNT(*) AS row_count
FROM {{ ref('stg_animal_feed') }}
