const ROUTING = require('../static/routing.json');

const PROXY_CONFIG = [
  {
    context: [ ROUTING.API_PREFIX ],
    target: `http://python:${process.env.PORT_TEST_SERVER}`,
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
