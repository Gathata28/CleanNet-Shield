#!/usr/bin/env python3
"""
Logging utility module for the Adult Content Blocker
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional


class Logger:
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the logger

        Args:
            log_dir: Directory to store logs. If None, uses data/logs
        """
        if log_dir is None:
            self.log_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "data", "logs"
            )
        else:
            self.log_dir = log_dir

        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        # Setup file paths
        self.log_file = os.path.join(
            self.log_dir, f"blocker_{datetime.now().strftime('%Y-%m')}.log"
        )
        self.json_log_file = os.path.join(
            self.log_dir, f"blocker_{datetime.now().strftime('%Y-%m')}.json"
        )

        # Setup Python logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup Python logging configuration"""
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Get logger
        self.logger = logging.getLogger("AdultBlocker")
        self.logger.setLevel(logging.INFO)

        # Add handlers if not already added
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def log(
        self, message: str, data: Optional[Dict[str, Any]] = None, level: str = "INFO"
    ):
        """
        Log a message with optional structured data

        Args:
            message: The log message
            data: Optional dictionary of additional data
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        timestamp = datetime.now().isoformat()

        # Create log entry
        log_entry = {
            "timestamp": timestamp,
            "level": level.upper(),
            "message": message,
            "data": data or {},
        }

        # Log to Python logger
        getattr(self.logger, level.lower())(f"{message} | Data: {data}")

        # Append to JSON log file
        try:
            # Read existing logs
            if os.path.exists(self.json_log_file):
                with open(self.json_log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            else:
                logs = []

            # Add new log entry
            logs.append(log_entry)

            # Keep only last 1000 entries to prevent huge files
            if len(logs) > 1000:
                logs = logs[-1000:]

            # Write back to file
            with open(self.json_log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"Failed to write to JSON log: {e}")

    def get_recent_logs(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent log entries

        Args:
            count: Number of recent entries to return

        Returns:
            List of log entries
        """
        try:
            if os.path.exists(self.json_log_file):
                with open(self.json_log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                return logs[-count:] if logs else []
            else:
                return []
        except Exception as e:
            self.logger.error(f"Failed to read logs: {e}")
            return []

    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log debug message"""
        self.log(message, data, "DEBUG")

    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log info message"""
        self.log(message, data, "INFO")

    def warning(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        self.log(message, data, "WARNING")

    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log error message"""
        self.log(message, data, "ERROR")

    def critical(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log critical message"""
        self.log(message, data, "CRITICAL")

    def log_blocking_action(
        self, action: str, domains_count: int = 0, success: bool = True
    ):
        """Log a blocking-related action"""
        self.log(
            f"Blocking action: {action}",
            {
                "action": action,
                "domains_count": domains_count,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            },
            "INFO" if success else "ERROR",
        )

    def log_recovery_action(
        self, action: str, details: Optional[Dict[str, Any]] = None
    ):
        """Log a recovery-related action"""
        data = {"action": action, "timestamp": datetime.now().isoformat()}
        if details:
            data.update(details)

        self.log(f"Recovery action: {action}", data)

    def get_daily_stats(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get statistics for a specific day

        Args:
            date: Date to get stats for. If None, uses today

        Returns:
            Dictionary with daily statistics
        """
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y-%m-%d")

        try:
            logs = self.get_recent_logs(1000)  # Get more logs for analysis

            # Filter logs for the specific date
            daily_logs = [log for log in logs if log["timestamp"].startswith(date_str)]

            # Calculate statistics
            stats = {
                "date": date_str,
                "total_actions": len(daily_logs),
                "blocking_actions": len(
                    [
                        log
                        for log in daily_logs
                        if "blocking" in log.get("message", "").lower()
                    ]
                ),
                "recovery_actions": len(
                    [
                        log
                        for log in daily_logs
                        if "recovery" in log.get("message", "").lower()
                    ]
                ),
                "errors": len(
                    [log for log in daily_logs if log.get("level") == "ERROR"]
                ),
                "log_entries": daily_logs[-10:],  # Last 10 entries for the day
            }

            return stats

        except Exception as e:
            self.error(f"Failed to get daily stats: {e}")
            return {"date": date_str, "error": str(e)}


if __name__ == "__main__":
    # Test the logger
    logger = Logger()

    logger.info("Logger test started")
    logger.log_blocking_action("enable_protection", domains_count=1500, success=True)
    logger.log_recovery_action("mark_clean_day", {"streak": 5})

    print("Recent logs:")
    for log in logger.get_recent_logs(5):
        print(f"  {log['timestamp']}: {log['message']}")

    print(f"Daily stats: {logger.get_daily_stats()}")
