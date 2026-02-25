"""Evaluation repository for database operations."""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session, joinedload

from src.models.evaluation import Evaluation
from src.repositories.base_repository import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):
    """Repository for Evaluation model operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        super().__init__(Evaluation, db)
    
    def create_evaluation(
        self,
        idea_id: uuid.UUID,
        evaluator_id: uuid.UUID,
        previous_status: str,
        new_status: str,
        comment: str
    ) -> Evaluation:
        """
        Create a new evaluation record.
        
        Args:
            idea_id: UUID of idea being evaluated
            evaluator_id: UUID of admin performing evaluation
            previous_status: Status before evaluation
            new_status: Status after evaluation
            comment: Evaluation feedback
            
        Returns:
            Created Evaluation instance
        """
        evaluation = Evaluation(
            idea_id=idea_id,
            evaluator_id=evaluator_id,
            previous_status=previous_status,
            new_status=new_status,
            comment=comment
        )
        return self.create(evaluation)
    
    def get_evaluations_by_idea(
        self,
        idea_id: uuid.UUID,
        load_relations: bool = True
    ) -> List[Evaluation]:
        """
        Get all evaluations for a specific idea, ordered by created_at descending.
        
        Args:
            idea_id: UUID of idea
            load_relations: Whether to eagerly load evaluator relationship
            
        Returns:
            List of Evaluation instances
        """
        query = self.db.query(Evaluation).filter(Evaluation.idea_id == idea_id)
        
        if load_relations:
            query = query.options(joinedload(Evaluation.evaluator))
        
        return query.order_by(Evaluation.created_at.desc()).all()
    
    def get_evaluations_by_evaluator(
        self,
        evaluator_id: uuid.UUID,
        limit: int = 50
    ) -> List[Evaluation]:
        """
        Get recent evaluations performed by a specific evaluator.
        
        Args:
            evaluator_id: UUID of evaluator (admin user)
            limit: Maximum number of evaluations to return
            
        Returns:
            List of Evaluation instances
        """
        return (
            self.db.query(Evaluation)
            .filter(Evaluation.evaluator_id == evaluator_id)
            .order_by(Evaluation.created_at.desc())
            .limit(limit)
            .all()
        )
