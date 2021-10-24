#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

cd $"$SCRIPT_DIR"
sudo docker-compose up --build -d
sudo docker-compose exec face_auth_web python manage.py migrate
sudo docker-compose exec face_auth_web python manage.py collectstatic --noinput
echo "project successfully started"