#!/bin/bash

cd backend
source env/bin/activate
cd src
python manage.py runserver 0.0.0.0:8888
