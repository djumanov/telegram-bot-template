"""
Logging configuration
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

from bot.config import settings


def setup_logging():
    """Configure application logging"""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File Handler (rotating)
    file_handler = RotatingFileHandler(
        logs_dir / 'bot.log',
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    # JSON formatter for file logs
    json_format = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(json_format)
    
    # Error File Handler
    error_handler = RotatingFileHandler(
        logs_dir / 'errors.log',
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_format)
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Set specific logger levels
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")
    