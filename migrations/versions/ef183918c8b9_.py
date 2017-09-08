"""empty message

Revision ID: ef183918c8b9
Revises: 3832c4b7c81a
Create Date: 2017-09-05 11:57:10.318755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef183918c8b9'
down_revision = '3832c4b7c81a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('user', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###