"""
Inline keyboards with internationalization support
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.locales import i18n
from bot.config import CallbackPrefix, settings


def main_menu_keyboard(language: str = None) -> InlineKeyboardMarkup:
    """Main menu inline keyboard"""
    keyboard = [
        [InlineKeyboardButton(
            i18n.get_menu('statistics', language),
            callback_data=f'{CallbackPrefix.MENU}:stats'
        )],
        [InlineKeyboardButton(
            i18n.get_menu('settings', language),
            callback_data=f'{CallbackPrefix.MENU}:settings'
        )],
        [InlineKeyboardButton(
            i18n.get_menu('help', language),
            callback_data=f'{CallbackPrefix.MENU}:help'
        )],
    ]
    return InlineKeyboardMarkup(keyboard)


def settings_keyboard(language: str = None) -> InlineKeyboardMarkup:
    """Settings keyboard"""
    keyboard = [
        [InlineKeyboardButton(
            i18n.get('settings.language', language),
            callback_data=f'{CallbackPrefix.SETTINGS}:language'
        )],
        [InlineKeyboardButton(
            i18n.get('settings.notifications', language),
            callback_data=f'{CallbackPrefix.SETTINGS}:notifications'
        )],
        [InlineKeyboardButton(
            i18n.get_button('back', language),
            callback_data=f'{CallbackPrefix.MENU}:main'
        )],
    ]
    return InlineKeyboardMarkup(keyboard)


def language_keyboard(current_language: str = None) -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = []
    
    languages = i18n.get_available_languages()
    
    for code, name in languages.items():
        # Add checkmark for current language
        text = f"✅ {name}" if code == current_language else name
        keyboard.append([InlineKeyboardButton(
            text,
            callback_data=f'{CallbackPrefix.LANGUAGE}:{code}'
        )])
    
    keyboard.append([InlineKeyboardButton(
        i18n.get_button('back', current_language),
        callback_data=f'{CallbackPrefix.SETTINGS}:main'
    )])
    
    return InlineKeyboardMarkup(keyboard)


def admin_menu_keyboard(language: str = None) -> InlineKeyboardMarkup:
    """Admin panel keyboard"""
    keyboard = [
        [InlineKeyboardButton(
            i18n.get('admin.statistics', language),
            callback_data=f'{CallbackPrefix.ADMIN}:stats'
        )],
        [InlineKeyboardButton(
            i18n.get('admin.users', language),
            callback_data=f'{CallbackPrefix.ADMIN}:users'
        )],
        [InlineKeyboardButton(
            i18n.get('admin.broadcast', language),
            callback_data=f'{CallbackPrefix.ADMIN}:broadcast'
        )],
        [InlineKeyboardButton(
            i18n.get_button('back', language),
            callback_data=f'{CallbackPrefix.MENU}:main'
        )],
    ]
    return InlineKeyboardMarkup(keyboard)


def confirm_keyboard(action: str, language: str = None) -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                i18n.get_button('confirm', language),
                callback_data=f'{CallbackPrefix.CONFIRM}:{action}'
            ),
            InlineKeyboardButton(
                i18n.get_button('cancel', language),
                callback_data=f'{CallbackPrefix.CANCEL}:{action}'
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def pagination_keyboard(
    page: int,
    total_pages: int,
    prefix: str = 'page',
    language: str = None
) -> InlineKeyboardMarkup:
    """Pagination keyboard"""
    keyboard = []
    
    buttons = []
    
    if page > 0:
        buttons.append(InlineKeyboardButton(
            "◀️",
            callback_data=f'{CallbackPrefix.PAGE}:{prefix}:{page-1}'
        ))
    
    buttons.append(InlineKeyboardButton(
        f"{page+1}/{total_pages}",
        callback_data='current_page'
    ))
    
    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton(
            "▶️",
            callback_data=f'{CallbackPrefix.PAGE}:{prefix}:{page+1}'
        ))
    
    keyboard.append(buttons)
    keyboard.append([InlineKeyboardButton(
        i18n.get_button('back', language),
        callback_data=f'{CallbackPrefix.MENU}:main'
    )])
    
    return InlineKeyboardMarkup(keyboard)
