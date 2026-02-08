"""
Keyboards package
"""
from bot.keyboards.inline import (
    main_menu_keyboard,
    settings_keyboard,
    language_keyboard,
    admin_menu_keyboard,
    confirm_keyboard,
    pagination_keyboard
)

from bot.keyboards.reply import (
    main_menu_reply_keyboard,
    cancel_keyboard,
    skip_keyboard,
    contact_keyboard,
    location_keyboard,
    remove_keyboard
)

__all__ = [
    'main_menu_keyboard',
    'settings_keyboard',
    'language_keyboard',
    'admin_menu_keyboard',
    'confirm_keyboard',
    'pagination_keyboard',
    'main_menu_reply_keyboard',
    'cancel_keyboard',
    'skip_keyboard',
    'contact_keyboard',
    'location_keyboard',
    'remove_keyboard'
]
