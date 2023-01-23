"""return to ununique

Revision ID: 676d0d47988f
Revises: 6e02f281b722
Create Date: 2023-01-18 02:54:01.044123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '676d0d47988f'
down_revision = '6e02f281b722'
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