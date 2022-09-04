#!/bin/sh

echo "Waiting for PostgreSQL to start..."
./wait-for db:8080

echo "Migrating the databse..."
python3 manage.py migrate

echo "Starting the server..."
python3 manage.py runserver 0.0.0.0:8000