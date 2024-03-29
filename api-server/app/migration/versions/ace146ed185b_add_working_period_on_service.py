"""Add working_period on Service

Revision ID: ace146ed185b
Revises: 66c14b4ca1c0
Create Date: 2024-01-16 13:53:34.661561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ace146ed185b"
down_revision: Union[str, None] = "66c14b4ca1c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("service", sa.Column("working_period", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("service", "working_period")
    # ### end Alembic commands ###
