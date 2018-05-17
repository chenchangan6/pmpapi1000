#!/bin/bash

service nginx restart

source /var/www/pmpapi1000/flask/bin/activate

echo -e "\e[31;47m**********English: server is running  **********\e[0m"

gunicorn main:app -c /var/www/pmpapi1000/config1000/gunicorn.conf.py


