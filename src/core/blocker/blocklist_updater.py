#!/usr/bin/env python3
"""
Blocklist updater module for fetching and managing domain blocklists
"""

import requests
import json
import os
import re
import io
import tempfile
import zipfile
import tarfile
from datetime import datetime, timedelta
from typing import Set, Dict, Optional

# Handle imports for both standalone and package usage
try:
    from src.utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from utils.logger import Logger


class BlocklistUpdater:
    def __init__(self):
        """Initialize blocklist updater"""
        self.logger = Logger()

        # Data directory
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)

        # Local files
        self.blocklist_file = os.path.join(self.data_dir, "blocklist.txt")
        self.config_file = os.path.join(self.data_dir, "updater_config.json")
        self.cache_file = os.path.join(self.data_dir, "blocklist_cache.json")

        # Default configuration
        self.default_config = {
            "update_interval_hours": 24,
            "max_cache_age_hours": 48,
            "timeout_seconds": 30,
            "sources": [
                {
                    "name": "StevenBlack Fakenews-Gambling-Porn",
                    "url": (
                        "https://raw.githubusercontent.com/StevenBlack/hosts/"
                        "master/alternates/fakenews-gambling-porn/hosts"
                    ),
                    "format": "hosts",
                    "enabled": True,
                },
                {
                    "name": "StevenBlack Porn",
                    "url": (
                        "https://raw.githubusercontent.com/StevenBlack/hosts/"
                        "master/alternates/porn/hosts"
                    ),
                    "format": "hosts",
                    "enabled": True,
                },
                {
                    "name": "Ultimate NSFW Blocklist",
                    "url": (
                        "https://raw.githubusercontent.com/chadmayfield/"
                        "my-pihole-blocklists/master/lists/pi_blocklist_porn_all.list"
                    ),
                    "format": "domains",
                    "enabled": True,
                },
                {
                    "name": "UT1 Adult",
                    "url": (
                        "https://dsi.ut-capitole.fr/blacklists/download/" "adult.tar.gz"
                    ),
                    "format": "ut1",
                    "enabled": False,  # Requires special handling
                },
                {
                    "name": "Energized Porn",
                    "url": ("https://block.energized.pro/porn/formats/" "domains.txt"),
                    "format": "domains",
                    "enabled": True,
                },
                {
                    "name": "Sinfonietta's Porn List",
                    "url": (
                        "https://raw.githubusercontent.com/Sinfonietta/"
                        "hostfiles/master/pornography-hosts"
                    ),
                    "format": "hosts",
                    "enabled": True,
                },
            ],
            "categories": {
                "adult": {"enabled": True, "description": "Adult content websites"},
                "gambling": {"enabled": True, "description": "Gambling websites"},
                "kenya": {
                    "enabled": True,
                    "description": "Kenya-specific adult content sites",
                },
                "pucs": {
                    "enabled": True,
                    "description": "Public upskirt and voyeur sites",
                },
            },
            "additional_domains": [
                # Social media adult content pages
                "reddit.com/r/gonewild",
                "reddit.com/r/nsfw",
                "reddit.com/r/porn",
                "reddit.com/r/sex",
                "reddit.com/r/amateur",
                "reddit.com/r/milf",
                "twitter.com/search?q=porn",
                "instagram.com/explore/tags/nsfw",
                # Major adult sites - comprehensive list
                "pornhub.com",
                "xvideos.com",
                "xnxx.com",
                "redtube.com",
                "youporn.com",
                "tube8.com",
                "spankbang.com",
                "xhamster.com",
                "brazzers.com",
                "bangbros.com",
                "naughtyamerica.com",
                "realitykings.com",
                "mofos.com",
                "digitalplayground.com",
                # Cam sites
                "chaturbate.com",
                "cam4.com",
                "bongacams.com",
                "stripchat.com",
                "livejasmin.com",
                "flirt4free.com",
                "streamate.com",
                # Dating/hookup sites
                "adultfriendfinder.com",
                "ashley-madison.com",
                "seeking.com",
                "benaughty.com",
                "fling.com",
                "alt.com",
                # Escort/adult services
                "tryst.link",
                "eros.com",
                "slixa.com",
                "skipthegames.com",
                "listcrawler.com",
                "bedpage.com",
                "cityxguide.com",
                # Fetish/BDSM sites
                "fetlife.com",
                "kink.com",
                "dungeoncorp.com",
                "subspace.land",
                # Adult gaming
                "nutaku.net",
                "f95zone.to",
                "lewdgamer.com",
                # International adult sites
                "javhd.com",
                "japanese-adult-video.com",
                "av01.tv",
                "eporner.com",
                "beeg.com",
                "tnaflix.com",
                "drtuber.com",
                # Adult comics/manga
                "nhentai.net",
                "tsumino.com",
                "hentai-foundry.com",
                "e-hentai.org",
                "exhentai.org",
                "fakku.net",
                # Torrents (adult)
                "empornium.me",
                "pornbay.org",
                "pornolab.net",
                # Kenya-specific adult sites
                "nairobiraha.com",
                "nairobihot.com",
                "nairobi-escorts.com",
                "kenyacupid.com",
                "kenyatopescorts.com",
                "hotkenya.com",
                "kenyagirls.net",
                "kenyaxrated.com",
                "mombasaplaymates.com",
                "kenyaicuts.net",
                "escortskenya.org",
                "mombasahot.com",
                # PUCs (Public Upskirt Content) sites
                "upskirtcollection.com",
                "voyeurforum.com",
                "upskirt-times.com",
                "candid-forum.net",
                "candidboard.com",
                "upskirt-voyeur.net",
                "voyeurpapa.com",
                "upskirtsource.com",
                "candidspot.net",
                "voyeurjapantv.com",
                "realwifestories.com",
                "voyeurhit.com",
                "upskirtjerk.org",
                "candidshores.com",
                "voyeurweb.com",
                "voyeurbeach.net",
                "upskirtcity.net",
                "candidcafe.net",
            ],
        }

        # Load or create configuration
        self.config = self._load_config()

        self.logger.debug("Blocklist updater initialized")

    def _load_config(self) -> Dict:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all required fields exist
                    merged_config = self.default_config.copy()
                    merged_config.update(config)
                    return merged_config
            else:
                # Create default config file
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            self.logger.error(f"Failed to load config, using defaults: {e}")
            return self.default_config

    def _save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            self.logger.debug("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    def _load_cache(self) -> Dict:
        """Load cached data"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load cache: {e}")
            return {}

    def _save_cache(self, cache_data: Dict):
        """Save cache data"""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=4)
            self.logger.debug("Cache data saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save cache: {e}")

    def _is_cache_valid(self, cache_data: Dict, source_name: str) -> bool:
        """Check if cached data is still valid"""
        if source_name not in cache_data:
            return False

        try:
            cached_time = datetime.fromisoformat(cache_data[source_name]["timestamp"])
            max_age = timedelta(hours=self.config["max_cache_age_hours"])
            return datetime.now() - cached_time < max_age
        except Exception:
            return False

    def _validate_domain(self, domain: str) -> bool:
        """Validate if a domain is properly formatted"""
        if not domain or len(domain) > 253:
            return False

        # Remove protocol if present
        if "://" in domain:
            domain = domain.split("://", 1)[1]

        # Remove path if present
        if "/" in domain:
            domain = domain.split("/", 1)[0]

        # Basic domain validation
        domain_pattern = re.compile(
            r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\."
            r"([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
            r"[a-zA-Z]{2,}$"
        )
        return bool(domain_pattern.match(domain))

    def _extract_domains_from_hosts(self, content: str) -> Set[str]:
        """Extract domains from hosts file format"""
        domains = set()

        for line in content.split("\n"):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Parse hosts format: "127.0.0.1 domain.com" or "0.0.0.0 domain.com"
            parts = line.split()
            if len(parts) >= 2:
                domain = parts[1].lower()
                if self._validate_domain(domain):
                    domains.add(domain)

        return domains

    def _extract_domains_from_list(self, content: str) -> Set[str]:
        """Extract domains from plain domain list format"""
        domains = set()

        for line in content.split("\n"):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
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
                source["url"],
                timeout=self.config["timeout_seconds"],
                headers={"User-Agent": "Adult Content Blocker 1.0"},
            )
            response.raise_for_status()

            # Handle different formats
            format_type = source["format"]

            # Text-based formats
            if format_type in ["hosts", "domains"]:
                content = response.text

                if format_type == "hosts":
                    domains = self._extract_domains_from_hosts(content)
                elif format_type == "domains":
                    domains = self._extract_domains_from_list(content)
                else:
                    self.logger.error(f"Unsupported format: {format_type}")
                    domains = set()
            # Compressed formats
            elif format_type in ["ut1", "zip"]:
                content = response.content
                domains = self._extract_domains_from_compressed(content, format_type)
            else:
                self.logger.error(f"Unsupported format: {format_type}")
                domains = set()

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
            cache_updated = False

            # Add additional domains from config
            additional_domains = set(self.config.get("additional_domains", []))
            valid_additional = {
                d for d in additional_domains if self._validate_domain(d)
            }
            self.logger.info(f"Added {len(valid_additional)} valid domains from config")
            all_domains.update(valid_additional)

            # Process each source
            for source in self.config["sources"]:
                if not source.get("enabled", True):
                    self.logger.info(f"Skipping disabled source: {source['name']}")
                    continue

                source_name = source["name"]
                # Check if we can use cached data
                if self._is_cache_valid(cache_data, source_name):
                    self.logger.info(f"Using cached data for {source_name}")
                    source_domains = set(cache_data[source_name]["domains"])
                    all_domains.update(source_domains)
                    continue

                # Fetch from source
                source_domains = self._fetch_from_source(source)

                # Update cache if we got domains
                if source_domains:
                    if source_name not in cache_data:
                        cache_data[source_name] = {}

                    cache_data[source_name]["domains"] = list(source_domains)
                    cache_data[source_name]["timestamp"] = datetime.now().isoformat()
                    cache_updated = True

                    all_domains.update(source_domains)

            # Save updated cache
            if cache_updated:
                self._save_cache(cache_data)

            # Save domains to file
            if all_domains:
                self._save_domains(all_domains)
                self.logger.info(
                    f"Successfully updated blocklist with {len(all_domains)} domains"
                )
                return all_domains
            else:
                self.logger.warning("No domains found to update blocklist")
                return None

        except Exception as e:
            self.logger.error(f"Failed to update from sources: {e}")
            return None

    def _save_domains(self, domains: Set[str]):
        """Save domains to local blocklist file"""
        try:
            # Sort domains for consistency
            sorted_domains = sorted(domains)

            with open(self.blocklist_file, "w", encoding="utf-8") as f:
                f.write("# Adult Content Blocker Domain List\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n")
                f.write(f"# Total domains: {len(sorted_domains)}\n\n")

                for domain in sorted_domains:
                    f.write(f"{domain}\n")

            self.logger.info(
                f"Successfully saved {len(domains)} domains to "
                f"{self.blocklist_file}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to save domains: {e}")
            return False

    def get_domains(self) -> Set[str]:
        """Get current list of blocked domains"""
        try:
            if not os.path.exists(self.blocklist_file):
                self.logger.warning(f"Blocklist file not found: {self.blocklist_file}")
                return set()

            domains = set()
            with open(self.blocklist_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    domains.add(line)

            self.logger.debug(f"Retrieved {len(domains)} domains from blocklist")
            return domains
        except Exception as e:
            self.logger.error(f"Failed to get domains: {e}")
            return set()

    def add_domain(self, domain: str) -> bool:
        """Add a single domain to the blocklist"""
        try:
            domain = domain.strip().lower()

            # Validate domain
            if not self._validate_domain(domain):
                self.logger.warning(f"Invalid domain format: {domain}")
                return False

            # Get current domains
            domains = self.get_domains()

            # Check if already in list
            if domain in domains:
                self.logger.info(f"Domain already in blocklist: {domain}")
                return True

            # Add to set and save
            domains.add(domain)
            self._save_domains(domains)

            self.logger.info(f"Added domain to blocklist: {domain}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add domain: {e}")
            return False

    def remove_domain(self, domain: str) -> bool:
        """Remove a single domain from the blocklist"""
        try:
            domain = domain.strip().lower()

            # Get current domains
            domains = self.get_domains()

            # Check if domain exists
            if domain not in domains:
                self.logger.info(f"Domain not found in blocklist: {domain}")
                return False

            # Remove from set and save
            domains.remove(domain)
            self._save_domains(domains)

            self.logger.info(f"Removed domain from blocklist: {domain}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove domain: {e}")
            return False

    def is_update_needed(self) -> bool:
        """Check if an update is needed based on configured interval"""
        try:
            # If blocklist doesn't exist, update is needed
            if not os.path.exists(self.blocklist_file):
                self.logger.info("Blocklist file not found, update needed")
                return True

            # Check file modification time
            mtime = os.path.getmtime(self.blocklist_file)
            last_update = datetime.fromtimestamp(mtime)
            now = datetime.now()

            # Get configured update interval
            update_interval = timedelta(
                hours=self.config.get("update_interval_hours", 24)
            )

            # Check if update interval has passed
            if now - last_update > update_interval:
                self.logger.info(
                    f"Update interval ({update_interval}) exceeded, update needed"
                )
                return True

            self.logger.debug("No update needed at this time")
            return False
        except Exception as e:
            self.logger.error(f"Failed to check if update is needed: {e}")
            # If there's an error, assume update is needed for safety
            return True

    def get_stats(self) -> Dict:
        """Get statistics about the blocklist"""
        try:
            domains = self.get_domains()

            stats = {
                "total_domains": len(domains),
                "blocklist_exists": os.path.exists(self.blocklist_file),
                "cache_exists": os.path.exists(self.cache_file),
                "config_exists": os.path.exists(self.config_file),
                "update_needed": self.is_update_needed(),
            }

            # Add last update time if file exists
            if os.path.exists(self.blocklist_file):
                mtime = os.path.getmtime(self.blocklist_file)
                stats["last_update"] = datetime.fromtimestamp(mtime).isoformat()
                stats["file_size"] = os.path.getsize(self.blocklist_file)

            # Add configured sources count
            stats["enabled_sources"] = sum(
                1 for s in self.config["sources"] if s.get("enabled", True)
            )
            stats["total_sources"] = len(self.config["sources"])

            # Additional domains count
            stats["additional_domains"] = len(self.config.get("additional_domains", []))

            return stats
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}

    def categorize_domains(self, domains: Set[str]) -> Dict[str, Set[str]]:
        """
        Categorize domains by type (adult, gambling, etc.)

        Args:
            domains: Set of domains to categorize

        Returns:
            Dictionary mapping categories to domain sets
        """
        categories = {
            "adult": set(),
            "gambling": set(),
            "social": set(),
            "streaming": set(),
            "dating": set(),
            "other": set(),
        }

        # Keywords for categorization
        category_keywords = {
            "adult": [
                "porn",
                "xxx",
                "adult",
                "sex",
                "nude",
                "naked",
                "hentai",
                "xvideos",
                "pornhub",
                "xnxx",
                "xhamster",
                "redtube",
                "youporn",
            ],
            "gambling": [
                "gambling",
                "casino",
                "bet",
                "poker",
                "roulette",
                "slot",
                "blackjack",
                "bingo",
                "lottery",
                "wager",
            ],
            "social": [
                "reddit",
                "twitter",
                "instagram",
                "tiktok",
                "facebook",
                "snapchat",
                "tumblr",
                "pinterest",
                "telegram",
            ],
            "streaming": [
                "stream",
                "video",
                "tube",
                "cam",
                "live",
                "webcam",
                "onlyfans",
                "chaturbate",
                "cam4",
            ],
            "dating": [
                "date",
                "dating",
                "match",
                "meet",
                "hookup",
                "friend",
                "flirt",
                "tinder",
                "bumble",
                "okcupid",
                "grindr",
            ],
        }

        for domain in domains:
            categorized = False

            # Check each category's keywords
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword in domain:
                        categories[category].add(domain)
                        categorized = True
                        break
                if categorized:
                    break

            # If not categorized, put in "other"
            if not categorized:
                categories["other"].add(domain)

        return categories

    def save_categorized_domains(self) -> Dict[str, int]:
        """
        Save domains in categorized files

        Returns:
            Dictionary with count of domains per category
        """
        try:
            domains = self.get_domains()
            categories = self.categorize_domains(domains)
            category_counts = {}

            # Create category directory if it doesn't exist
            category_dir = os.path.join(self.data_dir, "categories")
            os.makedirs(category_dir, exist_ok=True)

            # Save each category to its own file
            for category, cat_domains in categories.items():
                if not cat_domains:
                    continue

                category_file = os.path.join(category_dir, f"{category}.txt")

                with open(category_file, "w", encoding="utf-8") as f:
                    f.write(f"# {category.upper()} domains blocklist\n")
                    f.write(f"# Generated: {datetime.now().isoformat()}\n")
                    f.write(f"# Total domains: {len(cat_domains)}\n\n")

                    for domain in sorted(cat_domains):
                        f.write(f"{domain}\n")

                category_counts[category] = len(cat_domains)

            self.logger.info(f"Saved categorized domain lists: {category_counts}")
            return category_counts
        except Exception as e:
            self.logger.error(f"Failed to save categorized domains: {e}")
            return {}

    def export_blocklist(
        self, format_type: str, output_dir: Optional[str] = None
    ) -> str:
        """
        Export blocklist in different formats

        Args:
            format_type: Format to export ('hosts', 'domains', 'adblock', 'json')
            output_dir: Optional output directory, defaults to data directory

        Returns:
            Path to the exported file
        """
        if not output_dir:
            output_dir = self.data_dir

        os.makedirs(output_dir, exist_ok=True)

        try:
            domains = self.get_domains()
            if not domains:
                raise ValueError("No domains found to export")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if format_type == "hosts":
                # Hosts file format (0.0.0.0 domain.com)
                output_file = os.path.join(
                    output_dir, f"blocklist_hosts_{timestamp}.txt"
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    for domain in sorted(domains):
                        f.write(f"0.0.0.0 {domain}\n")
                self.logger.info(f"Exported blocklist to hosts format: {output_file}")
                return output_file

            elif format_type == "domains":
                # Plain domain list format
                output_file = os.path.join(
                    output_dir, f"blocklist_domains_{timestamp}.txt"
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    for domain in sorted(domains):
                        f.write(f"{domain}\n")
                self.logger.info(f"Exported blocklist to domains format: {output_file}")
                return output_file

            elif format_type == "adblock":
                # Adblock format (for use with browser extensions)
                output_file = os.path.join(
                    output_dir, f"blocklist_adblock_{timestamp}.txt"
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("! Adult Content Blocker Adblock List\n")
                    f.write("! Generated: {}\n".format(datetime.now().isoformat()))
                    f.write("! Total domains: {}\n\n".format(len(domains)))
                    for domain in sorted(domains):
                        f.write(f"||{domain}^$third-party\n")
                self.logger.info(f"Exported blocklist to adblock format: {output_file}")
                return output_file

            elif format_type == "json":
                # JSON format
                output_file = os.path.join(output_dir, f"blocklist_{timestamp}.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump({"domains": sorted(domains)}, f, indent=4)
                self.logger.info(f"Exported blocklist to JSON format: {output_file}")
                return output_file

            else:
                self.logger.error(f"Unsupported export format: {format_type}")
                raise ValueError(f"Unsupported export format: {format_type}")

        except Exception as e:
            self.logger.error(f"Failed to export blocklist: {e}")
            return str(e)

    def _extract_domains_from_compressed(
        self, content: bytes, format_type: str
    ) -> Set[str]:
        """
        Extract domains from compressed files (UT1, ZIP)

        Args:
            content: Compressed content bytes
            format_type: Format type ('ut1' or 'zip')

        Returns:
            Set of extracted domains
        """
        domains = set()

        try:
            if format_type == "ut1":
                # Temporary directory for extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    tgz_path = os.path.join(temp_dir, "blocklist.tgz")

                    # Write content to a temporary file
                    with open(tgz_path, "wb") as f:
                        f.write(content)

                    # Extract the tar.gz file with security validation
                    with tarfile.open(tgz_path, "r:gz") as tar:
                        # Validate members to prevent path traversal attacks
                        for member in tar.getmembers():
                            # Check for path traversal attempts
                            if ".." in member.name or member.name.startswith("/"):
                                self.logger.warning(
                                    f"Skipping suspicious file in archive: {member.name}"
                                )
                                continue
                            # Check for absolute paths
                            if os.path.isabs(member.name):
                                member.name = os.path.basename(member.name)

                        tar.extractall(path=temp_dir)

                    # Find and process domain files
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            # Skip metadata files
                            if file in ("domain", "urls"):
                                file_path = os.path.join(root, file)
                                try:
                                    with open(
                                        file_path,
                                        "r",
                                        encoding="utf-8",
                                        errors="ignore",
                                    ) as f:
                                        file_content = f.read()
                                        # Each line is a domain
                                        for line in file_content.split("\n"):
                                            domain = line.strip()
                                            if domain and self._validate_domain(domain):
                                                domains.add(domain)
                                except Exception as e:
                                    self.logger.warning(
                                        f"Error processing file in archive: "
                                        f"{file_path}, {e}"
                                    )

            elif format_type == "zip":  # ZIP format
                with io.BytesIO(content) as bytes_io:
                    with zipfile.ZipFile(bytes_io) as zip_file:
                        # Process each file in the zip
                        for file_name in zip_file.namelist():
                            # Skip directories and hidden files
                            if file_name.endswith("/") or os.path.basename(
                                file_name
                            ).startswith("."):
                                continue

                            try:
                                with zip_file.open(file_name) as f:
                                    file_content = f.read().decode(
                                        "utf-8", errors="ignore"
                                    )
                                    # Process based on file extension
                                    if file_name.endswith(".txt") or file_name.endswith(
                                        ".list"
                                    ):
                                        domains.update(
                                            self._extract_domains_from_list(
                                                file_content
                                            )
                                        )
                                    elif file_name.endswith(".hosts"):
                                        domains.update(
                                            self._extract_domains_from_hosts(
                                                file_content
                                            )
                                        )
                                    else:
                                        # Try to parse as domain list by default
                                        domains.update(
                                            self._extract_domains_from_list(
                                                file_content
                                            )
                                        )
                            except Exception as e:
                                self.logger.warning(
                                    f"Error processing file in zip: {file_name}, {e}"
                                )

            self.logger.info(
                f"Extracted {len(domains)} domains from compressed file: "
                f"{format_type}"
            )
            return domains

        except Exception as e:
            self.logger.error(f"Failed to process compressed content: {e}")
            return set()


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
