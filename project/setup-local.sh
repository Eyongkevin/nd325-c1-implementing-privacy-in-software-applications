#!/bin/sh
cd frontend/
npm install
cd -
cd backend/
#pip install -r requirements.txt
pipenv shell
export FLASK_APP=main/api/backend_rest_api.py;
flask run 
