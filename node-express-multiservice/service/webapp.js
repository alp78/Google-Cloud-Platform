const express = require('express');
const webapp = express();

webapp.get('/', (req, res) => {
  res.send("My Web App");
});

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
webapp.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});