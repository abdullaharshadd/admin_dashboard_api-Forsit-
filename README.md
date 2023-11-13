# Project Name
Admin Dashboard API

## Overview
This project is basically a sample admin dashboard api for e-commerce.

# Install uvicorn
`pip3 install "uvicorn[standard]"`

## Install dependencies
`pip3 install -r requirements.txt`

## Running mysql
```
docker run -d \
  --name=mysql-container \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=store \
  -e MYSQL_USER=store \
  -e MYSQL_PASSWORD=store \
  -p 3306:3306 \
  mysql:8.0
```

## Run the server
1. `cd app && python3 -m uvicorn main:app --reload`
2. Access the API via `http://localhost:8000`.

## Installation and Setup

### Prerequisites
- Python (Any) I have used python 3.9.6
- Docker (If you do not want to use docker then install MySQL directly)
- FastAPI
- ORMs
- MySQL

## Database Schema
The application's database schema consists of three primary tables: Products, Sales, and Inventory.

## Products Table
* **Columns:**
    * `id` (Primary Key): Unique identifier for each product.
    * `name`: Name of the product.
    * `description`: Description or details of the product.
    * `price`: Price of the product.
* **Purpose:**
    * Stores information about individual products available for sale.
    * Acts as a catalog representing the product's attributes.

## Sales Table
* **Columns:**
    * `id` (Primary Key): Unique identifier for each sale record.
    * `product_id` (Foreign Key to Products Table): References the product sold.
    * `quantity`: Quantity of the product sold.
    * `revenue`: Revenue generated from the sale.
    * `sale_date`: Date of the sale.
* **Purpose:**
    * Records individual sales transactions, linking to the corresponding product.
    * Tracks the quantity sold and the revenue generated per transaction.

## Inventory Table
* **Columns:**
    * `id` (Primary Key): Unique identifier for each inventory entry.
    * `product_id` (Foreign Key to Products Table): References the product in inventory.
    * `quantity`: Quantity of the product available in stock.
    * `low_stock_alert`: Threshold indicating low stock for a product.
* **Purpose:**
    * Manages the stock levels of each product in inventory.
    * Indicates the available quantity and sets an alert for low stock.

## Relationships
* **Products to Sales:** One-to-Many
    * Each product can have multiple sales entries in the Sales table.
    * The `product_id` in Sales references the `id` in Products, establishing the relationship.
* **Products to Inventory:** One-to-One
    * Each product has an entry in the Inventory table.
    * The `product_id` in Inventory references the `id` in Products, indicating the related product.

## API Endpoints

### Products
- **Create Product:** `POST /products/`
- **Get All Products:** `GET /products/`
- **Get Product by ID:** `GET /products/{product_id}`
- **Update Product:** `PUT /products/{product_id}`
- **Delete Product:** `DELETE /products/{product_id}`

### Sales
- **Create Sale:** `POST /sales/`
- **Get All Sales:** `GET /sales/`
- **Get Sale by ID:** `GET /sales/{sale_id}`
- **Get Daily Revenue:** `GET /sales/revenue/daily`
- **Get Weekly Revenue:** `GET /sales/revenue/weekly`
- **Get Monthly Revenue:** `GET /sales/revenue/monthly`
- **Get Annual Revenue:** `GET /sales/revenue/annual`

### Inventory
- **Create Inventory:** `POST /inventory/`
- **Get Product Inventory:** `GET /inventory/{product_id}`
- **Update Inventory:** `PUT /inventory/{product_id}`
- **Delete Product Inventory:** `DELETE /inventory/inventory/{product_id}`

## Testing
For testing the api endpoints, run the api_tests.py using the following command inside the testing folder:
`python3 api_tests.py`

## License
No License, it is free to use.

## Contact
If you have any queries, please contact at abdullah.arshad.314@gmail.com
