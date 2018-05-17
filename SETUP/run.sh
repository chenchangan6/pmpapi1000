#!/bin/bash

service nginx restart
echo -e "\e[31;47m**********English: server is running  **********\e[0m"

source /var/www/pmpapi1000/flask/bin/activate

cd /var/www/pmpapi1000/

gunicorn main:app -c /var/www/pmpapi1000/config1000/gunicorn.conf.py


