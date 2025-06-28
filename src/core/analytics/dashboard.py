"""
Advanced Analytics Dashboard for Recovery Progress and System Performance
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from collections import defaultdict

from src.utils.logger import Logger
from src.core.recovery.streak_tracker import StreakTracker
from src.core.recovery.journaling import Journal
from src.core.recovery.relapse_predictor import RelapsePredictor
from src.core.recovery.recommendation_engine import RecommendationEngine
from src.database.manager import DatabaseManager


@dataclass
class RecoveryMetrics:
    """Comprehensive recovery metrics"""
    current_streak: int
    longest_streak: int
    total_days: int
    relapse_count: int
    success_rate: float
    mood_trend: List[float]
    journal_activity: int
    recommendation_usage: float
    risk_level: str
    next_milestone: str


@dataclass
class SystemMetrics:
    """System performance metrics"""
    blocked_attempts: int
    blocked_domains: int
    ai_classifications: int
    false_positives: int
    system_uptime: float
    last_update: datetime
    platform_performance: Dict[str, float]


@dataclass
class AnalyticsReport:
    """Complete analytics report"""
    user_id: int
    generated_at: datetime
    recovery_metrics: RecoveryMetrics
    system_metrics: SystemMetrics
    insights: List[str]
    recommendations: List[str]
    charts_data: Dict[str, Any]


class AnalyticsDashboard:
    """Advanced analytics dashboard for recovery and system insights"""
    
    def __init__(self):
        self.logger = Logger()
        self.streak_tracker = StreakTracker()
        self.journal = Journal()
        self.relapse_predictor = RelapsePredictor()
        self.recommendation_engine = RecommendationEngine()
        self.db_manager = DatabaseManager()
        
        # Ensure analytics directory exists
        os.makedirs("data/analytics", exist_ok=True)
    
    def generate_comprehensive_report(self, user_id: int) -> AnalyticsReport:
        """Generate a comprehensive analytics report for a user"""
        try:
            # Gather recovery metrics
            recovery_metrics = self._gather_recovery_metrics(user_id)
            
            # Gather system metrics
            system_metrics = self._gather_system_metrics()
            
            # Generate insights
            insights = self._generate_insights(recovery_metrics, system_metrics)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(recovery_metrics, system_metrics)
            
            # Prepare charts data
            charts_data = self._prepare_charts_data(user_id)
            
            report = AnalyticsReport(
                user_id=user_id,
                generated_at=datetime.now(),
                recovery_metrics=recovery_metrics,
                system_metrics=system_metrics,
                insights=insights,
                recommendations=recommendations,
                charts_data=charts_data
            )
            
            # Save report
            self._save_report(report)
            
            self.logger.info(f"Generated comprehensive analytics report for user {user_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating analytics report: {e}")
            return self._create_error_report(user_id)
    
    def _gather_recovery_metrics(self, user_id: int) -> RecoveryMetrics:
        """Gather comprehensive recovery metrics"""
        try:
            # Get streak data
            current_streak = self.streak_tracker.get_current_streak(user_id)
            longest_streak = self.streak_tracker.get_longest_streak(user_id)
            total_days = self.streak_tracker.get_total_days(user_id)
            
            # Calculate relapse count and success rate
            relapse_count = self._calculate_relapse_count(user_id)
            success_rate = self._calculate_success_rate(current_streak, total_days)
            
            # Get mood trend
            mood_trend = self._get_mood_trend(user_id)
            
            # Get journal activity
            journal_activity = self._get_journal_activity(user_id)
            
            # Get recommendation usage
            recommendation_usage = self._get_recommendation_usage(user_id)
            
            # Get risk level
            risk_level = self._get_current_risk_level(user_id)
            
            # Calculate next milestone
            next_milestone = self._calculate_next_milestone(current_streak, longest_streak)
            
            return RecoveryMetrics(
                current_streak=current_streak,
                longest_streak=longest_streak,
                total_days=total_days,
                relapse_count=relapse_count,
                success_rate=success_rate,
                mood_trend=mood_trend,
                journal_activity=journal_activity,
                recommendation_usage=recommendation_usage,
                risk_level=risk_level,
                next_milestone=next_milestone
            )
            
        except Exception as e:
            self.logger.error(f"Error gathering recovery metrics: {e}")
            return RecoveryMetrics(
                current_streak=0,
                longest_streak=0,
                total_days=0,
                relapse_count=0,
                success_rate=0.0,
                mood_trend=[],
                journal_activity=0,
                recommendation_usage=0.0,
                risk_level="unknown",
                next_milestone="Start your recovery journey"
            )
    
    def _gather_system_metrics(self) -> SystemMetrics:
        """Gather system performance metrics"""
        try:
            # Get blocking statistics
            blocked_attempts = self._get_blocked_attempts_count()
            blocked_domains = self._get_blocked_domains_count()
            
            # Get AI classification stats
            ai_classifications = self._get_ai_classifications_count()
            false_positives = self._get_false_positives_count()
            
            # Get system uptime
            system_uptime = self._get_system_uptime()
            
            # Get last update time
            last_update = self._get_last_update_time()
            
            # Get platform performance
            platform_performance = self._get_platform_performance()
            
            return SystemMetrics(
                blocked_attempts=blocked_attempts,
                blocked_domains=blocked_domains,
                ai_classifications=ai_classifications,
                false_positives=false_positives,
                system_uptime=system_uptime,
                last_update=last_update,
                platform_performance=platform_performance
            )
            
        except Exception as e:
            self.logger.error(f"Error gathering system metrics: {e}")
            return SystemMetrics(
                blocked_attempts=0,
                blocked_domains=0,
                ai_classifications=0,
                false_positives=0,
                system_uptime=0.0,
                last_update=datetime.now(),
                platform_performance={}
            )
    
    def _calculate_relapse_count(self, user_id: int) -> int:
        """Calculate total relapse count for user"""
        try:
            # This would query the database for relapse events
            # For now, return a placeholder
            return 0
        except Exception as e:
            self.logger.error(f"Error calculating relapse count: {e}")
            return 0
    
    def _calculate_success_rate(self, current_streak: int, total_days: int) -> float:
        """Calculate success rate based on streak vs total days"""
        if total_days == 0:
            return 0.0
        return (current_streak / total_days) * 100
    
    def _get_mood_trend(self, user_id: int) -> List[float]:
        """Get mood trend over the last 7 days"""
        try:
            # This would query journal entries for mood scores
            # For now, return sample data
            return [3.5, 4.0, 3.8, 4.2, 3.9, 4.1, 4.3]
        except Exception as e:
            self.logger.error(f"Error getting mood trend: {e}")
            return []
    
    def _get_journal_activity(self, user_id: int) -> int:
        """Get journal activity count for the current week"""
        try:
            # This would query journal entries for the current week
            return 5  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting journal activity: {e}")
            return 0
    
    def _get_recommendation_usage(self, user_id: int) -> float:
        """Get recommendation usage rate"""
        try:
            analytics = self.recommendation_engine.get_recommendation_analytics()
            return analytics.get('usage_rate', 0.0) * 100
        except Exception as e:
            self.logger.error(f"Error getting recommendation usage: {e}")
            return 0.0
    
    def _get_current_risk_level(self, user_id: int) -> str:
        """Get current relapse risk level"""
        try:
            # This would use the relapse predictor
            user_data = {
                'current_streak': self.streak_tracker.get_current_streak(user_id),
                'longest_streak': self.streak_tracker.get_longest_streak(user_id),
                'mood_score': 4.0,  # Placeholder
                'stress_level': 3,   # Placeholder
            }
            prediction = self.relapse_predictor.predict_relapse_risk(user_data)
            return prediction.risk_level
        except Exception as e:
            self.logger.error(f"Error getting risk level: {e}")
            return "unknown"
    
    def _calculate_next_milestone(self, current_streak: int, longest_streak: int) -> str:
        """Calculate the next milestone to achieve"""
        milestones = [1, 3, 7, 14, 30, 60, 90, 180, 365]
        
        for milestone in milestones:
            if current_streak < milestone:
                days_to_go = milestone - current_streak
                return f"{milestone} days ({days_to_go} days to go)"
        
        return "365+ days - Amazing achievement!"
    
    def _get_blocked_attempts_count(self) -> int:
        """Get count of blocked access attempts"""
        try:
            # This would query the blocking logs
            return 42  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting blocked attempts count: {e}")
            return 0
    
    def _get_blocked_domains_count(self) -> int:
        """Get count of blocked domains"""
        try:
            # This would query the blocklist
            return 1500  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting blocked domains count: {e}")
            return 0
    
    def _get_ai_classifications_count(self) -> int:
        """Get count of AI domain classifications"""
        try:
            # This would query AI classifier logs
            return 250  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting AI classifications count: {e}")
            return 0
    
    def _get_false_positives_count(self) -> int:
        """Get count of false positive classifications"""
        try:
            # This would query user feedback on classifications
            return 3  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting false positives count: {e}")
            return 0
    
    def _get_system_uptime(self) -> float:
        """Get system uptime percentage"""
        try:
            # This would calculate actual uptime
            return 99.8  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting system uptime: {e}")
            return 0.0
    
    def _get_last_update_time(self) -> datetime:
        """Get last system update time"""
        try:
            # This would get actual last update time
            return datetime.now() - timedelta(hours=2)
        except Exception as e:
            self.logger.error(f"Error getting last update time: {e}")
            return datetime.now()
    
    def _get_platform_performance(self) -> Dict[str, float]:
        """Get platform-specific performance metrics"""
        try:
            return {
                "blocking_speed": 0.95,
                "ai_accuracy": 0.92,
                "user_satisfaction": 0.88,
                "system_reliability": 0.99
            }
        except Exception as e:
            self.logger.error(f"Error getting platform performance: {e}")
            return {}
    
    def _generate_insights(self, recovery_metrics: RecoveryMetrics, system_metrics: SystemMetrics) -> List[str]:
        """Generate insights from the metrics"""
        insights = []
        
        # Recovery insights
        if recovery_metrics.current_streak > recovery_metrics.longest_streak * 0.8:
            insights.append("You're approaching your longest streak! Keep up the great work.")
        
        if recovery_metrics.success_rate > 80:
            insights.append("Excellent success rate! Your recovery strategies are working well.")
        
        if recovery_metrics.mood_trend and recovery_metrics.mood_trend[-1] > 4.0:
            insights.append("Your mood has been consistently positive recently.")
        
        if recovery_metrics.journal_activity < 3:
            insights.append("Consider increasing your journaling frequency for better self-reflection.")
        
        if recovery_metrics.recommendation_usage < 50:
            insights.append("You might benefit from following more of the recommended activities.")
        
        # System insights
        if system_metrics.blocked_attempts > 0:
            insights.append(f"Successfully blocked {system_metrics.blocked_attempts} access attempts.")
        
        if system_metrics.ai_accuracy > 0.9:
            insights.append("AI classification is performing excellently with high accuracy.")
        
        if system_metrics.false_positives > 0:
            insights.append(f"Only {system_metrics.false_positives} false positives detected - great precision!")
        
        return insights[:5]  # Return top 5 insights
    
    def _generate_recommendations(self, recovery_metrics: RecoveryMetrics, system_metrics: SystemMetrics) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        # Recovery recommendations
        if recovery_metrics.current_streak < 7:
            recommendations.append("Focus on building your first week streak - the foundation is crucial.")
        
        if recovery_metrics.journal_activity < 3:
            recommendations.append("Try journaling daily to track your progress and emotions.")
        
        if recovery_metrics.recommendation_usage < 50:
            recommendations.append("Explore the recommended activities - they're personalized for your recovery.")
        
        if recovery_metrics.risk_level in ["high", "critical"]:
            recommendations.append("Consider reaching out to your support network during this challenging time.")
        
        # System recommendations
        if system_metrics.blocked_attempts > 10:
            recommendations.append("You're experiencing many triggers - review your coping strategies.")
        
        return recommendations[:4]  # Return top 4 recommendations
    
    def _prepare_charts_data(self, user_id: int) -> Dict[str, Any]:
        """Prepare data for charts and visualizations"""
        try:
            # Streak progression data
            streak_data = self._get_streak_progression_data(user_id)
            
            # Mood trend data
            mood_data = self._get_mood_trend_data(user_id)
            
            # Activity data
            activity_data = self._get_activity_data(user_id)
            
            # System performance data
            system_data = self._get_system_performance_data()
            
            return {
                "streak_progression": streak_data,
                "mood_trend": mood_data,
                "activity_distribution": activity_data,
                "system_performance": system_data
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing charts data: {e}")
            return {}
    
    def _get_streak_progression_data(self, user_id: int) -> Dict[str, Any]:
        """Get data for streak progression chart"""
        try:
            # This would query actual streak data
            return {
                "dates": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
                "streaks": [1, 2, 3, 4, 5],
                "milestones": [7, 30, 90]
            }
        except Exception as e:
            self.logger.error(f"Error getting streak progression data: {e}")
            return {}
    
    def _get_mood_trend_data(self, user_id: int) -> Dict[str, Any]:
        """Get data for mood trend chart"""
        try:
            return {
                "dates": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "mood_scores": [3.5, 4.0, 3.8, 4.2, 3.9, 4.1, 4.3],
                "average": 4.0
            }
        except Exception as e:
            self.logger.error(f"Error getting mood trend data: {e}")
            return {}
    
    def _get_activity_data(self, user_id: int) -> Dict[str, Any]:
        """Get data for activity distribution chart"""
        try:
            return {
                "activities": ["Journaling", "Exercise", "Meditation", "Social", "Hobbies"],
                "frequencies": [5, 3, 4, 2, 6],
                "recommended": [7, 5, 5, 3, 4]
            }
        except Exception as e:
            self.logger.error(f"Error getting activity data: {e}")
            return {}
    
    def _get_system_performance_data(self) -> Dict[str, Any]:
        """Get data for system performance chart"""
        try:
            return {
                "metrics": ["Blocking", "AI Accuracy", "Uptime", "User Satisfaction"],
                "values": [99.5, 92.0, 99.8, 88.0],
                "targets": [99.0, 90.0, 99.5, 85.0]
            }
        except Exception as e:
            self.logger.error(f"Error getting system performance data: {e}")
            return {}
    
    def _save_report(self, report: AnalyticsReport):
        """Save the analytics report to file"""
        try:
            report_file = f"data/analytics/report_{report.user_id}_{report.generated_at.strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert report to dict for JSON serialization
            report_dict = asdict(report)
            report_dict['generated_at'] = report.generated_at.isoformat()
            report_dict['recovery_metrics'] = asdict(report.recovery_metrics)
            report_dict['system_metrics'] = asdict(report.system_metrics)
            report_dict['system_metrics']['last_update'] = report.system_metrics.last_update.isoformat()
            
            with open(report_file, 'w') as f:
                json.dump(report_dict, f, indent=2)
                
            self.logger.info(f"Saved analytics report to {report_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving analytics report: {e}")
    
    def _create_error_report(self, user_id: int) -> AnalyticsReport:
        """Create a basic report when there's an error"""
        return AnalyticsReport(
            user_id=user_id,
            generated_at=datetime.now(),
            recovery_metrics=RecoveryMetrics(
                current_streak=0,
                longest_streak=0,
                total_days=0,
                relapse_count=0,
                success_rate=0.0,
                mood_trend=[],
                journal_activity=0,
                recommendation_usage=0.0,
                risk_level="unknown",
                next_milestone="Start your recovery journey"
            ),
            system_metrics=SystemMetrics(
                blocked_attempts=0,
                blocked_domains=0,
                ai_classifications=0,
                false_positives=0,
                system_uptime=0.0,
                last_update=datetime.now(),
                platform_performance={}
            ),
            insights=["Unable to generate insights at this time"],
            recommendations=["Please try again later or contact support"],
            charts_data={}
        ) 