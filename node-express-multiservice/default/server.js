const express = require('express');
const app = express();

app.get('/', (req, res) => {
  const index = require('./index');
  res.send(index.hello());
});

app.get('/webapp', (req, res) => {
    res.redirect('https://webapp-dot-multiple-app.appspot.com');
  });

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});