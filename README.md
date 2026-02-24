# 🛒 FastAPI E-Commerce Backend

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production--Ready-009688)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A structured, validation-driven E-Commerce Backend API built using **FastAPI** and **Pydantic v2**, demonstrating clean architecture, nested schemas, strict validation rules, and professional API design.

---

## 🔥 Key Highlights

* Clean modular backend architecture
* Strict request validation using Pydantic v2
* Nested schemas (Seller, Dimensions)
* Custom field validators (SKU format, email domain restriction)
* URL validation for image resources
* Automatic timestamp generation
* Filter & sorting support
* Proper HTTP status handling (404, 422, 201)
* Auto-generated OpenAPI documentation

---

## 🏗 Architecture Overview

```text
Client → FastAPI Router → Service Layer → JSON Data Store
                ↓
           Pydantic Models
         (Validation Layer)
```

The project follows separation of concerns:

* **Schema Layer** → Request/Response validation
* **Service Layer** → Business logic
* **Data Layer** → JSON persistence (replaceable with DB)

---

## 📁 Project Structure

```
fast-api-ecom/
│
├── app/
│   ├── main.py
│   ├── schema/
│   │   └── product.py
│   ├── services/
│   │   └── products.py
│   └── data/
│       └── products.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧩 Data Model Design

### Product Model

* `id` → UUID
* `sku` → Custom validated (must end with 3 digits)
* `price` → Must be > 0
* `rating` → Between 0 and 5
* `currency` → Literal enforced ("INR")
* `image_urls` → List of validated URLs
* `created_at` → Auto-generated timestamp

### Nested Models

**Seller**

* seller_id → UUID
* email → Validated EmailStr
* website → AnyUrl
* Domain restriction validator

**Dimensions**

* length, width, height (cm)

---

## 🌐 API Endpoints

### 1️⃣ Root

```
GET /
```

Response:

```json
{
  "message": "Welcome to FastAPI"
}
```

---

### 2️⃣ Get All Products

```
GET /products
```

Optional Query Params:

* `?name=iphone`
* `?sort_price=true`
* `?order=asc | desc`

---

### 3️⃣ Get Product By ID

```
GET /products/{product_id}
```

Returns 404 if not found.

---

### 4️⃣ Create Product

```
POST /products
```

Returns:

* `201 Created` on success
* `422 Unprocessable Entity` on validation failure

Example Validation Error:

```json
{
  "detail": [
    {
      "msg": "Invalid SKU must end with 3-digit number"
    }
  ]
}
```

---

## 🛠 Installation & Setup

Clone the repository:

```bash
git clone https://github.com/AJ58282/fast-api-ecom.git
cd fast-api-ecom
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

---

## 📘 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🧠 Engineering Concepts Demonstrated

* Pydantic v2 field validators
* Custom schema validation
* Nested model composition
* Literal type enforcement
* Clean exception handling
* Git best practices
* Proper repository hygiene

---

## 🚀 Future Enhancements

* Replace JSON with PostgreSQL
* Add SQLAlchemy ORM
* Implement authentication (JWT)
* Add pagination & caching
* Containerize with Docker
* Deploy to cloud (Render / Railway)
* Add CI/CD with GitHub Actions

---

## 👨‍💻 Author

Adith Jose
GitHub: [https://github.com/AJ58282](https://github.com/AJ58282)
