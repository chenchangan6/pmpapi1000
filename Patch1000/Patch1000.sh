#!/bin/bash
# 请务必使用
# nohup bash setup.sh &
# 来执行安装。记录反馈在 当前目录下的 nohup.out.
#PMPtikuAPI1000自动部署脚本 --2018.04.06 by Charles Chen.
#执行前，务必sudo -i，提权。
echo -e "\e[31;47m**********English:   [(SETP:8)]  Replace qcloudsms_py/httpclient.py**********\e[0m"
echo -e "\e[31;47m**********Chinese:   [(步骤:8)]  替换腾讯云短信SDK文件（SSL证书问题，CONTEXT=ssl._create_unverified_context()）**********\e[0m"
rm /var/www/pmpapi1000/flask/lib/python3.6/site-packages/qcloudsms_py/httpclient.py
cp /var/www/pmpapi1000/Patch1000/httpclient.py /var/www/pmpapi1000/flask/lib/python3.6/site-packages/qcloudsms_py/httpclient.py