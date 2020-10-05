"""empty message

Revision ID: cfefe0450701
Revises: 
Create Date: 2020-10-04 22:07:43.132188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfefe0450701'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('treehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brewery', sa.String(), nullable=True),
    sa.Column('item', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('treehouse')
    # ### end Alembic commands ###
