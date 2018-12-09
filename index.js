const express = require('express');

const PORT = 3000
    , HOST = '0.0.0.0'
    , app = express()
    , VESIONS_ROUTE = '/versions.json'
;


app.get('/', (req, res) => {

    return res.send(`
        <p>
            Open the container bash with:
        </p>
        <code>
            docker-compose exec node bash
        </code>
        <p>
            <a href="${VESIONS_ROUTE}">
                Version information
            </a>
        </p>
        <iframe src="${VESIONS_ROUTE}"></iframe>
    `);
});

app.get(VESIONS_ROUTE, (req, res) => {

    return res.json({
        'versions': global.process.versions,
        'env': global.process.env,
    });
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
