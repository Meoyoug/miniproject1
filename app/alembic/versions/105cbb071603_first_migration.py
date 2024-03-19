"""first migration

Revision ID: 105cbb071603
Revises: 9c3f66de421b
Create Date: 2024-03-18 07:48:54.355127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '105cbb071603'
down_revision: Union[str, None] = '9c3f66de421b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
