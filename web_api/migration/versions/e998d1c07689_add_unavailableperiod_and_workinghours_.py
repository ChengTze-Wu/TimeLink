"""Add UnavailablePeriod and WorkingHours table

Revision ID: e998d1c07689
Revises: df6157d8dc25
Create Date: 2023-12-24 15:51:18.410022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e998d1c07689'
down_revision: Union[str, None] = 'df6157d8dc25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unavailable_periods',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('service_id', sa.Uuid(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('working_hours',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('service_id', sa.Uuid(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('unavailable_period')
    op.drop_column('service', 'end_date')
    op.drop_column('service', 'close_time')
    op.drop_column('service', 'period_time')
    op.drop_column('service', 'open_time')
    op.drop_column('service', 'start_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('start_date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('open_time', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('period_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('close_time', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=True))
    op.create_table('unavailable_period',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('service_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('start_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('end_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], name='unavailable_period_service_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='unavailable_period_pkey')
    )
    op.drop_table('working_hours')
    op.drop_table('unavailable_periods')
    # ### end Alembic commands ###
