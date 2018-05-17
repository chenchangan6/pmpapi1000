#!/bin/bash

#7.创建虚拟运行环境
echo -e "\e[31;47m**********English:   [(SETP:7)] activate virtual env **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:7)]  创建虚拟运行环境**********\e[0m"
cd /var/www/pmpapi1000
virtualenv flask
source flask/bin/activate

#8.安装技术栈
echo -e "\e[31;47m**********English:   [(SETP:8)] install pyton package **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:8)]  安装技术栈**********\e[0m"
pip install flask
pip install flask-restful
pip install flask-cors
pip install flask-HTTPauth
pip install pymongo
pip install passlib
pip install qcloudsms_py

#9.安装gunicorn
echo -e "\e[31;47m**********English:   [(SETP:9)] install gunicorn **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:9)]  安装gunicorn**********\e[0m"
pip install gunicorn

#10.创建gunicorn日志
echo -e "\e[31;47m**********English:   [(SETP:10)] running gunicorn **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:10)]  运行gunicorn**********\e[0m"
touch /var/www/pmpapi1000/LOG1000/gunicorn.error.log