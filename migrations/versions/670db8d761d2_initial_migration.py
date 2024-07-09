"""Initial migration

Revision ID: 670db8d761d2
Revises: 
Create Date: 2024-07-09 21:05:53.421991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670db8d761d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=512), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_map')
    # ### end Alembic commands ###
