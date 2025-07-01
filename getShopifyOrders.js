import fetch from 'node-fetch';

export async function getShopifyOrders(shop, accessToken, startDate, endDate) {
  const url = `https://${shop}/admin/api/2023-07/orders.json?status=any&created_at_min=${startDate}&created_at_max=${endDate}&limit=250`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'X-Shopify-Access-Token': accessToken,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Shopify API error: ${error}`);
  }

  const data = await response.json();
  return data.orders;
}
