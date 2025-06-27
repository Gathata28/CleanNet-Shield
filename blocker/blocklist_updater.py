#!/usr/bin/env python3
"""
Blocklist updater module for fetching and managing domain blocklists
"""

import requests
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Set, Dict, Optional
from urllib.parse import urlparse

# Handle imports for both standalone and package usage
try:
    from ..utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.logger import Logger

class BlocklistUpdater:
    def __init__(self):
        """Initialize blocklist updater"""
        self.logger = Logger()
        
        # Data directory
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Local files
        self.blocklist_file = os.path.join(self.data_dir, 'blocklist.txt')
        self.config_file = os.path.join(self.data_dir, 'updater_config.json')
        self.cache_file = os.path.join(self.data_dir, 'blocklist_cache.json')
        
        # Default configuration
        self.default_config = {
            "update_interval_hours": 24,
            "max_cache_age_hours": 48,
            "timeout_seconds": 30,
            "sources": [
                {
                    "name": "StevenBlack Fakenews-Gambling-Porn",
                    "url": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts",
                    "format": "hosts",
                    "enabled": True
                },
                {
                    "name": "StevenBlack Porn",
                    "url": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts", 
                    "format": "hosts",
                    "enabled": True
                },
                {
                    "name": "Ultimate NSFW Blocklist",
                    "url": "https://raw.githubusercontent.com/chadmayfield/my-pihole-blocklists/master/lists/pi_blocklist_porn_all.list",
                    "format": "domains",
                    "enabled": True
                },
                {
                    "name": "UT1 Adult",
                    "url": "https://dsi.ut-capitole.fr/blacklists/download/adult.tar.gz",
                    "format": "ut1",
                    "enabled": False  # Requires special handling
                }
            ],
            "additional_domains": [
                # Social media adult content pages
                "reddit.com/r/gonewild", "reddit.com/r/nsfw", "reddit.com/r/porn",
                "reddit.com/r/sex", "reddit.com/r/amateur", "reddit.com/r/milf",
                "twitter.com/search?q=porn", "instagram.com/explore/tags/nsfw",
                
                # Major adult sites - comprehensive list
                "pornhub.com", "xvideos.com", "xnxx.com", "redtube.com",
                "youporn.com", "tube8.com", "spankbang.com", "xhamster.com",
                "brazzers.com", "bangbros.com", "naughtyamerica.com",
                "realitykings.com", "mofos.com", "digitalplayground.com",
                
                # Cam sites
                "chaturbate.com", "cam4.com", "bongacams.com", "stripchat.com",
                "livejasmin.com", "flirt4free.com", "streamate.com",
                
                # Dating/hookup sites  
                "adultfriendfinder.com", "ashley-madison.com", "seeking.com",
                "benaughty.com", "fling.com", "alt.com",
                
                # Escort/adult services
                "tryst.link", "eros.com", "slixa.com", "skipthegames.com",
                "listcrawler.com", "bedpage.com", "cityxguide.com",
                
                # Fetish/BDSM sites
                "fetlife.com", "kink.com", "dungeoncorp.com", "subspace.land",
                
                # Adult gaming
                "nutaku.net", "f95zone.to", "lewdgamer.com",
                
                # International adult sites
                "javhd.com", "japanese-adult-video.com", "av01.tv",
                "eporner.com", "beeg.com", "tnaflix.com", "drtuber.com",
                
                # Adult comics/manga
                "nhentai.net", "tsumino.com", "hentai-foundry.com",
                "e-hentai.org", "exhentai.org", "fakku.net",
                
                # Torrents (adult)
                "empornium.me", "pornbay.org", "pornolab.net"
            ]
        }
        
        # Load or create configuration
        self.config = self._load_config()
        
        self.logger.debug("Blocklist updater initialized")
    
    def _load_config(self) -> Dict:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            else:
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            self.logger.error(f"Failed to load config, using defaults: {e}")
            return self.default_config
    
    def _save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def _load_cache(self) -> Dict:
        """Load cached data"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load cache: {e}")
            return {}
    
    def _save_cache(self, cache_data: Dict):
        """Save cache data"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save cache: {e}")
    
    def _is_cache_valid(self, cache_data: Dict, source_name: str) -> bool:
        """Check if cached data is still valid"""
        if source_name not in cache_data:
            return False
        
        try:
            cached_time = datetime.fromisoformat(cache_data[source_name]['timestamp'])
            max_age = timedelta(hours=self.config['max_cache_age_hours'])
            return datetime.now() - cached_time < max_age
        except Exception:
            return False
    
    def _validate_domain(self, domain: str) -> bool:
        """Validate if a domain is properly formatted"""
        if not domain or len(domain) > 253:
            return False
        
        # Remove protocol if present
        if '://' in domain:
            domain = domain.split('://', 1)[1]
        
        # Remove path if present
        if '/' in domain:
            domain = domain.split('/', 1)[0]
        
        # Basic domain validation
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)*[a-zA-Z]{2,}$'
        )
        return bool(domain_pattern.match(domain))
    
    def _extract_domains_from_hosts(self, content: str) -> Set[str]:
        """Extract domains from hosts file format"""
        domains = set()
        
        for line in content.split('\\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse hosts format: "127.0.0.1 domain.com" or "0.0.0.0 domain.com"
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                domain = parts[1]
                
                # Check if it's a blocking entry
                if ip in ['127.0.0.1', '0.0.0.0'] and self._validate_domain(domain):
                    domains.add(domain.lower())
        
        return domains
    
    def _extract_domains_from_list(self, content: str) -> Set[str]:
        """Extract domains from plain domain list format"""
        domains = set()
        
        for line in content.split('\\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Clean domain
            domain = line.lower()
            if self._validate_domain(domain):
                domains.add(domain)
        
        return domains
    
    def _fetch_from_source(self, source: Dict) -> Set[str]:
        """Fetch domains from a single source"""
        try:
            self.logger.info(f"Fetching from source: {source['name']}")
            
            response = requests.get(
                source['url'],
                timeout=self.config['timeout_seconds'],
                headers={'User-Agent': 'Adult Content Blocker 1.0'}
            )
            response.raise_for_status()
            
            content = response.text
            
            # Extract domains based on format
            if source['format'] == 'hosts':
                domains = self._extract_domains_from_hosts(content)
            elif source['format'] == 'domains':
                domains = self._extract_domains_from_list(content)
            else:
                self.logger.warning(f"Unknown format: {source['format']}")
                return set()
            
            self.logger.info(f"Fetched {len(domains)} domains from {source['name']}")
            return domains
            
        except Exception as e:
            self.logger.error(f"Failed to fetch from {source['name']}: {e}")
            return set()
    
    def update_from_sources(self) -> Optional[Set[str]]:
        """Update blocklist from all configured sources"""
        try:
            self.logger.info("Starting blocklist update from sources")
            
            all_domains = set()
            cache_data = self._load_cache()
            
            # Add additional domains from config
            additional_domains = set(self.config.get('additional_domains', []))
            valid_additional = {d for d in additional_domains if self._validate_domain(d)}
            all_domains.update(valid_additional)
            self.logger.info(f"Added {len(valid_additional)} additional domains from config")
            
            # Fetch from each enabled source
            for source in self.config['sources']:
                if not source.get('enabled', True):
                    continue
                
                source_name = source['name']
                
                # Check cache first
                if self._is_cache_valid(cache_data, source_name):
                    cached_domains = set(cache_data[source_name]['domains'])
                    all_domains.update(cached_domains)
                    self.logger.info(f"Used cached data for {source_name}: {len(cached_domains)} domains")
                    continue
                
                # Fetch fresh data
                domains = self._fetch_from_source(source)
                if domains:
                    all_domains.update(domains)
                    
                    # Update cache
                    cache_data[source_name] = {
                        'domains': list(domains),
                        'timestamp': datetime.now().isoformat(),
                        'count': len(domains)
                    }
            
            # Save updated cache
            self._save_cache(cache_data)
            
            # Save consolidated blocklist
            self._save_domains(all_domains)
            
            self.logger.log_blocking_action("update_blocklist", len(all_domains), True)
            self.logger.info(f"Blocklist update completed: {len(all_domains)} total domains")
            
            return all_domains
            
        except Exception as e:
            self.logger.error(f"Failed to update blocklist: {e}")
            self.logger.log_blocking_action("update_blocklist", 0, False)
            return None
    
    def _save_domains(self, domains: Set[str]):
        """Save domains to local blocklist file"""
        try:
            sorted_domains = sorted(domains)
            
            with open(self.blocklist_file, 'w', encoding='utf-8') as f:
                f.write(f"# Adult Content Blocklist\\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"# Total domains: {len(sorted_domains)}\\n\\n")
                
                for domain in sorted_domains:
                    f.write(f"{domain}\\n")
            
            self.logger.info(f"Saved {len(sorted_domains)} domains to {self.blocklist_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save domains: {e}")
    
    def get_domains(self) -> Set[str]:
        """Get current list of blocked domains"""
        try:
            if os.path.exists(self.blocklist_file):
                with open(self.blocklist_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                domains = set()
                for line in content.split('\\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if self._validate_domain(line):
                            domains.add(line.lower())
                
                return domains
            else:
                # If no blocklist file exists, return additional domains from config
                additional = set(self.config.get('additional_domains', []))
                return {d for d in additional if self._validate_domain(d)}
                
        except Exception as e:
            self.logger.error(f"Failed to get domains: {e}")
            return set()
    
    def add_domain(self, domain: str) -> bool:
        """Add a single domain to the blocklist"""
        try:
            if not self._validate_domain(domain):
                raise ValueError(f"Invalid domain: {domain}")
            
            current_domains = self.get_domains()
            current_domains.add(domain.lower())
            
            self._save_domains(current_domains)
            self.logger.info(f"Added domain to blocklist: {domain}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add domain {domain}: {e}")
            return False
    
    def remove_domain(self, domain: str) -> bool:
        """Remove a single domain from the blocklist"""
        try:
            current_domains = self.get_domains()
            domain_lower = domain.lower()
            
            if domain_lower in current_domains:
                current_domains.remove(domain_lower)
                self._save_domains(current_domains)
                self.logger.info(f"Removed domain from blocklist: {domain}")
                return True
            else:
                self.logger.warning(f"Domain not found in blocklist: {domain}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove domain {domain}: {e}")
            return False
    
    def is_update_needed(self) -> bool:
        """Check if an update is needed based on configured interval"""
        try:
            if not os.path.exists(self.blocklist_file):
                return True
            
            last_modified = datetime.fromtimestamp(os.path.getmtime(self.blocklist_file))
            update_interval = timedelta(hours=self.config['update_interval_hours'])
            
            return datetime.now() - last_modified > update_interval
            
        except Exception as e:
            self.logger.error(f"Failed to check update status: {e}")
            return True
    
    def get_stats(self) -> Dict:
        """Get statistics about the blocklist"""
        try:
            domains = self.get_domains()
            
            stats = {
                "total_domains": len(domains),
                "last_update": None,
                "update_needed": self.is_update_needed(),
                "sources_count": len([s for s in self.config['sources'] if s.get('enabled', True)]),
                "cache_size": 0
            }
            
            # Get last update time
            if os.path.exists(self.blocklist_file):
                stats["last_update"] = datetime.fromtimestamp(
                    os.path.getmtime(self.blocklist_file)
                ).isoformat()
            
            # Get cache info
            if os.path.exists(self.cache_file):
                stats["cache_size"] = os.path.getsize(self.cache_file)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Test the blocklist updater
    updater = BlocklistUpdater()
    
    print(f"Stats: {updater.get_stats()}")
    print(f"Update needed: {updater.is_update_needed()}")
    print(f"Current domains count: {len(updater.get_domains())}")
    
    # Uncomment to test actual update (will take time)
    # print("Updating from sources...")
    # domains = updater.update_from_sources()
    # print(f"Update result: {len(domains) if domains else 0} domains")
