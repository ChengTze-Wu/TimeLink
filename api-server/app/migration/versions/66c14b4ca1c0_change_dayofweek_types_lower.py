"""Change DayOfWeek types lower

Revision ID: 66c14b4ca1c0
Revises: f5372dd654d9
Create Date: 2024-01-10 17:23:34.852841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "66c14b4ca1c0"
down_revision: Union[str, None] = "f5372dd654d9"
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
