-- Source table (loaded by Airflow)
CREATE TABLE IF NOT EXISTS source_spotify_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artist VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    _load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT SELECT ON source_spotify_tracks TO 'airflow'@'%';
FLUSH PRIVILEGES;