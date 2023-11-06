"""try date

Revision ID: 3a9ff4b5aaa1
Revises: a930fdd6ba14
Create Date: 2023-11-01 01:21:06.195373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a9ff4b5aaa1'
down_revision = 'a930fdd6ba14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('begin_at',
               existing_type=sa.DATETIME(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('end_at',
               existing_type=sa.DATETIME(),
               type_=sa.DATE(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('end_at',
               existing_type=sa.DATE(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.alter_column('begin_at',
               existing_type=sa.DATE(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###