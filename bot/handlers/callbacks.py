"""
Callback query handlers for inline buttons
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import parse_callback_data, format_statistics
from bot.keyboards import (
    main_menu_keyboard,
    settings_keyboard,
    language_keyboard,
    admin_menu_keyboard
)
from bot.locales import i18n
from bot.database import db
from bot.config import CallbackPrefix, settings

logger = logging.getLogger(__name__)


def get_user_language(update: Update) -> str:
    """Get user's language"""
    user_id = update.callback_query.from_user.id
    user = db.get_user(user_id)
    return user.language if user else settings.default_language


def main_callback_handler(update: Update, context: CallbackContext):
    """Handle all callback queries"""
    query = update.callback_query
    query.answer()
    
    # Parse callback data
    data = parse_callback_data(query.data)
    prefix = data['prefix']
    action = data['action']
    param = data['param']
    
    language = get_user_language(update)
    
    # Route to specific handler based on prefix
    if prefix == CallbackPrefix.MENU:
        handle_menu_callback(query, action, language)
    
    elif prefix == CallbackPrefix.SETTINGS:
        handle_settings_callback(query, action, language)
    
    elif prefix == CallbackPrefix.LANGUAGE:
        handle_language_callback(query, action, language)
    
    elif prefix == CallbackPrefix.ADMIN:
        handle_admin_callback(query, action, language)
    
    elif prefix == CallbackPrefix.PAGE:
        handle_pagination_callback(query, action, param, language)
    
    elif prefix == CallbackPrefix.CONFIRM:
        # Confirmation callbacks handled in respective modules
        pass
    
    elif prefix == CallbackPrefix.CANCEL:
        query.edit_message_text(
            i18n.get('info.cancelled', language)
        )


def handle_menu_callback(query, action: str, language: str):
    """Handle menu navigation callbacks"""
    
    if action == 'main':
        query.edit_message_text(
            i18n.get('menu.main', language),
            reply_markup=main_menu_keyboard(language)
        )
    
    elif action == 'stats':
        stats = db.get_statistics()
        from bot.utils import format_statistics
        text = format_statistics(stats, language)
        
        query.edit_message_text(
            text,
            reply_markup=main_menu_keyboard(language)
        )
    
    elif action == 'settings':
        query.edit_message_text(
            i18n.get('settings.title', language),
            reply_markup=settings_keyboard(language)
        )
    
    elif action == 'help':
        query.edit_message_text(
            i18n.get('commands.help.message', language),
            reply_markup=main_menu_keyboard(language)
        )


def handle_settings_callback(query, action: str, language: str):
    """Handle settings callbacks"""
    user_id = query.from_user.id
    
    if action == 'main':
        query.edit_message_text(
            i18n.get('settings.title', language),
            reply_markup=settings_keyboard(language)
        )
    
    elif action == 'language':
        query.edit_message_text(
            i18n.get('settings.language', language),
            reply_markup=language_keyboard(language)
        )
    
    elif action == 'notifications':
        user = db.get_user(user_id)
        
        if user:
            # Toggle notifications
            new_state = not user.notifications_enabled
            db.update_user(user_id, notifications_enabled=new_state)
            
            if new_state:
                text = i18n.get('settings.notifications_enabled', language)
            else:
                text = i18n.get('settings.notifications_disabled', language)
            
            query.answer(text, show_alert=True)
            
            # Update keyboard
            query.edit_message_text(
                i18n.get('settings.title', language),
                reply_markup=settings_keyboard(language)
            )


def handle_language_callback(query, action: str, current_language: str):
    """Handle language selection callbacks"""
    user_id = query.from_user.id
    new_language = action
    
    # Validate language
    if new_language not in settings.available_languages:
        query.answer("Invalid language")
        return
    
    # Update user language
    db.set_user_language(user_id, new_language)
    
    # Show success message
    language_name = i18n.get_language_name(new_language)
    success_msg = i18n.get('settings.language_changed', new_language, 
        language=language_name
    )
    
    query.answer(success_msg, show_alert=True)
    
    # Update keyboard with new language
    query.edit_message_text(
        i18n.get('settings.language', new_language),
        reply_markup=language_keyboard(new_language)
    )


def handle_admin_callback(query, action: str, language: str):
    """Handle admin panel callbacks"""
    user_id = query.from_user.id
    
    # Check if user is admin
    if not settings.is_admin(user_id):
        query.answer(
            i18n.get_error('permission_denied', language),
            show_alert=True
        )
        return
    
    if action == 'stats':
        stats = db.get_statistics()
        from bot.utils import format_statistics
        text = format_statistics(stats, language)
        
        query.edit_message_text(
            text,
            reply_markup=admin_menu_keyboard(language)
        )
    
    elif action == 'users':
        users = db.get_all_users()
        text = f"👥 Total Users: {len(users)}\n\n"
        text += "Use /users command for detailed list"
        
        query.edit_message_text(
            text,
            reply_markup=admin_menu_keyboard(language)
        )
    
    elif action == 'broadcast':
        text = "📨 Broadcast\n\nUse /broadcast command to start"
        
        query.edit_message_text(
            text,
            reply_markup=admin_menu_keyboard(language)
        )


def handle_pagination_callback(query, prefix: str, page: str, language: str):
    """Handle pagination callbacks"""
    try:
        page_num = int(page)
    except ValueError:
        query.answer("Invalid page")
        return
    
    # Here you would load the appropriate data based on prefix
    # Example: if prefix == 'users', load users for that page
    
    query.answer(f"Page {page_num + 1}")
    