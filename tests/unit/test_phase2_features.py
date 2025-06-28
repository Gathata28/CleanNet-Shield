"""
Unit tests for Phase 2 features
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from src.core.blocker.enhanced_platform_manager import (
    EnhancedPlatformManager,
    EnhancedWindowsManager,
    get_enhanced_platform_manager
)
from src.core.blocker.ai_classifier import AIDomainClassifier, DomainClassification
from src.core.monitoring.network_monitor import RealTimeNetworkMonitor, NetworkEvent, NetworkStats
from src.database.manager import DatabaseManager
from src.database.models import User, BlockingRule
from src.core.blocker.enhanced_blocking_service import EnhancedBlockingService


class TestEnhancedPlatformManager:
    """Test enhanced platform manager functionality"""
    
    @pytest.fixture
    def platform_manager(self):
        return EnhancedWindowsManager()
    
    @pytest.mark.asyncio
    async def test_block_domains_async(self, platform_manager):
        """Test async domain blocking"""
        domains = ["test.com", "example.org"]
        
        with patch.object(platform_manager, '_update_hosts_file') as mock_update, \
             patch.object(platform_manager, '_create_firewall_rules') as mock_firewall, \
             patch.object(platform_manager, '_configure_dns_blocking') as mock_dns:
            
            mock_update.return_value = None
            mock_firewall.return_value = None
            mock_dns.return_value = None
            
            result = await platform_manager.block_domains_async(domains)
            
            assert result is True
            mock_update.assert_called_once_with(domains, block=True)
            mock_firewall.assert_called_once_with(domains)
            mock_dns.assert_called_once_with(domains)
    
    @pytest.mark.asyncio
    async def test_unblock_domains_async(self, platform_manager):
        """Test async domain unblocking"""
        domains = ["test.com", "example.org"]
        
        with patch.object(platform_manager, '_update_hosts_file') as mock_update, \
             patch.object(platform_manager, '_remove_firewall_rules') as mock_firewall:
            
            mock_update.return_value = None
            mock_firewall.return_value = None
            
            result = await platform_manager.unblock_domains_async(domains)
            
            assert result is True
            mock_update.assert_called_once_with(domains, block=False)
            mock_firewall.assert_called_once_with(domains)
    
    def test_get_network_status(self, platform_manager):
        """Test network status retrieval"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "test output"
            status = platform_manager.get_network_status()
            
            assert isinstance(status, dict)
            assert "platform" in status
    
    def test_detect_bypass_attempts(self, platform_manager):
        """Test bypass attempt detection"""
        attempts = platform_manager.detect_bypass_attempts()
        assert isinstance(attempts, list)


class TestAIDomainClassifier:
    """Test AI domain classifier functionality"""
    
    @pytest.fixture
    def classifier(self):
        return AIDomainClassifier()
    
    @pytest.mark.asyncio
    async def test_classify_domain(self, classifier):
        """Test domain classification"""
        domain = "example.com"
        
        with patch.object(classifier, '_extract_domain_features') as mock_features:
            mock_features.return_value = {"length": 11, "suspicious_keywords": 0}
            
            classification = await classifier.classify_domain(domain)
            
            assert isinstance(classification, DomainClassification)
            assert classification.domain == domain
            assert isinstance(classification.risk_score, float)
    
    @pytest.mark.asyncio
    async def test_classify_batch(self, classifier):
        """Test batch domain classification"""
        domains = ["example.com", "test.org"]
        
        with patch.object(classifier, 'classify_domain') as mock_classify:
            mock_classify.return_value = DomainClassification(
                domain="test", category="safe", confidence=0.8, 
                features={}, risk_score=0.1
            )
            
            results = await classifier.classify_batch(domains)
            
            assert len(results) == 2
            assert all(isinstance(r, DomainClassification) for r in results)
    
    def test_extract_domain_features(self, classifier):
        """Test domain feature extraction"""
        domain = "test.example.com"
        features = classifier._extract_domain_features(domain)
        
        assert isinstance(features, dict)
        assert "length" in features
        assert "subdomain_count" in features
        assert "suspicious_keywords" in features
    
    def test_calculate_risk_score(self, classifier):
        """Test risk score calculation"""
        domain = "example.com"
        category = "safe"
        confidence = 0.8
        
        risk_score = classifier._calculate_risk_score(domain, category, confidence)
        
        assert isinstance(risk_score, float)
        assert 0.0 <= risk_score <= 1.0


class TestRealTimeNetworkMonitor:
    """Test real-time network monitoring functionality"""
    
    @pytest.fixture
    def monitor(self):
        return RealTimeNetworkMonitor()
    
    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, monitor):
        """Test starting and stopping monitoring"""
        # Start monitoring
        start_task = asyncio.create_task(monitor.start_monitoring())
        
        # Wait a bit then stop
        await asyncio.sleep(0.1)
        await monitor.stop_monitoring()
        
        # Cancel the start task
        start_task.cancel()
        
        assert not monitor.is_monitoring
    
    def test_add_callbacks(self, monitor):
        """Test adding event and stats callbacks"""
        event_callback = Mock()
        stats_callback = Mock()
        
        monitor.add_event_callback(event_callback)
        monitor.add_stats_callback(stats_callback)
        
        assert event_callback in monitor.event_callbacks
        assert stats_callback in monitor.stats_callbacks
    
    def test_get_performance_metrics(self, monitor):
        """Test performance metrics retrieval"""
        monitor.start_time = datetime.now()
        monitor.total_events = 100
        monitor.blocked_events = 10
        
        metrics = monitor.get_performance_metrics()
        
        assert isinstance(metrics, dict)
        assert "total_events" in metrics
        assert "blocked_events" in metrics
        assert "block_rate" in metrics


class TestDatabaseManager:
    """Test database manager functionality"""
    
    @pytest.fixture
    def db_manager(self):
        return DatabaseManager("sqlite:///:memory:")
    
    def test_create_user(self, db_manager):
        """Test user creation"""
        user = db_manager.create_user(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_get_user_by_username(self, db_manager):
        """Test user retrieval by username"""
        # Create user first
        db_manager.create_user(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        # Retrieve user
        user = db_manager.get_user_by_username("testuser")
        
        assert user is not None
        assert user.username == "testuser"
    
    def test_create_blocking_rule(self, db_manager):
        """Test blocking rule creation"""
        # Create user first
        user = db_manager.create_user(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        # Create blocking rule
        rule = db_manager.create_blocking_rule(
            user_id=user.id,
            domain="test.com",
            category="adult_content",
            risk_score=0.8
        )
        
        assert rule is not None
        assert rule.domain == "test.com"
        assert rule.category == "adult_content"
        assert rule.risk_score == 0.8
    
    def test_get_blocking_rules_for_user(self, db_manager):
        """Test retrieving blocking rules for a user"""
        # Create user and rules
        user = db_manager.create_user(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        db_manager.create_blocking_rule(user.id, "test1.com", "adult_content", 0.8)
        db_manager.create_blocking_rule(user.id, "test2.com", "gambling", 0.7)
        
        # Get rules
        rules = db_manager.get_blocking_rules_for_user(user.id)
        
        assert len(rules) == 2
        assert all(rule.user_id == user.id for rule in rules)


class TestEnhancedBlockingService:
    """Test enhanced blocking service functionality"""
    
    @pytest.fixture
    def blocking_service(self):
        return EnhancedBlockingService(user_id=1)
    
    @pytest.mark.asyncio
    async def test_start_stop_service(self, blocking_service):
        """Test starting and stopping the blocking service"""
        with patch.object(blocking_service.network_monitor, 'start_monitoring') as mock_start:
            with patch.object(blocking_service.network_monitor, 'stop_monitoring') as mock_stop:
                # Start service
                await blocking_service.start_service()
                assert blocking_service.is_active
                mock_start.assert_called_once()
                
                # Stop service
                await blocking_service.stop_service()
                assert not blocking_service.is_active
                mock_stop.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_block_domain(self, blocking_service):
        """Test domain blocking with AI classification"""
        domain = "test.com"
        
        with patch.object(blocking_service.ai_classifier, 'classify_domain') as mock_classify:
            mock_classify.return_value = DomainClassification(
                domain=domain, category="adult_content", confidence=0.9,
                features={}, risk_score=0.8
            )
            
            with patch.object(blocking_service.platform_manager, 'block_domains_async') as mock_block:
                mock_block.return_value = True
                
                with patch.object(blocking_service.db_manager, 'create_blocking_rule') as mock_create:
                    mock_create.return_value = Mock()
                    
                    result = await blocking_service.block_domain(domain)
                    
                    assert result is True
                    assert domain in blocking_service.blocked_domains
                    mock_classify.assert_called_once_with(domain)
                    mock_block.assert_called_once_with([domain])
    
    @pytest.mark.asyncio
    async def test_classify_and_block_domains(self, blocking_service):
        """Test batch classification and blocking"""
        domains = ["test1.com", "test2.com"]
        
        with patch.object(blocking_service.ai_classifier, 'classify_batch') as mock_classify:
            mock_classify.return_value = [
                DomainClassification(domain="test1.com", category="adult_content", 
                                   confidence=0.9, features={}, risk_score=0.8),
                DomainClassification(domain="test2.com", category="safe", 
                                   confidence=0.8, features={}, risk_score=0.2)
            ]
            
            with patch.object(blocking_service, 'block_domain') as mock_block:
                mock_block.return_value = True
                
                results = await blocking_service.classify_and_block_domains(domains)
                
                assert len(results) == 2
                assert results["test1.com"] is True  # High risk, should be blocked
                assert results["test2.com"] is False  # Low risk, not blocked
    
    @pytest.mark.asyncio
    async def test_get_blocking_stats(self, blocking_service):
        """Test blocking statistics retrieval"""
        with patch.object(blocking_service.network_monitor, 'get_current_stats') as mock_stats:
            mock_stats.return_value = NetworkStats(
                total_bytes_sent=1000, total_bytes_received=2000,
                active_connections=5, blocked_connections=2,
                suspicious_connections=1, timestamp=datetime.now()
            )
            
            with patch.object(blocking_service.network_monitor, 'get_performance_metrics') as mock_perf:
                mock_perf.return_value = {"events_per_second": 10}
                
                with patch.object(blocking_service.db_manager, 'get_blocking_rules_for_user') as mock_rules:
                    mock_rules.return_value = [Mock(), Mock()]  # 2 rules
                    
                    stats = await blocking_service.get_blocking_stats()
                    
                    assert isinstance(stats, dict)
                    assert "total_blocked_domains" in stats
                    assert "total_blocking_rules" in stats
                    assert "network_stats" in stats
                    assert "performance_metrics" in stats
                    assert "service_active" in stats
                    assert "platform_info" in stats


if __name__ == "__main__":
    pytest.main([__file__]) 