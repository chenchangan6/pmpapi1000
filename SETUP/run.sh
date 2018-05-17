#!/bin/bash

service nginx restart

source /var/www/pmpapi1000/flask/bin/activate

gunicorn -D main:app -c /var/www/pmpapi1000/config1000/gunicorn.conf.py


echo -e "\e[31;47m**********English: server is running  **********\e[0m"
echo -e "\e[31;47m**********Chinese: 服务器运行成功！**********\e[0m"