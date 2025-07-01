// getShopifyOrders.js
import { Tool } from "@arcade/sdk";
import fetch from "node-fetch";
import dayjs from "dayjs";
import { google } from "googleapis";
import { JWT } from "google-auth-library";

const SCOPES = ["https://www.googleapis.com/auth/spreadsheets"];
const SHEET_ID = "10Cm4k6Rz3LxYVn0hU4YQ3fe5p4Mi6XKU7RPZiDDIzos";
const TAB_NAME = "Shopify_SOT_View";

export const getShopifyOrders = new Tool({
  name: "getShopifyOrders",
  description: "Fetches Shopify order data for yesterday and appends a row to Google Sheets",
  inputSchema: {
    type: "object",
    required: ["shopName", "accessToken", "googleClientEmail", "googlePrivateKey"],
    properties: {
      shopName: { type: "string" },
      accessToken: { type: "string" },
      googleClientEmail: { type: "string" },
      googlePrivateKey: { type: "string" }
    }
  },
  run: async ({ shopName, accessToken, googleClientEmail, googlePrivateKey }) => {
    const start = dayjs().subtract(1, "day").startOf("day").toISOString();
    const end = dayjs().subtract(1, "day").endOf("day").toISOString();

    const url = `https://${shopName}.myshopify.com/admin/api/2023-07/orders.json?status=any&created_at_min=${start}&created_at_max=${end}`;

    const res = await fetch(url, {
      headers: {
        "X-Shopify-Access-Token": accessToken,
        "Content-Type": "application/json"
      }
    });

    const data = await res.json();
    const orders = data.orders || [];

    // Aggregate data
    let newCustomers = 0, returningCustomers = 0, grossSales = 0, totalShipping = 0,
      totalTaxes = 0, totalDiscounts = 0, totalReturns = 0, totalSales = 0;

    for (const order of orders) {
      if (order.customer && order.customer.orders_count === 1) newCustomers++;
      else returningCustomers++;

      grossSales += parseFloat(order.total_price || 0);
      totalShipping += parseFloat(order.total_shipping_price_set?.shop_money?.amount || 0);
      totalTaxes += parseFloat(order.total_tax || 0);
      totalDiscounts += parseFloat(order.total_discounts || 0);
      totalSales += parseFloat(order.current_total_price || 0);
    }

    // Prepare row
    const row = [
      dayjs().subtract(1, "day").format("YYYY-MM-DD"),
      newCustomers,
      returningCustomers,
      orders.length,
      grossSales,
      totalDiscounts,
      totalReturns,
      grossSales - totalDiscounts - totalReturns,
      totalShipping,
      0, // Duties (placeholder)
      0, // Additional (placeholder)
      totalTaxes,
      totalSales
    ];

    // Set up Google Sheets client
    const auth = new JWT({
      email: googleClientEmail,
      key: googlePrivateKey.replace(/\\n/g, "\n"),
      scopes: SCOPES
    });

    const sheets = google.sheets({ version: "v4", auth });
    await sheets.spreadsheets.values.append({
      spreadsheetId: SHEET_ID,
      range: `${TAB_NAME}!A1`,
      valueInputOption: "USER_ENTERED",
      insertDataOption: "INSERT_ROWS",
      requestBody: {
        values: [row]
      }
    });

    return {
      message: `Appended ${orders.length} orders to ${TAB_NAME}`
    };
  }
});
