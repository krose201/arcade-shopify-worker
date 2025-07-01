const fetch = require('node-fetch');

async function fetchShopifyOrders({ storeUrl, accessToken, params = {} }) {
  const query = new URLSearchParams(params).toString();
  const url = `https://${storeUrl}/admin/api/2023-10/orders.json${query ? '?' + query : ''}`;
  const response = await fetch(url, {
    headers: {
      'X-Shopify-Access-Token': accessToken,
      'Content-Type': 'application/json'
    }
  });
  if (!response.ok) {
    throw new Error(`[Shopify] ${response.status} ${response.statusText}: ${await response.text()}`);
  }
  const data = await response.json();
  return data.orders;
}

module.exports = { fetchShopifyOrders };
