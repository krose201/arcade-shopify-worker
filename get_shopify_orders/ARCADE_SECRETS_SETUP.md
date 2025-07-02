# Arcade Secrets Setup Guide for Shopify Orders

## 🔐 Why Use Arcade Secrets?

Arcade's secrets management is more secure than environment variables because:
- ✅ **Encrypted Storage**: Secrets are encrypted at rest
- ✅ **Access Control**: Only your tools can access the secrets
- ✅ **Audit Trail**: Track who accesses what secrets
- ✅ **No Local Files**: No `.env` files to accidentally commit
- ✅ **Production Ready**: Same system for dev and production

---

## 🚀 Setting Up Your Shopify Secrets

### Step 1: Access the Arcade Dashboard

1. Go to your **Arcade Dashboard**
2. Navigate to **Auth > Secrets** section
3. Click the **+ Add Secret** button

### Step 2: Add Required Secrets

#### For Single Store Setup:

**Secret 1: Store URL**
- **ID**: `SHOPIFY_STORE_URL`
- **Secret Value**: `yourstore.myshopify.com` (without https://)
- **Description**: `Shopify store URL for API access`

**Secret 2: Access Token**
- **ID**: `SHOPIFY_ACCESS_TOKEN`
- **Secret Value**: `shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Description**: `Shopify Admin API access token`

#### For Multi-Store Setup:

Add additional secrets for each store using the pattern `SHOPIFY_{STORE_KEY}_URL` and `SHOPIFY_{STORE_KEY}_ACCESS_TOKEN`:

**Store 1 Secrets:**
- **ID**: `SHOPIFY_STORE1_URL`
- **Secret Value**: `store1.myshopify.com`
- **Description**: `Store 1 URL`

- **ID**: `SHOPIFY_STORE1_ACCESS_TOKEN`
- **Secret Value**: `shpat_store1_token_here`
- **Description**: `Store 1 access token`

**Store 2 Secrets:**
- **ID**: `SHOPIFY_STORE2_URL`
- **Secret Value**: `store2.myshopify.com`
- **Description**: `Store 2 URL`

- **ID**: `SHOPIFY_STORE2_ACCESS_TOKEN`
- **Secret Value**: `shpat_store2_token_here`
- **Description**: `Store 2 access token`

---

## 🏪 Multi-Store Naming Patterns

### Recommended Store Key Patterns:

#### By Business Unit:
```
SHOPIFY_RETAIL_URL / SHOPIFY_RETAIL_ACCESS_TOKEN
SHOPIFY_WHOLESALE_URL / SHOPIFY_WHOLESALE_ACCESS_TOKEN
SHOPIFY_B2B_URL / SHOPIFY_B2B_ACCESS_TOKEN
```

#### By Region:
```
SHOPIFY_US_URL / SHOPIFY_US_ACCESS_TOKEN
SHOPIFY_EU_URL / SHOPIFY_EU_ACCESS_TOKEN
SHOPIFY_ASIA_URL / SHOPIFY_ASIA_ACCESS_TOKEN
```

#### By Brand:
```
SHOPIFY_BRANDX_URL / SHOPIFY_BRANDX_ACCESS_TOKEN
SHOPIFY_BRANDY_URL / SHOPIFY_BRANDY_ACCESS_TOKEN
SHOPIFY_BRANDZ_URL / SHOPIFY_BRANDZ_ACCESS_TOKEN
```

---

## 🔑 How to Get Shopify Access Tokens

### Step 1: Create a Private App

1. In your Shopify admin, go to **Apps > App and sales channel settings**
2. Click **Develop apps**
3. Click **Create an app**
4. Name your app (e.g., "Arcade Orders Tool")

### Step 2: Configure API Access

1. Click **Configure Admin API scopes**
2. Enable the following scopes:
   - `read_orders` - Required for fetching orders
   - `read_customers` - Required for customer data (new vs returning)
3. Click **Save**

### Step 3: Generate Access Token

1. Click **API credentials** tab
2. Click **Install app**
3. Copy the **Admin API access token** (starts with `shpat_`)
4. Store this securely - you won't see it again!

### Step 4: Get Your Store URL

Your store URL is: `{your-store-name}.myshopify.com`

---

## 🛠️ Usage Examples

### Single Store (Default):
```python
# Uses SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN secrets
result = await get_shopify_orders(context)
# Returns: {"summary": [...], "store": "default"}
```

### Multi-Store:
```python
# Uses SHOPIFY_STORE1_URL and SHOPIFY_STORE1_ACCESS_TOKEN secrets
result = await get_shopify_orders(context, "STORE1")
# Returns: {"summary": [...], "store": "STORE1"}

# Uses SHOPIFY_RETAIL_URL and SHOPIFY_RETAIL_ACCESS_TOKEN secrets
result = await get_shopify_orders(context, "RETAIL")
# Returns: {"summary": [...], "store": "RETAIL"}
```

---

## 🧪 Testing Your Setup

After adding your secrets, test the tool:

```python
# This should work if secrets are configured correctly
result = await get_shopify_orders(context)

# Check for errors
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Success! Found {len(result['summary'])} daily summaries")
    print(f"Store: {result['store']}")
```

---

## 🔒 Security Best Practices

### 1. Token Permissions
- Only grant the minimum required scopes (`read_orders`, `read_customers`)
- Never use tokens with `write` permissions unless absolutely necessary

### 2. Token Rotation
- Rotate access tokens every 90 days
- Update secrets in Arcade Dashboard when rotating

### 3. Store Separation
- Use different access tokens for each store
- Never share tokens between stores

### 4. Monitoring
- Monitor token usage in Shopify admin
- Set up alerts for unusual API activity

---

## 🚨 Troubleshooting

### Common Error Messages:

**"Missing Shopify secrets"**
- Solution: Add `SHOPIFY_STORE_URL` and `SHOPIFY_ACCESS_TOKEN` secrets

**"Missing Shopify secrets for store 'STORE1'"**
- Solution: Add `SHOPIFY_STORE1_URL` and `SHOPIFY_STORE1_ACCESS_TOKEN` secrets

**"[Shopify] 401 Unauthorized"**
- Solution: Check your access token is valid and has correct permissions

**"[Shopify] 404 Not Found"**
- Solution: Verify your store URL is correct (no https://, just the domain)

### Debugging Steps:

1. **Verify Secret Names**: Check exact spelling and capitalization
2. **Test Token**: Use Shopify's API explorer to test your token
3. **Check Permissions**: Ensure your app has `read_orders` scope
4. **Validate Store URL**: Should be `store.myshopify.com` format

---

## 📊 Response Format

Each successful call returns:

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

The `store` field helps you track which store the data came from when using multiple stores.

---

## 🎯 Migration from Environment Variables

If you were previously using environment variables, here's how to migrate:

### Old Way (Environment Variables):
```env
SHOPIFY_STORE_URL=store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_token
```

### New Way (Arcade Secrets):
1. Add `SHOPIFY_STORE_URL` secret with value `store.myshopify.com`
2. Add `SHOPIFY_ACCESS_TOKEN` secret with value `shpat_token`
3. Remove `.env` file (no longer needed)
4. Tool automatically uses secrets instead of environment variables

**No code changes required!** The tool signature remains the same, just more secure. 🔐 