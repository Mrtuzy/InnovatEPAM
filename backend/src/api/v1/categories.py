"""Category API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.repositories.category_repository import CategoryRepository
from src.schemas.category_schemas import CategoryResponse
from src.utils.logger import get_logger


logger = get_logger(__name__)
router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    """Dependency for category repository."""
    return CategoryRepository(db)


@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    include_inactive: bool = False,
    repository: CategoryRepository = Depends(get_category_repository)
):
    """
    Get all categories.
    
    Args:
        include_inactive: Whether to include inactive categories
        repository: Category repository
        
    Returns:
        List of categories sorted by display order
    """
    try:
        if include_inactive:
            categories = repository.get_all_categories(include_inactive=True)
        else:
            categories = repository.get_active_categories()
        
        logger.info(f"Retrieved {len(categories)} categories (include_inactive={include_inactive})")
        return categories
    
    except Exception as e:
        logger.error(f"Failed to get categories: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )
