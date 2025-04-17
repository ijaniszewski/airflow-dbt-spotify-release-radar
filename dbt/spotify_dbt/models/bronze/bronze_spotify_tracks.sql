{{ config(materialized='table') }}

SELECT
    -- {{ dbt_utils.generate_surrogate_key(['artist', 'name']) }} AS song_id,
    MD5(
        CONCAT(
            COALESCE(CAST(artist AS CHAR), '_dbt_utils_surrogate_key_null_'),
            '-',
            COALESCE(CAST(name AS CHAR), '_dbt_utils_surrogate_key_null_')
        )
    ) AS song_id,
    MIN(id) AS raw_id,
    artist,
    name,
    MIN(_load_ts) AS _load_ts,
    WEEK(MIN(_load_ts), 3) AS week_number,  -- ISO 8601 week
    YEAR(MIN(_load_ts)) AS year            -- Extract year from timestamp
FROM {{ source('spotify', 'source_spotify_tracks') }}
GROUP BY artist, name