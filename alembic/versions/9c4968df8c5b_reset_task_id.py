"""reset task_id

Revision ID: 9c4968df8c5b
Revises: 0eded53daf81
Create Date: 2024-09-23 21:32:07.298631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4968df8c5b'
down_revision: Union[str, None] = '0eded53daf81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
