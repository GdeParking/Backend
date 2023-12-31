"""initial migration

Revision ID: d491733a6196
Revises: 
Create Date: 2023-12-23 09:54:58.270625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd491733a6196'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('camera',
    sa.Column('cam_url', sa.String(length=255), nullable=False),
    sa.Column('timezone', sa.String(length=10), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('update_period', sa.Integer(), nullable=True),
    sa.Column('consent', sa.Boolean(), nullable=False),
    sa.Column('parking_places', sa.Integer(), nullable=False),
    sa.Column('last_connection', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cam_url')
    )
    op.create_table('zone',
    sa.Column('camera_id', sa.Integer(), nullable=False),
    sa.Column('internal_id', sa.Integer(), nullable=False),
    sa.Column('long', sa.Numeric(), nullable=False),
    sa.Column('lat', sa.Numeric(), nullable=False),
    sa.Column('x', sa.Numeric(), nullable=False),
    sa.Column('y', sa.Numeric(), nullable=False),
    sa.Column('w', sa.Numeric(), nullable=False),
    sa.Column('h', sa.Numeric(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['camera_id'], ['camera.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('zone')
    op.drop_table('camera')
    # ### end Alembic commands ###