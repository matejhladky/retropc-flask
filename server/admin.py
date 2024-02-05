from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from wtforms import Form, fields
from wtforms_sqlalchemy.fields import QuerySelectField
from werkzeug.utils import secure_filename
from flask_login import current_user
from flask import redirect, url_for
from .models import Product, Category, User
from .database import db

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class ProductModelView(ModelView):
    column_list = ('id', 'name', 'price', 'category_id', 'image_url', 'description')
    form_columns = ('name', 'price', 'category_id', 'image_url', 'description')

    form_overrides = {
        'image_url': ImageUploadField
    }

    form_args = {
        'image_url': {
            'label': 'Image',
            'base_path': '/var/data',
            'relative_path': '',
            'allow_overwrite': False,
            'namegen': lambda model, file_data: secure_filename(file_data.filename),
            'thumbnail_size': (100, 100, True)
        }
    }

    def _list_thumbnail(view, context, model, name):
        if not model.image_url:
            return ''
        
        return f'{model.image_url}'
    
    column_formatters = {
        'image_url': _list_thumbnail
    }


class CategoryModelView(ModelView):
    column_list = ('id', 'name', 'slug')


def setup_admin(app):
    admin = Admin(app, name='RetroPC Dashboard', index_view=CustomAdminIndexView(), template_mode='bootstrap3')
    admin.add_view(ProductModelView(Product, db.session))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(ModelView(User, db.session))

