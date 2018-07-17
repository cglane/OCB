#!/bin/bash


source virt/bin/activate

./cloud_sql_proxy -instances="brave-standard-180615:us-east1:bedswing"=tcp:5432 &

python sandbox/manage.py runserver 9000


=