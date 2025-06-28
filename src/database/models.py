"""
Database models for CleanNet Shield
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    blocking_rules = relationship("BlockingRule", back_populates="user")
    recovery_entries = relationship("RecoveryEntry", back_populates="user")
    network_events = relationship("NetworkEvent", back_populates="user")

class BlockingRule(Base):
    __tablename__ = 'blocking_rules'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    domain = Column(String(255), nullable=False)
    category = Column(String(50))
    risk_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="blocking_rules")

class NetworkEvent(Base):
    __tablename__ = 'network_events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String(50), nullable=False)
    source_ip = Column(String(45))
    destination_ip = Column(String(45))
    destination_port = Column(Integer)
    protocol = Column(String(10))
    bytes_sent = Column(Integer, default=0)
    bytes_received = Column(Integer, default=0)
    process_name = Column(String(100))
    risk_score = Column(Float, default=0.0)
    was_blocked = Column(Boolean, default=False)
    user = relationship("User", back_populates="network_events")

class RecoveryEntry(Base):
    __tablename__ = 'recovery_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    entry_type = Column(String(50), nullable=False)
    title = Column(String(200))
    content = Column(Text)
    mood_score = Column(Integer)
    triggers = Column(Text)
    coping_strategies = Column(Text)
    is_public = Column(Boolean, default=False)
    user = relationship("User", back_populates="recovery_entries")

class Streak(Base):
    __tablename__ = 'streaks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    streak_type = Column(String(50), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    start_date = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class SystemConfig(Base):
    __tablename__ = 'system_config'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(String(500))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    details = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True) 