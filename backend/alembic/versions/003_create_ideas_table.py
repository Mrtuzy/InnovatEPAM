"""Create ideas table.

Revision ID: 003_create_ideas_table
Revises: 002_create_categories_table
Create Date: 2026-02-25 10:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_create_ideas_table'
down_revision = '002_create_categories_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Create idea_status enum type if not exists
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE idea_status AS ENUM ('submitted', 'under_review', 'accepted', 'rejected');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    # Create ideas table
    op.create_table(
        'ideas',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('submitter_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', postgresql.ENUM('submitted', 'under_review', 'accepted', 'rejected', name='idea_status', create_type=False), 
                  nullable=False, server_default='submitted'),
        sa.Column('attachment_filename', sa.String(255), nullable=True),
        sa.Column('attachment_path', sa.String(500), nullable=True),
        sa.Column('attachment_size', sa.Integer(), nullable=True),
        sa.Column('attachment_mimetype', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='fk_ideas_category_id'),
        sa.ForeignKeyConstraint(['submitter_id'], ['users.id'], name='fk_ideas_submitter_id')
    )
    
    # Create indexes for efficient queries
    op.create_index('ix_ideas_category_id', 'ideas', ['category_id'])
    op.create_index('ix_ideas_submitter_id', 'ideas', ['submitter_id'])
    op.create_index('ix_ideas_status', 'ideas', ['status'])
    op.create_index('ix_ideas_created_at_desc', 'ideas', [sa.text('created_at DESC')])
    
    # Composite index for user's ideas list (most common query)
    op.create_index('ix_ideas_submitter_created', 'ideas', ['submitter_id', sa.text('created_at DESC')])


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop indexes
    op.drop_index('ix_ideas_submitter_created', table_name='ideas')
    op.drop_index('ix_ideas_created_at_desc', table_name='ideas')
    op.drop_index('ix_ideas_status', table_name='ideas')
    op.drop_index('ix_ideas_submitter_id', table_name='ideas')
    op.drop_index('ix_ideas_category_id', table_name='ideas')
    
    # Drop table
    op.drop_table('ideas')
    
    # Drop enum type
    op.execute("DROP TYPE idea_status")
