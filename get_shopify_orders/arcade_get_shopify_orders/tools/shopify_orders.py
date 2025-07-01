# arcade_get_shopify_orders/tools/shopify_orders.py
import os
from typing import Annotated, Dict, List, Any
from datetime import datetime, timedelta
import httpx

from arcade_tdk import tool


async def fetch_shopify_orders(store_url: str, access_token: str, limit: int = 250) -> List[Dict[str, Any]]:
    """Fetch orders from Shopify API"""
    url = f"https://{store_url}/admin/api/2023-10/orders.json"
    params = {"limit": limit, "status": "any"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json"
            },
            params=params
        )
        
        if not response.is_success:
            raise Exception(f"[Shopify] {response.status_code} {response.reason_phrase}: {response.text}")
        
        data = response.json()
        return data.get("orders", [])


def get_period_ends(date_str: str) -> Dict[str, str]:
    """Get week end and month end dates for a given date"""
    date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
    
    # Week ends on Saturday (6)
    days_until_saturday = (5 - date.weekday()) % 7
    if days_until_saturday == 0 and date.weekday() != 5:  # If not Saturday, go to next Saturday
        days_until_saturday = 6
    
    week_end = date + timedelta(days=days_until_saturday) if days_until_saturday > 0 else date
    
    # Month ends on last day of month
    if date.month == 12:
        next_month = date.replace(year=date.year + 1, month=1, day=1)
    else:
        next_month = date.replace(month=date.month + 1, day=1)
    month_end = next_month - timedelta(days=1)
    
    return {
        "weekEnd": week_end.isoformat(),
        "monthEnd": month_end.isoformat()
    }


def summarize_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregate raw Shopify orders into daily summary rows"""
    grouped = {}
    
    for order in orders:
        created_at = order["created_at"][:10]  # Get date part only
        is_returning = order.get("customer", {}).get("orders_count", 1) > 1
        group_key = f"{created_at}_{'Returning' if is_returning else 'New'}"
        
        if group_key not in grouped:
            period_ends = get_period_ends(created_at)
            grouped[group_key] = {
                "Day": created_at,
                "New_or_re": "Returning" if is_returning else "New",
                "Orders": 0,
                "Gross_sale": 0.0,
                "Discounts": 0.0,
                "Returns": 0.0,
                "Net_sales": 0.0,
                "Shipping_": 0.0,
                "Duties": 0.0,
                "Additional_": 0.0,
                "Taxes": 0.0,
                "Total_sales": 0.0,
                "Quantity_c": 0,
                "Quantity_r": 0,
                "Week_End": period_ends["weekEnd"],
                "Month_End": period_ends["monthEnd"]
            }
        
        g = grouped[group_key]
        g["Orders"] += 1
        g["Gross_sale"] += float(order.get("total_price", 0))
        g["Discounts"] += float(order.get("total_discounts", 0))
        g["Returns"] += 0  # Update this if you fetch refunds
        g["Net_sales"] += float(order.get("current_subtotal_price", 0))
        
        # Handle shipping price
        shipping_price_set = order.get("total_shipping_price_set", {})
        shop_money = shipping_price_set.get("shop_money", {})
        g["Shipping_"] += float(shop_money.get("amount", 0))
        
        g["Duties"] += float(order.get("total_duties", 0))
        g["Additional_"] += 0  # Not directly in Shopify, leave as 0 or custom field
        g["Taxes"] += float(order.get("total_tax", 0))
        g["Total_sales"] += float(order.get("current_total_price", 0))
        
        # Calculate total quantity
        qty = sum(item.get("quantity", 0) for item in order.get("line_items", []))
        g["Quantity_c"] += qty
        g["Quantity_r"] += 0  # Update if you want to handle returns/refunds
    
    # Sort by date descending
    return sorted(grouped.values(), key=lambda x: x["Day"], reverse=True)


@tool
async def get_shopify_orders() -> Annotated[Dict[str, Any], "Summary of Shopify orders grouped by day and customer type"]:
    """
    Fetch and summarize Shopify orders from the configured store.
    
    Retrieves the latest 250 orders from Shopify and groups them by day and customer type
    (new vs returning), providing sales metrics and quantities.
    
    Requires environment variables:
    - SHOPIFY_STORE_URL: Your Shopify store URL (e.g., 'your-store.myshopify.com')
    - SHOPIFY_ACCESS_TOKEN: Your Shopify Admin API access token
    
    Returns:
        Dictionary containing 'summary' key with list of daily order summaries
        
    Examples:
        get_shopify_orders() -> {"summary": [{"Day": "2024-01-15", "Orders": 5, ...}]}
    """
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not store_url or not access_token:
        return {
            "error": "Missing Shopify credentials. Please set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN environment variables."
        }
    
    try:
        orders = await fetch_shopify_orders(store_url, access_token, limit=250)
        summary = summarize_orders(orders)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}