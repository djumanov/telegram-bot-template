"""
Basic command handlers
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import protected_handler, format_statistics
from bot.keyboards import main_menu_keyboard, main_menu_reply_keyboard
from bot.locales import i18n
from bot.database import db
from bot.config import settings

logger = logging.getLogger(__name__)


def get_user_language(update: Update) -> str:
    """Get user's preferred language"""
    user = db.get_user(update.effective_user.id)
    return user.language if user else settings.default_language


@protected_handler
def start_command(update: Update, context: CallbackContext):
    """Handle /start command"""
    user = update.effective_user
    language = get_user_language(update)
    is_admin = settings.is_admin(user.id)
    
    message = i18n.get('commands.start.message', language, name=user.first_name)
    
    update.message.reply_text(
        message,
        reply_markup=main_menu_reply_keyboard(is_admin, language)
    )


@protected_handler
def help_command(update: Update, context: CallbackContext):
    """Handle /help command"""
    language = get_user_language(update)
    message = i18n.get('commands.help.message', language)
    
    update.message.reply_text(message)


@protected_handler
def menu_command(update: Update, context: CallbackContext):
    """Handle /menu command"""
    language = get_user_language(update)
    message = i18n.get('commands.menu.message', language)
    
    update.message.reply_text(
        message,
        reply_markup=main_menu_keyboard(language)
    )


@protected_handler
def profile_command(update: Update, context: CallbackContext):
    """Handle /profile command"""
    from bot.utils import format_user_info
    
    user_id = update.effective_user.id
    language = get_user_language(update)
    
    user = db.get_user(user_id)
    
    if not user:
        update.message.reply_text(i18n.get_error('not_found', language))
        return
    
    text = format_user_info(user, language)
    update.message.reply_text(text)


@protected_handler
def settings_command(update: Update, context: CallbackContext):
    """Handle /settings command"""
    from bot.keyboards import settings_keyboard
    
    language = get_user_language(update)
    message = i18n.get('commands.settings.message', language)
    
    update.message.reply_text(
        message,
        reply_markup=settings_keyboard(language)
    )


@protected_handler
def stats_command(update: Update, context: CallbackContext):
    """Handle /stats command"""
    language = get_user_language(update)
    stats = db.get_statistics()
    text = format_statistics(stats, language)
    
    update.message.reply_text(text)
    