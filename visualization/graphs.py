"""
Network topology graph visualization using NetworkX.

This module generates abstract network topology diagrams for each topology type.
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from typing import Optional
import io

from core.models import TopologyType


def create_three_tier_graph(num_racks: int = 12) -> nx.DiGraph:
    """
    Create a NetworkX graph representing a Three-Tier topology.
    
    Structure:
    - Core layer: 2 core switches
    - Aggregation layer: 2-4 aggregation switches
    - Access layer: Multiple access switches (one per rack)
    
    Args:
        num_racks: Number of racks (determines access switches)
        
    Returns:
        NetworkX DiGraph representing the topology
    """
    G = nx.DiGraph()
    
    # Limit racks for visualization clarity
    num_racks = min(num_racks, 12)
    
    # Core layer (2 switches)
    core_switches = [f"Core-{i+1}" for i in range(2)]
    for switch in core_switches:
        G.add_node(switch, layer="core", node_type="switch")
    
    # Aggregation layer (2-4 switches based on scale)
    num_agg = min(4, max(2, (num_racks + 1) // 3))
    agg_switches = [f"Agg-{i+1}" for i in range(num_agg)]
    for switch in agg_switches:
        G.add_node(switch, layer="aggregation", node_type="switch")
    
    # Access layer (one per rack)
    access_switches = [f"Access-{i+1}" for i in range(num_racks)]
    for switch in access_switches:
        G.add_node(switch, layer="access", node_type="switch")
    
    # Connect core to aggregation (full mesh)
    for core in core_switches:
        for agg in agg_switches:
            G.add_edge(core, agg)
    
    # Connect aggregation to access (distributed)
    for i, access in enumerate(access_switches):
        agg_idx = i % num_agg
        G.add_edge(agg_switches[agg_idx], access)
    
    # Add sample servers (2 per rack for visualization)
    server_count = 0
    for access in access_switches:
        for j in range(2):  # 2 servers per rack shown
            server_id = f"S{server_count+1}"
            G.add_node(server_id, layer="server", node_type="server")
            G.add_edge(access, server_id)
            server_count += 1
    
    return G


def create_leaf_spine_graph(num_racks: int = 12) -> nx.DiGraph:
    """
    Create a NetworkX graph representing a Leaf-Spine topology.
    
    Structural characteristics:
    - Spine layer: 2-4 spine switches (interconnection layer)
    - Leaf layer: Multiple leaf switches (one per rack, server-facing)
    - Two-tier flat structure (no intermediate aggregation)
    - Equal-cost multipath: All leaf-to-leaf paths have same hop count
    - Full mesh between spine and leaf layers
    
    This topology demonstrates a modern flat architecture where any
    two servers are exactly 2 hops away (via spine), unlike Three-Tier's
    variable path length or Fat-Tree's multi-level structure.
    
    Args:
        num_racks: Number of racks (determines leaf switches)
        
    Returns:
        NetworkX DiGraph representing the topology
    """
    G = nx.DiGraph()
    
    # Limit racks for visualization clarity
    num_racks = min(num_racks, 12)
    
    # Spine layer (2-4 switches)
    num_spine = min(4, max(2, (num_racks + 1) // 3))
    spine_switches = [f"Spine-{i+1}" for i in range(num_spine)]
    for switch in spine_switches:
        G.add_node(switch, layer="spine", node_type="switch")
    
    # Leaf layer (one per rack)
    leaf_switches = [f"Leaf-{i+1}" for i in range(num_racks)]
    for switch in leaf_switches:
        G.add_node(switch, layer="leaf", node_type="switch")
    
    # Connect spine to leaf (full mesh)
    for spine in spine_switches:
        for leaf in leaf_switches:
            G.add_edge(spine, leaf)
    
    # Add sample servers (2 per rack for visualization)
    server_count = 0
    for leaf in leaf_switches:
        for j in range(2):  # 2 servers per rack shown
            server_id = f"S{server_count+1}"
            G.add_node(server_id, layer="server", node_type="server")
            G.add_edge(leaf, server_id)
            server_count += 1
    
    return G


def create_fat_tree_graph(num_racks: int = 12) -> nx.DiGraph:
    """
    Create a NetworkX graph representing a Fat-Tree topology.
    
    Structural characteristics:
    - Core layer: Multiple core switches (top level)
    - Aggregation layer: Multiple aggregation switches (middle level)
    - Edge layer: Edge switches (server-facing, bottom level)
    - Clos-style k-ary structure with increasing bandwidth toward core
    - Multi-level hierarchy (3+ tiers) unlike Two-Tier Leaf-Spine
    - Designed for maximum bisection bandwidth and scalability
    
    This topology demonstrates a Clos network architecture where bandwidth
    increases ("fattens") toward the core, providing optimal performance
    for large-scale deployments. Structurally distinct from both Three-Tier
    (traditional hierarchy) and Leaf-Spine (flat two-tier).
    
    Args:
        num_racks: Number of racks (determines edge switches)
        
    Returns:
        NetworkX DiGraph representing the topology
    """
    G = nx.DiGraph()
    
    # Limit racks for visualization clarity
    num_racks = min(num_racks, 12)
    
    # Core layer (4-8 switches)
    num_core = min(8, max(4, num_racks // 2))
    core_switches = [f"Core-{i+1}" for i in range(num_core)]
    for switch in core_switches:
        G.add_node(switch, layer="core", node_type="switch")
    
    # Aggregation layer (4-8 switches)
    num_agg = min(8, max(4, num_racks // 2))
    agg_switches = [f"Agg-{i+1}" for i in range(num_agg)]
    for switch in agg_switches:
        G.add_node(switch, layer="aggregation", node_type="switch")
    
    # Edge layer (one per rack)
    edge_switches = [f"Edge-{i+1}" for i in range(num_racks)]
    for switch in edge_switches:
        G.add_node(switch, layer="edge", node_type="switch")
    
    # Connect core to aggregation (distributed)
    for i, agg in enumerate(agg_switches):
        core_idx = i % num_core
        G.add_edge(core_switches[core_idx], agg)
        # Also connect to adjacent cores for redundancy
        if core_idx + 1 < num_core:
            G.add_edge(core_switches[core_idx + 1], agg)
    
    # Connect aggregation to edge (distributed)
    for i, edge in enumerate(edge_switches):
        agg_idx = i % num_agg
        G.add_edge(agg_switches[agg_idx], edge)
        # Also connect to adjacent aggregators for redundancy
        if agg_idx + 1 < num_agg:
            G.add_edge(agg_switches[agg_idx + 1], edge)
    
    # Add sample servers (2 per rack for visualization)
    server_count = 0
    for edge in edge_switches:
        for j in range(2):  # 2 servers per rack shown
            server_id = f"S{server_count+1}"
            G.add_node(server_id, layer="server", node_type="server")
            G.add_edge(edge, server_id)
            server_count += 1
    
    return G


def draw_topology_graph(
    topology: TopologyType,
    num_racks: int = 12,
    figsize: tuple = (12, 8),
    dpi: int = 100
) -> plt.Figure:
    """
    Draw a topology graph using NetworkX and Matplotlib.
    
    Args:
        topology: Topology type to visualize
        num_racks: Number of racks (affects graph structure)
        figsize: Figure size (width, height)
        dpi: Resolution in dots per inch
        
    Returns:
        Matplotlib Figure object
    """
    # Create graph based on topology type
    graph_creators = {
        TopologyType.THREE_TIER: create_three_tier_graph,
        TopologyType.LEAF_SPINE: create_leaf_spine_graph,
        TopologyType.FAT_TREE: create_fat_tree_graph
    }
    
    G = graph_creators[topology](num_racks)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor='white')
    
    # Define layout based on topology
    if topology == TopologyType.THREE_TIER:
        pos = _hierarchical_layout(G, layers=["core", "aggregation", "access", "server"])
    elif topology == TopologyType.LEAF_SPINE:
        pos = _hierarchical_layout(G, layers=["spine", "leaf", "server"])
    else:  # FAT_TREE
        pos = _hierarchical_layout(G, layers=["core", "aggregation", "edge", "server"])
    
    # Color mapping
    color_map = {
        "switch": "#2E86AB",  # Blue
        "server": "#A23B72"   # Purple
    }
    
    # Draw nodes by type
    for node_type in ["switch", "server"]:
        nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == node_type]
        if nodes:
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=nodes,
                node_color=color_map[node_type],
                node_size=800 if node_type == "switch" else 300,
                node_shape="s" if node_type == "switch" else "o",
                ax=ax,
                alpha=0.8
            )
    
    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        edge_color="#6C757D",
        width=1.5,
        alpha=0.6,
        arrows=True,
        arrowsize=15,
        arrowstyle='->',
        ax=ax
    )
    
    # Draw labels (only for switches, not servers to avoid clutter)
    switch_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "switch"]
    labels = {n: n for n in switch_nodes}
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        font_size=8,
        font_weight="bold",
        ax=ax
    )
    
    # Add title with structural description
    title_map = {
        TopologyType.THREE_TIER: "Three-Tier Topology\n(Core → Aggregation → Access hierarchical structure)",
        TopologyType.LEAF_SPINE: "Leaf-Spine Topology\n(Equal-cost multipath, two-tier flat structure)",
        TopologyType.FAT_TREE: "Fat-Tree Topology\n(Clos-style k-ary structure with increasing bandwidth toward core)"
    }
    
    ax.set_title(title_map[topology], fontsize=14, fontweight="bold", pad=20)
    ax.axis("off")
    
    # Add caption explaining abstraction
    caption_text = (
        "Note: This is a logical abstraction showing network connectivity patterns.\n"
        "Nodes represent switches (squares) and servers (circles). "
        "Not a physical hardware layout."
    )
    fig.text(0.5, 0.02, caption_text, ha='center', fontsize=9, 
             style='italic', color='#666666', wrap=True)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.08)  # Make room for caption
    
    return fig


def _hierarchical_layout(G: nx.DiGraph, layers: list[str]) -> dict:
    """
    Create a hierarchical layout for the graph based on layers.
    
    Args:
        G: NetworkX graph
        layers: List of layer names in order from top to bottom
        
    Returns:
        Dictionary mapping nodes to (x, y) positions
    """
    pos = {}
    layer_nodes = {layer: [] for layer in layers}
    
    # Group nodes by layer
    for node, data in G.nodes(data=True):
        layer = data.get("layer", "unknown")
        if layer in layer_nodes:
            layer_nodes[layer].append(node)
    
    # Position nodes in layers
    num_layers = len([l for l in layers if layer_nodes[l]])
    y_spacing = 1.0 / (num_layers + 1) if num_layers > 0 else 1.0
    
    y_pos = 1.0
    for layer in layers:
        if not layer_nodes[layer]:
            continue
        
        nodes = layer_nodes[layer]
        num_nodes = len(nodes)
        x_spacing = 1.0 / (num_nodes + 1) if num_nodes > 0 else 1.0
        
        for i, node in enumerate(nodes):
            x = (i + 1) * x_spacing
            pos[node] = (x, y_pos)
        
        y_pos -= y_spacing
    
    return pos
