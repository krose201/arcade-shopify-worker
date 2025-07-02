# Multi-Store Shopify Orders Setup Guide

## 🔧 Environment Variable Management

### Single Store Setup (Default)

1. **Create your `.env` file** in the project root:
```bash
cp .env.example .env
```

2. **Configure your single store credentials**:
```env
# Single Store Configuration
SHOPIFY_STORE_URL=yourstore.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ARCADE_SECRET=your-secret-key
PORT=3000
```

3. **Usage**:
```python
# This will use the default SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN
result = await get_shopify_orders()
```

---

## 🏪 Multi-Store Setup

### Environment Variables for Multiple Stores

Add additional store configurations to your `.env` file using the pattern `SHOPIFY_{STORE_KEY}_URL` and `SHOPIFY_{STORE_KEY}_ACCESS_TOKEN`:

```env
# Single Store Configuration (backward compatible)
SHOPIFY_STORE_URL=yourstore.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Multi-Store Configuration
SHOPIFY_STORE1_URL=store1.myshopify.com
SHOPIFY_STORE1_ACCESS_TOKEN=shpat_store1_token_here

SHOPIFY_STORE2_URL=store2.myshopify.com
SHOPIFY_STORE2_ACCESS_TOKEN=shpat_store2_token_here

SHOPIFY_MAIN_URL=mainstore.myshopify.com
SHOPIFY_MAIN_ACCESS_TOKEN=shpat_main_token_here

SHOPIFY_PREMIUM_URL=premium.myshopify.com
SHOPIFY_PREMIUM_ACCESS_TOKEN=shpat_premium_token_here

# API Configuration
ARCADE_SECRET=your-secret-key
PORT=3000
```

### Usage Examples

```python
# Default store (backward compatible)
result = await get_shopify_orders()
# Returns: {"summary": [...], "store": "default"}

# Specific stores
result1 = await get_shopify_orders("STORE1")
# Returns: {"summary": [...], "store": "STORE1"}

result2 = await get_shopify_orders("STORE2")
# Returns: {"summary": [...], "store": "STORE2"}

result_main = await get_shopify_orders("MAIN")
# Returns: {"summary": [...], "store": "MAIN"}

result_premium = await get_shopify_orders("PREMIUM")
# Returns: {"summary": [...], "store": "PREMIUM"}
```

---

## 🚀 Deployment Considerations

### Local Development
- Use `.env` file in project root
- Supports both single and multi-store configurations
- Environment variables are automatically loaded

### Production Deployment (Railway, Heroku, etc.)
Set environment variables in your deployment platform:

**Single Store:**
- `SHOPIFY_STORE_URL`
- `SHOPIFY_ACCESS_TOKEN`

**Multi-Store:**
- `SHOPIFY_STORE_URL` (default)
- `SHOPIFY_ACCESS_TOKEN` (default)
- `SHOPIFY_STORE1_URL`
- `SHOPIFY_STORE1_ACCESS_TOKEN`
- `SHOPIFY_STORE2_URL`
- `SHOPIFY_STORE2_ACCESS_TOKEN`
- etc.

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** - they're already in `.gitignore`
2. **Use different access tokens** for each store
3. **Limit API permissions** to only what's needed (read orders)
4. **Rotate tokens regularly** for security
5. **Use descriptive store keys** that don't reveal sensitive information

---

## 🛠️ Advanced Multi-Store Patterns

### Option 1: By Business Unit
```env
SHOPIFY_RETAIL_URL=retail.myshopify.com
SHOPIFY_RETAIL_ACCESS_TOKEN=token_here

SHOPIFY_WHOLESALE_URL=wholesale.myshopify.com
SHOPIFY_WHOLESALE_ACCESS_TOKEN=token_here

SHOPIFY_INTERNATIONAL_URL=intl.myshopify.com
SHOPIFY_INTERNATIONAL_ACCESS_TOKEN=token_here
```

### Option 2: By Region
```env
SHOPIFY_US_URL=us-store.myshopify.com
SHOPIFY_US_ACCESS_TOKEN=token_here

SHOPIFY_EU_URL=eu-store.myshopify.com
SHOPIFY_EU_ACCESS_TOKEN=token_here

SHOPIFY_ASIA_URL=asia-store.myshopify.com
SHOPIFY_ASIA_ACCESS_TOKEN=token_here
```

### Option 3: By Brand
```env
SHOPIFY_BRANDX_URL=brandx.myshopify.com
SHOPIFY_BRANDX_ACCESS_TOKEN=token_here

SHOPIFY_BRANDY_URL=brandy.myshopify.com
SHOPIFY_BRANDY_ACCESS_TOKEN=token_here
```

---

## 📊 Response Format

Each call returns the store identifier along with the summary:

```json
{
  "summary": [
    {
      "Day": "2024-01-15",
      "New_or_re": "New",
      "Orders": 5,
      "Gross_sale": 500.0,
      "Discounts": 50.0,
      "Returns": 0.0,
      "Net_sales": 450.0,
      "Shipping_": 25.0,
      "Duties": 0.0,
      "Additional_": 0.0,
      "Taxes": 45.0,
      "Total_sales": 520.0,
      "Quantity_c": 10,
      "Quantity_r": 0,
      "Week_End": "2024-01-20",
      "Month_End": "2024-01-31"
    }
  ],
  "store": "STORE1"
}
```

This allows you to track which store the data came from and aggregate across multiple stores if needed.

---

## 🔄 Batch Processing Multiple Stores

For processing all stores at once, you could create a wrapper function:

```python
async def get_all_stores_orders():
    stores = ["STORE1", "STORE2", "MAIN", "PREMIUM"]
    results = {}
    
    for store in stores:
        try:
            result = await get_shopify_orders(store)
            if "summary" in result:
                results[store] = result["summary"]
            else:
                results[store] = {"error": result.get("error", "Unknown error")}
        except Exception as e:
            results[store] = {"error": str(e)}
    
    return results
``` 