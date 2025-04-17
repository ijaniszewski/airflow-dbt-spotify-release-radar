{{ config(materialized='table') }}

WITH ranked_weeks AS (
    SELECT
        year,
        week_number,
        RANK() OVER (ORDER BY year DESC, week_number DESC) AS rnk
    FROM {{ ref('silver_spotify_tracks') }}
),

latest_week AS (
    SELECT
        year,
        week_number
    FROM ranked_weeks
    WHERE rnk = 1
    LIMIT 1
)

SELECT
    artist,
    name
FROM {{ ref('silver_spotify_tracks') }} s
JOIN latest_week lw
  ON s.year = lw.year AND s.week_number = lw.week_number
