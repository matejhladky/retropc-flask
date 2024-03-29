"""Fix is_sold default value #2

Revision ID: 9f796b966345
Revises: 88d5e83c7213
Create Date: 2024-02-27 16:59:38.592238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f796b966345'
down_revision = '88d5e83c7213'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('is_sold',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('is_sold',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
