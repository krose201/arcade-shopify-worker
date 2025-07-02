# tests/test_get_shopify_orders.py
import pytest
import os
from unittest.mock import patch, AsyncMock, MagicMock
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


def test_summarize_orders_floating_point_rounding():
    """Test that monetary values are properly rounded to 2 decimal places"""
    sample_orders = [
        {
            "created_at": "2024-01-15T10:00:00Z",
            "total_price": "100.333333",  # Should round to 100.33
            "total_discounts": "10.666666",  # Should round to 10.67
            "current_subtotal_price": "89.999999",  # Should round to 90.00
            "total_tax": "9.123456",  # Should round to 9.12
            "current_total_price": "99.111111",  # Should round to 99.11
            "customer": {"orders_count": 1},
            "line_items": [{"quantity": 2}],
            "total_shipping_price_set": {
                "shop_money": {"amount": "5.555555"}  # Should round to 5.56
            }
        }
    ]
    
    result = summarize_orders(sample_orders)
    assert len(result) == 1
    
    summary = result[0]
    # Check that all monetary values are properly rounded to 2 decimal places
    assert summary["Gross_sale"] == 100.33
    assert summary["Discounts"] == 10.67
    assert summary["Net_sales"] == 90.00
    assert summary["Taxes"] == 9.12
    assert summary["Total_sales"] == 99.11
    assert summary["Shipping_"] == 5.56
    
    # Verify no floating point precision errors
    assert str(summary["Gross_sale"]) == "100.33"
    assert str(summary["Discounts"]) == "10.67"
    assert str(summary["Taxes"]) == "9.12"


@pytest.mark.asyncio
async def test_get_shopify_orders_missing_credentials():
    """Test error handling when secrets are missing"""
    mock_context = MagicMock()
    mock_context.get_secret.side_effect = Exception("Secret not found")
    
    result = await get_shopify_orders(mock_context)
    assert "error" in result
    assert "Missing Shopify secrets" in result["error"]
    assert "Arcade Dashboard" in result["error"]


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
    
    mock_context = MagicMock()
    mock_context.get_secret.side_effect = lambda key: {
        "SHOPIFY_STORE_URL": "test-store.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "test-token"
    }[key]
    
    with patch("arcade_get_shopify_orders.tools.shopify_orders.fetch_shopify_orders") as mock_fetch:
        mock_fetch.return_value = mock_orders
        
        result = await get_shopify_orders(mock_context)
        
        assert "summary" in result
        assert "store" in result
        assert result["store"] == "default"
        assert len(result["summary"]) == 1
        assert result["summary"][0]["Orders"] == 1


@pytest.mark.asyncio
async def test_get_shopify_orders_api_error():
    """Test error handling when Shopify API returns an error"""
    mock_context = MagicMock()
    mock_context.get_secret.side_effect = lambda key: {
        "SHOPIFY_STORE_URL": "test-store.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "invalid-token"
    }[key]
    
    with patch("arcade_get_shopify_orders.tools.shopify_orders.fetch_shopify_orders") as mock_fetch:
        mock_fetch.side_effect = Exception("[Shopify] 401 Unauthorized: Invalid access token")
        
        result = await get_shopify_orders(mock_context)
        
        assert "error" in result
        assert "[Shopify] 401" in result["error"]


@pytest.mark.asyncio
async def test_get_shopify_orders_multi_store_success():
    """Test successful multi-store order fetching"""
    mock_orders = [
        {
            "created_at": "2024-01-15T10:00:00Z",
            "total_price": "200.00",
            "total_discounts": "0.00",
            "current_subtotal_price": "200.00",
            "total_tax": "20.00",
            "current_total_price": "220.00",
            "customer": {"orders_count": 2},
            "line_items": [{"quantity": 3}],
            "total_shipping_price_set": {
                "shop_money": {"amount": "10.00"}
            }
        }
    ]
    
    mock_context = MagicMock()
    mock_context.get_secret.side_effect = lambda key: {
        "SHOPIFY_STORE1_URL": "store1.myshopify.com",
        "SHOPIFY_STORE1_ACCESS_TOKEN": "store1-token"
    }[key]
    
    with patch("arcade_get_shopify_orders.tools.shopify_orders.fetch_shopify_orders") as mock_fetch:
        mock_fetch.return_value = mock_orders
        
        result = await get_shopify_orders(mock_context, "STORE1")
        
        assert "summary" in result
        assert "store" in result
        assert result["store"] == "STORE1"
        assert len(result["summary"]) == 1
        assert result["summary"][0]["Orders"] == 1
        assert result["summary"][0]["New_or_re"] == "Returning"


@pytest.mark.asyncio
async def test_get_shopify_orders_multi_store_missing_credentials():
    """Test error handling when multi-store secrets are missing"""
    mock_context = MagicMock()
    mock_context.get_secret.side_effect = Exception("Secret not found")
    
    result = await get_shopify_orders(mock_context, "STORE1")
    assert "error" in result
    assert "Missing Shopify secrets for store 'STORE1'" in result["error"]
    assert "SHOPIFY_STORE1_URL" in result["error"]
    assert "Arcade Dashboard" in result["error"]