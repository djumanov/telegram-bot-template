"""
Database models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language = Column(String(10), default='uz')
    
    # Roles and permissions
    is_admin = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    
    # Settings
    notifications_enabled = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_activity = Column(DateTime, default=datetime.now)
    
    # Additional data
    data = Column(JSON, default={})
    
    def __repr__(self):
        return f'<User {self.user_id} - {self.first_name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'language': self.language,
            'is_admin': self.is_admin,
            'is_premium': self.is_premium,
            'is_blocked': self.is_blocked,
            'notifications_enabled': self.notifications_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
        }


class Message(Base):
    """Message model for tracking user messages"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    message_type = Column(String(50))  # text, photo, document, etc.
    text = Column(Text, nullable=True)
    data = Column(JSON, default={})  # Additional message data
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Message {self.id} from {self.user_id}>'


class Statistic(Base):
    """Statistics model"""
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now, index=True)
    
    # User statistics
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    blocked_users = Column(Integer, default=0)
    
    # Message statistics
    total_messages = Column(Integer, default=0)
    text_messages = Column(Integer, default=0)
    media_messages = Column(Integer, default=0)
    
    # Additional data
    data = Column(JSON, default={})
    
    def __repr__(self):
        return f'<Statistic {self.date}>'


class Subscription(Base):
    """Subscription model for premium features"""
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Subscription details
    plan = Column(String(50))  # basic, premium, vip
    status = Column(String(20))  # active, expired, cancelled
    
    # Dates
    started_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)
    
    # Payment
    amount = Column(Integer, default=0)
    currency = Column(String(10), default='UZS')
    payment_method = Column(String(50), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Subscription {self.user_id} - {self.plan}>'
    
    @property
    def is_active(self):
        """Check if subscription is active"""
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < datetime.now():
            return False
        return True
    