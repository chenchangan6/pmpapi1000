#!/bin/bash
# 请务必使用
# nohup bash setup.sh &
# 来执行安装。记录反馈在 当前目录下的 nohup.out.
#PMPtikuAPI1000自动部署脚本 --2018.04.06 by Charles Chen.
#执行前，务必sudo -i，提权。




#1.更新系统安装源
echo -e "\e[31;47m**********English:   [(SETP:1)] UPDATE apt-get SOURCE **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:1)]  更新系统安装源 **********\e[0m"

sudo apt-get update

#2.安装PYTHON3.6
echo -e "\e[31;47m**********English:   [(SETP:2)] Install python3.6 **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:2)]  安装PYTHON3.6 **********\e[0m"


#2.1添加软件仓库地址
echo -e "\e[31;47m**********Chinese:   [(步骤:2.1)]  添加软件仓库地址 **********\e[0m"
sudo apt-get -y install software-properties-common

#2.2添加python3.6地址,并更新地址库
echo -e "\e[31;47m**********Chinese:   [(步骤:2.2)]  添加python3.6地址,并更新地址库 **********\e[0m"
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update

#2.3安装python3.6
echo -e "\e[31;47m**********Chinese:   [(步骤:2.3)]  安装python3.6 **********\e[0m"
sudo apt-get -y install python3.6
sudo apt-get -y install zip



#2.4替换默认的PYTHON为PYTHON3.6
echo -e "\e[31;47m**********Chinese:   [(步骤:2.4)]  替换默认的PYTHON为PYTHON3.6 **********\e[0m"
sudo rm /usr/bin/python
sudo ln -s /usr/bin/python3.6 /usr/bin/python


#3.1安装PIP
echo -e "\e[31;47m**********English:   [(SETP:3)] Install pip **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:3)]  安装PIP **********\e[0m"
sudo curl https://bootstrap.pypa.io/get-pip.py | python


#4.安装 virtualenv
echo -e "\e[31;47m**********English:   [(SETP:4)] Install virtualenv **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:4)]  安装virtualenv**********\e[0m"
pip install virtualenv






#5.创建网站目录
echo -e "\e[31;47m**********English:   [(SETP:5)] Create Director **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:5)]  创建网站目录**********\e[0m"

mkdir -p /var/www/pmpapi1000
cd /var/www/
wget https://github.com/chenchangan6/pmpapi1000/archive/master.zip
unzip master.zip
mv /var/www/pmpapi1000-master/* /var/www/pmpapi1000/
rm -rf /var/www/pmpapi1000-master
rm master.zip


#6.安装 Nginx
echo -e "\e[31;47m**********English:   [(SETP:6)] install Nginx **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:6)]  安装 Nginx**********\e[0m"
sudo apt-get -y install nginx
rm /etc/nginx/sites-enabled/default
ln -s /var/www/pmpapi1000/config1000/pmpapi1000.conf /etc/nginx/conf.d/
service nginx restart


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

#9.安装gunicorn
echo -e "\e[31;47m**********English:   [(SETP:9)] install gunicorn **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:9)]  安装gunicorn**********\e[0m"
pip install gunicorn

#10.运行gunicorn
echo -e "\e[31;47m**********English:   [(SETP:10)] running gunicorn **********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:10)]  运行gunicorn**********\e[0m"
touch /var/www/pmpapi1000/LOG1000/gunicorn.error.log
gunicorn -D main:app -c /var/www/pmpapi1000/config1000/gunicorn.conf.py
