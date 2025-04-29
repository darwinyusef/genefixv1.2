"""create_configurations_manually

Revision ID: 94c91d573a28
Revises: adf8e8e0a7c1
Create Date: 2025-04-26 13:17:55.903654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '94c91d573a28'
down_revision: Union[str, None] = 'adf8e8e0a7c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
