"""
Helper utility functions
"""
import logging
from datetime import datetime
from typing import List, Dict, Any
from bot.config import Limits

logger = logging.getLogger(__name__)


def format_user_info(user, language: str = None) -> str:
    """Format user information for display"""
    from bot.locales import i18n
    
    status = "Premium ⭐️" if user.is_premium else "Regular"
    if user.is_admin:
        status = "Admin 👨‍💼"
    
    return i18n.get('profile.info', language,
        name=user.first_name or 'N/A',
        username=f"@{user.username}" if user.username else 'N/A',
        user_id=user.user_id,
        language=user.language.upper(),
        created_at=user.created_at.strftime('%d.%m.%Y'),
        status=status
    )


def format_statistics(stats: Dict[str, int], language: str = None) -> str:
    """Format statistics for display"""
    from bot.locales import i18n
    
    return i18n.get('admin.stats_message', language,
        total_users=stats.get('total_users', 0),
        active_users=stats.get('active_users', 0),
        total_messages=stats.get('total_messages', 0)
    )


def split_message(text: str, max_length: int = Limits.MAX_MESSAGE_LENGTH) -> List[str]:
    """Split long message into chunks"""
    chunks = []
    
    while len(text) > max_length:
        # Find last newline before max_length
        split_pos = text.rfind('\n', 0, max_length)
        
        if split_pos == -1:
            split_pos = max_length
        
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    
    if text:
        chunks.append(text)
    
    return chunks


def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text


def get_user_link(user_id: int, username: str = None, first_name: str = None) -> str:
    """Generate user link for mentions"""
    if username:
        return f"@{username}"
    elif first_name:
        return f"[{first_name}](tg://user?id={user_id})"
    else:
        return f"User {user_id}"


def format_datetime(dt: datetime, format_str: str = '%d.%m.%Y %H:%M:%S') -> str:
    """Format datetime for display"""
    return dt.strftime(format_str) if dt else 'N/A'


def parse_command_args(text: str) -> str:
    """Parse command arguments from message text"""
    parts = text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ''


def is_valid_user_id(text: str) -> bool:
    """Check if text is valid user ID"""
    try:
        user_id = int(text)
        return user_id > 0
    except (ValueError, TypeError):
        return False


def calculate_pagination(
    total_items: int,
    items_per_page: int = Limits.ITEMS_PER_PAGE,
    current_page: int = 0
) -> Dict[str, Any]:
    """Calculate pagination parameters"""
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    current_page = max(0, min(current_page, total_pages - 1))
    
    start_index = current_page * items_per_page
    end_index = min(start_index + items_per_page, total_items)
    
    return {
        'total_pages': total_pages,
        'current_page': current_page,
        'start_index': start_index,
        'end_index': end_index,
        'has_prev': current_page > 0,
        'has_next': current_page < total_pages - 1,
        'items_per_page': items_per_page
    }


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_callback_data(callback_data: str) -> Dict[str, str]:
    """
    Parse callback data in format 'prefix:action:param'
    
    Returns:
        dict: {'prefix': 'menu', 'action': 'settings', 'param': 'language'}
    """
    parts = callback_data.split(':', 2)
    
    result = {
        'prefix': parts[0] if len(parts) > 0 else '',
        'action': parts[1] if len(parts) > 1 else '',
        'param': parts[2] if len(parts) > 2 else ''
    }
    
    return result


def build_callback_data(prefix: str, action: str = '', param: str = '') -> str:
    """Build callback data string"""
    parts = [prefix]
    
    if action:
        parts.append(action)
    if param:
        parts.append(param)
    
    return ':'.join(parts)


def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def validate_file_type(filename: str, allowed_types: List[str] = None) -> bool:
    """Validate file type against allowed types"""
    if not allowed_types:
        from bot.config import settings
        allowed_types = settings.allowed_file_types
    
    file_ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return file_ext in allowed_types


def send_typing_action(update, context):
    """Send typing action"""
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action='typing'
    )
    