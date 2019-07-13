const dotenv = require('dotenv');
const ROUTING = require('./src/assets/routing.json');

dotenv.config({ path: '../.env' });

const PROXY_CONFIG = [
  {
    context: [ ROUTING.API_PREFIX ],
    target: `http://python:${process.env.PORT_TEST_SERVER}`,
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
