"""
Real-time network monitoring system
"""

import asyncio
import logging
import psutil
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class NetworkEvent:
    """Network event data"""
    timestamp: datetime
    event_type: str
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: str
    bytes_sent: int
    bytes_received: int
    process_name: str
    risk_score: float


@dataclass
class NetworkStats:
    """Network statistics"""
    total_bytes_sent: int
    total_bytes_received: int
    active_connections: int
    blocked_connections: int
    suspicious_connections: int
    timestamp: datetime


class RealTimeNetworkMonitor:
    """Real-time network monitoring system"""

    def __init__(self):
        self.is_monitoring = False
        self.event_callbacks: List[Callable] = []
        self.stats_callbacks: List[Callable] = []
        self.blocked_domains: set = set()
        self.suspicious_patterns: List[str] = []
        self.connection_history: List[NetworkEvent] = []
        self.stats_history: List[NetworkStats] = []
        
        # Performance tracking
        self.start_time = None
        self.total_events = 0
        self.blocked_events = 0

    async def start_monitoring(self):
        """Start real-time network monitoring"""
        if self.is_monitoring:
            logger.warning("Network monitoring already running")
            return
        
        self.is_monitoring = True
        self.start_time = datetime.now()
        logger.info("Starting real-time network monitoring")
        
        # Start monitoring tasks
        await asyncio.gather(
            self._monitor_connections(),
            self._monitor_network_stats(),
            self._detect_anomalies()
        )

    async def stop_monitoring(self):
        """Stop network monitoring"""
        self.is_monitoring = False
        logger.info("Stopping network monitoring")

    async def _monitor_connections(self):
        """Monitor network connections in real-time"""
        while self.is_monitoring:
            try:
                connections = psutil.net_connections()
                
                for conn in connections:
                    if conn.status == 'ESTABLISHED':
                        event = await self._create_network_event(conn)
                        if event:
                            await self._process_network_event(event)
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error monitoring connections: {e}")
                await asyncio.sleep(5)

    async def _create_network_event(self, connection) -> Optional[NetworkEvent]:
        """Create network event from connection"""
        try:
            # Get process information
            process = psutil.Process(connection.pid) if connection.pid else None
            process_name = process.name() if process else "unknown"
            
            # Calculate risk score
            risk_score = await self._calculate_connection_risk(connection, process_name)
            
            event = NetworkEvent(
                timestamp=datetime.now(),
                event_type="connection_established",
                source_ip=connection.laddr.ip if connection.laddr else "",
                destination_ip=connection.raddr.ip if connection.raddr else "",
                destination_port=connection.raddr.port if connection.raddr else 0,
                protocol="tcp" if connection.type == 1 else "udp",
                bytes_sent=0,  # Would need to track over time
                bytes_received=0,  # Would need to track over time
                process_name=process_name,
                risk_score=risk_score
            )
            
            return event
            
        except Exception as e:
            logger.error(f"Error creating network event: {e}")
            return None

    async def _calculate_connection_risk(self, connection, process_name: str) -> float:
        """Calculate risk score for connection"""
        risk_score = 0.0
        
        # Check destination port
        if connection.raddr:
            port = connection.raddr.port
            if port in [80, 443]:  # HTTP/HTTPS
                risk_score += 0.1
            elif port in [21, 22, 23]:  # FTP, SSH, Telnet
                risk_score += 0.3
            elif port > 49152:  # Dynamic ports
                risk_score += 0.2
        
        # Check process name
        suspicious_processes = ['browser', 'chrome', 'firefox', 'edge']
        if any(proc in process_name.lower() for proc in suspicious_processes):
            risk_score += 0.2
        
        # Check for suspicious patterns
        if connection.raddr:
            dest_ip = connection.raddr.ip
            for pattern in self.suspicious_patterns:
                if pattern in dest_ip:
                    risk_score += 0.5
        
        return min(risk_score, 1.0)

    async def _process_network_event(self, event: NetworkEvent):
        """Process network event"""
        self.total_events += 1
        self.connection_history.append(event)
        
        # Keep only last 1000 events
        if len(self.connection_history) > 1000:
            self.connection_history = self.connection_history[-1000:]
        
        # Check if connection should be blocked
        if event.risk_score > 0.7:
            await self._block_connection(event)
            self.blocked_events += 1
        
        # Notify callbacks
        for callback in self.event_callbacks:
            try:
                await callback(event)
            except Exception as e:
                logger.error(f"Error in event callback: {e}")

    async def _block_connection(self, event: NetworkEvent):
        """Block suspicious connection"""
        try:
            # Implementation would depend on platform
            logger.warning(f"Blocking suspicious connection: {event.destination_ip}:{event.destination_port}")
            
            # Add to blocked list
            self.blocked_domains.add(event.destination_ip)
            
        except Exception as e:
            logger.error(f"Failed to block connection: {e}")

    async def _monitor_network_stats(self):
        """Monitor network statistics"""
        while self.is_monitoring:
            try:
                # Get network I/O stats
                net_io = psutil.net_io_counters()
                
                # Get active connections count
                connections = psutil.net_connections()
                active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
                
                stats = NetworkStats(
                    total_bytes_sent=net_io.bytes_sent,
                    total_bytes_received=net_io.bytes_recv,
                    active_connections=active_connections,
                    blocked_connections=self.blocked_events,
                    suspicious_connections=len([e for e in self.connection_history if e.risk_score > 0.5]),
                    timestamp=datetime.now()
                )
                
                self.stats_history.append(stats)
                
                # Keep only last 1000 stats
                if len(self.stats_history) > 1000:
                    self.stats_history = self.stats_history[-1000:]
                
                # Notify callbacks
                for callback in self.stats_callbacks:
                    try:
                        await callback(stats)
                    except Exception as e:
                        logger.error(f"Error in stats callback: {e}")
                
                await asyncio.sleep(5)  # Update stats every 5 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring network stats: {e}")
                await asyncio.sleep(10)

    async def _detect_anomalies(self):
        """Detect network anomalies"""
        while self.is_monitoring:
            try:
                # Analyze recent events for anomalies
                recent_events = self.connection_history[-100:] if self.connection_history else []
                
                if recent_events:
                    # Detect unusual connection patterns
                    await self._detect_connection_anomalies(recent_events)
                    
                    # Detect unusual data transfer patterns
                    await self._detect_transfer_anomalies(recent_events)
                
                await asyncio.sleep(30)  # Check for anomalies every 30 seconds
                
            except Exception as e:
                logger.error(f"Error detecting anomalies: {e}")
                await asyncio.sleep(60)

    async def _detect_connection_anomalies(self, events: List[NetworkEvent]):
        """Detect connection anomalies"""
        # Group by destination
        dest_counts = defaultdict(int)
        for event in events:
            dest_counts[event.destination_ip] += 1
        
        # Check for unusual connection counts
        for dest_ip, count in dest_counts.items():
            if count > 10:  # More than 10 connections to same IP
                logger.warning(f"Unusual connection pattern detected: {count} connections to {dest_ip}")

    async def _detect_transfer_anomalies(self, events: List[NetworkEvent]):
        """Detect data transfer anomalies"""
        # Implementation for detecting unusual data transfer patterns
        pass

    def add_event_callback(self, callback: Callable):
        """Add callback for network events"""
        self.event_callbacks.append(callback)

    def add_stats_callback(self, callback: Callable):
        """Add callback for network statistics"""
        self.stats_callbacks.append(callback)

    def get_current_stats(self) -> Optional[NetworkStats]:
        """Get current network statistics"""
        return self.stats_history[-1] if self.stats_history else None

    def get_connection_history(self) -> List[NetworkEvent]:
        """Get connection history"""
        return self.connection_history.copy()

    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        if not self.start_time:
            return {}
        
        runtime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "runtime_seconds": runtime,
            "total_events": self.total_events,
            "blocked_events": self.blocked_events,
            "events_per_second": self.total_events / runtime if runtime > 0 else 0,
            "block_rate": self.blocked_events / self.total_events if self.total_events > 0 else 0
        }