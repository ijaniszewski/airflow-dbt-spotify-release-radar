import json
import os
from datetime import datetime, timezone

import spotipy
from airflow.datasets import Dataset
from airflow.decorators import dag, task
from spotipy.oauth2 import SpotifyClientCredentials


@dag(
    dag_id="spotify_weekly_ingest",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@weekly",
    catchup=False,
    tags=["spotify"],
)
def get_spotify_data_dag():

    # Dataset is used to trigger the downstream DAG (transform)
    @task(outlets=[Dataset("spotify")])
    def extract_data():
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        playlist_URI = os.environ["SPOTIPY_PLAYLIST_ID"]
        playlist_data = sp.playlist_tracks(playlist_URI)

        # Timestamp-based filename
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        file_path = f"/opt/airflow/datalake/spotify_data_{timestamp}.json"

        with open(file_path, "w") as f:
            json.dump(playlist_data, f)

        return file_path

    extract_data()


get_spotify_data = get_spotify_data_dag()
