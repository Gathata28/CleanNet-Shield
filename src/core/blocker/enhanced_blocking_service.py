"""
Enhanced blocking service integrating AI, database, and real-time monitoring
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime

from src.core.blocker.enhanced_platform_manager import get_enhanced_platform_manager, EnhancedPlatformManager
from src.core.blocker.ai_classifier import AIDomainClassifier, DomainClassification
from src.core.monitoring.network_monitor import RealTimeNetworkMonitor, NetworkEvent
from src.database.manager import DatabaseManager
from src.database.models import BlockingRule, NetworkEvent as DBNetworkEvent

logger = logging.getLogger(__name__)

class EnhancedBlockingService:
    """
    Enhanced blocking service that combines AI classification, 
    real-time monitoring, and database persistence
    """
    
    def __init__(self, user_id: int = 1):
        self.user_id = user_id
        self.platform_manager = get_enhanced_platform_manager()
        self.ai_classifier = AIDomainClassifier()
        self.network_monitor = RealTimeNetworkMonitor()
        self.db_manager = DatabaseManager()
        
        # Register callbacks
        self.network_monitor.add_event_callback(self._on_network_event)
        self.network_monitor.add_stats_callback(self._on_network_stats)
        
        # Blocking state
        self.is_active = False
        self.blocked_domains: set = set()
        self.whitelist_domains: set = set()
        
    async def start_service(self):
        """Start the enhanced blocking service"""
        try:
            logger.info("Starting enhanced blocking service")
            
            # Load existing blocking rules from database
            await self._load_blocking_rules()
            
            # Start network monitoring
            await self.network_monitor.start_monitoring()
            
            # Start async blocklist updates
            asyncio.create_task(self._periodic_blocklist_update())
            
            self.is_active = True
            logger.info("Enhanced blocking service started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start enhanced blocking service: {e}")
            raise
    
    async def stop_service(self):
        """Stop the enhanced blocking service"""
        try:
            logger.info("Stopping enhanced blocking service")
            
            await self.network_monitor.stop_monitoring()
            self.is_active = False
            
            logger.info("Enhanced blocking service stopped")
            
        except Exception as e:
            logger.error(f"Error stopping enhanced blocking service: {e}")
    
    async def block_domain(self, domain: str, category: str = None, risk_score: float = None) -> bool:
        """Block a domain with AI classification and database persistence"""
        try:
            # AI classification if not provided
            if category is None or risk_score is None:
                classification = await self.ai_classifier.classify_domain(domain)
                category = classification.category
                risk_score = classification.risk_score
            
            # Add to blocked domains set
            self.blocked_domains.add(domain)
            
            # Block on platform
            success = await self.platform_manager.block_domains_async([domain])
            
            if success:
                # Persist to database
                rule = self.db_manager.create_blocking_rule(
                    user_id=self.user_id,
                    domain=domain,
                    category=category,
                    risk_score=risk_score
                )
                
                if rule:
                    logger.info(f"Successfully blocked domain: {domain} (category: {category}, risk: {risk_score})")
                    return True
                else:
                    logger.error(f"Failed to persist blocking rule for domain: {domain}")
                    return False
            else:
                logger.error(f"Failed to block domain on platform: {domain}")
                return False
                
        except Exception as e:
            logger.error(f"Error blocking domain {domain}: {e}")
            return False
    
    async def unblock_domain(self, domain: str) -> bool:
        """Unblock a domain"""
        try:
            # Remove from blocked domains set
            self.blocked_domains.discard(domain)
            
            # Unblock on platform
            success = await self.platform_manager.unblock_domains_async([domain])
            
            if success:
                logger.info(f"Successfully unblocked domain: {domain}")
                return True
            else:
                logger.error(f"Failed to unblock domain on platform: {domain}")
                return False
                
        except Exception as e:
            logger.error(f"Error unblocking domain {domain}: {e}")
            return False
    
    async def classify_and_block_domains(self, domains: List[str]) -> Dict[str, bool]:
        """Classify and block multiple domains using AI"""
        try:
            # Batch classify domains
            classifications = await self.ai_classifier.classify_batch(domains)
            
            # Block domains based on classification
            results = {}
            for classification in classifications:
                if classification.risk_score > 0.5:  # Configurable threshold
                    success = await self.block_domain(
                        classification.domain,
                        classification.category,
                        classification.risk_score
                    )
                    results[classification.domain] = success
                else:
                    results[classification.domain] = False  # Not blocked due to low risk
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch classification and blocking: {e}")
            return {domain: False for domain in domains}
    
    async def get_blocking_stats(self) -> Dict:
        """Get comprehensive blocking statistics"""
        try:
            # Get network monitor stats
            network_stats = self.network_monitor.get_current_stats()
            performance_metrics = self.network_monitor.get_performance_metrics()
            
            # Get database stats
            blocking_rules = self.db_manager.get_blocking_rules_for_user(self.user_id)
            
            return {
                "total_blocked_domains": len(self.blocked_domains),
                "total_blocking_rules": len(blocking_rules),
                "network_stats": network_stats.__dict__ if network_stats else {},
                "performance_metrics": performance_metrics,
                "service_active": self.is_active,
                "platform_info": self.platform_manager.get_system_info()
            }
            
        except Exception as e:
            logger.error(f"Error getting blocking stats: {e}")
            return {}
    
    async def _load_blocking_rules(self):
        """Load existing blocking rules from database"""
        try:
            rules = self.db_manager.get_blocking_rules_for_user(self.user_id)
            
            for rule in rules:
                if rule.is_active:
                    self.blocked_domains.add(rule.domain)
            
            logger.info(f"Loaded {len(rules)} blocking rules from database")
            
        except Exception as e:
            logger.error(f"Error loading blocking rules: {e}")
    
    async def _periodic_blocklist_update(self):
        """Periodically update blocklists"""
        while self.is_active:
            try:
                # This would integrate with the existing blocklist_updater
                # For now, just log the periodic update
                logger.info("Performing periodic blocklist update")
                
                # Wait for 24 hours before next update
                await asyncio.sleep(24 * 60 * 60)
                
            except Exception as e:
                logger.error(f"Error in periodic blocklist update: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _on_network_event(self, event: NetworkEvent):
        """Handle network events from the monitor"""
        try:
            # Store in database
            db_event = DBNetworkEvent(
                user_id=self.user_id,
                timestamp=event.timestamp,
                event_type=event.event_type,
                source_ip=event.source_ip,
                destination_ip=event.destination_ip,
                destination_port=event.destination_port,
                protocol=event.protocol,
                bytes_sent=event.bytes_sent,
                bytes_received=event.bytes_received,
                process_name=event.process_name,
                risk_score=event.risk_score,
                was_blocked=event.risk_score > 0.7
            )
            
            # This would be stored via the database manager
            logger.debug(f"Network event: {event.destination_ip}:{event.destination_port} (risk: {event.risk_score})")
            
        except Exception as e:
            logger.error(f"Error handling network event: {e}")
    
    async def _on_network_stats(self, stats):
        """Handle network statistics updates"""
        try:
            logger.debug(f"Network stats update: {stats.active_connections} active connections")
        except Exception as e:
            logger.error(f"Error handling network stats: {e}")
    
    def get_bypass_attempts(self) -> List[Dict]:
        """Get detected bypass attempts"""
        try:
            return self.platform_manager.detect_bypass_attempts()
        except Exception as e:
            logger.error(f"Error getting bypass attempts: {e}")
            return []
    
    async def block_domains_async(self, domains: List[str]) -> Dict[str, bool]:
        """Block multiple domains asynchronously"""
        try:
            results = {}
            for domain in domains:
                success = await self.block_domain(domain)
                results[domain] = success
            return results
        except Exception as e:
            logger.error(f"Error blocking domains: {e}")
            return {domain: False for domain in domains}
    
    async def unblock_domains_async(self, domains: List[str]) -> Dict[str, bool]:
        """Unblock multiple domains asynchronously"""
        try:
            results = {}
            for domain in domains:
                success = await self.unblock_domain(domain)
                results[domain] = success
            return results
        except Exception as e:
            logger.error(f"Error unblocking domains: {e}")
            return {domain: False for domain in domains}
    
    async def classify_domain(self, domain: str) -> DomainClassification:
        """Classify a domain using AI"""
        try:
            return await self.ai_classifier.classify_domain(domain)
        except Exception as e:
            logger.error(f"Error classifying domain {domain}: {e}")
            # Return a default classification
            return DomainClassification(
                domain=domain,
                category="unknown",
                risk_score=0.0,
                features={}
            )
    
    def get_blocking_statistics(self) -> Dict:
        """Get blocking statistics (synchronous version)"""
        try:
            # Get network monitor stats
            network_stats = self.network_monitor.get_current_stats()
            performance_metrics = self.network_monitor.get_performance_metrics()
            
            # Get database stats
            blocking_rules = self.db_manager.get_blocking_rules_for_user(self.user_id)
            
            return {
                "total_blocked_domains": len(self.blocked_domains),
                "total_blocking_rules": len(blocking_rules),
                "network_stats": network_stats.__dict__ if network_stats else {},
                "performance_metrics": performance_metrics,
                "service_active": self.is_active,
                "platform_info": self.platform_manager.get_system_info()
            }
            
        except Exception as e:
            logger.error(f"Error getting blocking stats: {e}")
            return {}
