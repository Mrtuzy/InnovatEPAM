"""Database session management and configuration."""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.config.settings import get_settings

settings = get_settings()

# Create database engine with connection pooling
# pool_pre_ping: Verifies connections before using them
# pool_size: Number of connections to keep in pool
# max_overflow: Maximum number of connections to create beyond pool_size
# pool_recycle: Recycle connections after this many seconds (prevents timeout)
# connect_args: Additional connection arguments
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,  # Recycle connections every hour
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"  # 30 second statement timeout
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=True  # Expire objects after commit for fresh queries
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    Yields a database session that is automatically closed after use.
    
    Usage in FastAPI endpoints:
        def endpoint(db: Session = Depends(get_db)):
            ...
    
    Yields:
        SQLAlchemy Session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
