#! /bin/sh

npm install

if [ $NODE_ENV = development ];
  then npm run dev;
  else npm run prod;
fi
