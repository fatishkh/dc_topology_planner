# Adaptive Topology Selection in Data Center Networks

An academic decision-support system for recommending data center network topologies based on user inputs and explaining trade-offs.

## Overview

This application helps network architects and data center planners select the most suitable network topology (Three-Tier, Leaf-Spine, or Fat-Tree) based on deployment requirements including scale, budget, power constraints, and workload characteristics.

## Features

- **Rule-Based Decision Logic**: Implements flowchart-based decision rules for topology selection
- **Weighted Scoring System**: Multi-criteria evaluation with weighted scoring for all topologies
- **Interactive Visualization**: NetworkX-based topology diagrams and comparison charts
- **Comprehensive Analysis**: Detailed explanations, characteristics, and trade-offs for each topology
- **Academic UI**: Clean, minimal interface suitable for academic evaluation

## Technology Stack

- **Python 3.11**
- **Streamlit**: Web application framework
- **NetworkX**: Network topology graph generation
- **Matplotlib**: Visualization and plotting
- **Pandas**: Data manipulation and tabular outputs

## Project Structure

```
dc_topology_planner/
├── app.py                      # Main Streamlit application
├── core/
│   ├── models.py               # Data models and enums
│   ├── topology.py             # Topology definitions and characteristics
│   ├── decision_engine.py      # Rule-based decision logic
│   └── scoring.py              # Weighted scoring system
├── visualization/
│   ├── graphs.py               # NetworkX topology diagrams
│   └── charts.py               # Comparison charts and visualizations
├── utils/
│   └── validators.py           # Input validation utilities
├── data/
│   └── sample_inputs.json      # Sample input configurations
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Quick Start

### For New Users

**📖 Read the complete setup guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation and usage instructions.

### Quick Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

   Or on Windows, simply double-click `run.bat`

4. **Open browser** at `http://localhost:8501`

**For detailed instructions, troubleshooting, and advanced configuration, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

### Using the Application

1. **Enter Input Parameters**:
   - **Number of Racks**: Total server racks in the data center
   - **Number of Servers**: Total number of servers
   - **Budget (USD)**: Available budget for network infrastructure
   - **Power Limit (kW)**: Maximum power consumption limit
   - **Workload Type**: Select from AI Training, Web Services, Storage, or Mixed

2. **Click "Analyze & Recommend"**:
   - The system will classify your inputs
   - Apply rule-based logic to suggest a topology
   - Calculate weighted scores for all topologies
   - Generate visualizations and explanations

3. **Review Results**:
   - **Recommendation**: Highlighted suggested topology with confidence level
   - **Explanation**: Why this topology was chosen
   - **Topology Diagram**: NetworkX visualization of the recommended topology
   - **Score Comparison**: Bar chart comparing all topologies
   - **Comparison Table**: Side-by-side comparison of all topologies

## Decision Logic

The application uses a two-stage approach:

### 1. Rule-Based Selection (Primary)

Based on the flowchart logic:
- **Small scale OR Low budget OR Low power** → **Three-Tier**
- **Large scale AND High budget AND High power** → **Fat-Tree**
- **Else** → **Leaf-Spine**

### 2. Weighted Scoring (Secondary)

Each topology is scored based on:
- **Scale Match** (30%): How well topology matches deployment scale
- **Budget Match** (25%): Cost compatibility
- **Power Match** (20%): Power requirement alignment
- **Workload Suitability** (15%): Workload type compatibility
- **Scalability Needs** (10%): Future growth requirements

## Classification Thresholds

### Scale Classification
- **Small**: < 20 racks OR < 200 servers
- **Medium**: 20-100 racks AND 200-1000 servers
- **Large**: > 100 racks OR > 1000 servers

### Budget Classification
- **Low**: < $100,000
- **Medium**: $100,000 - $500,000
- **High**: > $500,000

### Power Classification
- **Low**: < 50 kW
- **Medium**: 50-200 kW
- **High**: > 200 kW

## Topology Types

### Three-Tier
- **Best for**: Small deployments, cost-sensitive projects
- **Characteristics**: Simple, hierarchical, cost-effective
- **Use Cases**: Small data centers, legacy infrastructure

### Leaf-Spine
- **Best for**: Medium to large deployments, modern cloud workloads
- **Characteristics**: Scalable, low latency, industry standard
- **Use Cases**: Cloud computing, virtualized environments

### Fat-Tree
- **Best for**: Large-scale deployments, high-performance computing
- **Characteristics**: Maximum scalability, optimal bandwidth
- **Use Cases**: HPC, AI/ML training, scientific computing

## Sample Inputs

Example configurations are provided in `data/sample_inputs.json`:
- Small deployment example
- Medium deployment example
- Large deployment example
- Cost-sensitive example
- High-performance example

## Development

### Code Structure

- **Modular Design**: Each component is in a separate module
- **Type Hints**: Full type annotations for better code clarity
- **Docstrings**: Comprehensive documentation for all functions
- **Validation**: Input validation at multiple levels

### Extending the System

To add new topologies or modify decision logic:
1. Add topology to `TopologyType` enum in `core/models.py`
2. Add characteristics in `core/topology.py`
3. Update decision rules in `core/decision_engine.py`
4. Add scoring logic in `core/scoring.py`
5. Create graph generator in `visualization/graphs.py`

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and you're in the project root directory
2. **Port Already in Use**: Change the port with `streamlit run app.py --server.port 8502`
3. **Visualization Not Showing**: Check that matplotlib backend is properly configured

## Academic Notes

This system is designed for academic evaluation and demonstrates:
- Rule-based decision support systems
- Multi-criteria decision analysis
- Network topology design principles
- Data visualization techniques
- Software engineering best practices

## Limitations

This system has several limitations that should be acknowledged for academic evaluation:

### 1. No Real Traffic Simulation
- The system does not perform packet-level network simulation
- No actual traffic patterns, congestion analysis, or latency measurements
- Recommendations are based on structural characteristics, not performance metrics
- Cannot validate recommendations against real network behavior

### 2. Heuristic Rules
- Decision rules are based on industry best practices and literature, but are heuristic
- Classification thresholds (scale, budget, power) are configurable but not validated against all deployment scenarios
- Rule-based logic is deterministic but may not capture edge cases
- Thresholds may need adjustment for specific industry contexts

### 3. Abstract Hardware Modeling
- NetworkX diagrams show logical connectivity, not physical hardware layouts
- No consideration of specific switch models, port counts, or hardware capabilities
- Topology visualizations are abstractions showing structure, not actual device placement
- Cost estimates are categorical (Low/Medium/High), not detailed cost models

### 4. Simplified Scoring Model
- Weighted scoring uses expert-assigned heuristics inspired by MCDA/AHP
- Weights are configurable but not derived from empirical data
- Match matrices (topology-criteria scores) are expert-defined, not learned
- No sensitivity analysis or robustness testing included

### 5. Static Decision Logic
- Rules are hardcoded and do not adapt based on historical data
- No machine learning or adaptive learning capabilities
- Cannot learn from deployment outcomes or user feedback
- Decision process is transparent but not self-improving

### 6. Limited Topology Options
- Only three topology types supported (Three-Tier, Leaf-Spine, Fat-Tree)
- Does not consider hybrid topologies or custom designs
- No support for emerging topologies (e.g., Dragonfly, Slim Fly)

## Future Work

Potential enhancements for future research and development:

### 1. Network Simulation Integration
- **NS-3 / Mininet Validation**: Integrate with network simulators to validate recommendations
  - Generate actual traffic patterns
  - Measure latency, throughput, and congestion
  - Compare predicted vs. actual performance
  - Validate topology recommendations against simulation results

### 2. Machine Learning Enhancement
- **ML-Assisted Weighting**: Use machine learning to learn optimal weights from historical deployments
  - Train models on successful deployment data
  - Adaptive weight adjustment based on outcomes
  - Feature importance analysis for decision criteria
  - Ensemble methods combining rule-based and ML approaches

### 3. Cost Model Refinement
- **Detailed Cost Modeling**: Develop comprehensive cost models
  - Hardware-specific pricing (switches, cables, transceivers)
  - Operational costs (power, cooling, maintenance)
  - Total Cost of Ownership (TCO) calculations
  - Integration with vendor pricing databases

### 4. Advanced Decision Methods
- **Multi-Objective Optimization**: Extend beyond weighted scoring
  - Pareto-optimal solutions
  - Constraint satisfaction programming
  - Game-theoretic approaches for multi-stakeholder scenarios

### 5. Extended Topology Support
- **Hybrid Topologies**: Support for custom and hybrid designs
- **Emerging Topologies**: Add Dragonfly, Slim Fly, and other modern architectures
- **Custom Topology Builder**: Allow users to define custom topologies

### 6. Validation and Testing
- **Case Study Validation**: Validate against real-world deployments
- **Sensitivity Analysis**: Test robustness of recommendations to parameter changes
- **A/B Testing Framework**: Compare recommendations with actual deployments

### 7. Enhanced Explainability
- **Interactive Decision Trees**: Visualize decision paths
- **What-If Analysis**: Allow users to explore alternative scenarios
- **Confidence Intervals**: Provide uncertainty estimates for recommendations

### 8. Integration Capabilities
- **API Interface**: RESTful API for integration with other systems
- **Database Backend**: Store historical recommendations and outcomes
- **Export Functionality**: Export recommendations in various formats (JSON, XML, PDF)

## Academic Notes

This system is designed for academic evaluation and demonstrates:
- Rule-based decision support systems
- Multi-criteria decision analysis (MCDA)
- Analytic Hierarchy Process (AHP) principles
- Network topology design principles
- Data visualization techniques
- Software engineering best practices
- Explainable AI concepts (XAI) in decision support

The system prioritizes **transparency** and **explainability** over performance optimization, making it suitable for academic viva defense and research evaluation.

## License

This project is created for academic purposes.

## Author

Academic Decision-Support System for Data Center Network Planning

---

**Note**: This is NOT a packet-level network simulator. It is a decision-support tool for topology selection based on high-level requirements. The system uses heuristic rules and weighted scoring, not real network simulation or machine learning models.
