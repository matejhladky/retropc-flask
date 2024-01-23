import click
from flask.cli import with_appcontext
from .database import db
from .models import User, Product, Category

@click.group()
def cli():
    pass

@cli.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo("Initialized the database!")

@cli.command("seed-db")
@with_appcontext
def seed_db_command():
    if not User.query.first():
        user = User(username='admin', password='admin')
        db.session.add(user)

    if not Category.query.first():
        categories = [
            Category(name='Category #1', slug='category_1'),
            Category(name='Category #2', slug='category_2'),
            Category(name='Category #3', slug='category_3')
        ]
        db.session.add_all(categories)

    if not Product.query.first():
        products = [
            Product(name='product_1', price=10, category_id=1, image_url='product1.png'),
            Product(name='product_2', price=20, category_id=2, image_url='product2.png'),
        ]
        db.session.add_all(products)

    db.session.commit()
    click.echo("Finished seeding the database!")

def register_commands(app):
    app.cli.add_command(cli)
