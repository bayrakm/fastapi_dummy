"""vote table  auto-generate

Revision ID: 2241ab9e3d6d
Revises: d6b5d6b33345
Create Date: 2024-04-08 13:29:03.575194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2241ab9e3d6d'
down_revision = 'd6b5d6b33345'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("phone", sa.Integer(), nullable=False))
    pass


def downgrade():
    op.drop_column("users", "phone")
    pass
