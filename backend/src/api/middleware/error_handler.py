"""Error handling middleware with standardized responses."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.utils.logger import logger


async def error_handler_middleware(
    request: Request,
    call_next
):
    """
    Global error handling middleware.
    
    Catches exceptions and returns standardized error responses.
    """
    try:
        return await call_next(request)
    except Exception as exc:
        return await handle_exception(exc)


async def handle_exception(exc: Exception) -> JSONResponse:
    """
    Handle different exception types.
    
    Args:
        exc: Exception instance
        
    Returns:
        JSONResponse with error details
    """
    # Log the exception
    logger.error(f"Exception occurred: {exc}", exc_info=True)
    
    # Handle validation errors
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        )
    
    # Handle database integrity errors
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "integrity_error",
                "message": "Database integrity constraint violated",
            }
        )
    
    # Handle other database errors
    if isinstance(exc, SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "database_error",
                "message": "Database operation failed",
            }
        )
    
    # Handle generic exceptions
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
        }
    )
