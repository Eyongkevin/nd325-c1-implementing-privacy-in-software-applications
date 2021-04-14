#!/bin/sh
cd frontend/
npm install
cd -
cd backend/
pip install -r requirements.txt
export FLASK_APP=main/api/backend_rest_api.py;
flask run 
