FROM docker.io/python:3.8

ARG UID_SERVER
ARG NAME_SERVER

RUN groupadd \
    --gid $UID_SERVER $NAME_SERVER && \
  useradd \
    --system \
    --uid $UID_SERVER \
    --gid $NAME_SERVER \
    --shell /bin/false \
    --create-home \
    --home-dir /opt/$NAME_SERVER \
    $NAME_SERVER && \
  mkdir /var/lib/$NAME_SERVER /etc/$NAME_SERVER && \
  chown -R $UID_SERVER:$UID_SERVER /var/lib/$NAME_SERVER

USER $NAME_SERVER

WORKDIR /opt/$NAME_SERVER

# pipenv will be intalled to ~/.local/bin/
ENV PATH="/opt/${NAME_SERVER}/.local/bin/:${PATH}"

RUN pip install --user \
  'pipenv==2020.08.13'

CMD ["pipenv", "run", "python_start"]
