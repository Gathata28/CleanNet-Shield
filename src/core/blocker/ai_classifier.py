"""
AI-powered domain classification system
"""

import asyncio
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

logger = logging.getLogger(__name__)

@dataclass
class DomainClassification:
    domain: str
    category: str
    confidence: float
    features: Dict[str, float]
    risk_score: float

class AIDomainClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3), stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.categories = [
            'adult_content', 'gambling', 'social_media', 'news', 'shopping', 'safe'
        ]
        self.model_path = "models/domain_classifier.joblib"
        self._load_model()

    def _load_model(self):
        try:
            model_data = joblib.load(self.model_path)
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            logger.info("Loaded pre-trained domain classifier")
        except Exception:
            logger.info("No pre-trained model found, will train new model")
            self._train_model()

    def _train_model(self):
        training_domains = ["example.com", "test.org", "sample.net"]
        training_labels = ["safe", "safe", "safe"]
        features = self.vectorizer.fit_transform(training_domains)
        self.classifier.fit(features, training_labels)
        model_data = {'vectorizer': self.vectorizer, 'classifier': self.classifier}
        joblib.dump(model_data, self.model_path)
        logger.info("Trained and saved domain classifier")

    async def classify_domain(self, domain: str) -> DomainClassification:
        try:
            features = self._extract_domain_features(domain)
            domain_vector = self.vectorizer.transform([domain])
            prediction = self.classifier.predict(domain_vector)[0]
            confidence = self.classifier.predict_proba(domain_vector).max()
            risk_score = self._calculate_risk_score(domain, prediction, confidence)
            return DomainClassification(domain, prediction, confidence, features, risk_score)
        except Exception as e:
            logger.error(f"Failed to classify domain {domain}: {e}")
            return DomainClassification(domain, "unknown", 0.0, {}, 0.5)

    def _extract_domain_features(self, domain: str) -> Dict[str, float]:
        features = {}
        features['length'] = len(domain)
        features['subdomain_count'] = domain.count('.')
        suspicious_keywords = ['adult', 'porn', 'sex', 'xxx', 'gambling', 'casino']
        features['suspicious_keywords'] = sum(1 for keyword in suspicious_keywords if keyword in domain.lower())
        features['estimated_age'] = 0.0
        features['ssl_valid'] = 1.0
        features['reputation_score'] = 0.5
        return features

    def _calculate_risk_score(self, domain: str, category: str, confidence: float) -> float:
        base_scores = {
            'adult_content': 0.9,
            'gambling': 0.8,
            'social_media': 0.3,
            'news': 0.1,
            'shopping': 0.2,
            'safe': 0.0,
            'unknown': 0.5
        }
        base_score = base_scores.get(category, 0.5)
        adjusted_score = base_score * confidence + (0.5 * (1 - confidence))
        if 'xxx' in domain.lower():
            adjusted_score += 0.1
        if domain.count('.') > 2:
            adjusted_score += 0.05
        return min(adjusted_score, 1.0)

    async def classify_batch(self, domains: List[str]) -> List[DomainClassification]:
        tasks = [self.classify_domain(domain) for domain in domains]
        return await asyncio.gather(*tasks)

    async def update_model(self, new_data: List[Tuple[str, str]]):
        domains, labels = zip(*new_data)
        features = self.vectorizer.fit_transform(domains)
        self.classifier.fit(features, labels)
        model_data = {'vectorizer': self.vectorizer, 'classifier': self.classifier}
        joblib.dump(model_data, self.model_path)
        logger.info("Updated domain classifier with new data") 