"""groups(cascade teacher_id)

Revision ID: d4a816f945c2
Revises: 4fef39d5f4be
Create Date: 2021-01-10 21:27:36.830614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a816f945c2'
down_revision = '4fef39d5f4be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_to_subject')
    op.drop_table('subjects')
    op.drop_constraint('groups_teacher_id_fkey', 'groups', type_='foreignkey')
    op.create_foreign_key(None, 'groups', 'teachers', ['teacher_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.create_foreign_key('groups_teacher_id_fkey', 'groups', 'teachers', ['teacher_id'], ['id'])

    op.create_table('subjects',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='subjects_pkey'),
    sa.UniqueConstraint('name', name='subjects_name_key')
    )

    op.create_table('teacher_to_subject',
                    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('subject_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], name='teacher_to_subject_subject_id_fkey',
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='teacher_to_subject_teacher_id_fkey',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('teacher_id', 'subject_id', name='teacher_to_subject_pkey')
                    )
    # ### end Alembic commands ###
