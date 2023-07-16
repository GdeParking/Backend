"""added_coordinates

Revision ID: 02
Revises: 01
Create Date: 2023-05-23 16:33:20.857067

"""
from alembic import op
import sqlalchemy as sa

# Идентификаторы версии, используемые Alembic.
revision = '02'
down_revision = '01'
branch_labels = None
depends_on = None



def upgrade():
    # Команды, автоматически сгенерированные Alembic - пожалуйста, настройте их!
    with op.batch_alter_table('zone', schema=None) as batch_op:
        batch_op.add_column(sa.Column('long', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('lat', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # Команды, автоматически сгенерированные Alembic - пожалуйста, настройте их!
    with op.batch_alter_table('zone', schema=None) as batch_op:
        batch_op.drop_column('lat')
        batch_op.drop_column('long')

    # ### end Alembic commands ###
