import { Tool } from "@arcade/sdk";
import fetch from "node-fetch";

export const getShopifyOrders = new Tool({
  name: "getShopifyOrders",
  description: "Fetch orders from Shopify",
  inputSchema: {
    type: "object",
    required: ["shopName", "accessToken", "startDate", "endDate"],
    properties: {
      shopName: { type: "string" },
      accessToken: { type: "string" },
      startDate: { type: "string" },
      endDate: { type: "string" }
    }
  },
  run: async ({ shopName, accessToken, startDate, endDate }) => {
    const res = await fetch(`https://${shopName}.myshopify.com/admin/api/2023-07/orders.json?status=any&created_at_min=${startDate}&created_at_max=${endDate}`, {
      headers: { "X-Shopify-Access-Token": accessToken }
    });

    const json = await res.json();
    return json.orders;
  }
});
