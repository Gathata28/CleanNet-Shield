"""
Blocking rule data structures for CleanNet Shield
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional, List
from enum import Enum


class BlockingSeverity(Enum):
    """Severity levels for blocking rules"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BlockingCategory(Enum):
    """Categories for blocking rules"""

    ADULT_CONTENT = "adult_content"
    SOCIAL_MEDIA = "social_media"
    GAMBLING = "gambling"
    DRUGS = "drugs"
    VIOLENCE = "violence"
    MALWARE = "malware"
    PHISHING = "phishing"
    CUSTOM = "custom"


@dataclass
class BlockingRule:
    """Represents a single blocking rule"""

    domain: str
    category: BlockingCategory
    severity: BlockingSeverity
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "manual"
    metadata: Dict[str, str] = field(default_factory=dict)
    is_active: bool = True
    expires_at: Optional[datetime] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate the blocking rule after initialization"""
        if not self.domain:
            raise ValueError("Domain cannot be empty")

        if not isinstance(self.category, BlockingCategory):
            self.category = BlockingCategory(self.category)

        if not isinstance(self.severity, BlockingSeverity):
            self.severity = BlockingSeverity(self.severity)

    def is_expired(self) -> bool:
        """Check if the rule has expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> Dict:
        """Convert rule to dictionary for serialization"""
        return {
            "domain": self.domain,
            "category": self.category.value,
            "severity": self.severity.value,
            "created_at": self.created_at.isoformat(),
            "source": self.source,
            "metadata": self.metadata,
            "is_active": self.is_active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "description": self.description,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BlockingRule":
        """Create rule from dictionary"""
        # Handle datetime fields
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if isinstance(data["created_at"], str)
            else data["created_at"]
        )
        expires_at = None
        if data.get("expires_at"):
            expires_at = (
                datetime.fromisoformat(data["expires_at"])
                if isinstance(data["expires_at"], str)
                else data["expires_at"]
            )

        return cls(
            domain=data["domain"],
            category=data["category"],
            severity=data["severity"],
            created_at=created_at,
            source=data.get("source", "manual"),
            metadata=data.get("metadata", {}),
            is_active=data.get("is_active", True),
            expires_at=expires_at,
            description=data.get("description"),
            tags=data.get("tags", []),
        )


@dataclass
class BlockingRuleSet:
    """Collection of blocking rules"""

    name: str
    description: Optional[str] = None
    rules: List[BlockingRule] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1.0.0"

    def add_rule(self, rule: BlockingRule) -> None:
        """Add a rule to the set"""
        self.rules.append(rule)
        self.updated_at = datetime.now(timezone.utc)

    def remove_rule(self, domain: str) -> bool:
        """Remove a rule by domain"""
        initial_count = len(self.rules)
        self.rules = [rule for rule in self.rules if rule.domain != domain]
        if len(self.rules) < initial_count:
            self.updated_at = datetime.now(timezone.utc)
            return True
        return False

    def get_active_rules(self) -> List[BlockingRule]:
        """Get all active, non-expired rules"""
        return [rule for rule in self.rules if rule.is_active and not rule.is_expired()]

    def get_rules_by_category(self, category: BlockingCategory) -> List[BlockingRule]:
        """Get rules by category"""
        return [rule for rule in self.get_active_rules() if rule.category == category]

    def get_rules_by_severity(self, severity: BlockingSeverity) -> List[BlockingRule]:
        """Get rules by severity"""
        return [rule for rule in self.get_active_rules() if rule.severity == severity]

    def to_dict(self) -> Dict:
        """Convert rule set to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "rules": [rule.to_dict() for rule in self.rules],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BlockingRuleSet":
        """Create rule set from dictionary"""
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if isinstance(data["created_at"], str)
            else data["created_at"]
        )
        updated_at = (
            datetime.fromisoformat(data["updated_at"])
            if isinstance(data["updated_at"], str)
            else data["updated_at"]
        )

        rules = [
            BlockingRule.from_dict(rule_data) for rule_data in data.get("rules", [])
        ]

        return cls(
            name=data["name"],
            description=data.get("description"),
            rules=rules,
            created_at=created_at,
            updated_at=updated_at,
            version=data.get("version", "1.0.0"),
        )
