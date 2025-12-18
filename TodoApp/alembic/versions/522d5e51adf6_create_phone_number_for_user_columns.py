"""Create phone number for user columns

Revision ID: 522d5e51adf6
Revises: 
Create Date: 2025-12-18 23:00:05.383701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '522d5e51adf6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add phone_number column to users table."""
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))


def downgrade() -> None:
    """Remove phone_number column from users table."""
    op.drop_column('users', 'phone_number')
