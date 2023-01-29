"""Timestamps

Revision ID: 9a87295335a0
Revises: 65a763b68873
Create Date: 2023-01-26 21:20:30.386533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a87295335a0'
down_revision = '65a763b68873'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feeds', sa.Column('checked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('feeds', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('feeds', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('feeds', 'updated_at')
    op.drop_column('feeds', 'created_at')
    op.drop_column('feeds', 'checked_at')
    # ### end Alembic commands ###
