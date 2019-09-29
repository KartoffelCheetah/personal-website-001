#! /bin/bash

pipenv install --dev
flask run \
    -h 0.0.0.0 \
    -p $PORT_TEST_SERVER \
    --with-threads
