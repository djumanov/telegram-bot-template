"""
Application constants
"""

# Conversation States
class ConversationState:
    """Conversation handler states"""
    # Registration
    REGISTRATION_NAME = 0
    REGISTRATION_AGE = 1
    REGISTRATION_PHONE = 2
    REGISTRATION_CITY = 3
    
    # Feedback
    FEEDBACK_MESSAGE = 10
    FEEDBACK_RATING = 11
    
    # Broadcast
    BROADCAST_MESSAGE = 20
    BROADCAST_CONFIRM = 21


# Callback Data Prefixes
class CallbackPrefix:
    """Callback query data prefixes"""
    MENU = "menu"
    SETTINGS = "settings"
    LANGUAGE = "lang"
    ADMIN = "admin"
    CONFIRM = "confirm"
    CANCEL = "cancel"
    PAGE = "page"


# User Roles
class UserRole:
    """User role types"""
    USER = "user"
    PREMIUM = "premium"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


# Cache Keys
class CacheKey:
    """Redis cache key templates"""
    USER_DATA = "user:{user_id}:data"
    USER_LANGUAGE = "user:{user_id}:language"
    USER_STATE = "user:{user_id}:state"
    STATISTICS = "stats:general"


# Limits
class Limits:
    """Application limits"""
    MAX_MESSAGE_LENGTH = 4096
    MAX_CAPTION_LENGTH = 1024
    MAX_BUTTONS_PER_ROW = 8
    MAX_INLINE_BUTTONS = 100
    ITEMS_PER_PAGE = 10


# Time Constants (seconds)
class Time:
    """Time constants in seconds"""
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000


# Message Templates
class Messages:
    """Common message templates"""
    ERROR_GENERIC = "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring."
    ERROR_PERMISSION = "⛔️ Sizda bu amalni bajarish uchun ruxsat yo'q."
    ERROR_NOT_FOUND = "❌ Topilmadi."
    SUCCESS_SAVED = "✅ Saqlandi."
    SUCCESS_DELETED = "✅ O'chirildi."
    PROCESSING = "⏳ Qayta ishlanmoqda..."
    CANCELLED = "❌ Bekor qilindi."
    