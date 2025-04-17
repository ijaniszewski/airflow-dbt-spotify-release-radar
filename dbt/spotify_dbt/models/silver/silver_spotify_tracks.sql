{{ config(materialized='table') }}

SELECT
    song_id,
    artist,
    name,
    week_number,
    year
FROM {{ ref('bronze_spotify_tracks') }}
