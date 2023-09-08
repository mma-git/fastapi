"""add foreign key to post table

Revision ID: 2cd58d2b3a02
Revises: 4259e51ca2a1
Create Date: 2023-09-08 09:29:38.257956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cd58d2b3a02'
down_revision: Union[str, None] = '4259e51ca2a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('account_id',sa.Integer(),nullable=False)
        
    )
    op.create_foreign_key('post_usersfkey',source_table="posts",referent_table="users",
                          local_cols=["account_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_usersfkey', table_name="posts")
    op.drop_column('posts', 'account_id')
    pass
