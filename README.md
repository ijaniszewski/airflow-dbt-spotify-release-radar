You need to have docker & docker compose installed


1. Initialize Airflow metadata DB and create user
```bash
docker compose up airflow-init
```

2. Start Airflow services
```bash
docker compose up
```