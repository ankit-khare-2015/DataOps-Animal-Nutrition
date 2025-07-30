SELECT
    region,
    CAST(avg_rainfall_mm AS INT) AS avg_rainfall_mm,
    main_livestock,
    climate_zone
FROM {{ source('raw', 'seed_region_profiles') }}
