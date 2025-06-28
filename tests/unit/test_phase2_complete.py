"""
Comprehensive Test Suite for Phase 2 Features
"""

import pytest
import asyncio
import json
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List

# Import all Phase 2 components
from src.core.recovery.relapse_predictor import RelapsePredictor, RelapsePrediction
from src.core.recovery.recommendation_engine import RecommendationEngine, RecoveryRecommendation, RecommendationType, RecommendationPriority
from src.core.blocker.enhanced_blocking_service import EnhancedBlockingService
from src.core.blocker.enhanced_platform_manager import EnhancedPlatformManager, EnhancedWindowsManager
from src.core.blocker.ai_classifier import AIDomainClassifier, DomainClassification
from src.core.monitoring.network_monitor import RealTimeNetworkMonitor, NetworkEvent
from src.database.manager import DatabaseManager
from src.database.models import User, BlockingRule, NetworkEvent as DBNetworkEvent


class TestRelapsePredictor:
    """Test the ML-based relapse prediction system"""
    
    @pytest.fixture
    def predictor(self):
        return RelapsePredictor()
    
    @pytest.fixture
    def sample_user_data(self):
        return {
            'current_streak': 15,
            'longest_streak': 30,
            'days_since_start': 45,
            'days_since_last_relapse': 15,
            'journal_entries_last_week': 5,
            'mood_scores_last_week': [4.0, 3.8, 4.2, 3.9, 4.1, 4.0, 3.7],
            'trigger_frequency': 2,
            'coping_strategy_usage': 4,
            'blocked_attempts_last_week': 1,
            'suspicious_connections': 0
        }
    
    def test_initialization(self, predictor):
        """Test predictor initialization"""
        assert predictor.model is not None
        assert predictor.scaler is not None
        assert predictor.logger is not None
    
    def test_extract_features(self, predictor, sample_user_data):
        """Test feature extraction"""
        features = predictor.extract_features(sample_user_data)
        
        assert features.shape == (1, 13)  # 13 features
        assert features[0][0] == 15  # current_streak
        assert features[0][1] == 30  # longest_streak
        assert features[0][2] == 0.5  # streak_ratio
    
    def test_predict_relapse_risk(self, predictor, sample_user_data):
        """Test relapse risk prediction"""
        prediction = predictor.predict_relapse_risk(sample_user_data)
        
        assert isinstance(prediction, RelapsePrediction)
        assert 0.0 <= prediction.risk_score <= 1.0
        assert 0.0 <= prediction.confidence <= 1.0
        assert prediction.risk_level in ["low", "medium", "high", "critical"]
        assert isinstance(prediction.factors, list)
        assert isinstance(prediction.recommendations, list)
        assert isinstance(prediction.next_check_date, datetime)
    
    def test_identify_contributing_factors(self, predictor, sample_user_data):
        """Test contributing factors identification"""
        factors = predictor._identify_contributing_factors(sample_user_data, 0.6)
        
        assert isinstance(factors, list)
        assert len(factors) <= 5  # Top 5 factors
    
    def test_generate_recommendations(self, predictor):
        """Test recommendation generation"""
        recommendations = predictor._generate_recommendations("high", ["Short current streak"])
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 6  # Top 6 recommendations
        assert all(isinstance(rec, str) for rec in recommendations)
    
    def test_calculate_next_check_date(self, predictor):
        """Test next check date calculation"""
        now = datetime.now()
        
        # Test critical risk level
        critical_date = predictor._calculate_next_check_date("critical")
        assert critical_date > now
        assert critical_date <= now + timedelta(hours=6)
        
        # Test low risk level
        low_date = predictor._calculate_next_check_date("low")
        assert low_date > now
        assert low_date <= now + timedelta(days=7)
        
        # Test medium risk level
        medium_date = predictor._calculate_next_check_date("medium")
        assert medium_date > now
        assert medium_date <= now + timedelta(days=3)
        
        # Test high risk level
        high_date = predictor._calculate_next_check_date("high")
        assert high_date > now
        assert high_date <= now + timedelta(days=1)


class TestRecommendationEngine:
    """Test the personalized recommendation engine"""
    
    @pytest.fixture
    def engine(self):
        return RecommendationEngine()
    
    @pytest.fixture
    def sample_user_data(self):
        return {
            'mood_score': 3.0,
            'stress_level': 6,
            'journal_entries_this_week': 2,
            'days_since_last_contact': 4,
            'urge_intensity': 8,
            'days_since_last_exercise': 3,
            'risk_level': 'medium'
        }
    
    def test_initialization(self, engine):
        """Test engine initialization"""
        assert engine.logger is not None
        assert len(engine.recommendations_db) > 0
        assert isinstance(engine.recommendation_history, list)
    
    def test_recommendation_database_loading(self, engine):
        """Test recommendation database loading"""
        db = engine.recommendations_db
        
        # Check that key recommendations exist
        assert "deep_breathing" in db
        assert "journal_reflection" in db
        assert "call_support" in db
        assert "exercise" in db
        
        # Check recommendation structure
        rec = db["deep_breathing"]
        assert isinstance(rec, RecoveryRecommendation)
        assert rec.id == "deep_breathing"
        assert rec.type == RecommendationType.COPING_STRATEGY
        assert rec.priority == RecommendationPriority.MEDIUM
        assert isinstance(rec.tags, list)
        assert isinstance(rec.conditions, dict)
    
    def test_get_personalized_recommendations(self, engine, sample_user_data):
        """Test personalized recommendation generation"""
        recommendations = engine.get_personalized_recommendations(sample_user_data, limit=3)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        assert all(isinstance(rec, RecoveryRecommendation) for rec in recommendations)
    
    def test_calculate_recommendation_score(self, engine, sample_user_data):
        """Test recommendation scoring"""
        rec = engine.recommendations_db["deep_breathing"]
        score = engine._calculate_recommendation_score(rec, sample_user_data)
        
        assert isinstance(score, float)
        assert score >= 0.0
    
    def test_meets_conditions(self, engine, sample_user_data):
        """Test condition checking"""
        rec = engine.recommendations_db["deep_breathing"]
        meets = engine._meets_conditions(rec, sample_user_data)
        
        assert isinstance(meets, bool)
    
    def test_priority_to_numeric(self, engine):
        """Test priority conversion"""
        assert engine._priority_to_numeric(RecommendationPriority.LOW) == 1
        assert engine._priority_to_numeric(RecommendationPriority.MEDIUM) == 2
        assert engine._priority_to_numeric(RecommendationPriority.HIGH) == 3
        assert engine._priority_to_numeric(RecommendationPriority.CRITICAL) == 4
    
    def test_track_recommendation_usage(self, engine):
        """Test recommendation usage tracking"""
        engine.track_recommendation_usage("test_rec", 1, True, "Great recommendation!")
        
        assert len(engine.recommendation_history) > 0
        last_record = engine.recommendation_history[-1]
        assert last_record["recommendation_id"] == "test_rec"
        assert last_record["used"] is True
        assert last_record["feedback"] == "Great recommendation!"
    
    def test_get_recommendation_analytics(self, engine):
        """Test recommendation analytics"""
        analytics = engine.get_recommendation_analytics()
        
        assert isinstance(analytics, dict)
        assert "total_recommendations" in analytics
        assert "used_recommendations" in analytics
        assert "usage_rate" in analytics


class TestEnhancedBlockingService:
    """Test the enhanced blocking service"""
    
    @pytest.fixture
    def blocking_service(self):
        return EnhancedBlockingService()
    
    def test_initialization(self, blocking_service):
        """Test service initialization"""
        assert blocking_service.platform_manager is not None
        assert blocking_service.ai_classifier is not None
        assert blocking_service.network_monitor is not None
        assert blocking_service.db_manager is not None
    
    @pytest.mark.asyncio
    async def test_block_domains_async(self, blocking_service):
        """Test async domain blocking"""
        domains = ["test.com", "example.org"]
        
        with patch.object(blocking_service, 'block_domain') as mock_block:
            mock_block.return_value = True
            
            result = await blocking_service.block_domains_async(domains)
            
            assert isinstance(result, dict)
            assert all(domain in result for domain in domains)
            assert mock_block.call_count == len(domains)
    
    @pytest.mark.asyncio
    async def test_unblock_domains_async(self, blocking_service):
        """Test async domain unblocking"""
        domains = ["test.com", "example.org"]
        
        with patch.object(blocking_service, 'unblock_domain') as mock_unblock:
            mock_unblock.return_value = True
            
            result = await blocking_service.unblock_domains_async(domains)
            
            assert isinstance(result, dict)
            assert all(domain in result for domain in domains)
            assert mock_unblock.call_count == len(domains)
    
    @pytest.mark.asyncio
    async def test_classify_domain(self, blocking_service):
        """Test domain classification"""
        domain = "test.com"
        
        with patch.object(blocking_service.ai_classifier, 'classify_domain') as mock_classify:
            mock_classify.return_value = DomainClassification(
                domain=domain,
                category="adult",
                confidence=0.9,
                features={},
                risk_score=0.8
            )
            
            result = await blocking_service.classify_domain(domain)
            
            assert result.domain == domain
            assert result.risk_score == 0.8
            assert result.category == "adult"
    
    def test_get_blocking_statistics(self, blocking_service):
        """Test blocking statistics"""
        with patch.object(blocking_service.platform_manager, 'get_system_info') as mock_info:
            mock_info.return_value = {"platform": "Windows", "status": "active"}
            
            stats = blocking_service.get_blocking_statistics()
            
            assert isinstance(stats, dict)
            assert "platform_info" in stats
            assert "total_blocked_domains" in stats
            assert "total_blocking_rules" in stats


class TestDatabaseIntegration:
    """Test database integration"""
    
    @pytest.fixture
    def db_manager(self):
        return DatabaseManager()
    
    def test_user_creation_and_retrieval(self, db_manager):
        """Test user creation and retrieval"""
        # Test user creation
        user = db_manager.create_user(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            is_admin=False
        )
        
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_admin is False
        
        # Test user retrieval
        retrieved_user = db_manager.get_user_by_username("testuser")
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
    
    def test_blocking_rule_management(self, db_manager):
        """Test blocking rule management"""
        # Test rule creation
        rule = db_manager.create_blocking_rule(
            domain="test.com",
            category="adult",
            risk_score=0.8,
            source="ai_classifier"
        )
        
        assert rule is not None
        assert rule.domain == "test.com"
        assert rule.category == "adult"
        assert rule.risk_score == 0.8
        
        # Test rule retrieval
        rules = db_manager.get_blocking_rules_by_domain("test.com")
        assert len(rules) > 0
        assert rules[0].domain == "test.com"
    
    def test_network_event_logging(self, db_manager):
        """Test network event logging"""
        # Test event creation
        event = db_manager.create_network_event(
            event_type="blocked_access",
            domain="test.com",
            user_id=1,
            details={"reason": "adult_content"}
        )
        
        assert event is not None
        assert event.event_type == "blocked_access"
        assert event.domain == "test.com"
        assert event.user_id == 1


class TestPhase2Integration:
    """Test Phase 2 integration"""
    
    def test_full_workflow(self):
        """Test full Phase 2 workflow"""
        # Test relapse prediction
        predictor = RelapsePredictor()
        user_data = {
            'current_streak': 10,
            'longest_streak': 30,
            'mood_score': 4.0,
            'stress_level': 3
        }
        prediction = predictor.predict_relapse_risk(user_data)
        assert isinstance(prediction, RelapsePrediction)
        
        # Test recommendation engine
        engine = RecommendationEngine()
        recommendations = engine.get_personalized_recommendations(user_data, limit=3)
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        
        # Test enhanced blocking service
        blocking_service = EnhancedBlockingService()
        assert blocking_service.platform_manager is not None
        assert blocking_service.ai_classifier is not None
        
        # Test database manager
        db_manager = DatabaseManager()
        assert db_manager is not None
    
    def test_error_handling(self):
        """Test error handling across Phase 2 components"""
        # Test with invalid data
        predictor = RelapsePredictor()
        engine = RecommendationEngine()
        
        # Invalid user data
        invalid_data = {}
        
        # Should handle gracefully
        prediction = predictor.predict_relapse_risk(invalid_data)
        assert isinstance(prediction, RelapsePrediction)
        
        recommendations = engine.get_personalized_recommendations(invalid_data, limit=3)
        assert isinstance(recommendations, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])