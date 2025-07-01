import { Arcade } from "@arcade/sdk";
import { getShopifyOrders } from "./getShopifyOrders.js";

const arcade = new Arcade();

arcade.register([
  getShopifyOrders
]);

arcade.listen();
