"""
initial

Revision ID: 01
Revises: 
Create Date: 2023-05-16 13:34:53.151556

"""
# Импортируем необходимые модули
from alembic import op
import sqlalchemy as sa

# Идентификаторы ревизии, используемые Alembic
revision = '01'
down_revision = None
branch_labels = None
depends_on = None

# Функция для обновления структуры базы данных
def upgrade():
    # Создаем таблицу 'camera' с указанными столбцами
    op.create_table(
        'camera',
        sa.Column('id', sa.Integer(), sa.Sequence('camera_id_seq'), primary_key=True),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('parking_places', sa.Integer(), nullable=True),
        sa.Column('timezone', sa.String(length=10), nullable=True),
        sa.Column('update_period', sa.Integer(), nullable=True),
        sa.Column('last_connection', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Создаем таблицу 'zone' с указанными столбцами
    op.create_table(
        'zone',
        sa.Column('id', sa.Integer(), sa.Sequence('zone_id_seq'), primary_key=True),
        sa.Column('camera_id', sa.Integer(), nullable=True),
        sa.Column('internal_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['camera_id'], ['camera.id']),
        sa.PrimaryKeyConstraint('id')
    )

# Функция для отката изменений структуры базы данных
def downgrade():
    # Удаляем таблицу 'zone'
    op.drop_table('zone')
    # Удаляем таблицу 'camera'
    op.drop_table('camera')
