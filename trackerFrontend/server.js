const express = require('express');
const path = require('path');
const app = express();

// Middleware to parse JSON bodies
app.use(express.static(path.join(__dirname, 'public')));

const port = 3000;
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});