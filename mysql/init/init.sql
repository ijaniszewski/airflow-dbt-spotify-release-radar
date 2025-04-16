CREATE TABLE IF NOT EXISTS spotify_tracks_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_number INT NOT NULL,
    artist VARCHAR(255),
    name VARCHAR(255),
    added_at DATETIME
);

CREATE TABLE IF NOT EXISTS spotify_tracks_final (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_number INT NOT NULL,
    artist VARCHAR(255),
    name VARCHAR(255),
    added_at DATETIME
);