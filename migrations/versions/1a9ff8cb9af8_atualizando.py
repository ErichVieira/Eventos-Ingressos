"""Atualizando

Revision ID: 1a9ff8cb9af8
Revises: 143f8ecafd39
Create Date: 2026-06-02 20:46:56.882909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a9ff8cb9af8'
down_revision: Union[str, Sequence[str], None] = '143f8ecafd39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
