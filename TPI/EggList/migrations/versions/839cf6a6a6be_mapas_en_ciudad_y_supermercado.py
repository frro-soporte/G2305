"""Mapas en ciudad y supermercado

Revision ID: 839cf6a6a6be
Revises: b64825e13094
Create Date: 2024-02-06 17:07:08.933942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '839cf6a6a6be'
down_revision = 'b64825e13094'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ciudades', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position_x', sa.Double(), nullable=False))
        batch_op.add_column(sa.Column('position_y', sa.Double(), nullable=False))
        batch_op.add_column(sa.Column('min_zoom', sa.Integer(), nullable=False))

    with op.batch_alter_table('supermercados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position_x', sa.Double(), nullable=False))
        batch_op.add_column(sa.Column('position_y', sa.Double(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('supermercados', schema=None) as batch_op:
        batch_op.drop_column('position_y')
        batch_op.drop_column('position_x')

    with op.batch_alter_table('ciudades', schema=None) as batch_op:
        batch_op.drop_column('min_zoom')
        batch_op.drop_column('position_y')
        batch_op.drop_column('position_x')

    # ### end Alembic commands ###