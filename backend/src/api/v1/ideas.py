"""Idea API endpoints."""
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.repositories.idea_repository import IdeaRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.evaluation_repository import EvaluationRepository
from src.services.idea_service import IdeaService
from src.schemas.idea_schemas import IdeaResponse, IdeaListResponse, PaginationInfo
from src.schemas.evaluation_schemas import (
    EvaluateRequest, 
    EvaluationResponse, 
    EvaluationListResponse
)
from src.utils.file_handler import FileHandler
from src.utils.logger import get_logger
from src.api.v1.auth import get_current_user
from src.models.user import User


logger = get_logger(__name__)
router = APIRouter(prefix="/ideas", tags=["Ideas"])


def get_idea_service(db: Session = Depends(get_db)) -> IdeaService:
    """Dependency for idea service."""
    idea_repository = IdeaRepository(db)
    category_repository = CategoryRepository(db)
    evaluation_repository = EvaluationRepository(db)
    file_handler = FileHandler()
    return IdeaService(idea_repository, category_repository, evaluation_repository, file_handler)


@router.post("", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
async def create_idea(
    title: str = Form(..., min_length=10, max_length=200),
    description: str = Form(..., min_length=50, max_length=5000),
    category_id: UUID = Form(...),
    attachment: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Create new idea with optional file attachment.
    
    Args:
        title: Idea title (10-200 characters)
        description: Detailed description (50-5000 characters)
        category_id: Category UUID
        attachment: Optional file upload (max 10MB)
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        Created idea with details
    """
    logger.info(f"Creating idea for user {current_user.email}")
    
    idea = await service.create_idea(
        title=title,
        description=description,
        category_id=category_id,
        submitter_id=current_user.id,
        attachment=attachment
    )
    
    return IdeaResponse.from_orm_with_attachment(idea)


@router.get("/my-ideas", response_model=IdeaListResponse)
async def get_my_ideas(
    status: Optional[str] = None,
    category_id: Optional[UUID] = None,
    page: int = 1,
    limit: int = 20,
    sort: str = "created_at_desc",
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Get current user's ideas with pagination and filtering.
    
    Args:
        status: Filter by status (submitted, under_review, accepted, rejected, all)
        category_id: Filter by category UUID
        page: Page number (1-based)
        limit: Items per page (1-100)
        sort: Sort order (created_at_desc, created_at_asc, title_asc)
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        Paginated list of user's ideas
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    # Validate page
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be >= 1"
        )
    
    # Validate sort
    valid_sorts = ["created_at_desc", "created_at_asc", "title_asc"]
    if sort not in valid_sorts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort. Valid options: {', '.join(valid_sorts)}"
        )
    
    logger.info(f"Getting ideas for user {current_user.email} (page={page}, limit={limit})")
    
    result = service.get_user_ideas(
        submitter_id=current_user.id,
        status=status,
        category_id=category_id,
        page=page,
        limit=limit,
        sort=sort
    )
    
    # Convert items to response schema
    items = [IdeaResponse.from_orm_with_attachment(idea) for idea in result['items']]
    
    return IdeaListResponse(
        items=items,
        pagination=PaginationInfo(**result['pagination'])
    )


@router.get("", response_model=IdeaListResponse)
async def get_all_ideas(
    status: Optional[str] = None,
    category_id: Optional[UUID] = None,
    page: int = 1,
    limit: int = 20,
    sort: str = "created_at_desc",
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Get all ideas with pagination and filtering (admin/evaluator view).
    
    Args:
        status: Filter by status
        category_id: Filter by category UUID
        page: Page number (1-based)
        limit: Items per page (1-100)
        sort: Sort order
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        Paginated list of all ideas
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    # Validate page
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be >= 1"
        )
    
    logger.info(f"Getting all ideas for user {current_user.email} (page={page}, limit={limit})")
    
    result = service.get_all_ideas(
        status=status,
        category_id=category_id,
        page=page,
        limit=limit,
        sort=sort
    )
    
    # Convert items to response schema
    items = [IdeaResponse.from_orm_with_attachment(idea) for idea in result['items']]
    
    return IdeaListResponse(
        items=items,
        pagination=PaginationInfo(**result['pagination'])
    )


@router.get("/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: UUID,
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Get idea by ID.
    
    Args:
        idea_id: Idea UUID
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        Idea details
    """
    logger.info(f"Getting idea {idea_id} for user {current_user.email}")
    
    idea = service.get_idea_by_id(idea_id)
    return IdeaResponse.from_orm_with_attachment(idea)


@router.get("/{idea_id}/attachment", response_class=FileResponse)
async def download_attachment(
    idea_id: UUID,
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Download idea attachment.
    
    Args:
        idea_id: Idea UUID
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        File download response
    """
    logger.info(f"Downloading attachment for idea {idea_id} by user {current_user.email}")
    
    # Get idea to check attachment and get filename
    idea = service.get_idea_by_id(idea_id)
    
    if not idea.attachment_filename:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea has no attachment"
        )
    
    # Get file path
    file_path = service.get_attachment_path(idea_id)
    
    # Return file
    return FileResponse(
        path=file_path,
        filename=idea.attachment_filename,
        media_type=idea.attachment_mimetype or "application/octet-stream"
    )


@router.post("/{idea_id}/evaluate", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
def evaluate_idea(
    idea_id: UUID,
    request: EvaluateRequest,
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Evaluate an idea (admin only).
    
    Changes idea status and records evaluation with comment.
    
    Args:
        idea_id: Idea UUID
        request: Evaluation request (new_status, comment)
        current_user: Authenticated admin user
        service: Idea service
        
    Returns:
        Created evaluation record
        
    Raises:
        403: If user is not admin
        404: If idea not found
        400: If invalid status or no-op transition
    """
    logger.info(f"Admin {current_user.email} evaluating idea {idea_id}")
    
    evaluation = service.evaluate_idea(
        idea_id=idea_id,
        evaluator_id=current_user.id,
        evaluator_role=current_user.role,
        new_status=request.new_status,
        comment=request.comment
    )
    
    return EvaluationResponse.from_orm_with_evaluator(evaluation)


@router.get("/{idea_id}/evaluations", response_model=EvaluationListResponse)
def get_idea_evaluations(
    idea_id: UUID,
    current_user: User = Depends(get_current_user),
    service: IdeaService = Depends(get_idea_service)
):
    """
    Get all evaluations for an idea.
    
    Returns evaluation history ordered by created_at descending.
    
    Args:
        idea_id: Idea UUID
        current_user: Authenticated user
        service: Idea service
        
    Returns:
        List of evaluations with evaluator info
        
    Raises:
        404: If idea not found
    """
    logger.info(f"Fetching evaluations for idea {idea_id} by user {current_user.email}")
    
    evaluations = service.get_evaluations(idea_id)
    
    return EvaluationListResponse(
        evaluations=[
            EvaluationResponse.from_orm_with_evaluator(eval)
            for eval in evaluations
        ],
        total=len(evaluations)
    )
