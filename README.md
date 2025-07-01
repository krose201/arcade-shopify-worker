# Arcade Shopify Worker

A simple API service to fetch Shopify orders from any storefront and expose them via a `/orders` endpoint with daily summary columns matching your desired report.

## Setup

1. **Copy `.env.example` to `.env` and fill in your Shopify store credentials.**

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the worker locally:**
   ```
   npm start
   ```

4. **Test your API:**
   ```
   curl "http://localhost:3000/orders?limit=5&status=any"
   ```

5. **Deploy to Railway:**
   - Connect your GitHub repo to Railway and deploy.
   - Set your environment variables in Railway’s dashboard (`SHOPIFY_STORE_URL`, `SHOPIFY_ACCESS_TOKEN`).
   - Railway will give you a public URL like `https://your-app.up.railway.app/orders`.

6. **Configure Arcade.dev or any service to pull from**  
   Use:  
   ```
   https://your-app.up.railway.app/orders
   ```
   as the data source.

## Output

- The `/orders` endpoint returns only the summary columns matching your screenshot: Day, New_or_re, Orders, Gross_sale, Discounts, Returns, Net_sales, Shipping_, Duties, Additional_, Taxes, Total_sales, Quantity_c, Quantity_r, Week_End, Month_End.

---

**No Arcade API key or endpoint is required for this "pull" model.**
