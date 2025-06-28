"""
Enhanced platform manager with advanced blocking capabilities
"""

import platform
import subprocess
import logging
import os
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class EnhancedPlatformManager(ABC):
    """Enhanced platform manager with advanced features"""

    @abstractmethod
    async def block_domains_async(self, domains: List[str]) -> bool:
        """Asynchronously block domains"""
        pass

    @abstractmethod
    async def unblock_domains_async(self, domains: List[str]) -> bool:
        """Asynchronously unblock domains"""
        pass

    @abstractmethod
    def configure_dns(self, dns_servers: List[str]) -> bool:
        """Configure DNS servers"""
        pass

    @abstractmethod
    def configure_firewall(self, rules: List[Dict]) -> bool:
        """Configure firewall rules"""
        pass

    @abstractmethod
    def get_network_status(self) -> Dict[str, any]:
        """Get current network status"""
        pass

    @abstractmethod
    def detect_bypass_attempts(self) -> List[Dict]:
        """Detect bypass attempts"""
        pass


class EnhancedWindowsManager(EnhancedPlatformManager):
    """Enhanced Windows implementation with PowerShell and registry support"""

    def __init__(self):
        self.hosts_file = Path(r"C:\Windows\System32\drivers\etc\hosts")
        self.powershell_path = "powershell.exe"
        self.registry_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"

    async def block_domains_async(self, domains: List[str]) -> bool:
        """Block domains using multiple methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=True)
            
            # Method 2: PowerShell firewall rules
            await self._create_firewall_rules(domains)
            
            # Method 3: DNS blocking via registry
            await self._configure_dns_blocking(domains)
            
            logger.info(f"Successfully blocked {len(domains)} domains on Windows")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on Windows: {e}")
            return False

    async def unblock_domains_async(self, domains: List[str]) -> bool:
        """Unblock domains using multiple methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=False)
            
            # Method 2: Remove PowerShell firewall rules
            await self._remove_firewall_rules(domains)
            
            logger.info(f"Successfully unblocked {len(domains)} domains on Windows")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on Windows: {e}")
            return False

    async def _update_hosts_file(self, domains: List[str], block: bool) -> None:
        """Update hosts file asynchronously"""
        content = self.hosts_file.read_text()
        
        if block:
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
        else:
            lines = content.split('\n')
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            content = '\n'.join(filtered_lines)
        
        self.hosts_file.write_text(content)

    async def _create_firewall_rules(self, domains: List[str]) -> None:
        """Create Windows Firewall rules"""
        for domain in domains:
            # Create outbound rule to block domain
            cmd = [
                self.powershell_path,
                "-Command",
                f"New-NetFirewallRule -DisplayName 'CleanNet-{domain}' "
                f"-Direction Outbound -Action Block -RemoteAddress {domain}"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

    async def _remove_firewall_rules(self, domains: List[str]) -> None:
        """Remove Windows Firewall rules"""
        for domain in domains:
            cmd = [
                self.powershell_path,
                "-Command",
                f"Remove-NetFirewallRule -DisplayName 'CleanNet-{domain}' -ErrorAction SilentlyContinue"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

    async def _configure_dns_blocking(self, domains: List[str]) -> None:
        """Configure DNS blocking via registry"""
        # Implementation for DNS blocking via Windows registry
        pass

    def configure_dns(self, dns_servers: List[str]) -> bool:
        """Configure DNS servers on Windows"""
        try:
            for i, server in enumerate(dns_servers):
                cmd = [
                    "netsh", "interface", "ip", "set", "dns",
                    f"name=*", f"static", server
                ]
                subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure DNS: {e}")
            return False

    def configure_firewall(self, rules: List[Dict]) -> bool:
        """Configure Windows Firewall rules"""
        try:
            for rule in rules:
                cmd = [
                    self.powershell_path,
                    "-Command",
                    f"New-NetFirewallRule -DisplayName '{rule['name']}' "
                    f"-Direction {rule['direction']} -Action {rule['action']}"
                ]
                subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure firewall: {e}")
            return False

    def get_network_status(self) -> Dict[str, any]:
        """Get Windows network status"""
        try:
            # Get network adapters
            cmd = [self.powershell_path, "-Command", "Get-NetAdapter | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "platform": "Windows",
                "adapters": result.stdout,
                "firewall_enabled": self._check_firewall_status(),
                "dns_servers": self._get_dns_servers()
            }
        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
            return {}

    def detect_bypass_attempts(self) -> List[Dict]:
        """Detect bypass attempts on Windows"""
        attempts = []
        
        # Check for VPN connections
        try:
            cmd = [self.powershell_path, "-Command", "Get-VpnConnection | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                attempts.append({
                    "type": "vpn_detected",
                    "details": result.stdout,
                    "timestamp": asyncio.get_event_loop().time()
                })
        except Exception as e:
            logger.error(f"Failed to detect VPN: {e}")
        
        # Check for proxy settings
        try:
            cmd = [self.powershell_path, "-Command", "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if "ProxyServer" in result.stdout:
                attempts.append({
                    "type": "proxy_detected",
                    "details": result.stdout,
                    "timestamp": asyncio.get_event_loop().time()
                })
        except Exception as e:
            logger.error(f"Failed to detect proxy: {e}")
        
        return attempts

    def _check_firewall_status(self) -> bool:
        """Check if Windows Firewall is enabled"""
        try:
            cmd = [self.powershell_path, "-Command", "Get-NetFirewallProfile | Select-Object Name,Enabled | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return "true" in result.stdout.lower()
        except Exception:
            return False

    def _get_dns_servers(self) -> List[str]:
        """Get current DNS servers"""
        try:
            cmd = [self.powershell_path, "-Command", "Get-DnsClientServerAddress | Select-Object ServerAddresses | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Parse JSON and extract DNS servers
            return []
        except Exception:
            return []


class EnhancedLinuxManager(EnhancedPlatformManager):
    """Enhanced Linux implementation with iptables and systemd-resolved"""

    def __init__(self):
        self.hosts_file = Path("/etc/hosts")
        self.iptables_path = "/usr/sbin/iptables"
        self.systemd_resolved_conf = Path("/etc/systemd/resolved.conf")

    async def block_domains_async(self, domains: List[str]) -> bool:
        """Block domains using multiple Linux methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=True)
            
            # Method 2: iptables rules
            await self._create_iptables_rules(domains)
            
            # Method 3: systemd-resolved DNS blocking
            await self._configure_systemd_dns(domains)
            
            logger.info(f"Successfully blocked {len(domains)} domains on Linux")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on Linux: {e}")
            return False

    async def unblock_domains_async(self, domains: List[str]) -> bool:
        """Unblock domains using multiple Linux methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=False)
            
            # Method 2: Remove iptables rules
            await self._remove_iptables_rules(domains)
            
            logger.info(f"Successfully unblocked {len(domains)} domains on Linux")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on Linux: {e}")
            return False

    async def _update_hosts_file(self, domains: List[str], block: bool) -> None:
        """Update hosts file asynchronously"""
        content = self.hosts_file.read_text()
        
        if block:
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
        else:
            lines = content.split('\n')
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            content = '\n'.join(filtered_lines)
        
        self.hosts_file.write_text(content)

    async def _create_iptables_rules(self, domains: List[str]) -> None:
        """Create iptables rules for domain blocking"""
        for domain in domains:
            # Block outbound traffic to domain
            cmd = [
                self.iptables_path,
                "-A", "OUTPUT",
                "-d", domain,
                "-j", "DROP"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

    async def _remove_iptables_rules(self, domains: List[str]) -> None:
        """Remove iptables rules for domain blocking"""
        for domain in domains:
            cmd = [
                self.iptables_path,
                "-D", "OUTPUT",
                "-d", domain,
                "-j", "DROP"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

    async def _configure_systemd_dns(self, domains: List[str]) -> None:
        """Configure systemd-resolved DNS blocking"""
        # Implementation for systemd-resolved DNS blocking
        pass

    def configure_dns(self, dns_servers: List[str]) -> bool:
        """Configure DNS servers on Linux"""
        try:
            # Update systemd-resolved configuration
            config_content = f"""[Resolve]
DNS={', '.join(dns_servers)}
#FallbackDNS=1.1.1.1 8.8.8.8
#Domains=
#DNSSEC=no
#DNSOverTLS=no
#MulticastDNS=yes
#LLMNR=yes
#Cache=yes
#DNSStubListener=yes
"""
            self.systemd_resolved_conf.write_text(config_content)
            
            # Restart systemd-resolved
            subprocess.run(["systemctl", "restart", "systemd-resolved"], check=True)
            return True
        except Exception as e:
            logger.error(f"Failed to configure DNS: {e}")
            return False

    def configure_firewall(self, rules: List[Dict]) -> bool:
        """Configure iptables firewall rules"""
        try:
            for rule in rules:
                cmd = [
                    self.iptables_path,
                    "-A", rule.get("chain", "OUTPUT"),
                    "-d", rule.get("destination", ""),
                    "-j", rule.get("action", "DROP")
                ]
                subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure firewall: {e}")
            return False

    def get_network_status(self) -> Dict[str, any]:
        """Get Linux network status"""
        try:
            # Get network interfaces
            cmd = ["ip", "addr", "show"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Get iptables rules
            cmd2 = [self.iptables_path, "-L", "-n"]
            result2 = subprocess.run(cmd2, capture_output=True, text=True)
            
            return {
                "platform": "Linux",
                "interfaces": result.stdout,
                "iptables_rules": result2.stdout,
                "systemd_resolved_status": self._check_systemd_status()
            }
        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
            return {}

    def detect_bypass_attempts(self) -> List[Dict]:
        """Detect bypass attempts on Linux"""
        attempts = []
        
        # Check for VPN interfaces
        try:
            cmd = ["ip", "tunnel", "show"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                attempts.append({
                    "type": "vpn_tunnel_detected",
                    "details": result.stdout,
                    "timestamp": asyncio.get_event_loop().time()
                })
        except Exception as e:
            logger.error(f"Failed to detect VPN tunnels: {e}")
        
        # Check for proxy environment variables
        proxy_vars = ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]
        for var in proxy_vars:
            if var in os.environ:
                attempts.append({
                    "type": "proxy_environment_detected",
                    "details": f"{var}={os.environ[var]}",
                    "timestamp": asyncio.get_event_loop().time()
                })
        
        return attempts

    def _check_systemd_status(self) -> Dict[str, any]:
        """Check systemd-resolved status"""
        try:
            cmd = ["systemctl", "status", "systemd-resolved"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"status": result.stdout}
        except Exception:
            return {"status": "unknown"}


class EnhancedMacOSManager(EnhancedPlatformManager):
    """Enhanced macOS implementation with pf firewall and DNS configuration"""
    
    def __init__(self):
        self.hosts_file = Path("/etc/hosts")
        self.pf_conf = Path("/etc/pf.conf")
        self.dns_conf = Path("/etc/resolv.conf")

    async def block_domains_async(self, domains: List[str]) -> bool:
        """Block domains using multiple macOS methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=True)
            
            # Method 2: pf firewall rules
            await self._create_pf_rules(domains)
            
            # Method 3: DNS configuration
            await self._configure_macos_dns(domains)
            
            logger.info(f"Successfully blocked {len(domains)} domains on macOS")
            return True
            
        except Exception as e:
            logger.error(f"Failed to block domains on macOS: {e}")
            return False

    async def unblock_domains_async(self, domains: List[str]) -> bool:
        """Unblock domains using multiple macOS methods"""
        try:
            # Method 1: Hosts file
            await self._update_hosts_file(domains, block=False)
            
            # Method 2: Remove pf firewall rules
            await self._remove_pf_rules(domains)
            
            logger.info(f"Successfully unblocked {len(domains)} domains on macOS")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unblock domains on macOS: {e}")
            return False

    async def _update_hosts_file(self, domains: List[str], block: bool) -> None:
        """Update hosts file asynchronously"""
        content = self.hosts_file.read_text()
        
        if block:
            for domain in domains:
                if domain not in content:
                    content += f"\n127.0.0.1 {domain}"
                    content += f"\n127.0.0.1 www.{domain}"
        else:
            lines = content.split('\n')
            filtered_lines = []
            for line in lines:
                should_keep = True
                for domain in domains:
                    if domain in line and "127.0.0.1" in line:
                        should_keep = False
                        break
                if should_keep:
                    filtered_lines.append(line)
            content = '\n'.join(filtered_lines)
        
        self.hosts_file.write_text(content)

    async def _create_pf_rules(self, domains: List[str]) -> None:
        """Create pf firewall rules for domain blocking"""
        # Implementation for pf firewall rules
        pass

    async def _remove_pf_rules(self, domains: List[str]) -> None:
        """Remove pf firewall rules for domain blocking"""
        # Implementation for removing pf firewall rules
        pass

    async def _configure_macos_dns(self, domains: List[str]) -> None:
        """Configure macOS DNS blocking"""
        # Implementation for macOS DNS configuration
        pass

    def configure_dns(self, dns_servers: List[str]) -> bool:
        """Configure DNS servers on macOS"""
        try:
            # Update DNS configuration
            dns_content = f"nameserver {' '.join(dns_servers)}\n"
            self.dns_conf.write_text(dns_content)
            return True
        except Exception as e:
            logger.error(f"Failed to configure DNS: {e}")
            return False

    def configure_firewall(self, rules: List[Dict]) -> bool:
        """Configure pf firewall rules"""
        try:
            # Implementation for pf firewall configuration
            return True
        except Exception as e:
            logger.error(f"Failed to configure firewall: {e}")
            return False

    def get_network_status(self) -> Dict[str, any]:
        """Get macOS network status"""
        try:
            # Get network interfaces
            cmd = ["ifconfig"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "platform": "macOS",
                "interfaces": result.stdout,
                "pf_status": self._check_pf_status()
            }
        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
            return {}

    def detect_bypass_attempts(self) -> List[Dict]:
        """Detect bypass attempts on macOS"""
        attempts = []
        
        # Check for VPN connections
        try:
            cmd = ["scutil", "--nc", "list"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if "Connected" in result.stdout:
                attempts.append({
                    "type": "vpn_connected",
                    "details": result.stdout,
                    "timestamp": asyncio.get_event_loop().time()
                })
        except Exception as e:
            logger.error(f"Failed to detect VPN: {e}")
        
        return attempts

    def _check_pf_status(self) -> Dict[str, any]:
        """Check pf firewall status"""
        try:
            cmd = ["pfctl", "-s", "info"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"status": result.stdout}
        except Exception:
            return {"status": "unknown"}


def get_enhanced_platform_manager() -> EnhancedPlatformManager:
    """Get the appropriate enhanced platform manager for the current system"""
    system = platform.system().lower()
    
    if system == "windows":
        return EnhancedWindowsManager()
    elif system == "linux":
        return EnhancedLinuxManager()
    elif system == "darwin":  # macOS
        return EnhancedMacOSManager()
    else:
        raise NotImplementedError(f"Platform {system} is not supported")
