SELECT
  region,
  AVG(price_per_kg) AS avg_price_per_kg
FROM {{ ref('stg_animal_feed') }}
GROUP BY region