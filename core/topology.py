"""
Topology definitions and characteristics.

This module provides detailed information about each supported network topology
and methods to retrieve topology characteristics.
"""

from core.models import TopologyType, TopologyCharacteristics


def get_topology_characteristics(topology: TopologyType) -> TopologyCharacteristics:
    """
    Retrieve detailed characteristics for a given topology type.
    
    Args:
        topology: The topology type to get characteristics for
        
    Returns:
        TopologyCharacteristics object with detailed information
    """
    characteristics = {
        TopologyType.THREE_TIER: TopologyCharacteristics(
            name="Three-Tier",
            description=(
                "Traditional hierarchical architecture with core, aggregation, "
                "and access layers. Suitable for small to medium deployments."
            ),
            typical_use_cases=[
                "Small data centers (< 20 racks)",
                "Legacy infrastructure",
                "Cost-sensitive deployments"
            ],
            advantages=[
                "Simple to design and manage",
                "Lower initial cost",
                "Clear separation of layers",
                "Good for predictable traffic patterns"
            ],
            disadvantages=[
                "Limited scalability",
                "Potential bottlenecks at aggregation layer",
                "Higher latency for east-west traffic",
                "Less efficient for modern cloud workloads"
            ],
            cost_estimate="Low",
            scalability="Low",
            complexity="Low"
        ),
        TopologyType.LEAF_SPINE: TopologyCharacteristics(
            name="Leaf-Spine",
            description=(
                "Modern two-tier architecture with leaf switches connecting "
                "servers and spine switches providing inter-leaf connectivity. "
                "Offers excellent scalability and performance."
            ),
            typical_use_cases=[
                "Medium to large data centers (20-100 racks)",
                "Cloud computing environments",
                "Virtualized workloads",
                "High east-west traffic"
            ],
            advantages=[
                "Excellent scalability",
                "Low latency (equal hop count)",
                "High bisection bandwidth",
                "Good for dynamic workloads",
                "Industry standard for modern DCs"
            ],
            disadvantages=[
                "Higher cost than three-tier",
                "Requires more switches",
                "More complex to manage at scale"
            ],
            cost_estimate="Medium",
            scalability="High",
            complexity="Medium"
        ),
        TopologyType.FAT_TREE: TopologyCharacteristics(
            name="Fat-Tree",
            description=(
                "Multi-level hierarchical topology with increasing bandwidth "
                "toward the core. Designed for maximum performance and "
                "scalability in large-scale deployments."
            ),
            typical_use_cases=[
                "Large data centers (> 100 racks)",
                "High-performance computing (HPC)",
                "AI/ML training clusters",
                "Scientific computing"
            ],
            advantages=[
                "Maximum scalability",
                "Optimal bisection bandwidth",
                "No oversubscription at core",
                "Excellent for high-bandwidth workloads",
                "Supports massive scale"
            ],
            disadvantages=[
                "Highest cost",
                "Complex design and management",
                "Requires significant power and cooling",
                "Overkill for smaller deployments"
            ],
            cost_estimate="High",
            scalability="Very High",
            complexity="High"
        )
    }
    
    return characteristics[topology]


def get_all_topologies() -> list[TopologyType]:
    """
    Get a list of all supported topology types.
    
    Returns:
        List of all TopologyType enum values
    """
    return list(TopologyType)


def get_topology_comparison() -> dict:
    """
    Get a comparison table of all topologies.
    
    Returns:
        Dictionary with topology names as keys and characteristics as values
    """
    comparison = {}
    for topology in get_all_topologies():
        chars = get_topology_characteristics(topology)
        comparison[topology.value] = {
            "Cost": chars.cost_estimate,
            "Scalability": chars.scalability,
            "Complexity": chars.complexity,
            "Description": chars.description
        }
    return comparison
