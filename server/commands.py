import click
from flask.cli import with_appcontext
from .database import db
from .models import User, Product, Category

DEFAULT_PROD_DESC = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

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
            Product('product_1', 10, 1, 'product1.png', DEFAULT_PROD_DESC),
            Product('product_2', 20, 2, 'product1.png', DEFAULT_PROD_DESC),
            Product('product_3', 30, 3, 'product1.png', DEFAULT_PROD_DESC),
            Product('product_4', 40, 1, 'product1.png', DEFAULT_PROD_DESC),
            Product('product_5', 50, 2, 'product1.png', DEFAULT_PROD_DESC),
            Product('product_6', 60, 3, 'product1.png', DEFAULT_PROD_DESC)
        ]
        db.session.add_all(products)

    db.session.commit()
    click.echo("Finished seeding the database!")

def register_commands(app):
    app.cli.add_command(cli)
