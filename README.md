**Lab Work 3 — REST API and Two Services**

**Description**

In this laboratory work, I created two REST API services using Python and Flask.

- Service A (`catalog.py`) manages products.
- Service B (`orders.py`) manages orders.

The services communicate using HTTP requests.

Data is stored in memory without a database.

**Files**

- `catalog.py` — Product Catalog Service
- `orders.py` — Order Service
- `requirements.txt` — Python dependencies
- `README.md` — Instructions and test results

**Installation**

Install the required libraries:

```bash
pip install -r requirements.txt
```

**How to Run**

Start Service A in the first terminal:

```bash
python catalog.py
```

Service A runs on port 5001.

Start Service B in the second terminal:

```bash
python orders.py
```

Service B runs on port 5002.

**API Endpoints**

Service A:

- `POST /products` — Create a product.
- `GET /products/{id}` — Get a product by ID.

Service B:

- `POST /orders` — Create an order.
- `GET /orders/{id}` — Get a saved order.

**Test 1 — Both Services Working**

First, I created a product:

```bash
curl -X POST http://127.0.0.1:5001/products -H "Content-Type: application/json" -d '{"name":"Mouse","price":5000}'
```

Then I created an order:

```bash
curl -i -X POST http://127.0.0.1:5002/orders -H "Content-Type: application/json" -d '{"product_id":1,"quantity":3}'
```

Result: `201 CREATED`

```json
{
  "id": 1,
  "name": "Mouse",
  "price": 5000,
  "product_id": 1,
  "quantity": 3,
  "total": 15000
}
```

Service B requested the product information from Service A and calculated the total price.

**[Insert Screenshot 1 — Product creation]**

**[Insert Screenshot 2 — Order creation]**

**Test 2 — Catalog Service Failure**

I stopped Service A using `Ctrl + C`.

Then I tried to create another order:

```bash
curl -i -X POST http://127.0.0.1:5002/orders -H "Content-Type: application/json" -d '{"product_id":1,"quantity":2}'
```

Result: `503 SERVICE UNAVAILABLE`

```json
{
  "error": "Catalog service is unavailable"
}
```

Service B handled the error and continued running.

**[Insert Screenshot 3 — 503 Service Unavailable]**

**Test 3 — Getting a Saved Order**

While Service A was still stopped, I requested the previously created order:

```bash
curl -i http://127.0.0.1:5002/orders/1
```

Result: `200 OK`

```json
{
  "id": 1,
  "name": "Mouse",
  "price": 5000,
  "product_id": 1,
  "quantity": 3,
  "total": 15000
}
```

The order was returned successfully because Service B stores order information in its own memory.

**[Insert Screenshot 4 — Saved order with Service A stopped]**

**Timeout**

Service B uses `timeout=3` when sending HTTP requests to Service A.

This prevents Service B from waiting indefinitely for a response from the catalog service.

**AI Usage**

I used ChatGPT to help write the Python code, explain HTTP requests and timeout handling, and prepare testing commands and documentation. I ran and tested both services myself.

**Conclusion**

In this laboratory work, I learned how to create two independent REST API services using Flask and how they communicate through HTTP.

I also learned how to handle service failures using HTTP status 503 and how to retrieve saved data when another service is unavailable.

All three required tests were completed successfully.
