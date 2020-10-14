"""Add Message Table

Revision ID: b3af2f3749dc
Revises: 6707f5f496cd
Create Date: 2020-10-08 17:34:18.911149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3af2f3749dc'
down_revision = '6707f5f496cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_date'), 'message', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_date'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###