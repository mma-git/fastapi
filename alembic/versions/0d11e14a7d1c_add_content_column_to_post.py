"""Add Content Column to Post

Revision ID: 0d11e14a7d1c
Revises: 523e81f0db87
Create Date: 2023-09-06 15:03:07.820649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d11e14a7d1c'
down_revision: Union[str, None] = '523e81f0db87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content',sa.String(),nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
