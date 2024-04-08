"""add foreign key to posts table

Revision ID: b1e1ecff1e00
Revises: 691fb404c268
Create Date: 2024-04-08 13:03:19.663561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e1ecff1e00'
down_revision = '691fb404c268'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraints("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
