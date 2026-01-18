"""
Chart and comparison visualization utilities.

This module provides functions to create comparison charts and tables
for topology analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

from core.models import TopologyScore, TopologyType
from core.topology import get_topology_comparison, get_topology_characteristics


def create_comparison_dataframe() -> pd.DataFrame:
    """
    Create a pandas DataFrame comparing all topologies.
    
    Returns:
        DataFrame with topology comparison data
    """
    comparison = get_topology_comparison()
    
    data = []
    for topology_name, props in comparison.items():
        data.append({
            "Topology": topology_name,
            "Cost": props["Cost"],
            "Scalability": props["Scalability"],
            "Complexity": props["Complexity"],
            "Description": props["Description"]
        })
    
    return pd.DataFrame(data)


def create_score_comparison_chart(scores: list[TopologyScore]) -> plt.Figure:
    """
    Create a bar chart comparing topology scores.
    
    Args:
        scores: List of TopologyScore objects (should be sorted)
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    
    topologies = [score.topology.value for score in scores]
    score_values = [score.score for score in scores]
    
    # Color mapping
    colors = {
        "Three-Tier": "#E63946",      # Red
        "Leaf-Spine": "#F77F00",      # Orange
        "Fat-Tree": "#FCBF49"         # Yellow
    }
    
    bars = ax.bar(
        topologies,
        score_values,
        color=[colors.get(t, "#6C757D") for t in topologies],
        alpha=0.8,
        edgecolor="black",
        linewidth=1.5
    )
    
    # Add value labels on bars
    for bar, score in zip(bars, score_values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height + 0.01,
            f'{score:.2f}',
            ha='center',
            va='bottom',
            fontweight='bold'
        )
    
    ax.set_ylabel('Weighted Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Topology', fontsize=12, fontweight='bold')
    ax.set_title('Topology Score Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, max(score_values) * 1.15 if score_values else 1.0)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    return fig


def create_score_breakdown_chart(score: TopologyScore) -> plt.Figure:
    """
    Create a horizontal bar chart showing score breakdown.
    
    Args:
        score: TopologyScore object to visualize
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    
    # Extract breakdown data (excluding Total Score)
    breakdown = {k: float(v.split()[0]) for k, v in score.breakdown.items() 
                 if k != "Total Score"}
    
    categories = list(breakdown.keys())
    values = list(breakdown.values())
    
    # Create horizontal bar chart
    bars = ax.barh(
        categories,
        values,
        color="#2E86AB",
        alpha=0.8,
        edgecolor="black",
        linewidth=1.5
    )
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        width = bar.get_width()
        ax.text(
            width + 0.01,
            bar.get_y() + bar.get_height() / 2.,
            f'{val:.2f}',
            ha='left',
            va='center',
            fontweight='bold'
        )
    
    ax.set_xlabel('Score', fontsize=12, fontweight='bold')
    ax.set_title(f'{score.topology.value} - Score Breakdown', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 1.0)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    return fig
