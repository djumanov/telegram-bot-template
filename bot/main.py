"""
Main bot application
"""
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

from bot.config import settings, ConversationState
from bot.utils import setup_logging
from bot.handlers import (
    # Basic
    start_command,
    help_command,
    menu_command,
    profile_command,
    settings_command,
    stats_command,
    # Admin
    admin_command,
    admin_stats_command,
    users_list_command,
    user_info_command,
    block_user_command,
    unblock_user_command,
    broadcast_start,
    broadcast_message_handler,
    broadcast_confirm_handler,
    broadcast_cancel,
    # Callbacks
    main_callback_handler
)

logger = logging.getLogger(__name__)


def error_handler(update, context):
    """Handle errors"""
    logger.error(f'Update {update} caused error {context.error}', exc_info=context.error)
    
    try:
        if update and update.effective_message:
            update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error in error_handler: {e}")


def main():
    """Start the bot"""
    # Setup logging
    setup_logging()
    
    logger.info("=" * 50)
    logger.info("Starting Telegram Bot")
    logger.info("=" * 50)
    logger.info(f"Bot token: {settings.bot_token[:10]}...")
    logger.info(f"Admin IDs: {settings.admin_ids}")
    logger.info(f"Default language: {settings.default_language}")
    logger.info(f"Available languages: {settings.available_languages}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info("=" * 50)
    
    # Create updater
    updater = Updater(settings.bot_token, use_context=True)
    dp = updater.dispatcher
    
    # ==================== Basic Commands ====================
    logger.info("Registering basic handlers...")
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('menu', menu_command))
    dp.add_handler(CommandHandler('profile', profile_command))
    dp.add_handler(CommandHandler('settings', settings_command))
    dp.add_handler(CommandHandler('stats', stats_command))
    
    # ==================== Admin Commands ====================
    logger.info("Registering admin handlers...")
    dp.add_handler(CommandHandler('admin', admin_command))
    dp.add_handler(CommandHandler('adminstats', admin_stats_command))
    dp.add_handler(CommandHandler('users', users_list_command))
    dp.add_handler(CommandHandler('userinfo', user_info_command))
    dp.add_handler(CommandHandler('block', block_user_command))
    dp.add_handler(CommandHandler('unblock', unblock_user_command))
    
    # ==================== Broadcast Conversation ====================
    logger.info("Registering broadcast conversation...")
    broadcast_conv = ConversationHandler(
        entry_points=[CommandHandler('broadcast', broadcast_start)],
        states={
            ConversationState.BROADCAST_MESSAGE: [
                MessageHandler(Filters.text & ~Filters.command, broadcast_message_handler)
            ],
            ConversationState.BROADCAST_CONFIRM: [
                CallbackQueryHandler(broadcast_confirm_handler, pattern='^(confirm|cancel):broadcast$')
            ]
        },
        fallbacks=[CommandHandler('cancel', broadcast_cancel)]
    )
    dp.add_handler(broadcast_conv)
    
    # ==================== Callback Handlers ====================
    logger.info("Registering callback handlers...")
    dp.add_handler(CallbackQueryHandler(main_callback_handler))
    
    # ==================== Error Handler ====================
    dp.add_error_handler(error_handler)
    
    # ==================== Start Bot ====================
    if settings.enable_webhooks and settings.webhook_url:
        logger.info(f"Starting in WEBHOOK mode: {settings.webhook_url}")
        updater.start_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=settings.bot_token,
            webhook_url=f"{settings.webhook_url}/{settings.bot_token}"
        )
    else:
        logger.info("Starting in POLLING mode")
        updater.start_polling(drop_pending_updates=True)
    
    logger.info("=" * 50)
    logger.info("✅ Bot started successfully!")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 50)
    
    updater.idle()
    
    logger.info("Bot stopped")


if __name__ == '__main__':
    main()
    