"""
Configuration module for classification thresholds and decision parameters.

This module centralizes all heuristic thresholds used in the decision-making process.
These values are inspired by industry literature and best practices, but are
configurable based on specific deployment contexts.

Note: These thresholds are heuristics derived from:
- Industry white papers (Cisco, Arista, Juniper)
- Academic research on data center network design
- Empirical observations from real-world deployments

For academic evaluation: These values can be adjusted based on domain expertise
or validated against specific use cases.
"""

# ============================================================================
# SCALE CLASSIFICATION THRESHOLDS
# ============================================================================
# These thresholds classify deployment scale based on racks and servers.
# Rationale: Small deployments (< 20 racks) typically don't require
# complex topologies. Large deployments (> 100 racks) need high scalability.

SCALE_THRESHOLDS = {
    "small_max_racks": 20,      # Maximum racks for "Small" classification
    "small_max_servers": 200,   # Maximum servers for "Small" classification
    "large_min_racks": 100,      # Minimum racks for "Large" classification
    "large_min_servers": 1000,   # Minimum servers for "Large" classification
    # Note: Values between small and large are classified as "Medium"
}

# ============================================================================
# BUDGET CLASSIFICATION THRESHOLDS
# ============================================================================
# These thresholds classify budget levels in USD.
# Rationale: Based on typical network infrastructure costs:
# - Low: Basic switches, minimal redundancy
# - Medium: Enterprise-grade switches, some redundancy
# - High: Premium switches, full redundancy, advanced features

BUDGET_THRESHOLDS = {
    "low_max": 100000,      # Maximum budget for "Low" classification (USD)
    "high_min": 500000,     # Minimum budget for "High" classification (USD)
    # Note: Values between low_max and high_min are classified as "Medium"
}

# ============================================================================
# POWER CLASSIFICATION THRESHOLDS
# ============================================================================
# These thresholds classify power consumption in kilowatts.
# Rationale: Based on typical power requirements:
# - Low: Small deployments, basic cooling
# - Medium: Medium deployments, standard cooling
# - High: Large deployments, advanced cooling and redundancy

POWER_THRESHOLDS = {
    "low_max": 50,      # Maximum power for "Low" classification (kW)
    "high_min": 200,    # Minimum power for "High" classification (kW)
    # Note: Values between low_max and high_min are classified as "Medium"
}

# ============================================================================
# DECISION RULE NOTES
# ============================================================================
# The decision rules follow a hierarchical logic:
# 1. Small scale OR Low budget OR Low power → Three-Tier
#    Rationale: Cost-effective, simple to manage, adequate for small deployments
#
# 2. Large scale AND High budget AND High power → Fat-Tree
#    Rationale: Maximum performance and scalability, requires significant investment
#
# 3. Else → Leaf-Spine
#    Rationale: Balanced choice for most medium-to-large deployments
#
# These rules are deterministic and can be validated against known use cases.
