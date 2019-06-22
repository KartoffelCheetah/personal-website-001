const dotenv = require('dotenv');

dotenv.config({ path: '../.env' });
dotenv.config({ path: '../.env.blueprint' });

const PROXY_CONFIG = [
  {
    context: [
      process.env.BLUEPRINT_ENDPOINT_MEDIA,
      process.env.BLUEPRINT_ENDPOINT_USER,
    ],
    target: `http://python:${process.env.PORT_TEST_SERVER}`,
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
