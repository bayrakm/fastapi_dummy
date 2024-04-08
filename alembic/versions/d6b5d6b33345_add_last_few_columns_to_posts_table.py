"""add last few columns to posts table

Revision ID: d6b5d6b33345
Revises: b1e1ecff1e00
Create Date: 2024-04-08 13:10:06.685369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6b5d6b33345'
down_revision = 'b1e1ecff1e00'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column("posts", sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")

    pass
