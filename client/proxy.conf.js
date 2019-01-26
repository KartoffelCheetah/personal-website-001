const PROXY_CONFIG = [
  {
    context: [
      "/api/v1",
      "/media",
      "/user",
    ],
    target: "http://python:5000",
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
