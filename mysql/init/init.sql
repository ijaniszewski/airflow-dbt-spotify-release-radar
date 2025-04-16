CREATE TABLE IF NOT EXISTS spotify_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_number INT NOT NULL,
    artist VARCHAR(255),
    name VARCHAR(255),
    added_at DATETIME
);