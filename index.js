import { Arcade } from "@arcade/sdk";
import { getShopifyOrders } from "./getShopifyOrders.js";

const arcade = new Arcade();

arcade.register([
  {
    tool: getShopifyOrders,
    name: "getShopifyOrders",
    description: "Fetch Shopify orders and write them to Google Sheets",
    parameters: [
      {
        name: "shopifyStore",
        type: "string",
        description: "Shopify store domain (e.g. ogthread.myshopify.com)",
        required: true,
      },
      {
        name: "shopifyApiKey",
        type: "string",
        description: "Shopify Admin API Key",
        required: true,
      },
      {
        name: "shopifySecret",
        type: "string",
        description: "Shopify Admin API Secret",
        required: true,
      },
      {
        name: "googleSheetId",
        type: "string",
        description: "Google Sheet ID to write the data to",
        required: true,
      },
    ],
  },
]);

arcade.listen({ port: process.env.PORT || 8000 });
