"""Change DayOfWeek types

Revision ID: f5372dd654d9
Revises: f482dd97c394
Create Date: 2024-01-10 17:14:58.074087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f5372dd654d9"
down_revision: Union[str, None] = "f482dd97c394"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # create enum before using it
    dayofweek = sa.Enum(
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        name="dayofweek",
    )
    dayofweek.create(op.get_bind())

    # add USING clause to provide conversion expression
    op.execute(
        "ALTER TABLE working_hour ALTER COLUMN day_of_week TYPE dayofweek USING day_of_week::text::dayofweek"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE working_hour ALTER COLUMN day_of_week TYPE varchar(255)")
    dayofweek = sa.Enum(name="dayofweek")
    dayofweek.drop(op.get_bind())
