"""
Data models for the Data Center Network Topology Planner.

This module defines the core data structures used throughout the application,
including input parameters, topology characteristics, and recommendation results.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class WorkloadType(str, Enum):
    """Enumeration of supported workload types."""
    AI_TRAINING = "AI Training"
    WEB_SERVICES = "Web Services"
    STORAGE = "Storage"
    MIXED = "Mixed"


class TopologyType(str, Enum):
    """Enumeration of supported network topologies."""
    THREE_TIER = "Three-Tier"
    LEAF_SPINE = "Leaf-Spine"
    FAT_TREE = "Fat-Tree"


class ScaleCategory(str, Enum):
    """Scale classification categories."""
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class BudgetCategory(str, Enum):
    """Budget classification categories."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class PowerCategory(str, Enum):
    """Power classification categories."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class UserInputs:
    """
    Container for user-provided input parameters.
    
    Attributes:
        racks: Number of server racks in the data center
        servers: Total number of servers
        budget_usd: Total budget in USD
        power_kw: Power limit in kilowatts
        workload_type: Type of workload to be hosted
    """
    racks: int
    servers: int
    budget_usd: float
    power_kw: float
    workload_type: WorkloadType
    
    def __post_init__(self):
        """Validate inputs after initialization."""
        if self.racks <= 0:
            raise ValueError("Number of racks must be positive")
        if self.servers <= 0:
            raise ValueError("Number of servers must be positive")
        if self.budget_usd < 0:
            raise ValueError("Budget cannot be negative")
        if self.power_kw <= 0:
            raise ValueError("Power limit must be positive")


@dataclass
class ClassificationResult:
    """
    Result of classifying user inputs into categories.
    
    Attributes:
        scale: Scale category (Small/Medium/Large)
        budget: Budget category (Low/Medium/High)
        power: Power category (Low/Medium/High)
    """
    scale: ScaleCategory
    budget: BudgetCategory
    power: PowerCategory


@dataclass
class TopologyScore:
    """
    Weighted score for a topology option.
    
    Attributes:
        topology: The topology type being scored
        score: Calculated weighted score
        breakdown: Dictionary explaining score components
    """
    topology: TopologyType
    score: float
    breakdown: dict


@dataclass
class TopologyRecommendation:
    """
    Complete recommendation result for a topology.
    
    Attributes:
        topology: Recommended topology type
        confidence: Confidence level (0-1)
        explanation: Textual explanation of why this topology was chosen
        scores: List of all topology scores (ranked)
        classification: Input classification result
    """
    topology: TopologyType
    confidence: float
    explanation: str
    scores: list[TopologyScore]
    classification: ClassificationResult


@dataclass
class TopologyCharacteristics:
    """
    Characteristics and properties of a network topology.
    
    Attributes:
        name: Topology name
        description: Brief description
        typical_use_cases: List of typical use cases
        advantages: List of advantages
        disadvantages: List of disadvantages
        cost_estimate: Estimated cost category (Low/Medium/High)
        scalability: Scalability rating (Low/Medium/High)
        complexity: Complexity rating (Low/Medium/High)
    """
    name: str
    description: str
    typical_use_cases: list[str]
    advantages: list[str]
    disadvantages: list[str]
    cost_estimate: str
    scalability: str
    complexity: str
