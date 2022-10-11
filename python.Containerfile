FROM docker.io/python:3.8

ARG UID_SERVER

RUN groupadd \
    --gid $UID_SERVER pw001_server && \
  useradd \
    --system \
    --uid $UID_SERVER \
    --gid pw001_server \
    --shell /bin/false \
    --create-home \
    --home-dir /opt/pw001_server \
    pw001_server && \
  mkdir /var/lib/pw001_server && \
  chown -R $UID_SERVER:$UID_SERVER /var/lib/pw001_server

USER pw001_server

WORKDIR /opt/pw001_server

# pipenv will be intalled to ~/.locale/bin/
ENV PATH="/opt/pw001_server/.local/bin/:${PATH}"

RUN pip install --user \
  'pipenv==2020.08.13'

CMD ["pipenv", "run", "python_start"]
