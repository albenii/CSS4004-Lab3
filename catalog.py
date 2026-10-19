
from flask import Flask, jsonify, request

app = Flask(__name__)

products = {}
next_id = 1


@app.route("/products", methods=["POST"])
def create_product():
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Invalid product name"}), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or not (0 < price < float("inf")):
        return jsonify({"error": "Price must be positive"}), 400

    product = {
        "id": next_id,
        "name": name.strip(),
        "price": price
    }

    products[next_id] = product
    next_id += 1

    return jsonify(product), 201


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = products.get(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
