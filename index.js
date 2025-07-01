import { getShopifyOrders } from './getShopifyOrders.js';

export default async function ({ input }) {
  const { shop, accessToken, startDate, endDate } = input;

  const orders = await getShopifyOrders(shop, accessToken, startDate, endDate);
  return { orders };
}
