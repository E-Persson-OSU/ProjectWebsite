web: gunicorn app:app
worker: python -u worker.py
heroku ps:scale worker=1