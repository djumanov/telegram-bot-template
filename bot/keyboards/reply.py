"""
Reply keyboards with internationalization support
"""
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot.locales import i18n


def main_menu_reply_keyboard(is_admin: bool = False, language: str = None) -> ReplyKeyboardMarkup:
    """Main menu reply keyboard"""
    keyboard = [
        [
            i18n.get_menu('statistics', language),
            i18n.get_menu('profile', language)
        ],
        [
            i18n.get_menu('settings', language),
            i18n.get_menu('help', language)
        ],
    ]
    
    if is_admin:
        keyboard.append([i18n.get_menu('admin', language)])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def cancel_keyboard(language: str = None) -> ReplyKeyboardMarkup:
    """Cancel keyboard"""
    keyboard = [[i18n.get_button('cancel', language)]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def skip_keyboard(language: str = None) -> ReplyKeyboardMarkup:
    """Skip keyboard"""
    keyboard = [
        [i18n.get_button('skip', language)],
        [i18n.get_button('cancel', language)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def contact_keyboard(language: str = None) -> ReplyKeyboardMarkup:
    """Request contact keyboard"""
    keyboard = [[
        KeyboardButton(
            "📱 " + i18n.get('buttons.share_contact', language) or "Share Contact",
            request_contact=True
        )
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def location_keyboard(language: str = None) -> ReplyKeyboardMarkup:
    """Request location keyboard"""
    keyboard = [[
        KeyboardButton(
            "📍 " + i18n.get('buttons.share_location', language) or "Share Location",
            request_location=True
        )
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    """Remove keyboard"""
    return ReplyKeyboardRemove()
