SELECT
    feed_id,
    animal_type,
    feed_name,
    CAST(protein AS FLOAT) AS protein,
    CAST(energy AS FLOAT) AS energy,
    CAST(fiber AS FLOAT) AS fiber,
    CAST(price_per_kg AS FLOAT) AS price_per_kg,
    region,
    CAST(date AS DATE) AS date
FROM {{ source('raw', 'seed_feed_data') }}
