
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = {}
next_id = 1

CATALOG_URL = "http://127.0.0.1:5001"


@app.route("/orders", methods=["POST"])
def create_order():
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if type(product_id) is not int or product_id < 1:
        return jsonify({"error": "Invalid product_id"}), 400

    if type(quantity) is not int or quantity < 1:
        return jsonify({"error": "Quantity must be positive"}), 400

    try:
        response = requests.get(
            f"{CATALOG_URL}/products/{product_id}",
            timeout=3
        )
    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Catalog service is unavailable"
        }), 503

    if response.status_code == 404:
        return jsonify({"error": "Product not found"}), 404

    if response.status_code != 200:
        return jsonify({
            "error": "Catalog service error"
        }), 503

    try:
        product = response.json()
        name = product["name"]
        price = product["price"]
    except (ValueError, KeyError, TypeError):
        return jsonify({
            "error": "Invalid catalog response"
        }), 503

    order = {
        "id": next_id,
        "product_id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "total": price * quantity
    }

    orders[next_id] = order
    next_id += 1

    return jsonify(order), 201


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = orders.get(order_id)

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)
