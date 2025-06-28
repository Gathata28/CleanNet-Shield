"""
Machine Learning-based Relapse Prediction System
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from src.utils.logger import Logger


@dataclass
class RelapsePrediction:
    """Relapse prediction result"""
    risk_score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    risk_level: str  # "low", "medium", "high", "critical"
    factors: List[str]  # Contributing factors
    recommendations: List[str]  # Suggested actions
    next_check_date: datetime  # When to re-evaluate


class RelapsePredictor:
    """Machine learning-based relapse prediction system"""
    
    def __init__(self):
        self.logger = Logger()
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/relapse_predictor.joblib"
        self.scaler_path = "models/relapse_scaler.joblib"
        
        # Ensure models directory exists
        os.makedirs("models", exist_ok=True)
        
        # Load or initialize model
        self._load_or_initialize_model()
    
    def _load_or_initialize_model(self):
        """Load existing model or initialize a new one"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.logger.info("Loaded existing relapse prediction model")
            else:
                self._initialize_model()
                self.logger.info("Initialized new relapse prediction model")
        except Exception as e:
            self.logger.error(f"Error loading relapse prediction model: {e}")
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize a new relapse prediction model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
    
    def extract_features(self, user_data: Dict) -> np.ndarray:
        """Extract features from user data for prediction"""
        features = []
        
        # Streak-related features
        current_streak = user_data.get('current_streak', 0)
        longest_streak = user_data.get('longest_streak', 0)
        streak_ratio = current_streak / max(longest_streak, 1)
        
        # Time-based features
        days_since_start = user_data.get('days_since_start', 0)
        days_since_last_relapse = user_data.get('days_since_last_relapse', 0)
        
        # Behavioral features
        journal_entries_last_week = user_data.get('journal_entries_last_week', 0)
        mood_scores_last_week = user_data.get('mood_scores_last_week', [])
        avg_mood = np.mean(mood_scores_last_week) if mood_scores_last_week else 3.0
        
        # Trigger-related features
        trigger_frequency = user_data.get('trigger_frequency', 0)
        coping_strategy_usage = user_data.get('coping_strategy_usage', 0)
        
        # Network activity features
        blocked_attempts_last_week = user_data.get('blocked_attempts_last_week', 0)
        suspicious_connections = user_data.get('suspicious_connections', 0)
        
        # Time of day and day of week features
        current_hour = datetime.now().hour
        current_day_of_week = datetime.now().weekday()
        
        # Combine all features
        feature_vector = [
            current_streak,
            longest_streak,
            streak_ratio,
            days_since_start,
            days_since_last_relapse,
            journal_entries_last_week,
            avg_mood,
            trigger_frequency,
            coping_strategy_usage,
            blocked_attempts_last_week,
            suspicious_connections,
            current_hour,
            current_day_of_week
        ]
        
        return np.array(feature_vector).reshape(1, -1)
    
    def predict_relapse_risk(self, user_data: Dict) -> RelapsePrediction:
        """Predict relapse risk for a user"""
        try:
            # Extract features
            features = self.extract_features(user_data)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            risk_score = self.model.predict_proba(features_scaled)[0][1]  # Probability of relapse
            
            # Determine confidence based on model certainty
            confidence = max(self.model.predict_proba(features_scaled)[0])
            
            # Determine risk level
            if risk_score < 0.3:
                risk_level = "low"
            elif risk_score < 0.6:
                risk_level = "medium"
            elif risk_score < 0.8:
                risk_level = "high"
            else:
                risk_level = "critical"
            
            # Identify contributing factors
            factors = self._identify_contributing_factors(user_data, risk_score)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(risk_level, factors)
            
            # Determine next check date
            next_check_date = self._calculate_next_check_date(risk_level)
            
            return RelapsePrediction(
                risk_score=risk_score,
                confidence=confidence,
                risk_level=risk_level,
                factors=factors,
                recommendations=recommendations,
                next_check_date=next_check_date
            )
            
        except Exception as e:
            self.logger.error(f"Error predicting relapse risk: {e}")
            # Return safe default prediction
            return RelapsePrediction(
                risk_score=0.5,
                confidence=0.0,
                risk_level="medium",
                factors=["Unable to analyze data"],
                recommendations=["Contact support for assistance"],
                next_check_date=datetime.now() + timedelta(days=1)
            )
    
    def _identify_contributing_factors(self, user_data: Dict, risk_score: float) -> List[str]:
        """Identify factors contributing to relapse risk"""
        factors = []
        
        # Analyze various risk factors
        if user_data.get('current_streak', 0) < 7:
            factors.append("Short current streak")
        
        if user_data.get('trigger_frequency', 0) > 5:
            factors.append("High trigger frequency")
        
        if user_data.get('blocked_attempts_last_week', 0) > 3:
            factors.append("Recent blocking attempts")
        
        if user_data.get('avg_mood', 3.0) < 2.5:
            factors.append("Low mood scores")
        
        if user_data.get('journal_entries_last_week', 0) < 3:
            factors.append("Low journal activity")
        
        if user_data.get('coping_strategy_usage', 0) < 2:
            factors.append("Limited coping strategy usage")
        
        # Time-based factors
        current_hour = datetime.now().hour
        if 22 <= current_hour or current_hour <= 6:
            factors.append("Late night activity")
        
        return factors[:5]  # Return top 5 factors
    
    def _generate_recommendations(self, risk_level: str, factors: List[str]) -> List[str]:
        """Generate personalized recommendations based on risk level and factors"""
        recommendations = []
        
        if risk_level == "critical":
            recommendations.extend([
                "Immediate action required - contact your support network",
                "Use emergency coping strategies",
                "Consider professional help if needed",
                "Remove yourself from triggering situations"
            ])
        elif risk_level == "high":
            recommendations.extend([
                "Increase journaling frequency",
                "Practice mindfulness exercises",
                "Reach out to accountability partner",
                "Review your recovery goals"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Stay consistent with your routine",
                "Continue using coping strategies",
                "Monitor your triggers",
                "Celebrate your progress"
            ])
        else:  # low
            recommendations.extend([
                "Maintain your current positive habits",
                "Continue building your support network",
                "Document what's working well",
                "Help others in their recovery journey"
            ])
        
        # Add factor-specific recommendations
        if "Short current streak" in factors:
            recommendations.append("Focus on building momentum with small wins")
        
        if "High trigger frequency" in factors:
            recommendations.append("Identify and avoid trigger situations")
        
        if "Low journal activity" in factors:
            recommendations.append("Write in your journal daily")
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _calculate_next_check_date(self, risk_level: str) -> datetime:
        """Calculate when to next check relapse risk"""
        now = datetime.now()
        
        if risk_level == "critical":
            return now + timedelta(hours=6)
        elif risk_level == "high":
            return now + timedelta(days=1)
        elif risk_level == "medium":
            return now + timedelta(days=3)
        else:  # low
            return now + timedelta(days=7)
    
    def train_model(self, training_data: List[Dict]) -> bool:
        """Train the relapse prediction model with user data"""
        try:
            if len(training_data) < 10:
                self.logger.warning("Insufficient training data for reliable model")
                return False
            
            # Prepare training data
            X = []
            y = []
            
            for data_point in training_data:
                features = self.extract_features(data_point['features'])
                X.append(features.flatten())
                y.append(data_point['relapsed'])
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
            
            self.logger.info(f"Model trained successfully - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
            
            # Save model
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error training relapse prediction model: {e}")
            return False
    
    def update_model(self, new_data: Dict) -> bool:
        """Update model with new user data"""
        try:
            # This would implement online learning or model updating
            # For now, we'll just log the new data
            self.logger.info(f"Received new data for model update: {new_data}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating model: {e}")
            return False 