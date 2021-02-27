import os

# Set the number of gunicorn workers
workers = int(os.environ.get('GUNICORN_WORKERS', '5'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '600'))
