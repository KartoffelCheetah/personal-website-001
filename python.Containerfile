  FROM docker.io/python:3.8

  RUN groupadd \
      --gid 1001 python && \
    useradd \
      --uid 1001 \
      --gid python \
      --shell /bin/bash \
      --create-home python && \
    mkdir /home/python/app

USER python

WORKDIR /home/python/app

# pipenv will be intalled to ~/.locale/bin/
ENV PATH="/home/python/.local/bin/:${PATH}"

RUN pip install --user \
  'pipenv==2020.08.13'

CMD ["pipenv", "run", "python_start"]
