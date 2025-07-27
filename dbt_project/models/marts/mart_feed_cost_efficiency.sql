SELECT
  af.feed_id,
  af.animal_type,
  af.feed_name,
  af.region,
  af.protein / NULLIF(af.price_per_kg, 0) AS protein_per_dollar,
  af.energy / NULLIF(af.price_per_kg, 0) AS energy_per_dollar,
  rp.climate_zone,
  rp.avg_rainfall_mm
FROM {{ ref('stg_animal_feed') }} af
LEFT JOIN {{ ref('dim_region') }} rp ON af.region = rp.region