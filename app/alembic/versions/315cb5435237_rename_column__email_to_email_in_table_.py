"""rename column _email to email in table User

Revision ID: 315cb5435237
Revises: 312430cac8bc
Create Date: 2020-10-08 23:13:58.745554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '315cb5435237'
down_revision = '312430cac8bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', '_email', new_column_name='email', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email', new_column_name='_email', server_default=None)
    # ### end Alembic commands ###
