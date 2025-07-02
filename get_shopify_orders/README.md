# Shopify Orders Arcade Tool

This tool fetches and summarizes Shopify orders data, supporting both single and multi-store configurations using **Arcade's secure secrets management**.

## 🔐 **Recommended Setup: Arcade Secrets**

**For the most secure setup, use Arcade's secrets management:**

👉 **[Complete Arcade Secrets Setup Guide](./ARCADE_SECRETS_SETUP.md)** 👈

### Quick Start with Secrets:
1. Go to your Arcade Dashboard → Auth → Secrets
2. Add these secrets:
   - `SHOPIFY_STORE_URL`: `yourstore.myshopify.com`
   - `SHOPIFY_ACCESS_TOKEN`: `shpat_your_token_here`
3. Your tool is ready to use! 🎉

---

## 🛠️ Installation

```bash
cd get_shopify_orders
uv sync
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Type checking
make type-check

# Linting
make lint
```

## 📊 Usage

### Single Store:
```python
# Uses SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN secrets
result = await get_shopify_orders(context)
```

### Multi-Store:
```python
# Uses SHOPIFY_STORE1_URL and SHOPIFY_STORE1_ACCESS_TOKEN secrets
result = await get_shopify_orders(context, "STORE1")
```

## 📋 Response Format

Returns daily order summaries with:
- Order counts (new vs returning customers)
- Sales data (gross, net, discounts, returns)
- Shipping, taxes, and additional fees
- Quantity sold and returned
- Week/month end dates for reporting

## 🔧 Alternative: Environment Variables

If you prefer environment variables over Arcade secrets:

👉 **[Environment Variables Setup Guide](./MULTI_STORE_SETUP.md)**

**Note**: Arcade secrets are more secure and recommended for production use.

## 🚨 Troubleshooting

- **"Missing Shopify secrets"**: Add required secrets in Arcade Dashboard
- **"401 Unauthorized"**: Check your access token permissions
- **"404 Not Found"**: Verify your store URL format

See the [Arcade Secrets Setup Guide](./ARCADE_SECRETS_SETUP.md) for detailed troubleshooting steps.

## 🔒 Security

- ✅ Uses Arcade's encrypted secrets management
- ✅ Minimum required API permissions (`read_orders`, `read_customers`)
- ✅ Separate tokens for each store
- ✅ No sensitive data in code or config files