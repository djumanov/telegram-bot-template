"""
Custom filters for message filtering
"""
from telegram.ext import MessageFilter
from bot.config import settings
from bot.database import db


class AdminFilter(MessageFilter):
    """Filter for admin users only"""
    
    def filter(self, message):
        user_id = message.from_user.id
        return settings.is_admin(user_id)


class SuperAdminFilter(MessageFilter):
    """Filter for super admin only"""
    
    def filter(self, message):
        user_id = message.from_user.id
        return settings.is_super_admin(user_id)


class PremiumFilter(MessageFilter):
    """Filter for premium users only"""
    
    def filter(self, message):
        user_id = message.from_user.id
        user = db.get_user(user_id)
        return user and user.is_premium


class NotBlockedFilter(MessageFilter):
    """Filter for non-blocked users"""
    
    def filter(self, message):
        user_id = message.from_user.id
        user = db.get_user(user_id)
        return not (user and user.is_blocked)


class PrivateChatFilter(MessageFilter):
    """Filter for private chat only"""
    
    def filter(self, message):
        return message.chat.type == 'private'


class GroupChatFilter(MessageFilter):
    """Filter for group chat only"""
    
    def filter(self, message):
        return message.chat.type in ['group', 'supergroup']


class LanguageFilter(MessageFilter):
    """Filter for specific language"""
    
    def __init__(self, language: str):
        self.language = language
    
    def filter(self, message):
        user_id = message.from_user.id
        user = db.get_user(user_id)
        return user and user.language == self.language


# Create filter instances
admin_filter = AdminFilter()
super_admin_filter = SuperAdminFilter()
premium_filter = PremiumFilter()
not_blocked_filter = NotBlockedFilter()
private_filter = PrivateChatFilter()
group_filter = GroupChatFilter()
