"""migration

Revision ID: 9c3f66de421b
Revises: f278cbbda0fb
Create Date: 2024-03-18 07:33:34.757524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c3f66de421b'
down_revision: Union[str, None] = 'f278cbbda0fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
