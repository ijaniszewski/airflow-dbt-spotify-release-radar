import os
from datetime import datetime

import spotipy
from airflow.decorators import dag, task
from spotipy.oauth2 import SpotifyClientCredentials


@dag(
    dag_id="get_spotify_data",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@weekly",
    catchup=False,
    tags=["spotify"],
)
def get_spotify_data_dag():

    @task
    def extract_data():
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        playlist_URI = os.environ["SPOTIPY_PLAYLIST_ID"]
        playlist_data = sp.playlist_tracks(playlist_URI)
        return playlist_data

    @task
    def transform_data(playlist_data):
        added_txt = playlist_data["items"][0]["added_at"]
        added_dt = datetime.strptime(added_txt, "%Y-%m-%dT%H:%M:%SZ")
        week_number = added_dt.isocalendar().week
        songs = []
        for item in playlist_data["items"]:
            song = {}
            song["name"] = item["track"]["name"]
            song["uri"] = item["track"]["uri"]
            song["artist"] = item["track"]["artists"][0]["name"]
            # artist_uri = item["track"]["artists"][0]["uri"]
            songs.append(song)
        return {"week_number": week_number, "songs": songs}

    @task
    def load_data(data):
        week_number = data["week_number"]
        songs = data["songs"]
        print(f"For week number: {week_number}:")
        for song in songs:
            print(f"{song['artist']} : {song['name']}")

    # Define task flow
    playlist_data = extract_data()
    transformed_data = transform_data(playlist_data)
    load_data(transformed_data)


# Assign the DAG to a variable Airflow can recognize
get_spotify_data = get_spotify_data_dag()
