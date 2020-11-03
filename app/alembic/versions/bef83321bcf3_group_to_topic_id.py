"""group_to_topic: +(id)

Revision ID: bef83321bcf3
Revises: b346e34b1b42
Create Date: 2020-10-27 04:00:53.451093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bef83321bcf3'
down_revision = 'b346e34b1b42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_to_topic', sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group_to_topic', 'id')
    # ### end Alembic commands ###
