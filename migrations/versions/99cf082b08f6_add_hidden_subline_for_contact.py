"""add hidden subline for contact

Revision ID: 99cf082b08f6
Revises: 07a2628ea3b1
Create Date: 2020-10-06 20:42:53.931197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99cf082b08f6'
down_revision = '07a2628ea3b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('static_elements', sa.Column('hidden_subline_contact', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('static_elements', 'hidden_subline_contact')
    # ### end Alembic commands ###