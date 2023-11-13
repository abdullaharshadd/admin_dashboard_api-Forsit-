import requests

BASE_URL = "http://localhost:8000"  # Update with the appropriate base URL

# Test Create Product endpoint
def test_create_product():
    endpoint = "/products/"
    payload = {
        "name": "Test Product",
        "description": "Description of test product",
        "price": 9.99
    }
    response = requests.post(BASE_URL + endpoint, json=payload)
    print(response.json())

# Test Get All Products endpoint
def test_get_all_products():
    endpoint = "/products/"
    response = requests.get(BASE_URL + endpoint)
    print(response.json())

# Test Get Product by ID endpoint
def test_get_product_by_id(product_id):
    endpoint = f"/products/{product_id}"
    response = requests.get(BASE_URL + endpoint)
    print(response.json())

# Test Update Product endpoint
def test_update_product(product_id):
    endpoint = f"/products/{product_id}"
    payload = {
        "name": "Updated Product Name",
        "price": 19.99
    }
    response = requests.put(BASE_URL + endpoint, json=payload)
    print(response.json())

# Test Delete Product endpoint
def test_delete_product(product_id):
    endpoint = f"/products/{product_id}"
    response = requests.delete(BASE_URL + endpoint)
    print(response.json())

# Test Create Sale endpoint
def test_create_sale():
    endpoint = "/sales/"
    payload = {
        "product_id": 1,  # Replace with a valid product ID
        "quantity": 5,
        "revenue": 49.99
    }
    response = requests.post(BASE_URL + endpoint, json=payload)
    print(response.json())

# Test Get Sale by ID endpoint
def test_get_sale_by_id(sale_id):
    endpoint = f"/sales/{sale_id}"
    response = requests.get(BASE_URL + endpoint)
    print(response.json())

# Test Create Inventory endpoint
def test_create_inventory():
    endpoint = "/inventory/"
    payload = {
        "product_id": 1,  # Replace with a valid product ID
        "quantity": 100,
        "low_stock_alert": 10
    }
    response = requests.post(BASE_URL + endpoint, json=payload)
    print(response.json())

# Test Get Product Inventory endpoint
def test_get_product_inventory(product_id):
    endpoint = f"/inventory/{product_id}"
    response = requests.get(BASE_URL + endpoint)
    print(response.json())

# Test Update Inventory endpoint
def test_update_inventory(product_id):
    endpoint = f"/inventory/{product_id}"
    payload = {
        "quantity": 120,
        "low_stock_alert": 15
    }
    response = requests.put(BASE_URL + endpoint, json=payload)
    print(response.json())

# Test Delete Product Inventory endpoint
def test_delete_inventory(product_id):
    endpoint = f"/inventory/inventory/{product_id}"
    response = requests.delete(BASE_URL + endpoint)
    print(response.json())

if __name__ == "__main__":
    # Perform tests for Products
    test_create_product()
    test_get_all_products()
    test_get_product_by_id(1)  # Replace 1 with a valid product ID
    test_update_product(1)  # Replace 1 with a valid product ID
    test_delete_product(1)  # Replace 1 with a valid product ID
    
    # Perform tests for Sales
    test_create_sale()
    test_get_sale_by_id(1)  # Replace 1 with a valid sale ID
    
    # Perform tests for Inventory
    test_create_inventory()
    test_get_product_inventory(1)  # Replace 1 with a valid product ID
    test_update_inventory(1)  # Replace 1 with a valid product ID
    #test_delete_inventory(1)  # Replace 1 with a valid product ID
