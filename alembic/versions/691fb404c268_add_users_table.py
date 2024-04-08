"""add users table

Revision ID: 691fb404c268
Revises: 471dcec2c3e0
Create Date: 2024-04-08 12:49:55.788489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '691fb404c268'
down_revision = '471dcec2c3e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column("id",sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password",sa.String(), nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")), 
                    sa.UniqueConstraint("email"),
                    sa.PrimaryKeyConstraint("id")
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
