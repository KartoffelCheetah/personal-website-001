const dotenv = require('dotenv');

dotenv.config({ path: '../.env.blueprint' });

const PROXY_CONFIG = [
  {
    context: [
      process.env.MEDIA_BLUEPRINT_ENDPOINT,
      process.env.USER_BLUEPRINT_ENDPOINT,
    ],
    target: "http://python:5000",
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
