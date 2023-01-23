"""not unique anymore

Revision ID: 36de2dbe8387
Revises: 6787ccb8b4ad
Create Date: 2023-01-18 01:11:54.006953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36de2dbe8387'
down_revision = '6787ccb8b4ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_dishes_title', table_name='dishes')
    op.create_index(op.f('ix_dishes_title'), 'dishes', ['title'], unique=False)
    op.drop_index('ix_submenus_title', table_name='submenus')
    op.create_index(op.f('ix_submenus_title'), 'submenus', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_submenus_title'), table_name='submenus')
    op.create_index('ix_submenus_title', 'submenus', ['title'], unique=False)
    op.drop_index(op.f('ix_dishes_title'), table_name='dishes')
    op.create_index('ix_dishes_title', 'dishes', ['title'], unique=False)
    # ### end Alembic commands ###
