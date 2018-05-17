FROM ubuntu:16.04

MAINTAINER charlesChen chenchangan6@gmail.com


RUN apt-get update
RUN apt-get -y install software-properties-common


RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt-get update


RUN apt-get -y install python3.6

RUN apt-get -y install zip
RUN apt-get -y install curl
RUN apt-get -y install wget


RUN rm -f /usr/bin/python
RUN ln -s /usr/bin/python3.6 /usr/bin/python



RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install virtualenv



RUN mkdir -p /var/www/pmpapi1000
RUN wget -c -P /var/www/ https://github.com/chenchangan6/pmpapi1000/archive/master.zip?1
RUN ls /var/www/
RUN unzip /var/www/master.zip?1 -d /var/www/
RUN mv /var/www/pmpapi1000-master/* /var/www/pmpapi1000/
RUN rm -rf /var/www/pmpapi1000-master
RUN rm -f /var/www/master.zip?1

RUN apt-get -y install nginx
RUN rm -f /etc/nginx/sites-enabled/default
RUN ln -s /var/www/pmpapi1000/config1000/pmpapi1000.conf /etc/nginx/conf.d/
RUN service nginx restart


RUN virtualenv /var/www/pmpapi1000/flask
RUN bash /var/www/pmpapi1000/SETUP/Dockersetupapi.sh
RUN bash /var/www/pmpapi1000/Patch1000/Patch1000.sh
CMD bash /var/www/pmpapi1000/SETUP/run.sh






EXPOSE 443
EXPOSE 8000
