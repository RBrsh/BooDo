"""create todos table

Revision ID: 4947f9d835f4
Revises: 
Create Date: 2022-10-28 10:29:54.568543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4947f9d835f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('is_complete', bool),
        sa.Column()
    )


def downgrade() -> None:
    op.drop_table('todos')
