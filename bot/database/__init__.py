"""
Database package
"""
from bot.database.manager import db
from bot.database.models import User, Message, Statistic, Subscription

__all__ = ['db', 'User', 'Message', 'Statistic', 'Subscription']
