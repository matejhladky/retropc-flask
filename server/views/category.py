from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from ..models import Category, Product

category_bp = Blueprint('categories', __name__)
category_api = Api(category_bp)

class CategoryResource(Resource):
    def get(self, category_slug=None):
        if category_slug:
            category = Category.query.filter_by(slug=category_slug).first()
            if category:
                products_in_category = Product.query.filter(Product.category.has(slug=category_slug)).all()
                return jsonify([product.serialize() for product in products_in_category])
            return {"error": "Category not found"}, 404
        else:
            categories = Category.query.all()
            return jsonify([category.serialize() for category in categories])

category_api.add_resource(CategoryResource, '/', '/<string:category_slug>')
