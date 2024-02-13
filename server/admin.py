from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from wtforms.fields import TextAreaField
from werkzeug.utils import secure_filename
from flask_login import current_user
from flask import redirect, url_for
from .models import Product, Category, User
from .database import db
import os
from PIL import Image


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class ProductModelView(ModelView):
    column_list = ('id', 'name', 'price', 'category_id',
                   'image_url', 'description')
    form_columns = ('name', 'price', 'category_id', 'image_url', 'description')

    form_overrides = {
        'image_url': ImageUploadField,
        'description': TextAreaField
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

    def on_model_change(self, form, model, is_created):
        super(ProductModelView, self).on_model_change(form, model, is_created)
        image_field = form.image_url.data
        if image_field:
            image_path = os.path.join(self.form_args['image_url']['base_path'], model.image_url)
            self.compress_image(image_path)

    def compress_image(self, image_path, quality=50):
        if os.path.isfile(image_path):
            img = Image.open(image_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(image_path, 'JPEG', quality=quality, optimize=True)


class CategoryModelView(ModelView):
    column_list = ('id', 'name', 'slug')


def setup_admin(app):
    admin = Admin(app, name='RetroPC Dashboard',
                  index_view=CustomAdminIndexView(), template_mode='bootstrap3')
    admin.add_view(ProductModelView(Product, db.session))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(ModelView(User, db.session))
