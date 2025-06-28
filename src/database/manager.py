"""
Database manager for CleanNet Shield
"""

import logging
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from .models import Base, User, BlockingRule

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str = "sqlite:///cleannet_shield.db"):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()

    def _initialize_database(self):
        try:
            self.engine = create_engine(
                self.database_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=300
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    @contextmanager
    def get_session(self) -> Session:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def create_user(self, username: str, email: str, password_hash: str, is_admin: bool = False) -> Optional[User]:
        try:
            with self.get_session() as session:
                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    is_admin=is_admin
                )
                session.add(user)
                session.flush()
                session.refresh(user)
                session.expunge(user)
                return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to create user: {e}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    session.expunge(user)
                return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to get user: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                if user:
                    session.expunge(user)
                return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to get user: {e}")
            return None

    def create_blocking_rule(self, user_id: int, domain: str, category: str = None, risk_score: float = 0.0) -> Optional[BlockingRule]:
        try:
            with self.get_session() as session:
                rule = BlockingRule(
                    user_id=user_id,
                    domain=domain,
                    category=category,
                    risk_score=risk_score
                )
                session.add(rule)
                session.flush()
                session.refresh(rule)
                session.expunge(rule)
                return rule
        except SQLAlchemyError as e:
            logger.error(f"Failed to create blocking rule: {e}")
            return None

    def get_blocking_rules_for_user(self, user_id: int) -> List[BlockingRule]:
        try:
            with self.get_session() as session:
                rules = session.query(BlockingRule).filter(BlockingRule.user_id == user_id).all()
                for rule in rules:
                    session.expunge(rule)
                return rules
        except SQLAlchemyError as e:
            logger.error(f"Failed to get blocking rules: {e}")
            return []

    def create_network_event(self, user_id: int, event_type: str, domain: str = None, details: dict = None) -> Optional['NetworkEvent']:
        try:
            with self.get_session() as session:
                from .models import NetworkEvent
                event = NetworkEvent(
                    user_id=user_id,
                    event_type=event_type,
                    domain=domain,
                    details=details
                )
                session.add(event)
                session.flush()
                session.refresh(event)
                session.expunge(event)
                return event
        except SQLAlchemyError as e:
            logger.error(f"Failed to create network event: {e}")
            return None 