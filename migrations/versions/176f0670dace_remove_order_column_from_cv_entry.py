"""remove order column from CV entry

Revision ID: 176f0670dace
Revises: b3af2f3749dc
Create Date: 2020-10-14 17:27:42.991597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '176f0670dace'
down_revision = 'b3af2f3749dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cv_entry') as batch_op:
        batch_op.drop_column('order')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cv_entry', sa.Column('order', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
