#!/bin/bash

../cloud_sql_proxy -instances="brave-standard-180615:us-east1:bedswing"=tcp:0.0.0.0:3306 &

gunicorn --preload -b 0.0.0.0:8000 wsgi