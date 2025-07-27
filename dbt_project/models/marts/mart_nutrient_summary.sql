SELECT
  animal_type,
  AVG(protein) AS avg_protein,
  AVG(energy) AS avg_energy,
  AVG(fiber) AS avg_fiber
FROM {{ ref('stg_animal_feed') }}
GROUP BY animal_type