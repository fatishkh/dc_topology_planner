# Data Center Network Topology Planner

An intelligent decision-support system for selecting optimal data center network topologies based on scale, budget, power, and workload requirements.

## Features

- **Rule-based topology selection** (Three-Tier, Leaf-Spine, Fat-Tree)
- **Weighted scoring analysis** with configurable criteria
- **Interactive visualizations** of network topologies
- **Detailed explanations** for decision transparency
- **Clean, responsive web interface** built with Streamlit

## Quick Start

1. **Install Python 3.11+**
2. **Clone/download this project**
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** to `http://localhost:8501`

## Usage

1. Enter your data center requirements (racks, servers, budget, power, workload)
2. Click "Analyze & Recommend Topology"
3. Review the recommended topology with detailed explanations
4. Explore visualizations and comparison charts

## Project Structure

```
dc_topology_planner/
├── app.py                    # Main Streamlit application
├── core/                     # Business logic
│   ├── models.py            # Data models and enums
│   ├── config.py            # Configuration thresholds
│   ├── decision_engine.py   # Rule-based decision logic
│   ├── scoring.py           # Weighted scoring system
│   └── topology.py          # Topology characteristics
├── visualization/           # Charts and graphs
│   ├── graphs.py           # Network topology diagrams
│   └── charts.py           # Score comparison charts
├── utils/                  # Utilities
│   └── validators.py       # Input validation
└── requirements.txt        # Dependencies
```

## Configuration

- **Modify thresholds:** Edit `core/config.py`
- **Adjust scoring weights:** Edit `core/scoring.py`
- **Customize UI theme:** Edit `.streamlit/config.toml`

## Requirements

- Python 3.11+
- Streamlit 1.28+
- NetworkX 3.1+
- Matplotlib 3.7+
- Pandas 2.0+

## License

Academic/Educational Use
