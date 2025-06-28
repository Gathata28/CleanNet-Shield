"""
Unit tests for blocking functionality
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta, timezone

from src.core.blocker.blocking_rule import BlockingRule, BlockingCategory, BlockingSeverity
from src.core.blocker.advanced_blocker import AdvancedBlocker
from src.core.blocker.platform_manager import WindowsManager, LinuxManager, MacOSManager


class TestBlockingRule:
    """Test BlockingRule class"""
    
    def test_blocking_rule_creation(self):
        """Test creating a blocking rule"""
        rule = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH
        )
        
        assert rule.domain == "example.com"
        assert rule.category == BlockingCategory.ADULT_CONTENT
        assert rule.severity == BlockingSeverity.HIGH
        assert rule.is_active is True
    
    def test_blocking_rule_validation(self):
        """Test blocking rule validation"""
        with pytest.raises(ValueError):
            BlockingRule(domain="", category=BlockingCategory.ADULT_CONTENT, severity=BlockingSeverity.HIGH)
    
    def test_blocking_rule_expiration(self):
        """Test rule expiration logic"""
        from datetime import timedelta
        
        # Rule with no expiration
        rule1 = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH
        )
        assert not rule1.is_expired()
        
        # Rule with future expiration
        rule2 = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )
        assert not rule2.is_expired()
        
        # Rule with past expiration
        rule3 = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        assert rule3.is_expired()
    
    def test_blocking_rule_serialization(self):
        """Test rule serialization to/from dict"""
        rule = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH,
            description="Test rule"
        )
        
        rule_dict = rule.to_dict()
        restored_rule = BlockingRule.from_dict(rule_dict)
        
        assert restored_rule.domain == rule.domain
        assert restored_rule.category == rule.category
        assert restored_rule.severity == rule.severity
        assert restored_rule.description == rule.description


class TestAdvancedBlocker:
    """Test AdvancedBlocker class"""
    
    def test_advanced_blocker_initialization(self):
        """Test blocker initialization"""
        blocker = AdvancedBlocker()
        assert len(blocker.rules) == 0
        assert len(blocker.blocklist_sources) > 0
    
    @pytest.mark.asyncio
    async def test_update_blocklists(self):
        """Test blocklist update functionality"""
        blocker = AdvancedBlocker()

        # Mock the HTTP response
        mock_content = """
# Test hosts file
127.0.0.1 example.com
127.0.0.1 test.com
# Comment line
0.0.0.0 blocked.com
        """

        class MockResponse:
            async def text(self):
                return mock_content
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                pass

        class MockSession:
            def get(self, url):
                return MockResponse()
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                pass

        # Patch aiohttp.ClientSession to use our mock
        with patch('aiohttp.ClientSession', return_value=MockSession()):
            results = await blocker.update_blocklists()
            assert len(results) > 0
            assert len(blocker.rules) > 0
    
    def test_parse_hosts_file(self):
        """Test hosts file parsing"""
        blocker = AdvancedBlocker()
        
        content = """
# Test hosts file
127.0.0.1 example.com
127.0.0.1 test.com
# Comment line
0.0.0.0 blocked.com
        """
        
        domains = blocker._parse_hosts_file(content)
        assert "example.com" in domains
        assert "test.com" in domains
        assert "blocked.com" in domains
        assert len(domains) == 3
    
    def test_get_stats(self):
        """Test statistics retrieval"""
        blocker = AdvancedBlocker()
        
        # Add some test rules
        rule1 = BlockingRule(
            domain="example.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.HIGH
        )
        rule2 = BlockingRule(
            domain="test.com",
            category=BlockingCategory.ADULT_CONTENT,
            severity=BlockingSeverity.MEDIUM,
            is_active=False
        )
        
        blocker.rules = [rule1, rule2]
        
        stats = blocker.get_stats()
        assert stats["total_rules"] == 2
        assert stats["active_rules"] == 1


class TestPlatformManager:
    """Test platform manager functionality"""
    
    def test_windows_manager_initialization(self):
        """Test Windows manager initialization"""
        manager = WindowsManager()
        assert manager.hosts_file == r"C:\Windows\System32\drivers\etc\hosts"
    
    def test_linux_manager_initialization(self):
        """Test Linux manager initialization"""
        manager = LinuxManager()
        assert manager.hosts_file == "/etc/hosts"
    
    def test_macos_manager_initialization(self):
        """Test macOS manager initialization"""
        manager = MacOSManager()
        assert manager.hosts_file == "/etc/hosts"
    
    @patch('builtins.open', new_callable=mock_open, read_data="127.0.0.1 localhost\n")
    def test_windows_block_domains(self, mock_file):
        """Test Windows domain blocking"""
        manager = WindowsManager()
        
        # Mock file operations
        mock_file.return_value.read.return_value = "127.0.0.1 localhost\n"
        
        success = manager.block_domains(["example.com", "test.com"])
        assert success is True
    
    @patch('builtins.open', new_callable=mock_open, read_data="127.0.0.1 localhost\n127.0.0.1 example.com\n")
    def test_windows_unblock_domains(self, mock_file):
        """Test Windows domain unblocking"""
        manager = WindowsManager()
        
        # Mock file operations
        mock_file.return_value.readlines.return_value = [
            "127.0.0.1 localhost\n",
            "127.0.0.1 example.com\n"
        ]
        
        success = manager.unblock_domains(["example.com"])
        assert success is True
    
    def test_get_system_info(self):
        """Test system info retrieval"""
        manager = WindowsManager()
        info = manager.get_system_info()
        
        assert "platform" in info
        assert "version" in info
        assert "architecture" in info
        assert "hosts_file" in info
        assert info["platform"] == "Windows" 