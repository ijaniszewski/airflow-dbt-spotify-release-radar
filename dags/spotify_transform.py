import json
import os
from datetime import datetime, timezone

import mysql.connector
from airflow.datasets import Dataset
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator


@dag(
    dag_id="spotify_transform",
    start_date=datetime(2021, 1, 1),
    # Dataset from the upstream DAG (ingest)
    schedule=[Dataset("spotify")],
    catchup=False,
    tags=["spotify"],
)
def process_spotify_data_dag():

    @task
    def load_json_file():
        # Find the latest file by listing datalake dir
        folder = "/opt/airflow/datalake"
        files = sorted(
            [
                f
                for f in os.listdir(folder)
                if f.startswith("spotify_data_") and f.endswith(".json")
            ],
            reverse=True,
        )
        if not files:
            raise FileNotFoundError("No raw data files found.")
        file_name = files[0]  # Example: spotify_data_2025-04-17T12:31:17.json
        file_path = os.path.join(folder, file_name)

        with open(file_path, "r") as f:
            data = json.load(f)

        return {"file_name": file_name, "data": data}

    @task
    def transform_data(loaded):
        file_name = loaded["file_name"]
        playlist_data = loaded["data"]

        # Extract _load_ts from filename
        ts_str = file_name.replace("spotify_data_", "").replace(".json", "")
        _load_ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")

        songs = []
        for item in playlist_data["items"]:
            song = {
                "name": item["track"]["name"],
                "uri": item["track"]["uri"],
                "artist": item["track"]["artists"][0]["name"],
            }
            songs.append(song)

        return {"_load_ts": _load_ts.isoformat(), "songs": songs}

    @task
    def log_songs(data):
        songs = data["songs"]
        for song in songs:
            print(f"{song['artist']} : {song['name']}")

    @task
    def store_in_mysql(data):
        connection = mysql.connector.connect(
            host="mysql",
            user="airflow",
            password="airflow",
            database="spotify",
        )
        cursor = connection.cursor()

        songs = data["songs"]

        for song in songs:
            cursor.execute(
                """
                INSERT INTO source_spotify_tracks (artist, name, _load_ts)
                VALUES (%s, %s, %s)
                """,
                (song["artist"], song["name"], data["_load_ts"]),
            )

        connection.commit()
        cursor.close()
        connection.close()

    run_dbt = BashOperator(
        task_id="run_dbt_transform",
        bash_command="cd /opt/airflow/dbt/spotify_dbt && dbt build",
    )

    raw_data = load_json_file()
    transformed = transform_data(raw_data)
    log_songs(transformed)
    store_in_mysql(transformed) >> run_dbt


process_spotify_data = process_spotify_data_dag()
