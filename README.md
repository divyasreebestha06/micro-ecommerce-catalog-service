# 🛍️ micro-ecommerce-catalog-service

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Microservice](https://img.shields.io/badge/Architecture-Microservice-orange?style=for-the-badge)](app/)

Microservice Product Catalog & Inventory Service with category filtering, search, and stock checks.

## Features
- **Categorical Indexing:** Fast filtering by department and category.
- **Stock Boundary Protection:** Atomic quantity decrement preventing overselling.
- **RESTful Endpoints:** Full Swagger/OpenAPI specification.

## Endpoints
- `POST /products`: Add a product to the catalog.
- `GET /products?category=...&q=...`: Search products.
- `POST /products/{id}/stock?delta=-1`: Reserve or replenish stock.
