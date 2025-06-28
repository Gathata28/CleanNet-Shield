#!/usr/bin/env python3
"""
Streak tracking module for recovery progress monitoring
"""

import os
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple

# Handle imports for both standalone and package usage
try:
    from src.utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.logger import Logger

class StreakTracker:
    def __init__(self):
        """Initialize the streak tracking system"""
        self.logger = Logger()
        
        # Data directory
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'streaks')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Data files
        self.streak_file = os.path.join(self.data_dir, 'streak_data.json')
        self.history_file = os.path.join(self.data_dir, 'streak_history.json')
        
        # Milestone rewards/achievements
        self.milestones = {
            1: "🌱 First Day Clean!",
            3: "🔥 3-Day Streak!",
            7: "⭐ One Week Strong!",
            14: "💪 Two Weeks Clean!",
            30: "🏆 One Month Achievement!",
            60: "🎉 Two Months of Progress!",
            90: "🚀 Three Months - Amazing!",
            180: "💎 Six Months - Diamond Streak!",
            365: "👑 One Year - You're a Champion!"
        }
        
        self.logger.debug("Streak tracker initialized")
    
    def _load_streak_data(self) -> Dict:
        """Load current streak data"""
        try:
            if os.path.exists(self.streak_file):
                with open(self.streak_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._create_default_data()
        except Exception as e:
            self.logger.error(f"Failed to load streak data: {e}")
            return self._create_default_data()
    
    def _create_default_data(self) -> Dict:
        """Create default streak data structure"""
        return {
            "current_streak": 0,
            "last_clean_date": None,
            "longest_streak": 0,
            "total_clean_days": 0,
            "streak_start_date": None,
            "last_reset_date": None,
            "achievements_unlocked": [],
            "created_date": datetime.now().isoformat()
        }
    
    def _save_streak_data(self, data: Dict):
        """Save streak data to file"""
        try:
            with open(self.streak_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save streak data: {e}")
    
    def _load_history(self) -> List[Dict]:
        """Load streak history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Failed to load streak history: {e}")
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save streak history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save streak history: {e}")
    
    def _add_to_history(self, event_type: str, data: Dict):
        """Add an event to streak history"""
        try:
            history = self._load_history()
            
            event = {
                "date": datetime.now().isoformat(),
                "type": event_type,
                "data": data
            }
            
            history.append(event)
            
            # Keep only last 1000 events
            if len(history) > 1000:
                history = history[-1000:]
            
            self._save_history(history)
            
        except Exception as e:
            self.logger.error(f"Failed to add to history: {e}")
    
    def mark_clean_day(self, day_date: Optional[date] = None) -> Dict:
        """
        Mark a day as clean and update streak
        
        Args:
            day_date: Date to mark as clean. If None, uses today
            
        Returns:
            Dictionary with updated streak information
        """
        try:
            if day_date is None:
                day_date = date.today()
            
            data = self._load_streak_data()
            today_str = day_date.isoformat()
            
            # Check if this day was already marked
            if data.get("last_clean_date") == today_str:
                self.logger.info(f"Day {today_str} already marked as clean")
                return self._get_streak_info(data)
            
            # Update streak based on continuity
            last_clean = data.get("last_clean_date")
            if last_clean:
                last_clean_date = datetime.fromisoformat(last_clean).date()
                
                # Check if this is the next consecutive day
                if day_date == last_clean_date + timedelta(days=1):
                    # Continue streak
                    data["current_streak"] += 1
                elif day_date == last_clean_date:
                    # Same day, no change needed
                    pass
                else:
                    # Gap in streak, restart
                    if data["current_streak"] > 0:
                        self._add_to_history("streak_broken", {
                            "previous_streak": data["current_streak"],
                            "last_clean_date": last_clean,
                            "gap_days": (day_date - last_clean_date).days
                        })
                    
                    data["current_streak"] = 1
                    data["streak_start_date"] = today_str
            else:
                # First clean day ever
                data["current_streak"] = 1
                data["streak_start_date"] = today_str
            
            # Update other fields
            data["last_clean_date"] = today_str
            data["total_clean_days"] += 1
            
            # Update longest streak
            if data["current_streak"] > data["longest_streak"]:
                data["longest_streak"] = data["current_streak"]
            
            # Check for new achievements
            new_achievements = self._check_achievements(data)
            
            self._save_streak_data(data)
            
            # Log the action
            self.logger.log_recovery_action("clean_day_marked", {
                "date": today_str,
                "current_streak": data["current_streak"],
                "new_achievements": new_achievements
            })
            
            # Add to history
            self._add_to_history("clean_day_marked", {
                "date": today_str,
                "streak": data["current_streak"],
                "achievements": new_achievements
            })
            
            result = self._get_streak_info(data)
            result["new_achievements"] = new_achievements
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to mark clean day: {e}")
            return {"error": str(e)}
    
    def reset_streak(self, reason: str = "Manual reset") -> Dict:
        """
        Reset the current streak
        
        Args:
            reason: Reason for the reset
            
        Returns:
            Dictionary with reset information
        """
        try:
            data = self._load_streak_data()
            
            # Record the broken streak in history
            if data["current_streak"] > 0:
                self._add_to_history("streak_reset", {
                    "previous_streak": data["current_streak"],
                    "reason": reason,
                    "last_clean_date": data.get("last_clean_date"),
                    "reset_date": datetime.now().isoformat()
                })
            
            # Reset streak data
            data["current_streak"] = 0
            data["last_reset_date"] = datetime.now().isoformat()
            data["streak_start_date"] = None
            
            self._save_streak_data(data)
            
            # Log the action
            self.logger.log_recovery_action("streak_reset", {
                "reason": reason,
                "previous_streak": data.get("current_streak", 0)
            })
            
            return {
                "success": True,
                "message": "Streak has been reset. Tomorrow is a new beginning!",
                "reset_date": data["last_reset_date"]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to reset streak: {e}")
            return {"error": str(e)}
    
    def get_current_streak(self) -> int:
        """Get the current streak count"""
        try:
            data = self._load_streak_data()
            
            # Check if streak is still valid (no gaps)
            last_clean = data.get("last_clean_date")
            if last_clean:
                last_clean_date = datetime.fromisoformat(last_clean).date()
                days_since = (date.today() - last_clean_date).days
                
                # If more than 1 day gap, streak is broken
                if days_since > 1:
                    data["current_streak"] = 0
                    self._save_streak_data(data)
            
            return data.get("current_streak", 0)
            
        except Exception as e:
            self.logger.error(f"Failed to get current streak: {e}")
            return 0
    
    def get_last_clean_date(self) -> Optional[date]:
        """Get the last date marked as clean"""
        try:
            data = self._load_streak_data()
            last_clean = data.get("last_clean_date")
            if last_clean:
                return datetime.fromisoformat(last_clean).date()
            return None
        except Exception as e:
            self.logger.error(f"Failed to get last clean date: {e}")
            return None
    
    def _check_achievements(self, data: Dict) -> List[str]:
        """Check for new achievements and return them"""
        current_streak = data["current_streak"]
        achieved = data.get("achievements_unlocked", [])
        new_achievements = []
        
        for milestone, message in self.milestones.items():
            if current_streak >= milestone and milestone not in achieved:
                achieved.append(milestone)
                new_achievements.append(message)
                
                self.logger.log_recovery_action("achievement_unlocked", {
                    "milestone": milestone,
                    "message": message,
                    "streak": current_streak
                })
        
        data["achievements_unlocked"] = achieved
        return new_achievements
    
    def _get_streak_info(self, data: Dict) -> Dict:
        """Get formatted streak information"""
        current_streak = data.get("current_streak", 0)
        last_clean = data.get("last_clean_date")
        
        # Calculate days since last clean
        days_since_clean = 0
        if last_clean:
            last_clean_date = datetime.fromisoformat(last_clean).date()
            days_since_clean = (date.today() - last_clean_date).days
        
        # Get next milestone
        next_milestone = None
        next_milestone_message = None
        for milestone, message in sorted(self.milestones.items()):
            if current_streak < milestone:
                next_milestone = milestone
                next_milestone_message = message
                break
        
        return {
            "current_streak": current_streak,
            "longest_streak": data.get("longest_streak", 0),
            "total_clean_days": data.get("total_clean_days", 0),
            "last_clean_date": last_clean,
            "days_since_clean": days_since_clean,
            "streak_start_date": data.get("streak_start_date"),
            "next_milestone": next_milestone,
            "next_milestone_message": next_milestone_message,
            "days_to_next_milestone": next_milestone - current_streak if next_milestone else None,
            "achievements_count": len(data.get("achievements_unlocked", [])),
            "is_streak_active": days_since_clean <= 1
        }
    
    def get_streak_summary(self) -> Dict:
        """Get comprehensive streak summary"""
        try:
            data = self._load_streak_data()
            return self._get_streak_info(data)
        except Exception as e:
            self.logger.error(f"Failed to get streak summary: {e}")
            return {"error": str(e)}
    
    def get_achievements(self) -> List[Dict]:
        """Get list of unlocked achievements"""
        try:
            data = self._load_streak_data()
            achieved_milestones = data.get("achievements_unlocked", [])
            
            achievements = []
            for milestone in achieved_milestones:
                if milestone in self.milestones:
                    achievements.append({
                        "milestone": milestone,
                        "message": self.milestones[milestone],
                        "unlocked": True
                    })
            
            # Add next few locked achievements
            current_streak = data.get("current_streak", 0)
            for milestone, message in sorted(self.milestones.items()):
                if milestone not in achieved_milestones and milestone > current_streak:
                    achievements.append({
                        "milestone": milestone,
                        "message": message,
                        "unlocked": False,
                        "days_remaining": milestone - current_streak
                    })
                    if len([a for a in achievements if not a.get("unlocked", True)]) >= 3:
                        break
            
            return achievements
            
        except Exception as e:
            self.logger.error(f"Failed to get achievements: {e}")
            return []
    
    def get_weekly_progress(self) -> Dict:
        """Get progress for the current week"""
        try:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())  # Monday
            
            data = self._load_streak_data()
            last_clean = data.get("last_clean_date")
            
            week_progress = {}
            for i in range(7):
                day = week_start + timedelta(days=i)
                day_str = day.isoformat()
                
                # Check if this day was clean
                is_clean = False
                if last_clean:
                    last_clean_date = datetime.fromisoformat(last_clean).date()
                    if day <= last_clean_date and day >= last_clean_date - timedelta(days=data.get("current_streak", 0) - 1):
                        is_clean = True
                
                week_progress[day_str] = {
                    "date": day_str,
                    "day_name": day.strftime("%A"),
                    "is_clean": is_clean,
                    "is_today": day == today,
                    "is_future": day > today
                }
            
            return {
                "week_start": week_start.isoformat(),
                "days": week_progress,
                "clean_days_this_week": sum(1 for d in week_progress.values() if d["is_clean"])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get weekly progress: {e}")
            return {"error": str(e)}
    
    def get_monthly_stats(self) -> Dict:
        """Get statistics for the current month"""
        try:
            today = date.today()
            month_start = today.replace(day=1)
            
            data = self._load_streak_data()
            
            # Count clean days this month
            clean_days_this_month = 0
            last_clean = data.get("last_clean_date")
            
            if last_clean:
                last_clean_date = datetime.fromisoformat(last_clean).date()
                streak_length = data.get("current_streak", 0)
                
                # Check each day of the month
                current_day = month_start
                while current_day <= today:
                    # Check if this day was part of the streak
                    if current_day <= last_clean_date and current_day >= last_clean_date - timedelta(days=streak_length - 1):
                        clean_days_this_month += 1
                    current_day += timedelta(days=1)
            
            days_in_month = today.day
            clean_percentage = (clean_days_this_month / days_in_month) * 100 if days_in_month > 0 else 0
            
            return {
                "month": today.strftime("%B %Y"),
                "clean_days": clean_days_this_month,
                "total_days": days_in_month,
                "clean_percentage": round(clean_percentage, 1),
                "longest_streak_this_month": min(data.get("current_streak", 0), days_in_month)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get monthly stats: {e}")
            return {"error": str(e)}
    
    def get_history_summary(self, days: int = 30) -> List[Dict]:
        """Get streak history for recent days"""
        try:
            history = self._load_history()
            
            # Filter recent events
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_history = [
                event for event in history
                if datetime.fromisoformat(event["date"]) >= cutoff_date
            ]
            
            return recent_history[-20:]  # Last 20 events
            
        except Exception as e:
            self.logger.error(f"Failed to get history summary: {e}")
            return []

if __name__ == "__main__":
    # Test the streak tracker
    tracker = StreakTracker()
    
    # Mark today as clean
    result = tracker.mark_clean_day()
    print(f"Marked clean day: {result}")
    
    # Get streak summary
    summary = tracker.get_streak_summary()
    print(f"Streak summary: {summary}")
    
    # Get achievements
    achievements = tracker.get_achievements()
    print(f"Achievements: {achievements}")
    
    # Get weekly progress
    weekly = tracker.get_weekly_progress()
    print(f"Weekly progress: {weekly}")
    
    # Get monthly stats
    monthly = tracker.get_monthly_stats()
    print(f"Monthly stats: {monthly}")
