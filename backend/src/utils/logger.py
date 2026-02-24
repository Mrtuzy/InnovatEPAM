"""Structured logging configuration."""
import logging
import sys
from typing import Any

from src.config.settings import get_settings

settings = get_settings()


class StructuredLogger:
    """Structured logger with no sensitive data logging."""
    
    def __init__(self, name: str = "innovatepam"):
        """Initialize logger."""
        self.logger = logging.getLogger(name)
        self._configure()
    
    def _configure(self) -> None:
        """Configure logger with appropriate handlers."""
        # Set level
        level = logging.DEBUG if settings.DEBUG else logging.INFO
        self.logger.setLevel(level)
        
        # Avoid duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Format
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def _sanitize(self, data: Any) -> Any:
        """
        Remove sensitive data from logs.
        
        Args:
            data: Data to sanitize
            
        Returns:
            Sanitized data
        """
        if isinstance(data, dict):
            sensitive_keys = {
                'password',
                'hashed_password',
                'secret_key',
                'token',
                'refresh_token',
                'access_token',
            }
            return {
                k: '***REDACTED***' if k.lower() in sensitive_keys else v
                for k, v in data.items()
            }
        return data
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        sanitized = self._sanitize(kwargs)
        self.logger.debug(f"{message} {sanitized}" if sanitized else message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        sanitized = self._sanitize(kwargs)
        self.logger.info(f"{message} {sanitized}" if sanitized else message)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        sanitized = self._sanitize(kwargs)
        self.logger.warning(f"{message} {sanitized}" if sanitized else message)
    
    def error(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """Log error message."""
        sanitized = self._sanitize(kwargs)
        self.logger.error(
            f"{message} {sanitized}" if sanitized else message,
            exc_info=exc_info
        )


# Singleton instance
logger = StructuredLogger()
