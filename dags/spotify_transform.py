import json
import os
from datetime import datetime

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
        file_path = os.path.join(folder, files[0])
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    @task
    def transform_data(playlist_data):
        added_txt = playlist_data["items"][0]["added_at"]
        added_dt = datetime.strptime(added_txt, "%Y-%m-%dT%H:%M:%SZ")
        week_number = added_dt.isocalendar().week
        songs = []
        for item in playlist_data["items"]:
            song = {
                "name": item["track"]["name"],
                "uri": item["track"]["uri"],
                "artist": item["track"]["artists"][0]["name"],
            }
            songs.append(song)
        return {"week_number": week_number, "songs": songs}

    @task
    def load_data(data):
        week_number = data["week_number"]
        songs = data["songs"]
        print(f"For week number: {week_number}:")
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

        week_number = data["week_number"]
        songs = data["songs"]

        for song in songs:
            cursor.execute(
                """
                INSERT INTO spotify_tracks_raw (week_number, artist, name, added_at)
                VALUES (%s, %s, %s, NOW())
                """,
                (week_number, song["artist"], song["name"]),
            )

        connection.commit()
        cursor.close()
        connection.close()

    run_dbt = BashOperator(
        task_id="run_dbt_transform",
        bash_command="cd /opt/airflow/dbt/spotify_dbt && dbt run",
    )

    raw_data = load_json_file()
    transformed = transform_data(raw_data)
    load_data(transformed)
    store_in_mysql(transformed) >> run_dbt


process_spotify_data = process_spotify_data_dag()
