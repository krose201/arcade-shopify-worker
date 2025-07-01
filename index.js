iimport { Arcade } from "@arcade/sdk";
import { getShopifyOrders } from "./getShopifyOrders.js";

const arcade = new Arcade();

arcade.register([getShopifyOrders]);

arcade.listen(); // this tells Arcade to expose this worker's tools
