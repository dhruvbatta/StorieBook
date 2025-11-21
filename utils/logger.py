"""
Logging Utility
Provides structured logging for the application
"""

import logging
import sys
from typing import Optional
from utils.constants import LOG_LEVEL, LOG_FORMAT


class Logger:
    """Singleton logger class for consistent logging across the application"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "StorieBook") -> logging.Logger:
        """
        Get or create a logger instance
        
        Args:
            name: Logger name (default: "StorieBook")
            
        Returns:
            Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(name)
        return cls._instance
    
    @staticmethod
    def _create_logger(name: str) -> logging.Logger:
        """
        Create and configure a logger
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Set log level
        log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        
        return logger


# Convenience function for getting logger
def get_logger(name: str = "StorieBook") -> logging.Logger:
    """
    Convenience function to get logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return Logger.get_logger(name)


# Module-level logger instance
logger = get_logger()
