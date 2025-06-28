"""
Platform manager for cross-platform blocking support
"""

import platform
import logging
from abc import ABC, abstractmethod
from typing import Dict, List

logger = logging.getLogger(__name__)


class PlatformManager(ABC):
    """Abstract platform manager for cross-platform support"""
    
    @abstractmethod
    def block_domains(self, domains: List[str]) -> bool:
        """Block domains on this platform"""
        pass
    
    @abstractmethod
    def unblock_domains(self, domains: List[str]) -> bool:
        """Unblock domains on this platform"""
        pass
    
    @abstractmethod
    def get_system_info(self) -> Dict[str, str]:
        """Get system information"""
        pass


class WindowsManager(PlatformManager):
    """Windows-specific implementation"""
    
    def __init__(self):
        self.hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
    
    def block_domains(self, domains: List[str]) -> bool:
        """Block domains using Windows hosts file"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                content = f.read()
            
            # Add blocking entries
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Blocked {len(domains)} domains on Windows")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on Windows: {e}")
            return False
    
    def unblock_domains(self, domains: List[str]) -> bool:
        """Unblock domains on Windows"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                lines = f.readlines()
            
            # Remove blocking entries
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.writelines(filtered_lines)
            
            logger.info(f"Unblocked {len(domains)} domains on Windows")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on Windows: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """Get Windows system information"""
        return {
            "platform": "Windows",
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "hosts_file": self.hosts_file
        }


class LinuxManager(PlatformManager):
    """Linux-specific implementation"""
    
    def __init__(self):
        self.hosts_file = "/etc/hosts"
    
    def block_domains(self, domains: List[str]) -> bool:
        """Block domains using Linux hosts file"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                content = f.read()
            
            # Add blocking entries
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Blocked {len(domains)} domains on Linux")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on Linux: {e}")
            return False
    
    def unblock_domains(self, domains: List[str]) -> bool:
        """Unblock domains on Linux"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                lines = f.readlines()
            
            # Remove blocking entries
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.writelines(filtered_lines)
            
            logger.info(f"Unblocked {len(domains)} domains on Linux")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on Linux: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """Get Linux system information"""
        return {
            "platform": "Linux",
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "hosts_file": self.hosts_file
        }


class MacOSManager(PlatformManager):
    """macOS-specific implementation"""
    
    def __init__(self):
        self.hosts_file = "/etc/hosts"
    
    def block_domains(self, domains: List[str]) -> bool:
        """Block domains using macOS hosts file"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                content = f.read()
            
            # Add blocking entries
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Blocked {len(domains)} domains on macOS")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on macOS: {e}")
            return False
    
    def unblock_domains(self, domains: List[str]) -> bool:
        """Unblock domains on macOS"""
        try:
            # Read existing hosts file
            with open(self.hosts_file, 'r') as f:
                lines = f.readlines()
            
            # Remove blocking entries
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            
            # Write back to hosts file
            with open(self.hosts_file, 'w') as f:
                f.writelines(filtered_lines)
            
            logger.info(f"Unblocked {len(domains)} domains on macOS")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on macOS: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """Get macOS system information"""
        return {
            "platform": "macOS",
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "hosts_file": self.hosts_file
        }


def get_platform_manager() -> PlatformManager:
    """Factory function to get the appropriate platform manager"""
    system = platform.system().lower()
    
    if system == "windows":
        return WindowsManager()
    elif system == "linux":
        return LinuxManager()
    elif system == "darwin":
        return MacOSManager()
    else:
        raise NotImplementedError(f"Platform {system} is not supported") 