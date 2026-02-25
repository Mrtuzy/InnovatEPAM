"""Create categories table.

Revision ID: 002_create_categories_table
Revises: 001_create_users_table
Create Date: 2026-02-25 10:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '002_create_categories_table'
down_revision = '001_create_users_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_categories_name')
    )
    
    # Create indexes
    op.create_index('ix_categories_name', 'categories', ['name'])
    op.create_index('ix_categories_display_order', 'categories', ['display_order'])
    op.create_index('ix_categories_is_active', 'categories', ['is_active'])
    
    # Insert seed data for initial categories
    categories_table = sa.table(
        'categories',
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('display_order', sa.Integer),
        sa.column('is_active', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )
    
    now = datetime.utcnow()
    
    op.bulk_insert(
        categories_table,
        [
            {
                'name': 'Process Improvement',
                'description': 'Ideas to streamline workflows and procedures',
                'display_order': 1,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
            {
                'name': 'Technology Innovation',
                'description': 'New tools, platforms, or technical solutions',
                'display_order': 2,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
            {
                'name': 'Cost Reduction',
                'description': 'Ideas to reduce expenses or improve efficiency',
                'display_order': 3,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
            {
                'name': 'Customer Experience',
                'description': 'Improvements to client interactions and satisfaction',
                'display_order': 4,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
            {
                'name': 'Employee Experience',
                'description': 'Workplace improvements and team culture',
                'display_order': 5,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
            {
                'name': 'Other',
                'description': 'Ideas that don\'t fit other categories',
                'display_order': 99,
                'is_active': True,
                'created_at': now,
                'updated_at': now,
            },
        ]
    )


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop indexes
    op.drop_index('ix_categories_is_active', table_name='categories')
    op.drop_index('ix_categories_display_order', table_name='categories')
    op.drop_index('ix_categories_name', table_name='categories')
    # Drop table
    op.drop_table('categories')
