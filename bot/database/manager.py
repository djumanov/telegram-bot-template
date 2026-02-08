"""
Database manager with CRUD operations
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session

from bot.config import settings
from bot.database.models import Base, User, Message, Statistic, Subscription


class DatabaseManager:
    """Database manager for all database operations"""
    
    def __init__(self):
        self.engine = create_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True
        )
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
    
    @contextmanager
    def session_scope(self):
        """Provide transactional scope for database operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ==================== User Operations ====================
    
    def get_or_create_user(
        self,
        user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        language: str = None
    ) -> User:
        """Get existing user or create new one"""
        with self.session_scope() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            
            if not user:
                user = User(
                    user_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    language=language or settings.default_language
                )
                session.add(user)
                session.flush()
            else:
                # Update user info
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.last_activity = datetime.now()
            
            session.expunge(user)
            return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with self.session_scope() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                session.expunge(user)
            return user
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user fields"""
        with self.session_scope() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = datetime.now()
                session.expunge(user)
            return user
    
    def get_all_users(self, is_blocked: bool = None) -> List[User]:
        """Get all users"""
        with self.session_scope() as session:
            query = session.query(User)
            if is_blocked is not None:
                query = query.filter_by(is_blocked=is_blocked)
            users = query.all()
            for user in users:
                session.expunge(user)
            return users
    
    def set_user_language(self, user_id: int, language: str):
        """Set user language"""
        self.update_user(user_id, language=language)
    
    def block_user(self, user_id: int):
        """Block user"""
        self.update_user(user_id, is_blocked=True)
    
    def unblock_user(self, user_id: int):
        """Unblock user"""
        self.update_user(user_id, is_blocked=False)
    
    def set_admin(self, user_id: int, is_admin: bool = True):
        """Set user admin status"""
        self.update_user(user_id, is_admin=is_admin)
    
    def set_premium(self, user_id: int, is_premium: bool = True):
        """Set user premium status"""
        self.update_user(user_id, is_premium=is_premium)
    
    # ==================== Message Operations ====================
    
    def add_message(
        self,
        user_id: int,
        message_type: str,
        text: str = None,
        data: Dict = None
    ):
        """Add message to database"""
        with self.session_scope() as session:
            message = Message(
                user_id=user_id,
                message_type=message_type,
                text=text,
                data=data or {}
            )
            session.add(message)
    
    def get_user_messages(self, user_id: int, limit: int = 100) -> List[Message]:
        """Get user messages"""
        with self.session_scope() as session:
            messages = session.query(Message)\
                .filter_by(user_id=user_id)\
                .order_by(Message.created_at.desc())\
                .limit(limit)\
                .all()
            for msg in messages:
                session.expunge(msg)
            return messages
    
    def get_messages_count(self, user_id: int = None) -> int:
        """Get total messages count"""
        with self.session_scope() as session:
            query = session.query(Message)
            if user_id:
                query = query.filter_by(user_id=user_id)
            return query.count()
    
    # ==================== Statistics Operations ====================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics"""
        with self.session_scope() as session:
            total_users = session.query(User).count()
            active_users = session.query(User).filter_by(is_blocked=False).count()
            blocked_users = session.query(User).filter_by(is_blocked=True).count()
            total_messages = session.query(Message).count()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'blocked_users': blocked_users,
                'total_messages': total_messages
            }
    
    def save_daily_statistics(self):
        """Save daily statistics"""
        stats = self.get_statistics()
        
        with self.session_scope() as session:
            statistic = Statistic(
                date=datetime.now(),
                total_users=stats['total_users'],
                active_users=stats['active_users'],
                blocked_users=stats['blocked_users'],
                total_messages=stats['total_messages']
            )
            session.add(statistic)
    
    # ==================== Subscription Operations ====================
    
    def create_subscription(
        self,
        user_id: int,
        plan: str,
        expires_at: datetime = None,
        **kwargs
    ) -> Subscription:
        """Create new subscription"""
        with self.session_scope() as session:
            subscription = Subscription(
                user_id=user_id,
                plan=plan,
                status='active',
                expires_at=expires_at,
                **kwargs
            )
            session.add(subscription)
            session.flush()
            session.expunge(subscription)
            return subscription
    
    def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """Get user's active subscription"""
        with self.session_scope() as session:
            sub = session.query(Subscription)\
                .filter_by(user_id=user_id, status='active')\
                .order_by(Subscription.created_at.desc())\
                .first()
            if sub:
                session.expunge(sub)
            return sub


# Global database instance
db = DatabaseManager()
