"""
Personalized Recovery Recommendation Engine
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from src.utils.logger import Logger


class RecommendationType(Enum):
    """Types of recovery recommendations"""
    COPING_STRATEGY = "coping_strategy"
    ACTIVITY_SUGGESTION = "activity_suggestion"
    SUPPORT_ACTION = "support_action"
    GOAL_SETTING = "goal_setting"
    EMERGENCY_ACTION = "emergency_action"


class RecommendationPriority(Enum):
    """Priority levels for recommendations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RecoveryRecommendation:
    """Individual recovery recommendation"""
    id: str
    type: RecommendationType
    title: str
    description: str
    priority: RecommendationPriority
    estimated_duration: int  # minutes
    difficulty: str  # "easy", "medium", "hard"
    tags: List[str]
    conditions: Dict  # When to show this recommendation
    created_at: datetime
    expires_at: Optional[datetime] = None


class RecommendationEngine:
    """AI-driven personalized recovery recommendation system"""
    
    def __init__(self):
        self.logger = Logger()
        self.recommendations_db = {}
        self.user_preferences = {}
        self.recommendation_history = []
        
        # Load recommendation database
        self._load_recommendation_database()
    
    def _load_recommendation_database(self):
        """Load the recommendation database"""
        self.recommendations_db = {
            # Coping Strategies
            "deep_breathing": RecoveryRecommendation(
                id="deep_breathing",
                type=RecommendationType.COPING_STRATEGY,
                title="Deep Breathing Exercise",
                description="Practice 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8",
                priority=RecommendationPriority.MEDIUM,
                estimated_duration=5,
                difficulty="easy",
                tags=["stress", "anxiety", "immediate"],
                conditions={"mood_score": "<3", "stress_level": ">5"},
                created_at=datetime.now()
            ),
            
            "mindful_walk": RecoveryRecommendation(
                id="mindful_walk",
                type=RecommendationType.ACTIVITY_SUGGESTION,
                title="Mindful Walking",
                description="Take a 15-minute walk focusing on your surroundings and breathing",
                priority=RecommendationPriority.MEDIUM,
                estimated_duration=15,
                difficulty="easy",
                tags=["exercise", "mindfulness", "outdoor"],
                conditions={"weather": "good", "time_of_day": "daylight"},
                created_at=datetime.now()
            ),
            
            "journal_reflection": RecoveryRecommendation(
                id="journal_reflection",
                type=RecommendationType.COPING_STRATEGY,
                title="Journal Reflection",
                description="Write about your current feelings and what triggered them",
                priority=RecommendationPriority.HIGH,
                estimated_duration=10,
                difficulty="medium",
                tags=["self-reflection", "emotional-awareness"],
                conditions={"journal_entries_this_week": "<3"},
                created_at=datetime.now()
            ),
            
            "call_support": RecoveryRecommendation(
                id="call_support",
                type=RecommendationType.SUPPORT_ACTION,
                title="Reach Out to Support",
                description="Call your accountability partner or a trusted friend",
                priority=RecommendationPriority.HIGH,
                estimated_duration=15,
                difficulty="medium",
                tags=["social", "support", "connection"],
                conditions={"days_since_last_contact": ">2"},
                created_at=datetime.now()
            ),
            
            "cold_shower": RecoveryRecommendation(
                id="cold_shower",
                type=RecommendationType.COPING_STRATEGY,
                title="Cold Shower Technique",
                description="Take a 2-3 minute cold shower to reset your nervous system",
                priority=RecommendationPriority.MEDIUM,
                estimated_duration=3,
                difficulty="hard",
                tags=["physical", "immediate", "reset"],
                conditions={"urge_intensity": ">7"},
                created_at=datetime.now()
            ),
            
            "meditation": RecoveryRecommendation(
                id="meditation",
                type=RecommendationType.COPING_STRATEGY,
                title="Guided Meditation",
                description="Listen to a 10-minute guided meditation for recovery",
                priority=RecommendationPriority.MEDIUM,
                estimated_duration=10,
                difficulty="medium",
                tags=["mindfulness", "relaxation"],
                conditions={"stress_level": ">4"},
                created_at=datetime.now()
            ),
            
            "exercise": RecoveryRecommendation(
                id="exercise",
                type=RecommendationType.ACTIVITY_SUGGESTION,
                title="Physical Exercise",
                description="Do 20 minutes of moderate exercise (walking, jogging, or home workout)",
                priority=RecommendationPriority.HIGH,
                estimated_duration=20,
                difficulty="medium",
                tags=["physical", "endorphins", "health"],
                conditions={"days_since_last_exercise": ">1"},
                created_at=datetime.now()
            ),
            
            "goal_review": RecoveryRecommendation(
                id="goal_review",
                type=RecommendationType.GOAL_SETTING,
                title="Review Recovery Goals",
                description="Review and update your recovery goals and progress",
                priority=RecommendationPriority.MEDIUM,
                estimated_duration=15,
                difficulty="medium",
                tags=["planning", "motivation"],
                conditions={"days_since_goal_review": ">7"},
                created_at=datetime.now()
            ),
            
            "emergency_plan": RecoveryRecommendation(
                id="emergency_plan",
                type=RecommendationType.EMERGENCY_ACTION,
                title="Emergency Action Plan",
                description="Execute your emergency action plan: remove triggers, call support, use coping strategies",
                priority=RecommendationPriority.CRITICAL,
                estimated_duration=30,
                difficulty="hard",
                tags=["emergency", "crisis", "immediate"],
                conditions={"risk_level": "critical"},
                created_at=datetime.now()
            ),
            
            "hobby_activity": RecoveryRecommendation(
                id="hobby_activity",
                type=RecommendationType.ACTIVITY_SUGGESTION,
                title="Engage in Hobby",
                description="Spend time on a hobby or activity you enjoy",
                priority=RecommendationPriority.LOW,
                estimated_duration=30,
                difficulty="easy",
                tags=["enjoyment", "distraction", "positive"],
                conditions={"mood_score": "<4"},
                created_at=datetime.now()
            )
        }
    
    def get_personalized_recommendations(self, user_data: Dict, limit: int = 5) -> List[RecoveryRecommendation]:
        """Get personalized recommendations based on user data"""
        try:
            recommendations = []
            
            # Score each recommendation based on user data
            scored_recommendations = []
            
            for rec_id, recommendation in self.recommendations_db.items():
                score = self._calculate_recommendation_score(recommendation, user_data)
                
                # Check if recommendation meets conditions
                if self._meets_conditions(recommendation, user_data):
                    scored_recommendations.append((recommendation, score))
            
            # Sort by score (highest first) and priority
            scored_recommendations.sort(
                key=lambda x: (x[1], self._priority_to_numeric(x[0].priority)),
                reverse=True
            )
            
            # Return top recommendations
            for recommendation, score in scored_recommendations[:limit]:
                recommendations.append(recommendation)
            
            self.logger.info(f"Generated {len(recommendations)} personalized recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating personalized recommendations: {e}")
            return self._get_fallback_recommendations(limit)
    
    def _calculate_recommendation_score(self, recommendation: RecoveryRecommendation, user_data: Dict) -> float:
        """Calculate a score for how well a recommendation fits the user's current situation"""
        score = 0.0
        
        # Base score from priority
        score += self._priority_to_numeric(recommendation.priority) * 10
        
        # Time-based scoring
        current_hour = datetime.now().hour
        
        if recommendation.id == "mindful_walk" and 6 <= current_hour <= 18:
            score += 5  # Good time for outdoor activity
        
        if recommendation.id == "cold_shower" and user_data.get('urge_intensity', 0) > 7:
            score += 15  # High urge situation
        
        if recommendation.id == "call_support" and user_data.get('days_since_last_contact', 0) > 3:
            score += 10  # Been a while since contact
        
        if recommendation.id == "journal_reflection" and user_data.get('journal_entries_this_week', 0) < 2:
            score += 8  # Low journal activity
        
        if recommendation.id == "exercise" and user_data.get('days_since_last_exercise', 0) > 2:
            score += 12  # Need exercise
        
        # Mood-based scoring
        mood_score = user_data.get('mood_score', 3)
        if mood_score < 3 and recommendation.type == RecommendationType.COPING_STRATEGY:
            score += 7  # Low mood needs coping strategies
        
        # Stress-based scoring
        stress_level = user_data.get('stress_level', 5)
        if stress_level > 6 and recommendation.id in ["deep_breathing", "meditation"]:
            score += 10  # High stress needs relaxation
        
        return score
    
    def _meets_conditions(self, recommendation: RecoveryRecommendation, user_data: Dict) -> bool:
        """Check if recommendation meets the conditions to be shown"""
        conditions = recommendation.conditions
        
        for condition_key, condition_value in conditions.items():
            if condition_key == "mood_score":
                if condition_value.startswith("<"):
                    threshold = float(condition_value[1:])
                    if user_data.get('mood_score', 3) >= threshold:
                        return False
                elif condition_value.startswith(">"):
                    threshold = float(condition_value[1:])
                    if user_data.get('mood_score', 3) <= threshold:
                        return False
            
            elif condition_key == "stress_level":
                if condition_value.startswith(">"):
                    threshold = float(condition_value[1:])
                    if user_data.get('stress_level', 5) <= threshold:
                        return False
            
            elif condition_key == "urge_intensity":
                if condition_value.startswith(">"):
                    threshold = float(condition_value[1:])
                    if user_data.get('urge_intensity', 0) <= threshold:
                        return False
            
            elif condition_key == "days_since_last_contact":
                if condition_value.startswith(">"):
                    threshold = int(condition_value[1:])
                    if user_data.get('days_since_last_contact', 0) <= threshold:
                        return False
            
            elif condition_key == "journal_entries_this_week":
                if condition_value.startswith("<"):
                    threshold = int(condition_value[1:])
                    if user_data.get('journal_entries_this_week', 0) >= threshold:
                        return False
            
            elif condition_key == "days_since_last_exercise":
                if condition_value.startswith(">"):
                    threshold = int(condition_value[1:])
                    if user_data.get('days_since_last_exercise', 0) <= threshold:
                        return False
            
            elif condition_key == "risk_level":
                if user_data.get('risk_level', 'low') != condition_value:
                    return False
        
        return True
    
    def _priority_to_numeric(self, priority: RecommendationPriority) -> int:
        """Convert priority to numeric value for sorting"""
        priority_map = {
            RecommendationPriority.LOW: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.HIGH: 3,
            RecommendationPriority.CRITICAL: 4
        }
        return priority_map.get(priority, 1)
    
    def _get_fallback_recommendations(self, limit: int) -> List[RecoveryRecommendation]:
        """Get fallback recommendations when personalized ones fail"""
        fallback_ids = ["deep_breathing", "journal_reflection", "call_support"]
        recommendations = []
        
        for rec_id in fallback_ids[:limit]:
            if rec_id in self.recommendations_db:
                recommendations.append(self.recommendations_db[rec_id])
        
        return recommendations
    
    def track_recommendation_usage(self, recommendation_id: str, user_id: int, used: bool, feedback: Optional[str] = None):
        """Track when recommendations are used and get feedback"""
        try:
            usage_record = {
                "recommendation_id": recommendation_id,
                "user_id": user_id,
                "used": used,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            }
            
            self.recommendation_history.append(usage_record)
            
            # Save to file for analysis
            self._save_recommendation_history()
            
            self.logger.info(f"Tracked recommendation usage: {recommendation_id}, used: {used}")
            
        except Exception as e:
            self.logger.error(f"Error tracking recommendation usage: {e}")
    
    def _save_recommendation_history(self):
        """Save recommendation history to file"""
        try:
            history_file = "data/recommendation_history.json"
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            
            with open(history_file, 'w') as f:
                json.dump(self.recommendation_history, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving recommendation history: {e}")
    
    def get_recommendation_analytics(self) -> Dict:
        """Get analytics about recommendation usage"""
        try:
            total_recommendations = len(self.recommendation_history)
            used_recommendations = sum(1 for record in self.recommendation_history if record.get('used', False))
            
            # Usage by type
            usage_by_type = {}
            for record in self.recommendation_history:
                rec_id = record.get('recommendation_id')
                if rec_id in self.recommendations_db:
                    rec_type = self.recommendations_db[rec_id].type.value
                    if rec_type not in usage_by_type:
                        usage_by_type[rec_type] = {'total': 0, 'used': 0}
                    usage_by_type[rec_type]['total'] += 1
                    if record.get('used', False):
                        usage_by_type[rec_type]['used'] += 1
            
            return {
                "total_recommendations": total_recommendations,
                "used_recommendations": used_recommendations,
                "usage_rate": used_recommendations / max(total_recommendations, 1),
                "usage_by_type": usage_by_type
            }
            
        except Exception as e:
            self.logger.error(f"Error getting recommendation analytics: {e}")
            return {}
