#!/usr/bin/env python3
"""
DNS configuration module for setting family-safe DNS servers
"""

import subprocess
import re
from typing import List, Dict, Optional, Tuple

# Handle imports for both standalone and package usage
try:
    from ..utils.permissions import check_admin_rights
    from ..utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.permissions import check_admin_rights
    from utils.logger import Logger

class DNSConfig:
    def __init__(self):
        """Initialize DNS configuration manager"""
        self.logger = Logger()
        
        # Family-safe DNS servers
        self.dns_servers = {
            "CleanBrowsing": {
                "primary": "185.228.168.168",
                "secondary": "185.228.169.168",
                "description": "CleanBrowsing Family Filter - Blocks adult content"
            },
            "OpenDNS Family": {
                "primary": "208.67.222.123",
                "secondary": "208.67.220.123", 
                "description": "OpenDNS FamilyShield - Free family protection"
            },
            "Cloudflare for Families": {
                "primary": "1.1.1.3",
                "secondary": "1.0.0.3",
                "description": "Cloudflare for Families - Blocks malware and adult content"
            },
            "Quad9 Family": {
                "primary": "9.9.9.11",
                "secondary": "149.112.112.11",
                "description": "Quad9 with malware and adult content blocking"
            },
            "AdGuard Family": {
                "primary": "94.140.14.15",
                "secondary": "94.140.15.16",
                "description": "AdGuard DNS Family Protection"
            }
        }
        
        self.logger.debug("DNS configuration manager initialized")
    
    def _run_command(self, command: List[str]) -> Tuple[bool, str]:
        """
        Run a system command and return result
        
        Args:
            command: Command to run as list of strings
            
        Returns:
            Tuple of (success, output)
        """
        try:
            # For Windows, try to find the executable
            if command and command[0] in ['powershell', 'powershell.exe']:
                # Try different PowerShell paths
                powershell_paths = [
                    'powershell.exe',
                    'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
                    'C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe'
                ]
                
                for path in powershell_paths:
                    try:
                        test_command = [path] + command[1:]
                        result = subprocess.run(
                            test_command,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.returncode == 0:
                            return True, result.stdout
                    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                        continue
                
                # If PowerShell fails, return a helpful error
                return False, "PowerShell not available or command failed"
            
            # For other commands, try direct execution
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {' '.join(command)}")
            return False, "Command timed out"
        except FileNotFoundError:
            self.logger.error(f"Command not found: {' '.join(command)}")
            return False, "Command not found"
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return False, str(e)
    
    def get_network_interfaces(self) -> List[str]:
        """
        Get list of active network interface names
        
        Returns:
            List of interface names
        """
        try:
            # Try PowerShell first
            success, output = self._run_command([
                'powershell.exe', '-Command',
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object -ExpandProperty Name'
            ])
            
            if success and output.strip():
                interfaces = [line.strip() for line in output.strip().split('\n') if line.strip()]
                self.logger.debug(f"Found network interfaces via PowerShell: {interfaces}")
                return interfaces
            else:
                # Fallback: Use ipconfig to get interface names
                self.logger.warning("PowerShell failed, trying ipconfig fallback")
                return self._get_interfaces_fallback()
                
        except Exception as e:
            self.logger.error(f"Failed to get network interfaces: {e}")
            return self._get_interfaces_fallback()
    
    def _get_interfaces_fallback(self) -> List[str]:
        """Fallback method to get network interfaces using ipconfig"""
        try:
            success, output = self._run_command(['ipconfig', '/all'])
            if success:
                interfaces = []
                lines = output.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(' ') and ':' in line and not line.startswith('Windows IP'):
                        # Extract interface name (remove trailing colon and spaces)
                        interface_name = line.split(':')[0].strip()
                        if interface_name and interface_name not in ['Windows IP Configuration', 'Ethernet adapter', 'Wireless LAN adapter']:
                            interfaces.append(interface_name)
                
                self.logger.debug(f"Found network interfaces via ipconfig: {interfaces}")
                return interfaces
            else:
                # Last resort: return a default interface
                self.logger.warning("Using default interface name")
                return ['Ethernet']
        except Exception as e:
            self.logger.error(f"Fallback interface detection failed: {e}")
            return ['Ethernet']
    
    def get_current_dns(self, interface: Optional[str] = None) -> Dict[str, str]:
        """
        Get current DNS configuration for interface(s)
        
        Args:
            interface: Specific interface name, or None for all active interfaces
            
        Returns:
            Dictionary with DNS information
        """
        try:
            if interface:
                interfaces = [interface]
            else:
                interfaces = self.get_network_interfaces()
            
            dns_info = {}
            
            for iface in interfaces:
                success, output = self._run_command([
                    'powershell.exe', '-Command',
                    f'Get-DnsClientServerAddress -InterfaceAlias "{iface}" -AddressFamily IPv4 | Select-Object -ExpandProperty ServerAddresses'
                ])
                
                if success:
                    dns_servers = [line.strip() for line in output.strip().split('\\n') if line.strip()]
                    dns_info[iface] = dns_servers
                else:
                    dns_info[iface] = []
            
            return dns_info
            
        except Exception as e:
            self.logger.error(f"Failed to get current DNS: {e}")
            return {}
    
    def set_dns_servers(self, primary: str, secondary: str, interface: Optional[str] = None) -> bool:
        """
        Set DNS servers for network interface(s)
        
        Args:
            primary: Primary DNS server IP
            secondary: Secondary DNS server IP
            interface: Specific interface name, or None for all active interfaces
            
        Returns:
            True if DNS was set successfully
        """
        if not check_admin_rights():
            self.logger.error("Admin rights required to change DNS settings")
            raise PermissionError("Administrator privileges required")
        
        try:
            if interface:
                interfaces = [interface]
            else:
                interfaces = self.get_network_interfaces()
            
            # If no interfaces found, use fallback
            if not interfaces:
                self.logger.warning("No network interfaces found, using fallback")
                interfaces = ['Ethernet']
            
            success_count = 0
            
            for iface in interfaces:
                # Set DNS servers
                success, output = self._run_command([
                    'powershell.exe', '-Command',
                    f'Set-DnsClientServerAddress -InterfaceAlias "{iface}" -ServerAddresses "{primary}","{secondary}"'
                ])
                
                if success:
                    success_count += 1
                    self.logger.info(f"DNS set for interface {iface}: {primary}, {secondary}")
                else:
                    self.logger.warning(f"Failed to set DNS for interface {iface}: {output}")
            
            if success_count > 0:
                self.logger.log_blocking_action("set_dns_servers", success_count, True)
                # Flush DNS cache
                self._flush_dns_cache()
                return True
            else:
                self.logger.log_blocking_action("set_dns_servers", 0, False)
                self.logger.warning("DNS configuration failed - you may need to set DNS manually")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to set DNS servers: {e}")
            self.logger.log_blocking_action("set_dns_servers", 0, False)
            return False
    
    def set_dns_by_type(self, dns_type: str, interface: Optional[str] = None) -> bool:
        """
        Set DNS servers by predefined type
        
        Args:
            dns_type: Type of DNS (e.g., "CleanBrowsing", "OpenDNS Family")
            interface: Specific interface name, or None for all active interfaces
            
        Returns:
            True if DNS was set successfully
        """
        if dns_type not in self.dns_servers:
            raise ValueError(f"Unknown DNS type: {dns_type}")
        
        dns_config = self.dns_servers[dns_type]
        primary = dns_config["primary"]
        secondary = dns_config["secondary"]
        
        self.logger.info(f"Setting DNS to {dns_type}: {primary}, {secondary}")
        
        return self.set_dns_servers(primary, secondary, interface)
    
    def set_family_safe_dns(self, interface: Optional[str] = None) -> bool:
        """
        Set family-safe DNS (defaults to CleanBrowsing)
        
        Args:
            interface: Specific interface name, or None for all active interfaces
            
        Returns:
            True if DNS was set successfully
        """
        return self.set_dns_by_type("CleanBrowsing", interface)
    
    def reset_dns(self, interface: Optional[str] = None) -> bool:
        """
        Reset DNS to automatic (DHCP)
        
        Args:
            interface: Specific interface name, or None for all active interfaces
            
        Returns:
            True if DNS was reset successfully
        """
        if not check_admin_rights():
            self.logger.error("Admin rights required to change DNS settings")
            raise PermissionError("Administrator privileges required")
        
        try:
            if interface:
                interfaces = [interface]
            else:
                interfaces = self.get_network_interfaces()
            
            success_count = 0
            
            for iface in interfaces:
                # Reset to automatic DNS
                success, output = self._run_command([
                    'powershell.exe', '-Command',
                    f'Set-DnsClientServerAddress -InterfaceAlias "{iface}" -ResetServerAddresses'
                ])
                
                if success:
                    success_count += 1
                    self.logger.info(f"DNS reset to automatic for interface {iface}")
                else:
                    self.logger.error(f"Failed to reset DNS for interface {iface}")
            
            if success_count > 0:
                self.logger.log_blocking_action("reset_dns", success_count, True)
                # Flush DNS cache
                self._flush_dns_cache()
                return True
            else:
                self.logger.log_blocking_action("reset_dns", 0, False)
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to reset DNS: {e}")
            self.logger.log_blocking_action("reset_dns", 0, False)
            raise
    
    def _flush_dns_cache(self):
        """Flush DNS cache to ensure changes take effect immediately"""
        try:
            success, output = self._run_command(['ipconfig', '/flushdns'])
            if success:
                self.logger.info("DNS cache flushed successfully")
            else:
                self.logger.warning("Failed to flush DNS cache")
        except Exception as e:
            self.logger.warning(f"Failed to flush DNS cache: {e}")
    
    def test_dns_resolution(self, domain: str = "google.com") -> Dict[str, any]:
        """
        Test DNS resolution to verify DNS is working
        
        Args:
            domain: Domain to test resolution for
            
        Returns:
            Dictionary with test results
        """
        try:
            success, output = self._run_command([
                'nslookup', domain
            ])
            
            if success:
                # Parse nslookup output to extract IP
                lines = output.split('\\n')
                ips = []
                for line in lines:
                    line = line.strip()
                    if re.match(r'^Address: \\d+\\.\\d+\\.\\d+\\.\\d+$', line):
                        ip = line.split(': ')[1]
                        ips.append(ip)
                
                return {
                    "success": True,
                    "domain": domain,
                    "resolved_ips": ips,
                    "output": output
                }
            else:
                return {
                    "success": False,
                    "domain": domain,
                    "error": output
                }
                
        except Exception as e:
            return {
                "success": False,
                "domain": domain,
                "error": str(e)
            }
    
    def get_dns_info_summary(self) -> str:
        """
        Get a human-readable summary of current DNS configuration
        
        Returns:
            String with DNS summary
        """
        try:
            current_dns = self.get_current_dns()
            summary = "Current DNS Configuration:\\n\\n"
            
            for interface, dns_list in current_dns.items():
                summary += f"Interface: {interface}\\n"
                if dns_list:
                    for i, dns in enumerate(dns_list):
                        summary += f"  DNS {i+1}: {dns}\\n"
                        
                        # Check if it matches any known family-safe DNS
                        for dns_type, config in self.dns_servers.items():
                            if dns == config["primary"] or dns == config["secondary"]:
                                summary += f"    ({dns_type})\\n"
                                break
                else:
                    summary += "  No DNS servers configured (using DHCP)\\n"
                summary += "\\n"
            
            return summary
            
        except Exception as e:
            return f"Error getting DNS info: {e}"
    
    def get_available_dns_types(self) -> Dict[str, str]:
        """
        Get list of available family-safe DNS types
        
        Returns:
            Dictionary mapping DNS type names to descriptions
        """
        return {dns_type: config["description"] 
                for dns_type, config in self.dns_servers.items()}
    
    def is_family_safe_dns_active(self) -> bool:
        """
        Check if any family-safe DNS is currently active
        
        Returns:
            True if family-safe DNS is detected
        """
        try:
            current_dns = self.get_current_dns()
            
            # Get all family-safe DNS IPs
            family_safe_ips = set()
            for config in self.dns_servers.values():
                family_safe_ips.add(config["primary"])
                family_safe_ips.add(config["secondary"])
            
            # Check if any interface is using family-safe DNS
            for interface, dns_list in current_dns.items():
                for dns_ip in dns_list:
                    if dns_ip in family_safe_ips:
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check family-safe DNS status: {e}")
            return False

if __name__ == "__main__":
    # Test DNS configuration
    dns_config = DNSConfig()
    
    print("Available DNS types:")
    for dns_type, description in dns_config.get_available_dns_types().items():
        print(f"  {dns_type}: {description}")
    
    print(f"\\nCurrent DNS info:\\n{dns_config.get_dns_info_summary()}")
    print(f"Family-safe DNS active: {dns_config.is_family_safe_dns_active()}")
    
    # Test DNS resolution
    test_result = dns_config.test_dns_resolution()
    print(f"\\nDNS test result: {test_result}")
