#!/usr/bin/env python3
"""
Hosts file blocker module for blocking adult content domains
"""

import os
import re
import shutil
from datetime import datetime
from typing import List, Set, Optional

# Handle imports for both standalone and package usage
try:
    from src.utils.permissions import check_admin_rights, can_modify_hosts
    from src.utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.permissions import check_admin_rights, can_modify_hosts
    from utils.logger import Logger

class HostsBlocker:
    def __init__(self):
        """Initialize the hosts file blocker"""
        self.logger = Logger()
        
        # Windows hosts file path
        self.hosts_path = os.path.join(
            os.environ.get('WINDIR', 'C:\\Windows'),
            'System32', 'drivers', 'etc', 'hosts'
        )
        
        # Backup file path
        self.backup_path = self.hosts_path + '.blocker_backup'
        
        # Marker comments for our entries
        self.start_marker = "# === ADULT CONTENT BLOCKER START ==="
        self.end_marker = "# === ADULT CONTENT BLOCKER END ==="
        
        self.logger.debug(f"Hosts blocker initialized. Hosts path: {self.hosts_path}")
    
    def _create_backup(self) -> bool:
        """
        Create a backup of the current hosts file
        
        Returns:
            True if backup was created successfully
        """
        try:
            if os.path.exists(self.hosts_path):
                shutil.copy2(self.hosts_path, self.backup_path)
                self.logger.info("Hosts file backup created")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to create hosts backup: {e}")
            return False
    
    def _restore_backup(self) -> bool:
        """
        Restore hosts file from backup
        
        Returns:
            True if backup was restored successfully
        """
        try:
            if os.path.exists(self.backup_path):
                shutil.copy2(self.backup_path, self.hosts_path)
                self.logger.info("Hosts file restored from backup")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to restore hosts backup: {e}")
            return False
    
    def _read_hosts_file(self) -> str:
        """
        Read the current hosts file content
        
        Returns:
            Content of hosts file as string
        """
        try:
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(self.hosts_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to read hosts file: {e}")
            return ""
    
    def _write_hosts_file(self, content: str) -> bool:
        """
        Write content to hosts file
        
        Args:
            content: Content to write to hosts file
            
        Returns:
            True if write was successful
        """
        try:
            with open(self.hosts_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Failed to write hosts file: {e}")
            return False
    
    def _remove_existing_blocks(self, content: str) -> str:
        """
        Remove existing blocker entries from hosts content
        
        Args:
            content: Current hosts file content
            
        Returns:
            Content with blocker entries removed
        """
        lines = content.split('\\n')
        new_lines = []
        in_blocker_section = False
        
        for line in lines:
            if self.start_marker in line:
                in_blocker_section = True
                continue
            elif self.end_marker in line:
                in_blocker_section = False
                continue
            
            if not in_blocker_section:
                new_lines.append(line)
        
        return '\\n'.join(new_lines)
    
    def _validate_domain(self, domain: str) -> bool:
        """
        Validate if a domain is properly formatted
        
        Args:
            domain: Domain to validate
            
        Returns:
            True if domain is valid
        """
        # Basic domain validation
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)*.+$'
        )
        return bool(domain_pattern.match(domain))
    
    def block_domains(self, domains: List[str]) -> bool:
        """
        Block a list of domains by adding them to hosts file
        
        Args:
            domains: List of domains to block
            
        Returns:
            True if blocking was successful
        """
        if not check_admin_rights():
            self.logger.error("Admin rights required to modify hosts file")
            raise PermissionError("Administrator privileges required")
        
        if not can_modify_hosts():
            self.logger.error("Cannot modify hosts file")
            raise PermissionError("Cannot modify hosts file")
        
        try:
            # Create backup first
            self._create_backup()
            
            # Read current hosts file
            current_content = self._read_hosts_file()
            
            # Remove any existing blocker entries
            clean_content = self._remove_existing_blocks(current_content)
            
            # Validate and clean domains
            valid_domains = set()
            for domain in domains:
                domain = domain.strip().lower()
                if self._validate_domain(domain):
                    valid_domains.add(domain)
                    # Also add www. variant if it doesn't start with www.
                    if not domain.startswith('www.'):
                        valid_domains.add(f'www.{domain}')
            
            if not valid_domains:
                self.logger.warning("No valid domains to block")
                return False
            
            # Create blocker section
            blocker_section = [
                "",
                self.start_marker,
                f"# Adult Content Blocker - {len(valid_domains)} domains blocked",
                f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                ""
            ]
            
            # Add blocking entries
            for domain in sorted(valid_domains):
                blocker_section.append(f"0.0.0.0 {domain}")
            
            blocker_section.extend(["", self.end_marker, ""])
            
            # Combine content
            new_content = clean_content.rstrip() + '\\n' + '\\n'.join(blocker_section)
            
            # Write to hosts file
            if self._write_hosts_file(new_content):
                self.logger.log_blocking_action("hosts_block_domains", len(valid_domains), True)
                self.logger.info(f"Successfully blocked {len(valid_domains)} domains in hosts file")
                
                # Flush DNS cache
                self._flush_dns_cache()
                
                return True
            else:
                self.logger.log_blocking_action("hosts_block_domains", len(valid_domains), False)
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to block domains: {e}")
            self.logger.log_blocking_action("hosts_block_domains", len(domains), False)
            
            # Try to restore backup
            self._restore_backup()
            raise
    
    def remove_blocks(self) -> bool:
        """
        Remove all blocker entries from hosts file
        
        Returns:
            True if removal was successful
        """
        if not check_admin_rights():
            self.logger.error("Admin rights required to modify hosts file")
            raise PermissionError("Administrator privileges required")
        
        try:
            # Read current hosts file
            current_content = self._read_hosts_file()
            
            # Remove blocker entries
            clean_content = self._remove_existing_blocks(current_content)
            
            # Write clean content back
            if self._write_hosts_file(clean_content):
                self.logger.log_blocking_action("hosts_remove_blocks", 0, True)
                self.logger.info("Successfully removed all blocking entries from hosts file")
                
                # Flush DNS cache
                self._flush_dns_cache()
                
                return True
            else:
                self.logger.log_blocking_action("hosts_remove_blocks", 0, False)
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove blocks: {e}")
            self.logger.log_blocking_action("hosts_remove_blocks", 0, False)
            raise
    
    def is_active(self) -> bool:
        """
        Check if the blocker is currently active (has entries in hosts file)
        
        Returns:
            True if blocker entries exist in hosts file
        """
        try:
            content = self._read_hosts_file()
            return self.start_marker in content and self.end_marker in content
        except Exception as e:
            self.logger.error(f"Failed to check if blocker is active: {e}")
            return False
    
    def get_blocked_domains(self) -> Set[str]:
        """
        Get list of currently blocked domains
        
        Returns:
            Set of blocked domains
        """
        try:
            content = self._read_hosts_file()
            lines = content.split('\\n')
            
            blocked_domains = set()
            in_blocker_section = False
            
            for line in lines:
                if self.start_marker in line:
                    in_blocker_section = True
                    continue
                elif self.end_marker in line:
                    in_blocker_section = False
                    continue
                
                if in_blocker_section and line.strip():
                    # Parse line: "0.0.0.0 domain.com"
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0] == "0.0.0.0":
                        blocked_domains.add(parts[1])
            
            return blocked_domains
            
        except Exception as e:
            self.logger.error(f"Failed to get blocked domains: {e}")
            return set()
    
    def _flush_dns_cache(self):
        """Flush DNS cache to ensure changes take effect immediately"""
        try:
            import subprocess
            subprocess.run(['ipconfig', '/flushdns'], 
                         capture_output=True, check=True)
            self.logger.info("DNS cache flushed")
        except Exception as e:
            self.logger.warning(f"Failed to flush DNS cache: {e}")
    
    def get_stats(self) -> dict:
        """
        Get statistics about current blocking status
        
        Returns:
            Dictionary with blocking statistics
        """
        try:
            blocked_domains = self.get_blocked_domains()
            
            return {
                "is_active": self.is_active(),
                "total_blocked_domains": len(blocked_domains),
                "has_backup": os.path.exists(self.backup_path),
                "hosts_file_size": os.path.getsize(self.hosts_path) if os.path.exists(self.hosts_path) else 0,
                "can_modify": can_modify_hosts(),
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(self.hosts_path)
                ).isoformat() if os.path.exists(self.hosts_path) else None
            }
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Test the hosts blocker
    blocker = HostsBlocker()
    
    print(f"Blocker stats: {blocker.get_stats()}")
    print(f"Is active: {blocker.is_active()}")
    print(f"Blocked domains count: {len(blocker.get_blocked_domains())}")
