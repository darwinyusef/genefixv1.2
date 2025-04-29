"""create_configurations_manually

Revision ID: dc4fd2a6d53d
Revises: 94c91d573a28
Create Date: 2025-04-26 15:28:05.752134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc4fd2a6d53d'
down_revision: Union[str, None] = '94c91d573a28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
