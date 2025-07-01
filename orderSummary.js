/**
 * Aggregates raw Shopify orders into daily summary rows matching the screenshot headers.
 */
function summarizeOrders(orders) {
  function getPeriodEnds(date) {
    const d = new Date(date);
    // Week ends on Saturday (6)
    const weekEnd = new Date(d);
    weekEnd.setDate(d.getDate() + (6 - d.getDay()));
    // Month ends on last day of month
    const monthEnd = new Date(d.getFullYear(), d.getMonth() + 1, 0);
    return {
      weekEnd: weekEnd.toISOString().slice(0, 10),
      monthEnd: monthEnd.toISOString().slice(0, 10)
    };
  }

  const grouped = {};

  orders.forEach(order => {
    const createdAt = order.created_at.slice(0, 10);
    const isReturning = order.customer && order.customer.orders_count > 1;
    const groupKey = `${createdAt}_${isReturning ? 'Returning' : 'New'}`;

    if (!grouped[groupKey]) {
      const { weekEnd, monthEnd } = getPeriodEnds(createdAt);
      grouped[groupKey] = {
        Day: createdAt,
        New_or_re: isReturning ? 'Returning' : 'New',
        Orders: 0,
        Gross_sale: 0,
        Discounts: 0,
        Returns: 0,
        Net_sales: 0,
        Shipping_: 0,
        Duties: 0,
        Additional_: 0,
        Taxes: 0,
        Total_sales: 0,
        Quantity_c: 0,
        Quantity_r: 0,
        Week_End: weekEnd,
        Month_End: monthEnd
      };
    }

    const g = grouped[groupKey];
    g.Orders += 1;
    g.Gross_sale += parseFloat(order.total_price) || 0;
    g.Discounts += (order.total_discounts ? parseFloat(order.total_discounts) : 0);
    g.Returns += 0; // Update this if you fetch refunds
    g.Net_sales += (order.current_subtotal_price ? parseFloat(order.current_subtotal_price) : 0);
    g.Shipping_ += (order.total_shipping_price_set && order.total_shipping_price_set.shop_money ? parseFloat(order.total_shipping_price_set.shop_money.amount) : 0);
    g.Duties += (order.total_duties ? parseFloat(order.total_duties) : 0);
    g.Additional_ += 0; // Not directly in Shopify, leave as 0 or custom field
    g.Taxes += (order.total_tax ? parseFloat(order.total_tax) : 0);
    g.Total_sales += (order.current_total_price ? parseFloat(order.current_total_price) : 0);

    let qty = 0;
    order.line_items.forEach(item => {
      qty += item.quantity;
    });
    g.Quantity_c += qty;

    g.Quantity_r += 0; // Update if you want to handle returns/refunds
  });

  return Object.values(grouped).sort((a, b) => b.Day.localeCompare(a.Day));
}

module.exports = { summarizeOrders };
