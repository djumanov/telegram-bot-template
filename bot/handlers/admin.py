"""
Admin panel handlers
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.utils import admin_only, super_admin_only, format_statistics, format_user_info
from bot.keyboards import admin_menu_keyboard, confirm_keyboard
from bot.locales import i18n
from bot.database import db
from bot.config import ConversationState, settings

logger = logging.getLogger(__name__)


def get_user_language(update: Update) -> str:
    """Get user's language"""
    user = db.get_user(update.effective_user.id)
    return user.language if user else settings.default_language


@admin_only
def admin_command(update: Update, context: CallbackContext):
    """Handle /admin command"""
    language = get_user_language(update)
    message = i18n.get('commands.admin.message', language)
    
    update.message.reply_text(
        message,
        reply_markup=admin_menu_keyboard(language)
    )


@admin_only
def admin_stats_command(update: Update, context: CallbackContext):
    """Handle /adminstats command"""
    language = get_user_language(update)
    stats = db.get_statistics()
    text = format_statistics(stats, language)
    
    update.message.reply_text(text)


@admin_only
def users_list_command(update: Update, context: CallbackContext):
    """Handle /users command - list all users"""
    from bot.utils import calculate_pagination
    
    language = get_user_language(update)
    users = db.get_all_users()
    
    page = int(context.args[0]) if context.args else 0
    pagination = calculate_pagination(len(users), current_page=page)
    
    text = f"👥 {i18n.get('admin.users', language)}\n\n"
    text += f"Total: {len(users)}\n"
    text += f"Page: {pagination['current_page'] + 1}/{pagination['total_pages']}\n\n"
    
    for i, user in enumerate(users[pagination['start_index']:pagination['end_index']], 1):
        status = "✅" if not user.is_blocked else "⛔️"
        admin_badge = "👨‍💼" if user.is_admin else ""
        premium_badge = "⭐️" if user.is_premium else ""
        
        text += f"{i}. {status} {admin_badge}{premium_badge} {user.first_name} "
        text += f"(@{user.username or 'N/A'}) - {user.user_id}\n"
    
    update.message.reply_text(text)


@admin_only
def user_info_command(update: Update, context: CallbackContext):
    """Handle /userinfo <user_id> command"""
    from bot.utils import is_valid_user_id
    
    language = get_user_language(update)
    
    if not context.args:
        update.message.reply_text(
            "Usage: /userinfo <user_id>"
        )
        return
    
    user_id_str = context.args[0]
    
    if not is_valid_user_id(user_id_str):
        update.message.reply_text(
            i18n.get('errors.invalid_input', language)
        )
        return
    
    user_id = int(user_id_str)
    user = db.get_user(user_id)
    
    if not user:
        update.message.reply_text(
            i18n.get('errors.not_found', language)
        )
        return
    
    text = format_user_info(user, language)
    
    # Add user statistics
    message_count = db.get_messages_count(user_id)
    text += f"\n💬 Messages: {message_count}"
    
    update.message.reply_text(text)


@super_admin_only
def block_user_command(update: Update, context: CallbackContext):
    """Handle /block <user_id> command"""
    from bot.utils import is_valid_user_id
    
    language = get_user_language(update)
    
    if not context.args:
        update.message.reply_text("Usage: /block <user_id>")
        return
    
    user_id_str = context.args[0]
    
    if not is_valid_user_id(user_id_str):
        update.message.reply_text(
            i18n.get('errors.invalid_input', language)
        )
        return
    
    user_id = int(user_id_str)
    db.block_user(user_id)
    
    update.message.reply_text(
        f"✅ User {user_id} blocked"
    )
    logger.info(f"Admin {update.effective_user.id} blocked user {user_id}")


@super_admin_only
def unblock_user_command(update: Update, context: CallbackContext):
    """Handle /unblock <user_id> command"""
    from bot.utils import is_valid_user_id
    
    language = get_user_language(update)
    
    if not context.args:
        update.message.reply_text("Usage: /unblock <user_id>")
        return
    
    user_id_str = context.args[0]
    
    if not is_valid_user_id(user_id_str):
        update.message.reply_text(
            i18n.get('errors.invalid_input', language)
        )
        return
    
    user_id = int(user_id_str)
    db.unblock_user(user_id)
    
    update.message.reply_text(
        f"✅ User {user_id} unblocked"
    )
    logger.info(f"Admin {update.effective_user.id} unblocked user {user_id}")


# ==================== BROADCAST CONVERSATION ====================

@admin_only
def broadcast_start(update: Update, context: CallbackContext):
    """Start broadcast conversation"""
    from bot.keyboards import cancel_keyboard
    
    language = get_user_language(update)
    
    update.message.reply_text(
        i18n.get('admin.broadcast_start', language),
        reply_markup=cancel_keyboard(language)
    )
    
    return ConversationState.BROADCAST_MESSAGE


def broadcast_message_handler(update: Update, context: CallbackContext):
    """Handle broadcast message"""
    language = get_user_language(update)
    message_text = update.message.text
    
    if message_text == i18n.get_button('cancel', language):
        update.message.reply_text(
            i18n.get('admin.broadcast_cancelled', language)
        )
        return ConversationHandler.END
    
    # Store message in context
    context.user_data['broadcast_message'] = message_text
    
    # Get user count
    users = db.get_all_users(is_blocked=False)
    user_count = len(users)
    
    update.message.reply_text(
        i18n.get('admin.broadcast_confirm', language, count=user_count),
        reply_markup=confirm_keyboard('broadcast', language)
    )
    
    return ConversationState.BROADCAST_CONFIRM


def broadcast_confirm_handler(update: Update, context: CallbackContext):
    """Confirm and send broadcast"""
    query = update.callback_query
    query.answer()
    
    language = get_user_language(update)
    
    if query.data.startswith('cancel:'):
        query.edit_message_text(
            i18n.get('admin.broadcast_cancelled', language)
        )
        return ConversationHandler.END
    
    # Get message from context
    message_text = context.user_data.get('broadcast_message')
    
    if not message_text:
        query.edit_message_text(
            i18n.get_error('generic', language)
        )
        return ConversationHandler.END
    
    # Send to all users
    users = db.get_all_users(is_blocked=False)
    
    success_count = 0
    failed_count = 0
    
    for user in users:
        try:
            context.bot.send_message(chat_id=user.user_id, text=message_text)
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send broadcast to {user.user_id}: {e}")
            failed_count += 1
    
    result_text = i18n.get('admin.broadcast_success', language,
        success=success_count,
        failed=failed_count
    )
    
    query.edit_message_text(result_text)
    
    logger.info(
        f"Admin {update.effective_user.id} sent broadcast: "
        f"{success_count} success, {failed_count} failed"
    )
    
    return ConversationHandler.END


def broadcast_cancel(update: Update, context: CallbackContext):
    """Cancel broadcast"""
    language = get_user_language(update)
    
    update.message.reply_text(
        i18n.get('admin.broadcast_cancelled', language)
    )
    
    return ConversationHandler.END
