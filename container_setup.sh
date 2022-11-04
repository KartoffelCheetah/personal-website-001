#!/usr/bin/sh

. ./.env

UID_SERVER=1001
NAME_SERVER=pw001_server
POD_NAME_TEST=pw001
IMG_TAG_PYTHON=localhost/${POD_NAME_TEST}__python

podman image build \
  --file ./python.Containerfile \
  --build-arg UID_SERVER=$UID_SERVER \
  --build-arg NAME_SERVER=$NAME_SERVER \
  --tag $IMG_TAG_PYTHON

podman pod create \
  --name $POD_NAME_TEST \
  --publish $PORT_TEST_SERVER:$PORT_TEST_SERVER/TCP \
  --publish $PORT_TEST_CLIENT:$PORT_TEST_CLIENT/TCP \
  --publish $PORT_ADMINER:8080/TCP

podman container run \
  --detach \
  --pod $POD_NAME_TEST \
  --name ${POD_NAME_TEST}_adminer \
  --env ADMINER_PLUGINS=$ADMINER_PLUGINS \
  --env PASS_ADMINER=$PASS_ADMINER \
  --volume ./database/login-password-less.php:/var/www/html/plugins-enabled/login-password-less.php:ro \
  --volume ./database/storage/:/storage/ \
  docker.io/adminer

# 1000:1000 is NODE's

podman unshare \
  chown \
    1000:1000 \
    ./client/ \
    ./client/package-lock.json \
    ./client/package.json

podman unshare \
  chown \
    1000:1000 \
    -R \
    ./client/node_modules/ \
    ./static/client/

podman unshare \
  chown \
    $UID_SERVER:$UID_SERVER \
    -R \
    ./.venv/ \
    ./Pipfile \
    ./Pipfile.lock \
    ./static/uploads/ \
    ./database/storage/

podman container run \
  --detach \
  --pod $POD_NAME_TEST \
  --name ${POD_NAME_TEST}_python \
  --env PIPENV_VENV_IN_PROJECT=$PIPENV_VENV_IN_PROJECT \
  --env FLASK_ENV=$FLASK_ENV \
  --env FLASK_APP=$FLASK_APP \
  --env PORT_TEST_SERVER=$PORT_TEST_SERVER \
  --volume ./.venv/:/opt/$NAME_SERVER/.venv/ \
  --volume ./app/:/opt/$NAME_SERVER/app/ \
  --volume ./bin/:/opt/$NAME_SERVER/bin/ \
  --volume ./database/:/var/lib/$NAME_SERVER/database/ \
  --volume ./static/:/var/lib/$NAME_SERVER/static/ \
  --volume ./server.py:/opt/$NAME_SERVER/server.py \
  --volume ./.env:/etc/$NAME_SERVER/.env \
  --volume ./.env.dist:/opt/$NAME_SERVER/.env.dist \
  --volume ./Pipfile:/opt/$NAME_SERVER/Pipfile \
  --volume ./Pipfile.lock:/opt/$NAME_SERVER/Pipfile.lock \
  $IMG_TAG_PYTHON

podman container run \
  --detach \
  --pod $POD_NAME_TEST \
  --name ${POD_NAME_TEST}_node \
  --user node \
  --workdir /home/node/app/ \
  --env NODE_ENV=$NODE_ENV \
  --env PORT_TEST_SERVER=$PORT_TEST_SERVER \
  --env PORT_TEST_CLIENT=$PORT_TEST_CLIENT \
  --volume ./client/:/home/node/app/ \
  --volume ./static/:/home/node/static/\
  docker.io/node:14.15.0-alpine3.12 \
  npm run start
