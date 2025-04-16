# Your first data engineering pipeline (Airflow + dbt)!

## Spotify Release Radar songs

1. Create an app from Spotify Developer account. Get Client ID and secret. Create `.env` file (same as `.env.example`):
```bash
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=
SPOTIPY_REDIRECT_URI=https://127.0.0.1:7777/callback
```

2. Get your Release Radar playlist ID
    * via link (`https://open.spotify.com/playlist/<playlist_id>`)
    * via `get_release_radar_id.py` Python script. There you need to authenticate by copying link from opened browser tab into shell

3. Install docker-compose and run Docker Daemon

4. Initialize Airflow metadata DB and create user
```bash
docker compose up airflow-init
```

5. Start Airflow services
```bash
docker compose up
```