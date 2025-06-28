"""
Advanced blocking engine for CleanNet Shield
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from .blocking_rule import BlockingRule, BlockingCategory, BlockingSeverity

logger = logging.getLogger(__name__)


class AdvancedBlocker:
    """Advanced blocking engine with multiple sources"""
    
    def __init__(self):
        self.rules: List[BlockingRule] = []
        self.blocklist_sources = {
            "steven_black": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
            "ultimate_hosts": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/Ultimate.Hosts.Blacklist/master/hosts",
        }
    
    async def update_blocklists(self) -> Dict[str, int]:
        """Update blocklists from multiple sources"""
        logger.info("Starting blocklist update...")
        
        results = {}
        async with aiohttp.ClientSession() as session:
            for source_name, url in self.blocklist_sources.items():
                try:
                    domains = await self._fetch_source(session, url)
                    results[source_name] = len(domains)
                    
                    # Convert to rules
                    for domain in domains:
                        rule = BlockingRule(
                            domain=domain,
                            category=BlockingCategory.ADULT_CONTENT,
                            severity=BlockingSeverity.HIGH,
                            source=source_name
                        )
                        self.rules.append(rule)
                        
                except Exception as e:
                    logger.error(f"Failed to fetch {source_name}: {e}")
                    results[source_name] = 0
        
        logger.info(f"Blocklist update completed: {sum(results.values())} domains")
        return results
    
    async def _fetch_source(self, session: aiohttp.ClientSession, url: str) -> List[str]:
        """Fetch blocklist from source"""
        async with session.get(url) as response:
            content = await response.text()
            return self._parse_hosts_file(content)
    
    def _parse_hosts_file(self, content: str) -> List[str]:
        """Parse hosts file content"""
        domains = set()
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2 and parts[0] in ['127.0.0.1', '0.0.0.0']:
                    domains.add(parts[1])
        return list(domains)
    
    def get_stats(self) -> Dict:
        """Get blocking statistics"""
        return {
            "total_rules": len(self.rules),
            "active_rules": len([r for r in self.rules if r.is_active]),
            "sources": list(self.blocklist_sources.keys())
        }
