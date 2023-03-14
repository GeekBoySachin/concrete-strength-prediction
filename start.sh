#!bin/sh
gunicorn -w 3 app:app