"""add CV and Course Tables

Revision ID: 07a2628ea3b1
Revises: a30e2fc5d0d4
Create Date: 2020-10-06 20:36:53.638690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07a2628ea3b1'
down_revision = 'a30e2fc5d0d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('course_name', sa.String(length=255), nullable=True),
    sa.Column('paragraph', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cv_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('start', sa.Date(), nullable=True),
    sa.Column('end', sa.Date(), nullable=True),
    sa.Column('workplace', sa.String(length=255), nullable=True),
    sa.Column('paragraph', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cv_entry')
    op.drop_table('course_entry')
    # ### end Alembic commands ###
