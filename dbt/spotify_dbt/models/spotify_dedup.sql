{{ config(materialized='table') }}

SELECT
    MIN(id) as id,
    week_number,
    artist,
    name,
    MIN(added_at) as added_at
FROM spotify_tracks_raw
GROUP BY week_number, artist, name