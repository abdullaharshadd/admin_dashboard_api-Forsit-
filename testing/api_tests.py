import asyncio
import os
import sys
import requests
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.authentication.auth import get_access_token

BASE_URL = "http://localhost:8000"  # Update with the appropriate base URL

async def main():
    BEARER_TOKEN = await get_access_token()
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    # Perform tests for Products
    test_create_product(headers)
    test_get_all_products(headers)
    test_get_product_by_id(1, headers)  # Replace 1 with a valid product ID
    test_update_product(1, headers)  # Replace 1 with a valid product ID
    test_delete_product(1, headers)  # Replace 1 with a valid product ID

    # Perform tests for Sales
    #test_create_sale(headers)
    test_get_sale_by_id(1, headers)  # Replace 1 with a valid sale ID

    # # Perform tests for Inventory
    test_create_inventory(headers)
    test_get_product_inventory(1, headers)  # Replace 1 with a valid product ID
    test_update_inventory(1, headers)  # Replace 1 with a valid product ID
    test_delete_inventory(1, headers)  # Replace 1 with a valid product ID

def test_create_product(headers):
    endpoint = "/products/"
    payload = {
        "name": "Test Product",
        "description": "Description of test product",
        "price": 9.99
    }
    response = requests.post(BASE_URL + endpoint, json=payload, headers=headers)
    print(response.json())

def test_get_all_products(headers):
    endpoint = "/products/"
    response = requests.get(BASE_URL + endpoint, headers=headers)
    print(response.json())

def test_get_product_by_id(product_id, headers):
    endpoint = f"/products/{product_id}"
    response = requests.get(BASE_URL + endpoint, headers=headers)
    print(response.json())

def test_update_product(product_id, headers):
    endpoint = f"/products/{product_id}"
    payload = {
        "name": "Updated Product Name",
        "price": 19.99,
        "description" : "Updated description"
    }
    response = requests.put(BASE_URL + endpoint, json=payload, headers=headers)
    print(response.json())

def test_delete_product(product_id, headers):
    endpoint = f"/products/{product_id}"
    response = requests.delete(BASE_URL + endpoint, headers=headers)
    print(response.json())

def test_create_sale(headers):
    endpoint = "/sales/"

    payload = {
        "product_id": 1,  # Replace with a valid product ID
        "quantity_sold": 5,
        "revenue": 49.99,
        "sale_date": datetime.date(2023, 1, 25),
    }
    response = requests.post(BASE_URL + endpoint, json=payload, headers=headers)
    print(response.json())

def test_get_sale_by_id(sale_id, headers):
    endpoint = f"/sales/{sale_id}"
    response = requests.get(BASE_URL + endpoint, headers=headers)
    print(response.json())

def test_create_inventory(headers):
    endpoint = "/inventory/"
    payload = {
        "product_id": 1,  # Replace with a valid product ID
        "quantity": 100,
        "low_stock_alert": False
    }
    response = requests.post(BASE_URL + endpoint, json=payload, headers=headers)
    print(response.json())

def test_get_product_inventory(product_id, headers):
    endpoint = f"/inventory/{product_id}"
    response = requests.get(BASE_URL + endpoint, headers=headers)
    print(response.json())

def test_update_inventory(product_id, headers):
    endpoint = f"/inventory/{product_id}"
    payload = {
        "product_id": 303,
        "quantity": 120,
        "low_stock_alert": False
    }
    response = requests.put(BASE_URL + endpoint, json=payload, headers=headers)
    print(response.json())

# Test Delete Product Inventory endpoint
def test_delete_inventory(product_id, headers):
    endpoint = f"/inventory/inventory/{product_id}"
    response = requests.delete(BASE_URL + endpoint, headers=headers)
    print(response.json())

if __name__ == "__main__":
    asyncio.run(main())
