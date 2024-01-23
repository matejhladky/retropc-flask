from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api
from ..models import Product

product_bp = Blueprint('products', __name__)
product_api = Api(product_bp)

class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return make_response(jsonify(product.serialize(True)), 200)
            return {"error": "Product not found"}, 404
        else:
            products = Product.query.all()
            return make_response(jsonify([product.serialize(True) for product in products]), 200)

product_api.add_resource(ProductResource, '/', '/<int:product_id>')
