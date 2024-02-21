"""ADD table

Revision ID: 8c05fe06933d
Revises: 122e184725c9
Create Date: 2024-01-02 15:47:02.910752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c05fe06933d"
down_revision: Union[str, None] = "122e184725c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
