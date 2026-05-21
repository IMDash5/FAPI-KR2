from fastapi import FastAPI
from typing import Optional


app = FastAPI()

sample_products = [
  {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
  },
  {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
  },
  {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
  },
  {
    "product_id": 101,
    "name": "Headphones",
    "category": "Electronics",
    "price": 199.99
  },
  {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
  }
]

@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product


@app.get("/products/search")
def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: Optional[int] = 10
):
    results = []

    for product in sample_products:
        if keyword.lower() in product["name"].lower():

            if category is None or product["category"].lower() == category.lower():
                results.append(product)
                
    return results[:limit]