"""ADD table

Revision ID: e27462e44ffb
Revises: 8c05fe06933d
Create Date: 2024-01-02 15:47:57.132994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e27462e44ffb'
down_revision: Union[str, None] = '8c05fe06933d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
