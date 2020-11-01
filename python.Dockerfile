FROM python:3.6

RUN groupadd --gid 1000 python

RUN useradd \
    --uid 1000 \
    --gid python \
    --shell /bin/bash \
    --create-home python

RUN mkdir /home/python/app

USER python
# pipenv will be intalled to ~/.locale/bin/
ENV PATH="/home/python/.local/bin/:${PATH}"

RUN pip install --user \
   'pipenv==2020.08.13'
