"""Idea service for business logic."""
import os
from typing import Optional, Dict, Any, List
from uuid import UUID
from fastapi import UploadFile, HTTPException, status

from src.repositories.idea_repository import IdeaRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.evaluation_repository import EvaluationRepository
from src.models.evaluation import Evaluation
from src.utils.file_handler import FileHandler
from src.utils.logger import get_logger


logger = get_logger(__name__)


class IdeaService:
    """
    Service for idea business logic.
    
    Handles:
    - Idea creation with file upload
    - Idea retrieval with pagination and filtering
    - File attachment management
    """
    
    def __init__(
        self,
        idea_repository: IdeaRepository,
        category_repository: CategoryRepository,
        evaluation_repository: EvaluationRepository,
        file_handler: FileHandler
    ):
        """
        Initialize IdeaService.
        
        Args:
            idea_repository: Idea repository
            category_repository: Category repository
            evaluation_repository: Evaluation repository
            file_handler: File handler utility
        """
        self.idea_repository = idea_repository
        self.category_repository = category_repository
        self.evaluation_repository = evaluation_repository
        self.file_handler = file_handler
    
    async def create_idea(
        self,
        title: str,
        description: str,
        category_id: UUID,
        submitter_id: UUID,
        attachment: Optional[UploadFile] = None
    ):
        """
        Create new idea with optional file attachment.
        
        Args:
            title: Idea title
            description: Detailed description
            category_id: Category UUID
            submitter_id: Submitter User UUID
            attachment: Optional file upload
            
        Returns:
            Created idea
            
        Raises:
            HTTPException: If validation fails or category not found
        """
        try:
            # Validate category exists and is active
            category = self.category_repository.get_by_id(category_id)
            if not category:
                logger.error(f"Category not found: {category_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
            
            if not category.is_active:
                logger.error(f"Category is inactive: {category_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Selected category is no longer available"
                )
            
            # Handle file upload if present
            attachment_filename = None
            attachment_path = None
            attachment_size = None
            attachment_mimetype = None
            
            if attachment and attachment.filename:
                logger.info(f"Processing file upload: {attachment.filename}")
                
                # Validate file type
                if not self.file_handler.validate_file_type(
                    attachment.filename,
                    attachment.content_type
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid file type. Allowed: PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG, GIF"
                    )
                
                # Read file content
                file_content = await attachment.read()
                file_size = len(file_content)
                
                # Validate file size
                if not self.file_handler.validate_file_size(file_size):
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File too large. Maximum size: 10MB"
                    )
                
                # Create idea first to get ID for storage path
                idea_temp = self.idea_repository.create_idea(
                    title=title,
                    description=description,
                    category_id=category_id,
                    submitter_id=submitter_id
                )
                
                # Generate storage path
                storage_path = self.file_handler.generate_storage_path(
                    str(idea_temp.id),
                    attachment.filename
                )
                
                # Save file
                try:
                    self.file_handler.save_file(file_content, storage_path)
                    logger.info(f"File saved: {storage_path}")
                except Exception as e:
                    logger.error(f"Failed to save file: {str(e)}")
                    # Delete idea if file save fails
                    self.idea_repository.delete(idea_temp.id)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to save attachment"
                    )
                
                # Update idea with attachment metadata
                idea_temp.attachment_filename = attachment.filename
                idea_temp.attachment_path = storage_path
                idea_temp.attachment_size = file_size
                idea_temp.attachment_mimetype = attachment.content_type
                self.idea_repository.db.commit()
                self.idea_repository.db.refresh(idea_temp)
                
                logger.info(f"Idea created with attachment: {idea_temp.id}")
                return idea_temp
            
            else:
                # Create idea without attachment
                idea = self.idea_repository.create_idea(
                    title=title,
                    description=description,
                    category_id=category_id,
                    submitter_id=submitter_id
                )
                logger.info(f"Idea created without attachment: {idea.id}")
                return idea
        
        except HTTPException:
            raise
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Failed to create idea: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create idea"
            )
    
    def get_idea_by_id(self, idea_id: UUID):
        """
        Get idea by ID.
        
        Args:
            idea_id: Idea UUID
            
        Returns:
            Idea if found
            
        Raises:
            HTTPException: If not found
        """
        idea = self.idea_repository.get_by_id(idea_id)
        if not idea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Idea not found"
            )
        return idea
    
    def get_user_ideas(
        self,
        submitter_id: UUID,
        status: Optional[str] = None,
        category_id: Optional[UUID] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "created_at_desc"
    ) -> Dict[str, Any]:
        """
        Get ideas submitted by user with pagination.
        
        Args:
            submitter_id: Submitter User UUID
            status: Optional status filter
            category_id: Optional category filter
            page: Page number (1-based)
            limit: Items per page
            sort: Sort order
            
        Returns:
            Dictionary with 'items' and 'pagination' keys
        """
        return self.idea_repository.get_by_submitter(
            submitter_id=submitter_id,
            status=status,
            category_id=category_id,
            page=page,
            limit=limit,
            sort=sort
        )
    
    def get_all_ideas(
        self,
        status: Optional[str] = None,
        category_id: Optional[UUID] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "created_at_desc"
    ) -> Dict[str, Any]:
        """
        Get all ideas with pagination (admin view).
        
        Args:
            status: Optional status filter
            category_id: Optional category filter
            page: Page number (1-based)
            limit: Items per page
            sort: Sort order
            
        Returns:
            Dictionary with 'items' and 'pagination' keys
        """
        return self.idea_repository.get_all_paginated(
            status=status,
            category_id=category_id,
            page=page,
            limit=limit,
            sort=sort
        )
    
    def get_attachment_path(self, idea_id: UUID) -> str:
        """
        Get absolute file path for idea attachment.
        
        Args:
            idea_id: Idea UUID
            
        Returns:
            Absolute file path
            
        Raises:
            HTTPException: If idea not found or has no attachment
        """
        idea = self.get_idea_by_id(idea_id)
        
        if not idea.attachment_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Idea has no attachment"
            )
        
        file_path = self.file_handler.get_file_path(idea.attachment_path)
        
        if not os.path.exists(file_path):
            logger.error(f"Attachment file not found: {file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment file not found"
            )
        
        return file_path
    
    def evaluate_idea(
        self,
        idea_id: UUID,
        evaluator_id: UUID,
        evaluator_role: str,
        new_status: str,
        comment: str
    ) -> Evaluation:
        """
        Evaluate an idea with status change and comment.
        
        Admin-only operation. Creates evaluation record and updates idea status.
        
        Args:
            idea_id: UUID of idea to evaluate
            evaluator_id: UUID of evaluating admin
            evaluator_role: Role of evaluator (must be 'admin')
            new_status: New status (under_review/accepted/rejected)
            comment: Evaluation feedback (required)
            
        Returns:
            Created Evaluation instance
            
        Raises:
            HTTPException: If not admin, idea not found, or invalid status
        """
        # Verify admin role
        if evaluator_role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can evaluate ideas"
            )
        
        # Get idea
        idea = self.get_idea_by_id(idea_id)
        previous_status = idea.status
        
        # Validate status transition
        valid_statuses = ['under_review', 'accepted', 'rejected']
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Prevent no-op transitions
        if previous_status == new_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Idea is already in '{new_status}' status"
            )
        
        # Create evaluation record
        evaluation = self.evaluation_repository.create_evaluation(
            idea_id=idea_id,
            evaluator_id=evaluator_id,
            previous_status=previous_status,
            new_status=new_status,
            comment=comment
        )
        
        # Update idea status
        self.idea_repository.update_status(idea_id, new_status)
        
        logger.info(
            f"Idea {idea_id} evaluated by {evaluator_id}: "
            f"{previous_status} → {new_status}"
        )
        
        return evaluation
    
    def get_evaluations(self, idea_id: UUID) -> List[Evaluation]:
        """
        Get all evaluations for an idea.
        
        Args:
            idea_id: UUID of idea
            
        Returns:
            List of Evaluation instances ordered by created_at desc
        """
        # Verify idea exists
        self.get_idea_by_id(idea_id)
        
        return self.evaluation_repository.get_evaluations_by_idea(
            idea_id=idea_id,
            load_relations=True
        )
