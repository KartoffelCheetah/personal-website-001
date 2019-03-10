const PROXY_CONFIG = [
  {
    context: [
      "/media",
      "/user",
    ],
    target: "http://python:5000",
    secure: false //DEV
  }
];

module.exports = PROXY_CONFIG;
