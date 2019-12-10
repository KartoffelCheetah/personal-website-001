FROM python:3.6

RUN echo "alias ll='ls -laF'" \
>> /etc/bash.bashrc

RUN groupadd --gid 1000 python

RUN useradd \
    --uid 1000 \
    --gid python \
    --shell /bin/bash \
    --create-home python

RUN mkdir /home/python/app

RUN apt-get update \
    && apt-get -y install \
        vim

RUN pip install \
    'pipenv==2018.10.13'
