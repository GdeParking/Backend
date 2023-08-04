"""unique at camera.camera_url, add cascade deletion to zones

Revision ID: 7a1d4b03d9c1
Revises: ad339ef2272d
Create Date: 2023-08-04 16:07:08.202192

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7a1d4b03d9c1'
down_revision = 'ad339ef2272d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('camera', schema=None) as batch_op:
        batch_op.alter_column('registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
        batch_op.alter_column('cam_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.create_unique_constraint(None, ['cam_url'])

    with op.batch_alter_table('zone', schema=None) as batch_op:
        batch_op.alter_column('registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
        batch_op.drop_constraint('zone_camera_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'camera', ['camera_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zone', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('zone_camera_id_fkey', 'camera', ['camera_id'], ['id'])
        batch_op.alter_column('updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
        batch_op.alter_column('registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    with op.batch_alter_table('camera', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('cam_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
        batch_op.alter_column('registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###