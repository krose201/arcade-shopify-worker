# tests/test_get_shopify_orders.py
import pytest
import os
from unittest.mock import patch, AsyncMock
import httpx

from arcade_get_shopify_orders.tools.shopify_orders import get_shopify_orders, summarize_orders, get_period_ends


def test_get_period_ends():
    """Test the period ends calculation"""
    result = get_period_ends("2024-01-15")  # Monday
    assert "weekEnd" in result
    assert "monthEnd" in result
    assert result["monthEnd"] == "2024-01-31"


def test_summarize_orders():
    """Test order summarization with sample data"""
    sample_orders = [
        {
            "created_at": "2024-01-15T10:00:00Z",
            "total_price": "100.00",
            "total_discounts": "10.00",
            "current_subtotal_price": "90.00",
            "total_tax": "9.00",
            "current_total_price": "99.00",
            "customer": {"orders_count": 1},
            "line_items": [{"quantity": 2}],
            "total_shipping_price_set": {
                "shop_money": {"amount": "5.00"}
            }
        }
    ]
    
    result = summarize_orders(sample_orders)
    assert len(result) == 1
    assert result[0]["Day"] == "2024-01-15"
    assert result[0]["New_or_re"] == "New"
    assert result[0]["Orders"] == 1
    assert result[0]["Gross_sale"] == 100.0
    assert result[0]["Quantity_c"] == 2


@pytest.mark.asyncio
async def test_get_shopify_orders_missing_credentials():
    """Test error handling when credentials are missing"""
    with patch.dict(os.environ, {}, clear=True):
        result = await get_shopify_orders()
        assert "error" in result
        assert "Missing Shopify credentials" in result["error"]


@pytest.mark.asyncio
async def test_get_shopify_orders_success():
    """Test successful order fetching and summarization"""
    mock_orders = [
        {
            "created_at": "2024-01-15T10:00:00Z",
            "total_price": "100.00",
            "total_discounts": "0.00",
            "current_subtotal_price": "100.00",
            "total_tax": "10.00",
            "current_total_price": "110.00",
            "customer": {"orders_count": 1},
            "line_items": [{"quantity": 1}],
            "total_shipping_price_set": {
                "shop_money": {"amount": "0.00"}
            }
        }
    ]
    
    with patch.dict(os.environ, {
        "SHOPIFY_STORE_URL": "test-store.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "test-token"
    }):
        with patch("arcade_get_shopify_orders.tools.shopify_orders.fetch_shopify_orders") as mock_fetch:
            mock_fetch.return_value = mock_orders
            
            result = await get_shopify_orders()
            
            assert "summary" in result
            assert len(result["summary"]) == 1
            assert result["summary"][0]["Orders"] == 1


@pytest.mark.asyncio
async def test_get_shopify_orders_api_error():
    """Test error handling when Shopify API returns an error"""
    with patch.dict(os.environ, {
        "SHOPIFY_STORE_URL": "test-store.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "invalid-token"
    }):
        with patch("arcade_get_shopify_orders.tools.shopify_orders.fetch_shopify_orders") as mock_fetch:
            mock_fetch.side_effect = Exception("[Shopify] 401 Unauthorized: Invalid access token")
            
            result = await get_shopify_orders()
            
            assert "error" in result
            assert "[Shopify] 401" in result["error"]