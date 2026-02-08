"""
Decorators for handlers
"""
import logging
from functools import wraps
from typing import Callable

from bot.config import settings
from bot.database import db
from bot.locales import i18n

logger = logging.getLogger(__name__)


def get_user_language(update) -> str:
    """Get user's language"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    return user.language if user else settings.default_language


def admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to admin users only"""
    @wraps(func)
    def wrapper(update, context):
        user_id = update.effective_user.id
        
        if not settings.is_admin(user_id):
            language = get_user_language(update)
            update.message.reply_text(
                i18n.get_error('permission_denied', language)
            )
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            return
        
        return func(update, context)
    
    return wrapper


def super_admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to super admin only"""
    @wraps(func)
    def wrapper(update, context):
        user_id = update.effective_user.id
        
        if not settings.is_super_admin(user_id):
            language = get_user_language(update)
            update.message.reply_text(
                i18n.get_error('permission_denied', language)
            )
            logger.warning(f"Unauthorized super admin access by user {user_id}")
            return
        
        return func(update, context)
    
    return wrapper


def premium_only(func: Callable) -> Callable:
    """Decorator to restrict access to premium users only"""
    @wraps(func)
    def wrapper(update, context):
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if not (user and user.is_premium):
            language = get_user_language(update)
            update.message.reply_text(
                i18n.get('errors.premium_required', language) or
                "⭐️ This feature is for premium users only."
            )
            return
        
        return func(update, context)
    
    return wrapper


def track_user(func: Callable) -> Callable:
    """Decorator to track and update user information"""
    @wraps(func)
    def wrapper(update, context):
        user = update.effective_user
        
        # Get or create user in database
        db.get_or_create_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        return func(update, context)
    
    return wrapper


def check_blocked(func: Callable) -> Callable:
    """Decorator to check if user is blocked"""
    @wraps(func)
    def wrapper(update, context):
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if user and user.is_blocked:
            language = get_user_language(update)
            update.message.reply_text(
                i18n.get_error('user_blocked', language)
            )
            logger.warning(f"Blocked user {user_id} tried to use bot")
            return
        
        return func(update, context)
    
    return wrapper


def log_command(func: Callable) -> Callable:
    """Decorator to log command usage"""
    @wraps(func)
    def wrapper(update, context):
        user = update.effective_user
        message = update.message or update.callback_query.message
        text = message.text if message else 'callback'
        
        logger.info(
            f"User {user.id} ({user.username or user.first_name}) "
            f"executed: {text}"
        )
        
        # Save to database
        if message and message.text:
            message_type = 'command' if text.startswith('/') else 'text'
            db.add_message(user.id, message_type, text)
        
        return func(update, context)
    
    return wrapper


def error_handler_decorator(func: Callable) -> Callable:
    """Decorator to handle errors gracefully"""
    @wraps(func)
    def wrapper(update, context):
        try:
            return func(update, context)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            
            language = get_user_language(update)
            
            if update.message:
                update.message.reply_text(
                    i18n.get_error('generic', language)
                )
            elif update.callback_query:
                update.callback_query.answer(
                    i18n.get_error('generic', language),
                    show_alert=True
                )
    
    return wrapper


# Combined decorator for common use
def protected_handler(func: Callable) -> Callable:
    """
    Combined decorator: track user, check if blocked, log command, handle errors
    
    Usage:
        @protected_handler
        def my_handler(update, context):
            pass
    """
    return error_handler_decorator(
        log_command(
            check_blocked(
                track_user(func)
            )
        )
    )
