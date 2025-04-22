# Your first data engineering pipeline (Airflow + dbt)!

Read the full [tutorial on Medium](https://ijaniszewski.medium.com/your-first-data-engineering-pipeline-airflow-dbt-spotify-release-radar-songs-65fd36cd1670)

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

6. Install dbt-deps (`dbt_utils`):
```bash
docker-compose exec airflow-webserver dbt deps --project-dir /opt/airflow/dbt/
```


### Re-build compose
```bash
# Stop and remove all containers and volumes
# -v: removes named volumes (MySQL and Postgres data)
# --remove-orphans: cleans up any lingering containers
docker compose down -v --remove-orphans
 
# to force-rebuild the Airflow image:
docker compose build --no-cache
 
# startup & re-initialize Airflow DB and MySQL
docker compose up airflow-init
 
# starts everything
# including:
    # MySQL (which will now run init.sql again),
    # Redis, Postgres,
    # Airflow webserver, scheduler, worker, etc.
docker compose up
```


### Check dbt
```bash
# connect to Airflow container
docker-compose exec airflow-webserver bash

cd /opt/airflow/dbt/spotify_dbt/
dbt debug
```

### Check database
```bash
docker-compose exec mysql mysql -uairflow -p
USE spotify;
SHOW TABLES;
SELECT * FROM source_spotify_tracks;
```
