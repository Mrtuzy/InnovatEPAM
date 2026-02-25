"""Idea repository for data access operations."""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, desc, asc

from src.models.idea import Idea, IdeaStatus
from src.repositories.base_repository import BaseRepository


class IdeaRepository(BaseRepository[Idea]):
    """
    Repository for Idea model operations.
    
    Extends BaseRepository with Idea-specific queries:
    - create_idea: Create new idea with attachment metadata
    - get_by_submitter: Get ideas by submitter with pagination
    - get_all_paginated: Get all ideas with pagination (admin view)
    - apply_filters: Apply status/category filters
    """
    
    def __init__(self, db: Session):
        """
        Initialize IdeaRepository.
        
        Args:
            db: Database session
        """
        super().__init__(Idea, db)
    
    def create_idea(
        self,
        title: str,
        description: str,
        category_id: UUID,
        submitter_id: UUID,
        attachment_filename: Optional[str] = None,
        attachment_path: Optional[str] = None,
        attachment_size: Optional[int] = None,
        attachment_mimetype: Optional[str] = None
    ) -> Idea:
        """
        Create new idea.
        
        Args:
            title: Idea title
            description: Detailed description
            category_id: Category UUID
            submitter_id: Submitter User UUID
            attachment_filename: Optional filename
            attachment_path: Optional storage path
            attachment_size: Optional file size
            attachment_mimetype: Optional MIME type
            
        Returns:
            Created idea
            
        Raises:
            ValueError: If validation fails
        """
        try:
            idea = Idea(
                title=title,
                description=description,
                category_id=category_id,
                submitter_id=submitter_id,
                status="submitted",
                attachment_filename=attachment_filename,
                attachment_path=attachment_path,
                attachment_size=attachment_size,
                attachment_mimetype=attachment_mimetype
            )
            self.db.add(idea)
            self.db.commit()
            self.db.refresh(idea)
            return idea
        except ValueError:
            raise
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create idea: {str(e)}")
    
    def get_by_id(self, idea_id: UUID, load_relations: bool = True) -> Optional[Idea]:
        """
        Get idea by ID with optional eager loading.
        
        Args:
            idea_id: Idea UUID
            load_relations: Load category and submitter relationships
            
        Returns:
            Idea if found, None otherwise
        """
        query = self.db.query(Idea)
        
        if load_relations:
            query = query.options(
                joinedload(Idea.category),
                joinedload(Idea.submitter)
            )
        
        return query.filter(Idea.id == idea_id).first()
    
    def get_by_submitter(
        self,
        submitter_id: UUID,
        status: Optional[str] = None,
        category_id: Optional[UUID] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "created_at_desc"
    ) -> Dict[str, Any]:
        """
        Get ideas by submitter with pagination and filtering.
        
        Args:
            submitter_id: Submitter User UUID
            status: Optional status filter
            category_id: Optional category filter
            page: Page number (1-based)
            limit: Items per page
            sort: Sort order (created_at_desc, created_at_asc, title_asc)
            
        Returns:
            Dictionary with 'items' and 'pagination' keys
        """
        # Base query
        query = self.db.query(Idea).options(
            joinedload(Idea.category),
            joinedload(Idea.submitter)
        ).filter(
            Idea.submitter_id == submitter_id
        )
        
        # Apply filters
        query = self._apply_filters(query, status, category_id)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        query = self._apply_sorting(query, sort)
        
        # Apply pagination
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return {
            'items': items,
            'pagination': {
                'total': total,
                'page': page,
                'limit': limit,
                'pages': pages
            }
        }
    
    def get_all_paginated(
        self,
        status: Optional[str] = None,
        category_id: Optional[UUID] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "created_at_desc"
    ) -> Dict[str, Any]:
        """
        Get all ideas with pagination and filtering (admin view).
        
        Args:
            status: Optional status filter
            category_id: Optional category filter
            page: Page number (1-based)
            limit: Items per page
            sort: Sort order
            
        Returns:
            Dictionary with 'items' and 'pagination' keys
        """
        # Base query
        query = self.db.query(Idea).options(
            joinedload(Idea.category),
            joinedload(Idea.submitter)
        )
        
        # Apply filters
        query = self._apply_filters(query, status, category_id)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        query = self._apply_sorting(query, sort)
        
        # Apply pagination
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return {
            'items': items,
            'pagination': {
                'total': total,
                'page': page,
                'limit': limit,
                'pages': pages
            }
        }
    
    def _apply_filters(self, query, status: Optional[str], category_id: Optional[UUID]):
        """Apply status and category filters to query."""
        if status and status != 'all':
            query = query.filter(Idea.status == status)
        
        if category_id:
            query = query.filter(Idea.category_id == category_id)
        
        return query
    
    def _apply_sorting(self, query, sort: str):
        """Apply sorting to query."""
        if sort == "created_at_asc":
            query = query.order_by(asc(Idea.created_at))
        elif sort == "title_asc":
            query = query.order_by(asc(Idea.title))
        else:  # default: created_at_desc
            query = query.order_by(desc(Idea.created_at))
        
        return query
    
    def update_status(self, idea_id: UUID, new_status: str) -> Optional[Idea]:
        """
        Update idea status.
        
        Args:
            idea_id: Idea UUID
            new_status: New status value
            
        Returns:
            Updated idea or None if not found
        """
        idea = self.get_by_id(idea_id)
        if idea:
            idea.status = new_status
            self.db.commit()
            self.db.refresh(idea)
        return idea
