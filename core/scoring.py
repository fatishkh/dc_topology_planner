"""
Weighted scoring system for topology ranking.

This module implements a Multi-Criteria Decision Analysis (MCDA) approach
inspired by Analytic Hierarchy Process (AHP) principles. Each topology is
evaluated against multiple criteria with expert-assigned weights.

Academic Note: The weights are heuristics derived from:
- Expert domain knowledge
- Industry best practices
- Literature on network topology selection
- Trade-off analysis between criteria

The weights can be adjusted based on:
- Specific deployment priorities
- Validated against real-world deployments
- Sensitivity analysis for robustness testing

Weight Configuration:
The SCORING_WEIGHTS dictionary below can be easily modified to reflect
different priorities. For example, if budget is more critical, increase
budget_match weight and decrease others proportionally.
"""

from core.models import (
    UserInputs,
    ClassificationResult,
    TopologyType,
    TopologyScore,
    ScaleCategory,
    BudgetCategory,
    PowerCategory,
    WorkloadType
)
from core.topology import get_topology_characteristics

# ============================================================================
# SCORING WEIGHTS (Expert-Assigned Heuristics)
# ============================================================================
# These weights determine the relative importance of each criterion.
# They sum to 1.0 and can be adjusted based on deployment priorities.
#
# Rationale:
# - Scale Match (30%): Deployment size is fundamental to topology choice
# - Budget Match (25%): Budget constraints are critical in real deployments
# - Power Match (20%): Power affects cooling and infrastructure costs
# - Workload Suitability (15%): Different workloads have different needs
# - Scalability Needs (10%): Future growth considerations
#
# To modify weights: Adjust values below (ensure they sum to 1.0)
# ============================================================================

SCORING_WEIGHTS = {
    "scale_match": 0.30,        # 30% - How well topology matches scale
    "budget_match": 0.25,       # 25% - Budget compatibility
    "power_match": 0.20,        # 20% - Power requirement alignment
    "workload_suitability": 0.15,  # 15% - Workload type compatibility
    "scalability_match": 0.10   # 10% - Future growth requirements
}

# Validate weights sum to 1.0
assert abs(sum(SCORING_WEIGHTS.values()) - 1.0) < 0.001, \
    "Scoring weights must sum to 1.0"


def calculate_topology_score(
    topology: TopologyType,
    inputs: UserInputs,
    classification: ClassificationResult
) -> TopologyScore:
    """
    Calculate a weighted score for a topology based on inputs.
    
    This implements a weighted linear combination (WLC) method, a common
    MCDA technique. Each criterion is scored 0.0-1.0, then multiplied
    by its weight and summed.
    
    Scoring criteria and weights (from SCORING_WEIGHTS config):
    - Scale match: 30% (default, configurable)
    - Budget match: 25% (default, configurable)
    - Power match: 20% (default, configurable)
    - Workload suitability: 15% (default, configurable)
    - Scalability needs: 10% (default, configurable)
    
    Academic Note: This is a deterministic scoring function. The individual
    criterion scores are based on expert-defined match matrices. Sensitivity
    analysis can be performed by adjusting weights.
    
    Args:
        topology: Topology type to score
        inputs: User input parameters
        classification: Classified input categories
        
    Returns:
        TopologyScore with calculated score and breakdown
    """
    characteristics = get_topology_characteristics(topology)
    breakdown = {}
    total_score = 0.0
    
    # 1. Scale match
    scale_score = _score_scale_match(topology, classification.scale)
    weight = SCORING_WEIGHTS["scale_match"]
    breakdown["Scale Match"] = f"{scale_score:.2f} ({weight*100:.0f}%)"
    total_score += scale_score * weight
    
    # 2. Budget match
    budget_score = _score_budget_match(topology, classification.budget)
    weight = SCORING_WEIGHTS["budget_match"]
    breakdown["Budget Match"] = f"{budget_score:.2f} ({weight*100:.0f}%)"
    total_score += budget_score * weight
    
    # 3. Power match
    power_score = _score_power_match(topology, classification.power)
    weight = SCORING_WEIGHTS["power_match"]
    breakdown["Power Match"] = f"{power_score:.2f} ({weight*100:.0f}%)"
    total_score += power_score * weight
    
    # 4. Workload suitability
    workload_score = _score_workload_match(topology, inputs.workload_type)
    weight = SCORING_WEIGHTS["workload_suitability"]
    breakdown["Workload Suitability"] = f"{workload_score:.2f} ({weight*100:.0f}%)"
    total_score += workload_score * weight
    
    # 5. Scalability needs
    scalability_score = _score_scalability_match(topology, classification.scale)
    weight = SCORING_WEIGHTS["scalability_match"]
    breakdown["Scalability Match"] = f"{scalability_score:.2f} ({weight*100:.0f}%)"
    total_score += scalability_score * weight
    
    breakdown["Total Score"] = f"{total_score:.2f}"
    
    return TopologyScore(
        topology=topology,
        score=total_score,
        breakdown=breakdown
    )


def _score_scale_match(topology: TopologyType, scale: ScaleCategory) -> float:
    """
    Score how well topology matches the scale category.
    
    Returns a normalized score (0.0-1.0) based on expert-defined match matrix.
    The scores reflect how well each topology type suits different scales.
    
    Match matrix rationale:
    - Three-Tier: Optimized for small deployments (1.0), struggles at large scale (0.2)
    - Leaf-Spine: Versatile, good for medium (0.9), excellent for large (0.95)
    - Fat-Tree: Overkill for small (0.1), optimal for large (1.0)
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Expert-defined match matrix: topology -> scale -> score
    match_matrix = {
        TopologyType.THREE_TIER: {
            ScaleCategory.SMALL: 1.0,
            ScaleCategory.MEDIUM: 0.6,
            ScaleCategory.LARGE: 0.2
        },
        TopologyType.LEAF_SPINE: {
            ScaleCategory.SMALL: 0.5,
            ScaleCategory.MEDIUM: 0.9,
            ScaleCategory.LARGE: 0.95
        },
        TopologyType.FAT_TREE: {
            ScaleCategory.SMALL: 0.1,
            ScaleCategory.MEDIUM: 0.4,
            ScaleCategory.LARGE: 1.0
        }
    }
    
    return match_matrix[topology][scale]


def _score_budget_match(topology: TopologyType, budget: BudgetCategory) -> float:
    """
    Score how well topology matches the budget category.
    
    Returns a normalized score (0.0-1.0) based on cost compatibility.
    
    Match matrix rationale:
    - Three-Tier: Cost-effective for low budgets (1.0), less suitable for high (0.3)
    - Leaf-Spine: Balanced cost, good for medium (0.9), acceptable for high (0.8)
    - Fat-Tree: Requires high budget (1.0), unsuitable for low (0.1)
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Expert-defined match matrix: topology -> budget -> score
    match_matrix = {
        TopologyType.THREE_TIER: {
            BudgetCategory.LOW: 1.0,
            BudgetCategory.MEDIUM: 0.7,
            BudgetCategory.HIGH: 0.3
        },
        TopologyType.LEAF_SPINE: {
            BudgetCategory.LOW: 0.4,
            BudgetCategory.MEDIUM: 0.9,
            BudgetCategory.HIGH: 0.8
        },
        TopologyType.FAT_TREE: {
            BudgetCategory.LOW: 0.1,
            BudgetCategory.MEDIUM: 0.3,
            BudgetCategory.HIGH: 1.0
        }
    }
    
    return match_matrix[topology][budget]


def _score_power_match(topology: TopologyType, power: PowerCategory) -> float:
    """
    Score how well topology matches the power category.
    
    Returns a normalized score (0.0-1.0) based on power requirement alignment.
    
    Match matrix rationale:
    - Three-Tier: Efficient for low power (1.0), less suitable for high (0.3)
    - Leaf-Spine: Balanced power needs, good for medium (0.9), acceptable for high (0.8)
    - Fat-Tree: Requires high power capacity (1.0), unsuitable for low (0.2)
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Expert-defined match matrix: topology -> power -> score
    match_matrix = {
        TopologyType.THREE_TIER: {
            PowerCategory.LOW: 1.0,
            PowerCategory.MEDIUM: 0.6,
            PowerCategory.HIGH: 0.3
        },
        TopologyType.LEAF_SPINE: {
            PowerCategory.LOW: 0.5,
            PowerCategory.MEDIUM: 0.9,
            PowerCategory.HIGH: 0.8
        },
        TopologyType.FAT_TREE: {
            PowerCategory.LOW: 0.2,
            PowerCategory.MEDIUM: 0.4,
            PowerCategory.HIGH: 1.0
        }
    }
    
    return match_matrix[topology][power]


def _score_workload_match(topology: TopologyType, workload_type) -> float:
    """
    Score how well topology matches the workload type.
    
    Returns a normalized score (0.0-1.0) based on workload characteristics.
    
    Match matrix rationale:
    - AI Training: High bandwidth needs favor Fat-Tree (1.0), good with Leaf-Spine (0.8)
    - Web Services: Balanced traffic patterns favor Leaf-Spine (0.9)
    - Storage: Predictable patterns work with Three-Tier (0.8) and Leaf-Spine (0.7)
    - Mixed: Versatile Leaf-Spine is optimal (0.95)
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Expert-defined match matrix: topology -> workload -> score
    match_matrix = {
        TopologyType.THREE_TIER: {
            WorkloadType.AI_TRAINING: 0.3,
            WorkloadType.WEB_SERVICES: 0.7,
            WorkloadType.STORAGE: 0.8,
            WorkloadType.MIXED: 0.5
        },
        TopologyType.LEAF_SPINE: {
            WorkloadType.AI_TRAINING: 0.8,
            WorkloadType.WEB_SERVICES: 0.9,
            WorkloadType.STORAGE: 0.7,
            WorkloadType.MIXED: 0.95
        },
        TopologyType.FAT_TREE: {
            WorkloadType.AI_TRAINING: 1.0,
            WorkloadType.WEB_SERVICES: 0.6,
            WorkloadType.STORAGE: 0.5,
            WorkloadType.MIXED: 0.7
        }
    }
    
    return match_matrix[topology][workload_type]


def _score_scalability_match(topology: TopologyType, scale: ScaleCategory) -> float:
    """
    Score how well topology's scalability matches the scale needs.
    
    Returns a normalized score (0.0-1.0) based on future growth requirements.
    
    Match matrix rationale:
    - Small scale: Doesn't need high scalability, Three-Tier sufficient (0.9)
    - Medium scale: Needs moderate scalability, Leaf-Spine optimal (0.9)
    - Large scale: Needs high scalability, Fat-Tree optimal (1.0)
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Expert-defined match matrix: topology -> scale -> score
    match_matrix = {
        TopologyType.THREE_TIER: {
            ScaleCategory.SMALL: 0.9,
            ScaleCategory.MEDIUM: 0.5,
            ScaleCategory.LARGE: 0.2
        },
        TopologyType.LEAF_SPINE: {
            ScaleCategory.SMALL: 0.4,
            ScaleCategory.MEDIUM: 0.9,
            ScaleCategory.LARGE: 0.95
        },
        TopologyType.FAT_TREE: {
            ScaleCategory.SMALL: 0.2,
            ScaleCategory.MEDIUM: 0.5,
            ScaleCategory.LARGE: 1.0
        }
    }
    
    return match_matrix[topology][scale]


def rank_topologies(
    inputs: UserInputs,
    classification: ClassificationResult
) -> list[TopologyScore]:
    """
    Calculate scores for all topologies and rank them.
    
    Args:
        inputs: User input parameters
        classification: Classified input categories
        
    Returns:
        List of TopologyScore objects, sorted by score (descending)
    """
    from core.topology import get_all_topologies
    
    scores = []
    for topology in get_all_topologies():
        score = calculate_topology_score(topology, inputs, classification)
        scores.append(score)
    
    # Sort by score (descending)
    scores.sort(key=lambda x: x.score, reverse=True)
    
    return scores
