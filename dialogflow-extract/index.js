'use strict';

const {WebhookClient} = require('dialogflow-fulfillment');
const express = require('express');
const bodyParser = require('body-parser');
var path = require('path');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

function WebhookProcessing(req, res) {
    const agent = new WebhookClient({request: req, response: res});

    console.log('Dialogflow Request headers: ' + JSON.stringify(req.headers));
    console.log('Dialogflow Request body: ' + JSON.stringify(req.body));

    console.log(JSON.stringify(req.body.queryResult.queryText));
    console.log(JSON.stringify(req.body.queryResult.fulfillmentText));

}

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/index.html'));
    
});

app.post('/fulfillment', function (req, res) {
    WebhookProcessing(req, res);
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});