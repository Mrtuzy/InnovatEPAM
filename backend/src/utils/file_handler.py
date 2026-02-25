"""File handling utility for idea attachments."""
import os
import re
import uuid
from typing import Optional, Tuple
from pathlib import Path

from src.config.settings import get_settings
from src.utils.logger import logger

settings = get_settings()

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

# Allowed MIME types for attachments
ALLOWED_MIME_TYPES = {
    # Documents
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    # Spreadsheets
    'application/vnd.ms-excel': ['.xls'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    # Images
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/gif': ['.gif'],
}

# Flatten allowed extensions
ALLOWED_EXTENSIONS = set()
for extensions in ALLOWED_MIME_TYPES.values():
    ALLOWED_EXTENSIONS.update(extensions)


class FileHandler:
    """Utility class for file upload handling and validation."""
    
    @staticmethod
    def validate_file_type(filename: str, mimetype: str) -> bool:
        """
        Validate file type against allowed MIME types and extensions.
        
        Args:
            filename: Original filename
            mimetype: File MIME type from upload
            
        Returns:
            True if file type is allowed, False otherwise
        """
        # Get file extension
        ext = Path(filename).suffix.lower()
        
        # Check if extension is allowed
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning(f"File type validation failed: extension {ext} not allowed")
            return False
        
        # Check if MIME type is allowed
        if mimetype not in ALLOWED_MIME_TYPES:
            logger.warning(f"File type validation failed: MIME type {mimetype} not allowed")
            return False
        
        # Verify extension matches MIME type
        expected_extensions = ALLOWED_MIME_TYPES.get(mimetype, [])
        if ext not in expected_extensions:
            logger.warning(
                f"File type validation failed: extension {ext} doesn't match MIME type {mimetype}"
            )
            return False
        
        return True
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        Validate file size against maximum allowed size.
        
        Args:
            file_size: File size in bytes
            
        Returns:
            True if size is within limit, False otherwise
        """
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File size validation failed: {file_size} bytes exceeds {MAX_FILE_SIZE} bytes")
            return False
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal and other attacks.
        
        Removes dangerous characters and limits length.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename safe for storage
        """
        # Get just the filename (remove any path components)
        filename = os.path.basename(filename)
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove any character that isn't alphanumeric, underscore, dash, or dot
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        
        # Prevent double dots (path traversal attempt)
        filename = filename.replace('..', '.')
        
        # Limit filename length (keep extension)
        name, ext = os.path.splitext(filename)
        if len(name) > 200:
            name = name[:200]
        
        sanitized = name + ext
        
        # Ensure filename is not empty after sanitization
        if not sanitized or sanitized == ext:
            sanitized = f"file{ext}"
        
        return sanitized
    
    @staticmethod
    def generate_storage_path(idea_id: uuid.UUID, original_filename: str) -> Tuple[str, str]:
        """
        Generate unique storage path for file.
        
        Uses idea ID and unique suffix to prevent collisions.
        
        Args:
            idea_id: Idea UUID
            original_filename: Original filename (will be sanitized)
            
        Returns:
            Tuple of (relative_path, absolute_path)
        """
        # Sanitize filename
        safe_filename = FileHandler.sanitize_filename(original_filename)
        
        # Generate unique filename with UUID prefix
        unique_prefix = uuid.uuid4().hex[:8]
        name, ext = os.path.splitext(safe_filename)
        unique_filename = f"{unique_prefix}_{name}{ext}"
        
        # Create path structure: uploads/ideas/{idea_id}/{unique_filename}
        relative_path = os.path.join('ideas', str(idea_id), unique_filename)
        
        # Get absolute path from settings
        upload_dir = Path(settings.UPLOAD_DIR)
        absolute_path = upload_dir / relative_path
        
        # Ensure directory exists
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        
        return (relative_path, str(absolute_path))
    
    @staticmethod
    async def save_file(file_content: bytes, storage_path: str) -> bool:
        """
        Save file content to storage path.
        
        Args:
            file_content: Binary file content
            storage_path: Absolute filesystem path
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Ensure parent directory exists
            Path(storage_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(storage_path, 'wb') as f:
                f.write(file_content)
            
            logger.info(f"File saved successfully: {storage_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def get_file_path(relative_path: str) -> Optional[str]:
        """
        Get absolute file path from relative path.
        
        Args:
            relative_path: Relative path from storage
            
        Returns:
            Absolute path if file exists, None otherwise
        """
        upload_dir = Path(settings.UPLOAD_DIR)
        absolute_path = upload_dir / relative_path
        
        if absolute_path.exists() and absolute_path.is_file():
            return str(absolute_path)
        
        return None
    
    @staticmethod
    def delete_file(relative_path: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            relative_path: Relative path from storage
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            absolute_path = FileHandler.get_file_path(relative_path)
            if absolute_path:
                os.remove(absolute_path)
                logger.info(f"File deleted: {absolute_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}", exc_info=True)
            return False


# Singleton instance
file_handler = FileHandler()
