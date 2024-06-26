"""Datatables remake

Revision ID: ba7b2463d0f5
Revises: 
Create Date: 2024-06-22 21:12:45.756436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = 'ba7b2463d0f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('firstname', sa.String(length=30), nullable=True),
    sa.Column('lastname', sa.String(length=30), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.String(length=30), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(length=1000), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('background', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('column',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follower',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=30), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('permission', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('column_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(length=1000), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('background', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['column_id'], ['column.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscriber',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=30), nullable=True),
    sa.Column('card_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriber')
    op.drop_table('card')
    op.drop_table('follower')
    op.drop_table('column')
    op.drop_table('board')
    op.drop_table('user')
    # ### end Alembic commands ###
