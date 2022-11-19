"""async_initial

Revision ID: 941329c9a0ca
Revises: 
Create Date: 2022-11-18 15:41:06.402206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '941329c9a0ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rubrics', sa.Text(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    # ### end Alembic commands ###
