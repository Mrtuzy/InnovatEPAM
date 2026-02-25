"""Create evaluations table

Revision ID: 004_create_evaluations_table
Revises: 003_create_ideas_table
Create Date: 2026-02-25
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '004_create_evaluations_table'
down_revision = '003_create_ideas_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create evaluations table."""
    op.create_table(
        'evaluations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('idea_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ideas.id'), nullable=False),
        sa.Column('evaluator_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('previous_status', sa.String(50), nullable=False),
        sa.Column('new_status', sa.String(50), nullable=False),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    
    # Create indexes for better query performance
    op.create_index('ix_evaluations_idea_id', 'evaluations', ['idea_id'])
    op.create_index('ix_evaluations_evaluator_id', 'evaluations', ['evaluator_id'])
    op.create_index('ix_evaluations_created_at', 'evaluations', ['created_at'])
    # Composite index for common query pattern (idea evaluations ordered by date)
    op.create_index('ix_evaluations_idea_created', 'evaluations', ['idea_id', 'created_at'])


def downgrade() -> None:
    """Drop evaluations table."""
    op.drop_index('ix_evaluations_idea_created', table_name='evaluations')
    op.drop_index('ix_evaluations_created_at', table_name='evaluations')
    op.drop_index('ix_evaluations_evaluator_id', table_name='evaluations')
    op.drop_index('ix_evaluations_idea_id', table_name='evaluations')
    op.drop_table('evaluations')
