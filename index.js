const express = require("express");
const { Arcade } = require("arcade-js");
const { getShopifyOrders } = require("./getShopifyOrders");

const app = express();
const port = process.env.PORT || 8002;

const arcade = new Arcade({ secret: process.env.ARCADE_SECRET || "dev" });

// Register your tool
arcade.tool("getShopifyOrders", getShopifyOrders);

// Register with Express
app.use("/", arcade.router());

app.listen(port, () => {
  console.log(`Arcade worker running on port ${port}`);
});
