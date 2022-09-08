#!/usr/bin/sh

. ./.env

POD_NAME_TEST=pw001
IMG_TAG_PYTHON=localhost/${POD_NAME_TEST}__python

podman image build \
  --file ./python.Containerfile \
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
  --volume ./config/login-password-less.php:/var/www/html/plugins-enabled/login-password-less.php:ro \
  --volume ./database/website.db:/website.db \
  docker.io/adminer

# 1000:1000 is NODE's
podman unshare \
  chown \
    1000:1000 \
    -R \
    ./client/node_modules/ \
    ./app/static/

# 1001:1001 is PYTHON's
podman unshare \
  chown \
    1001:1001 \
    -R \
    ./app/static/uploads/ \
    ./database/

podman container run \
  --detach \
  --pod $POD_NAME_TEST \
  --name ${POD_NAME_TEST}_python \
  --env PIPENV_VENV_IN_PROJECT=$PIPENV_VENV_IN_PROJECT \
  --env FLASK_ENV=$FLASK_ENV \
  --env FLASK_APP=$FLASK_APP \
  --volume ./:/home/python/app/ \
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
  --volume ./app/static/:/home/node/static/\
  docker.io/node:14.15.0-alpine3.12 \
  npm run start
