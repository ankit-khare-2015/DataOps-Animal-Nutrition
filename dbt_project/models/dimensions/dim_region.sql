SELECT
    region,
    avg_rainfall_mm,
    main_livestock,
    climate_zone
FROM {{ ref('stg_region_profiles') }}
