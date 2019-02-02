FROM python:3.6

RUN echo "alias ll='ls -laF'" >> /etc/bash.bashrc

RUN groupadd --gid 1000 python \
&& useradd --uid 1000 --gid python --shell /bin/bash --create-home python

RUN mkdir /home/python/app

RUN apt-get update

RUN apt-get -y install nano

RUN pip install 'pipenv==2018.10.13'
