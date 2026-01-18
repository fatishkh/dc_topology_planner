"""
Rule-based decision engine for topology selection.

This module implements the decision logic based on the flowchart:
- Small scale OR Low budget OR Low power → Three-Tier
- Large scale AND High budget AND High power → Fat-Tree
- Else → Leaf-Spine

Academic Note: This is a deterministic rule-based system. The rules are
inspired by industry best practices and can be validated against known
deployment scenarios. Thresholds are configurable via core.config module.
"""

from core.models import (
    UserInputs,
    ClassificationResult,
    TopologyType,
    ScaleCategory,
    BudgetCategory,
    PowerCategory
)
from core.config import (
    SCALE_THRESHOLDS,
    BUDGET_THRESHOLDS,
    POWER_THRESHOLDS
)


def classify_scale(racks: int, servers: int) -> ScaleCategory:
    """
    Classify the scale of the deployment.
    
    Uses configurable thresholds from core.config module.
    Classification logic:
    - Small: racks < threshold OR servers < threshold
    - Large: racks > threshold OR servers > threshold
    - Medium: All other cases
    
    Heuristic rationale: Small deployments don't require complex topologies,
    while large deployments need high scalability. Medium deployments benefit
    from balanced solutions.
    
    Args:
        racks: Number of racks
        servers: Number of servers
        
    Returns:
        ScaleCategory classification
    """
    if (racks < SCALE_THRESHOLDS["small_max_racks"] or 
        servers < SCALE_THRESHOLDS["small_max_servers"]):
        return ScaleCategory.SMALL
    elif (racks >= SCALE_THRESHOLDS["large_min_racks"] or 
          servers >= SCALE_THRESHOLDS["large_min_servers"]):
        return ScaleCategory.LARGE
    else:
        return ScaleCategory.MEDIUM


def classify_budget(budget_usd: float) -> BudgetCategory:
    """
    Classify the budget level.
    
    Uses configurable thresholds from core.config module.
    Classification logic:
    - Low: budget < threshold
    - High: budget > threshold
    - Medium: All other cases
    
    Heuristic rationale: Budget constraints directly impact topology choice.
    Low budgets favor simpler topologies, while high budgets enable advanced
    architectures with better performance characteristics.
    
    Args:
        budget_usd: Budget in USD
        
    Returns:
        BudgetCategory classification
    """
    if budget_usd < BUDGET_THRESHOLDS["low_max"]:
        return BudgetCategory.LOW
    elif budget_usd >= BUDGET_THRESHOLDS["high_min"]:
        return BudgetCategory.HIGH
    else:
        return BudgetCategory.MEDIUM


def classify_power(power_kw: float) -> PowerCategory:
    """
    Classify the power level.
    
    Uses configurable thresholds from core.config module.
    Classification logic:
    - Low: power < threshold
    - High: power > threshold
    - Medium: All other cases
    
    Heuristic rationale: Power constraints affect cooling requirements and
    infrastructure complexity. High-power deployments can support more
    sophisticated topologies with better performance.
    
    Args:
        power_kw: Power limit in kilowatts
        
    Returns:
        PowerCategory classification
    """
    if power_kw < POWER_THRESHOLDS["low_max"]:
        return PowerCategory.LOW
    elif power_kw >= POWER_THRESHOLDS["high_min"]:
        return PowerCategory.HIGH
    else:
        return PowerCategory.MEDIUM


def classify_inputs(inputs: UserInputs) -> ClassificationResult:
    """
    Classify all user inputs into categories.
    
    Args:
        inputs: UserInputs object containing all parameters
        
    Returns:
        ClassificationResult with scale, budget, and power categories
    """
    scale = classify_scale(inputs.racks, inputs.servers)
    budget = classify_budget(inputs.budget_usd)
    power = classify_power(inputs.power_kw)
    
    return ClassificationResult(scale=scale, budget=budget, power=power)


def suggest_topology_by_rules(classification: ClassificationResult) -> TopologyType:
    """
    Suggest topology based on rule-based logic from the flowchart.
    
    This implements a deterministic decision tree with three rules evaluated
    in order. The rules are mutually exclusive and collectively exhaustive.
    
    Rules (evaluated in order):
    1. Small scale OR Low budget OR Low power → Three-Tier
       Rationale: Cost-effective solution for constrained deployments
    2. Large scale AND High budget AND High power → Fat-Tree
       Rationale: Maximum performance for large-scale deployments
    3. Else → Leaf-Spine
       Rationale: Balanced default for most medium-to-large deployments
    
    Academic Note: This is a rule-based expert system. The rules can be
    validated against known deployment scenarios and adjusted based on
    domain expertise.
    
    Args:
        classification: ClassificationResult with categorized inputs
        
    Returns:
        Suggested TopologyType
    """
    # Rule 1: Small OR Low budget OR Low power → Three-Tier
    # This rule fires if ANY constraint suggests a simpler topology
    if (classification.scale == ScaleCategory.SMALL or
        classification.budget == BudgetCategory.LOW or
        classification.power == PowerCategory.LOW):
        return TopologyType.THREE_TIER
    
    # Rule 2: Large AND High budget AND High power → Fat-Tree
    # This rule requires ALL conditions for high-performance topology
    if (classification.scale == ScaleCategory.LARGE and
        classification.budget == BudgetCategory.HIGH and
        classification.power == PowerCategory.HIGH):
        return TopologyType.FAT_TREE
    
    # Rule 3: Default → Leaf-Spine
    # Catches all remaining cases (medium scale, medium budget, etc.)
    return TopologyType.LEAF_SPINE


def explain_rule_application(classification: ClassificationResult) -> dict:
    """
    Explain which rule fired and why other topologies were not selected.
    
    This function provides explainability for the decision-making process,
    suitable for academic viva defense.
    
    Args:
        classification: ClassificationResult with categorized inputs
        
    Returns:
        Dictionary with explanation details:
        - fired_rule: Which rule number fired (1, 2, or 3)
        - rule_conditions: Conditions that triggered the rule
        - why_not_others: Explanation for why other topologies weren't selected
    """
    suggested = suggest_topology_by_rules(classification)
    
    explanation = {
        "fired_rule": None,
        "rule_conditions": [],
        "why_not_others": {}
    }
    
    # Check Rule 1
    rule1_conditions = []
    if classification.scale == ScaleCategory.SMALL:
        rule1_conditions.append("Small scale")
    if classification.budget == BudgetCategory.LOW:
        rule1_conditions.append("Low budget")
    if classification.power == PowerCategory.LOW:
        rule1_conditions.append("Low power")
    
    if rule1_conditions:
        explanation["fired_rule"] = 1
        explanation["rule_conditions"] = rule1_conditions
        explanation["why_not_others"] = {
            "Leaf-Spine": "Not selected because deployment has constraints (small scale, low budget, or low power) that favor simpler topology",
            "Fat-Tree": "Not selected because Fat-Tree requires large scale AND high budget AND high power, which is not met"
        }
        return explanation
    
    # Check Rule 2
    if (classification.scale == ScaleCategory.LARGE and
        classification.budget == BudgetCategory.HIGH and
        classification.power == PowerCategory.HIGH):
        explanation["fired_rule"] = 2
        explanation["rule_conditions"] = ["Large scale", "High budget", "High power"]
        explanation["why_not_others"] = {
            "Three-Tier": "Not selected because Three-Tier is designed for smaller deployments and would be a bottleneck at this scale",
            "Leaf-Spine": "Not selected because deployment has sufficient resources (large scale, high budget, high power) to support Fat-Tree's superior performance"
        }
        return explanation
    
    # Rule 3 (default)
    explanation["fired_rule"] = 3
    explanation["rule_conditions"] = ["Medium scale/budget/power or mixed conditions"]
    explanation["why_not_others"] = {
        "Three-Tier": "Not selected because deployment scale/budget/power exceeds Three-Tier's optimal range",
        "Fat-Tree": "Not selected because Fat-Tree requires all three conditions (large scale AND high budget AND high power) to be met simultaneously"
    }
    
    return explanation


def generate_explanation(
    topology: TopologyType,
    classification: ClassificationResult,
    rule_based: bool = True
) -> str:
    """
    Generate a textual explanation for why a topology was recommended.
    
    Args:
        topology: The recommended topology
        classification: Input classification result
        rule_based: Whether this was a rule-based recommendation
        
    Returns:
        Explanation string
    """
    explanations = {
        TopologyType.THREE_TIER: (
            f"Three-Tier topology is recommended because your deployment "
            f"is classified as {classification.scale.value} scale with "
            f"{classification.budget.value} budget and {classification.power.value} power. "
            f"This topology is cost-effective for smaller deployments and provides "
            f"adequate performance for traditional workloads."
        ),
        TopologyType.LEAF_SPINE: (
            f"Leaf-Spine topology is recommended as it balances performance, "
            f"scalability, and cost for your {classification.scale.value} scale "
            f"deployment with {classification.budget.value} budget. This modern "
            f"architecture offers excellent east-west traffic performance and is "
            f"the industry standard for medium to large data centers."
        ),
        TopologyType.FAT_TREE: (
            f"Fat-Tree topology is recommended for your {classification.scale.value} "
            f"scale deployment with {classification.budget.value} budget and "
            f"{classification.power.value} power. This topology provides maximum "
            f"scalability and performance, making it ideal for high-performance "
            f"computing and large-scale AI/ML workloads."
        )
    }
    
    base_explanation = explanations.get(topology, "Topology recommended based on your inputs.")
    
    if not rule_based:
        base_explanation += " This recommendation is based on weighted scoring analysis."
    
    return base_explanation
