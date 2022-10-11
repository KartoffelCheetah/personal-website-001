#!/usr/bin/sh

. ./.env

UID_SERVER=1001
POD_NAME_TEST=pw001
IMG_TAG_PYTHON=localhost/${POD_NAME_TEST}__python

podman image build \
  --file ./python.Containerfile \
  --build-arg UID_SERVER=$UID_SERVER \
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
    -R \
    ./client/node_modules/ \
    ./static/

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
  --volume ./.venv/:/opt/pw001_server/.venv/ \
  --volume ./app/:/opt/pw001_server/app/ \
  --volume ./bin/:/opt/pw001_server/bin/ \
  --volume ./database/:/var/lib/pw001_server/database/ \
  --volume ./static/:/var/lib/pw001_server/static/ \
  --volume ./server.py:/opt/pw001_server/server.py \
  --volume ./.env:/opt/pw001_server/.env \
  --volume ./.env.dist:/opt/pw001_server/.env.dist \
  --volume ./Pipfile:/opt/pw001_server/Pipfile \
  --volume ./Pipfile.lock:/opt/pw001_server/Pipfile.lock \
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
