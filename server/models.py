import base64

from flask_login import UserMixin
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .database import db


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    image_url = Column(String(255))
    description = Column(String(1000))

    def __init__(self, name, price, category_id, image_url, description):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.image_url = image_url
        self.description = description

    def serialize(self, include_image=True):
        data = {
            'product_id': self.id,
            'name': self.name,
            'price': self.price,
            'category_id': self.category_id,
            'description': self.description
        }

        if include_image and self.image_url:
            with open('/var/data/' + self.image_url, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            data['image'] = encoded_image

        return data


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def serialize(self):
        return {
            'category_id': self.id,
            'name': self.name,
            'slug': self.slug
        }

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
