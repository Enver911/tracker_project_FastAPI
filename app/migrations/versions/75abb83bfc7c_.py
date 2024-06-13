"""empty message

Revision ID: 75abb83bfc7c
Revises: b8d3efdccce6
Create Date: 2024-06-14 01:13:24.699543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75abb83bfc7c'
down_revision: Union[str, None] = 'b8d3efdccce6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
