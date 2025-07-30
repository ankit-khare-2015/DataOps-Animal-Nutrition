SELECT
  af.feed_id,
  af.animal_type,
  af.feed_name,
  af.region,
  rp.climate_zone,
  rp.avg_rainfall_mm,
  af.protein / NULLIF(af.price_per_kg, 0) AS protein_per_dollar,
  af.energy / NULLIF(af.price_per_kg, 0) AS energy_per_dollar
FROM {{ ref('stg_animal_feed') }} AS af
LEFT JOIN {{ ref('dim_region') }} AS rp ON af.region = rp.region
