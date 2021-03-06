"""empty message

Revision ID: e5cfa6782b6a
Revises: 493467d07285
Create Date: 2018-06-11 18:50:59.983404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5cfa6782b6a'
down_revision = '493467d07285'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events_db', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_db', 'description')
    # ### end Alembic commands ###
