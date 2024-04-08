"""add content columns to posts table

Revision ID: 471dcec2c3e0
Revises: 71f11c09d42b
Create Date: 2024-04-08 12:40:16.940568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '471dcec2c3e0'
down_revision = '71f11c09d42b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
