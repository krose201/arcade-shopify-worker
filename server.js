require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { fetchShopifyOrders } = require('./shopify');
const { summarizeOrders } = require('./orderSummary');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());

// Secret authentication middleware
app.use((req, res, next) => {
  const arcadeSecret = process.env.ARCADE_SECRET;
  const authHeader = req.headers['authorization'];
  if (arcadeSecret && authHeader !== arcadeSecret) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
});

app.get('/', (req, res) => {
  res.send('Arcade Shopify Worker is running!');
});

app.get('/orders', async (req, res) => {
  const {
    SHOPIFY_STORE_URL,
    SHOPIFY_ACCESS_TOKEN
  } = process.env;

  if (!SHOPIFY_STORE_URL || !SHOPIFY_ACCESS_TOKEN) {
    return res.status(500).json({ error: 'Missing Shopify credentials in environment variables.' });
  }

  try {
    const orders = await fetchShopifyOrders({
      storeUrl: SHOPIFY_STORE_URL,
      accessToken: SHOPIFY_ACCESS_TOKEN,
      params: { limit: 50, status: 'any', ...req.query }
    });

    const summary = summarizeOrders(orders);

    res.json({ summary });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Arcade Shopify Worker running on port ${PORT}`);
});
