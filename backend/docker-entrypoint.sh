echo "Starting backend" && cd /app && uvicorn backend.api.asgi:app --host 0.0.0.0 --port 5000 --workers 1
