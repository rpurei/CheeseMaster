#!/bin/bash
cd /var/www/CheeseMaster/api
source /var/www/CheeseMaster/api/venv/bin/activate
pip install -r requirements.txt
/var/www/CheeseMaster/api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 4000
