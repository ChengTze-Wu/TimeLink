"""Change DayOfWeek value

Revision ID: f482dd97c394
Revises: e27462e44ffb
Create Date: 2024-01-10 17:06:27.187132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f482dd97c394'
down_revision: Union[str, None] = 'e27462e44ffb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###