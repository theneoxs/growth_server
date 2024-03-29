"""Init Database

Revision ID: dc7013112448
Revises: 
Create Date: 2024-01-08 16:48:24.192797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc7013112448'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('surname', sa.String(length=100), nullable=True),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auth_data',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('login', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.UniqueConstraint('login')
    )
    op.create_table('block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('level', sa.String(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('block_res',
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('res_id', sa.Integer(), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('block_id')
    )
    op.create_table('status_block',
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('block_status', sa.String(length=100), server_default='0', nullable=True),
    sa.Column('is_favorite', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('block_id', 'user_id')
    )
    op.create_table('tree_block',
    sa.Column('mother_id', sa.Integer(), nullable=True),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['block.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['mother_id'], ['block.id'], ondelete='CASCADE')
    )
    op.create_table('program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tag', sa.String(length=100), nullable=True),
    sa.Column('is_public', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('program_list',
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('program_id', 'block_id')
    )
    op.create_table('program_to_user',
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('program_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program_to_user')
    op.drop_table('program_list')
    op.drop_table('program')
    op.drop_table('tree_block')
    op.drop_table('status_block')
    op.drop_table('block_res')
    op.drop_table('block')
    op.drop_table('auth_data')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('branch')
    # ### end Alembic commands ###
