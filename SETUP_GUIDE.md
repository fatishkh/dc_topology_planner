# Complete Setup and User Guide
## Adaptive Topology Selection in Data Center Networks

**Version:** 1.0  
**Last Updated:** 2024  
**Python Version Required:** 3.11 or higher

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Running the Application](#running-the-application)
5. [How It Works](#how-it-works)
6. [Using the Application](#using-the-application)
7. [Understanding the Results](#understanding-the-results)
8. [Project Structure](#project-structure)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Configuration](#advanced-configuration)

---

## Introduction

This is a **decision-support system** for selecting data center network topologies. It helps network architects and planners choose between three topology types (Three-Tier, Leaf-Spine, or Fat-Tree) based on their specific requirements.

### What This System Does

- **Analyzes** your data center requirements (scale, budget, power, workload)
- **Classifies** inputs into categories (Small/Medium/Large, Low/Medium/High)
- **Recommends** the best topology using rule-based logic
- **Scores** all topologies using weighted multi-criteria analysis
- **Visualizes** network topologies and provides detailed explanations
- **Explains** why each topology was or wasn't selected

### What This System Does NOT Do

- ❌ Does NOT simulate actual network traffic
- ❌ Does NOT measure real performance metrics
- ❌ Does NOT use machine learning
- ❌ Does NOT connect to real hardware

**This is a decision-support tool, not a network simulator.**

---

## System Requirements

### Required Software

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **pip** (usually comes with Python)
   - Verify: `pip --version`

3. **Web Browser** (Chrome, Firefox, Edge, or Safari)

### Operating System

- ✅ Windows 10/11
- ✅ macOS 10.14 or later
- ✅ Linux (Ubuntu 18.04+, Debian 10+, etc.)

### Hardware Requirements

- **Minimum:** 4GB RAM, 1GB free disk space
- **Recommended:** 8GB RAM, 2GB free disk space

---

## Installation Guide

### Step 1: Download/Clone the Project

If you received this project as a ZIP file:
1. Extract it to a folder (e.g., `C:\Users\YourName\Desktop\dc_topology_planner`)
2. Open the folder

If you have Git:
```bash
git clone <repository-url>
cd dc_topology_planner
```

### Step 2: Verify Python Installation

Open Command Prompt (Windows) or Terminal (Mac/Linux):

```bash
python --version
```

You should see: `Python 3.11.x` or higher

If you see an error, Python is not installed or not in PATH.

### Step 3: Create Virtual Environment (Recommended)

**Why use a virtual environment?**
- Keeps project dependencies isolated
- Prevents conflicts with other Python projects
- Makes the project portable

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` at the start of your command prompt.**

### Step 4: Install Dependencies

With virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `networkx` - Network graph generation
- `matplotlib` - Visualization
- `pandas` - Data manipulation

**Expected output:** "Successfully installed streamlit-... networkx-... matplotlib-... pandas-..."

### Step 5: Verify Installation

Test that everything works:

```bash
python -c "import streamlit, networkx, matplotlib, pandas; print('All packages installed successfully!')"
```

If you see "All packages installed successfully!", you're ready to go!

---

## Running the Application

### Method 1: Using the Batch File (Windows Only)

1. Double-click `run.bat` in the project folder
2. Wait for the browser to open automatically
3. The app will be available at `http://localhost:8501`

### Method 2: Manual Start (All Platforms)

1. **Activate virtual environment** (if not already active):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser**:
   - The app should open automatically
   - If not, go to: `http://localhost:8501`

### Method 3: Using Python Module (Alternative)

If `streamlit` command doesn't work:

```bash
python -m streamlit run app.py
```

Or with full path:

```bash
venv\Scripts\python.exe -m streamlit run app.py
```

### Stopping the Application

- Press `Ctrl + C` in the terminal/command prompt
- Or close the terminal window

---

## How It Works

### Architecture Overview

The system uses a **two-stage decision process**:

```
User Inputs → Classification → Rule-Based Selection → Weighted Scoring → Recommendation
```

### Stage 1: Input Classification

Your inputs are classified into categories:

**Scale Classification:**
- **Small:** < 20 racks OR < 200 servers
- **Medium:** 20-100 racks AND 200-1000 servers  
- **Large:** > 100 racks OR > 1000 servers

**Budget Classification:**
- **Low:** < $100,000
- **Medium:** $100,000 - $500,000
- **High:** > $500,000

**Power Classification:**
- **Low:** < 50 kW
- **Medium:** 50-200 kW
- **High:** > 200 kW

**Configuration:** Thresholds are in `core/config.py` and can be adjusted.

### Stage 2: Rule-Based Decision Logic

Three rules are evaluated in order:

**Rule 1:** Small scale **OR** Low budget **OR** Low power  
→ **Three-Tier** topology

**Rule 2:** Large scale **AND** High budget **AND** High power  
→ **Fat-Tree** topology

**Rule 3:** Everything else  
→ **Leaf-Spine** topology

**Implementation:** `core/decision_engine.py`

### Stage 3: Weighted Scoring (Secondary Analysis)

All three topologies are scored using weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Scale Match | 30% | How well topology matches deployment scale |
| Budget Match | 25% | Cost compatibility |
| Power Match | 20% | Power requirement alignment |
| Workload Suitability | 15% | Workload type compatibility |
| Scalability Match | 10% | Future growth requirements |

**Total Score = Σ (Criterion Score × Weight)**

**Configuration:** Weights are in `core/scoring.py` (SCORING_WEIGHTS dictionary)

### Stage 4: Final Recommendation

- **Primary:** Rule-based recommendation (takes precedence)
- **Secondary:** Top-scoring topology from weighted analysis
- **Confidence:** Higher if both methods agree

---

## Using the Application

### Step-by-Step Guide

#### 1. Enter Input Parameters

Open the "📝 Enter Data Center Requirements" section and fill in:

**Infrastructure Scale:**
- **Number of Racks:** Total server racks (1-10,000)
- **Number of Servers:** Total servers (1-1,000,000)

**Resource Constraints:**
- **Budget (USD):** Available budget (0 - $1,000,000,000)
- **Power Limit (kW):** Maximum power (0.1 - 100,000 kW)

**Workload Configuration:**
- **Workload Type:** Select from dropdown
  - **AI Training:** Machine learning, deep learning workloads
  - **Web Services:** Web applications, APIs, microservices
  - **Storage:** File storage, backup, archival systems
  - **Mixed:** Combination of different workload types

#### 2. Click "🔍 Analyze & Recommend Topology"

The system will:
- Validate your inputs
- Classify them into categories
- Apply decision rules
- Calculate scores
- Generate visualizations

#### 3. Review the Results

You'll see several sections:

**🎯 Topology Recommendation**
- Highlighted recommended topology
- Confidence level (70-80%)

**📋 Input Classification Results**
- How your inputs were classified
- Visual cards showing Scale, Budget, and Power categories

**🔍 Explain Decision** (Important for understanding!)
- Which rule was applied
- Why other topologies weren't selected
- Plain-English explanation

**📈 Analysis & Visualization**
- Network topology diagram (NetworkX graph)
- Score comparison chart
- Score breakdown for recommended topology

**📊 Topology Comparison**
- Side-by-side comparison table
- Detailed score breakdown for all topologies
- Scoring weights used

---

## Understanding the Results

### Topology Types Explained

#### Three-Tier Topology

**Best For:**
- Small deployments (< 20 racks)
- Cost-sensitive projects
- Traditional workloads

**Characteristics:**
- ✅ Simple and easy to manage
- ✅ Cost-effective
- ✅ Good for hierarchical traffic
- ❌ Limited scalability
- ❌ Higher latency for east-west traffic

**Typical Use Cases:**
- Small data centers
- Legacy infrastructure
- Budget-constrained deployments

#### Leaf-Spine Topology

**Best For:**
- Medium to large deployments
- Modern cloud workloads
- Most common use case

**Characteristics:**
- ✅ Excellent scalability
- ✅ Low latency (equal-cost multipath)
- ✅ Industry standard
- ✅ Good for east-west traffic
- ❌ More complex than Three-Tier
- ❌ Higher cost than Three-Tier

**Typical Use Cases:**
- Cloud computing
- Virtualized environments
- Enterprise data centers

#### Fat-Tree Topology

**Best For:**
- Large-scale deployments (> 100 racks)
- High-performance computing
- AI/ML training clusters

**Characteristics:**
- ✅ Maximum scalability
- ✅ Optimal bandwidth
- ✅ Best for HPC workloads
- ❌ Highest cost
- ❌ Complex to manage
- ❌ Requires significant power

**Typical Use Cases:**
- HPC clusters
- AI/ML training
- Scientific computing

### Understanding Scores

**Score Range:** 0.0 to 1.0 (higher is better)

**Example Score Breakdown:**
```
Topology: Leaf-Spine
Scale Score: 0.80 (30% weight) = 0.24
Budget Score: 0.90 (25% weight) = 0.225
Power Score: 0.75 (20% weight) = 0.15
Workload Score: 0.85 (15% weight) = 0.1275
Scalability Score: 0.95 (10% weight) = 0.095
─────────────────────────────────────────
Total Score: 0.8425
```

**What the scores mean:**
- **0.8-1.0:** Excellent match
- **0.6-0.8:** Good match
- **0.4-0.6:** Moderate match
- **0.0-0.4:** Poor match

### Understanding the Decision Explanation

The "Explain Decision" section shows:

1. **Rule Applied:** Which of the three rules fired
2. **Conditions:** What conditions triggered the rule
3. **Why Not Others:** Why other topologies weren't selected
4. **Plain-English Summary:** Easy-to-understand explanation

**Example:**
```
Rule Applied: Rule #1
Conditions:
  ✓ Scale is Small
  ✓ Budget is Low

Why Other Topologies Were Not Selected:
  Leaf-Spine: Too complex and expensive for small scale deployment
  Fat-Tree: Requires large scale, high budget, and high power
```

---

## Project Structure

```
dc_topology_planner/
│
├── app.py                          # Main Streamlit application (entry point)
│
├── core/                           # Core business logic
│   ├── __init__.py
│   ├── models.py                   # Data models, enums, dataclasses
│   ├── config.py                   # Configuration (thresholds, parameters)
│   ├── decision_engine.py          # Rule-based decision logic
│   ├── scoring.py                  # Weighted scoring system
│   └── topology.py                 # Topology definitions and characteristics
│
├── visualization/                  # Visualization modules
│   ├── __init__.py
│   ├── graphs.py                   # NetworkX topology diagrams
│   └── charts.py                   # Matplotlib charts and plots
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── validators.py               # Input validation
│
├── data/                           # Data files
│   └── sample_inputs.json          # Example input configurations
│
├── venv/                           # Virtual environment (don't edit)
│
├── requirements.txt                # Python dependencies
├── run.bat                         # Quick start script (Windows)
├── README.md                       # Project overview
└── SETUP_GUIDE.md                  # This file
```

### Key Files Explained

**app.py**
- Main application entry point
- Streamlit UI components
- User interaction handling
- Results display

**core/models.py**
- `UserInputs`: User input data structure
- `WorkloadType`: Enum for workload types
- `TopologyType`: Enum for topology types
- `ClassificationResult`: Classification output
- `TopologyRecommendation`: Final recommendation structure

**core/config.py**
- `SCALE_THRESHOLDS`: Scale classification thresholds
- `BUDGET_THRESHOLDS`: Budget classification thresholds
- `POWER_THRESHOLDS`: Power classification thresholds
- **Modify these to adjust classification logic**

**core/decision_engine.py**
- `classify_inputs()`: Classifies user inputs
- `suggest_topology_by_rules()`: Applies rule-based logic
- `explain_rule_application()`: Generates explanations
- `generate_explanation()`: Creates plain-English explanations

**core/scoring.py**
- `SCORING_WEIGHTS`: Weight configuration
- `calculate_topology_score()`: Calculates weighted scores
- `rank_topologies()`: Ranks all topologies by score
- **Modify SCORING_WEIGHTS to adjust scoring**

**core/topology.py**
- Topology characteristics and definitions
- Comparison data
- Use case information

**visualization/graphs.py**
- `draw_topology_graph()`: Creates NetworkX diagrams
- Topology-specific graph generators

**visualization/charts.py**
- `create_comparison_dataframe()`: Comparison table
- `create_score_comparison_chart()`: Score bar chart
- `create_score_breakdown_chart()`: Score breakdown pie chart

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "streamlit is not recognized"

**Symptoms:**
```
'streamlit' is not recognized as an internal or external command
```

**Solution:**
1. Make sure virtual environment is activated (you should see `(venv)` in prompt)
2. If not activated:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```
3. Verify streamlit is installed:
   ```bash
   pip list | findstr streamlit  # Windows
   pip list | grep streamlit  # Mac/Linux
   ```
4. If not installed:
   ```bash
   pip install -r requirements.txt
   ```

#### Issue 2: "No module named 'core'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'core'
```

**Solution:**
1. Make sure you're in the project root directory:
   ```bash
   cd C:\Users\YourName\Desktop\dc_topology_planner
   ```
2. Verify you're in the right folder:
   ```bash
   dir  # Windows (should see app.py, core/, etc.)
   ls   # Mac/Linux
   ```
3. Run from the project root:
   ```bash
   streamlit run app.py
   ```

#### Issue 3: Port 8501 Already in Use

**Symptoms:**
```
Port 8501 is already in use
```

**Solution:**
1. Use a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```
2. Or stop the other application using port 8501
3. Or find and kill the process:
   ```bash
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <process_id> /F
   
   # Mac/Linux
   lsof -ti:8501 | xargs kill
   ```

#### Issue 4: Virtual Environment Not Found

**Symptoms:**
```
The system cannot find the path specified
```

**Solution:**
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Issue 5: Import Errors After Installation

**Symptoms:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution:**
1. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
2. Verify Python version:
   ```bash
   python --version  # Should be 3.11+
   ```
3. Check for conflicting packages:
   ```bash
   pip list
   ```

#### Issue 6: Browser Doesn't Open Automatically

**Symptoms:**
App runs but browser doesn't open

**Solution:**
1. Manually open browser
2. Go to: `http://localhost:8501`
3. Check terminal for the exact URL (might be different port)

#### Issue 7: Dropdown Text Not Visible

**Symptoms:**
Workload Type dropdown text is invisible

**Solution:**
1. This is a known UI issue with Streamlit's BaseWeb components
2. The app includes JavaScript fixes that should resolve this
3. Try refreshing the page (F5)
4. If still not visible, check browser console for errors

#### Issue 8: Visualization Not Showing

**Symptoms:**
Charts or graphs don't appear

**Solution:**
1. Check browser console for errors (F12)
2. Verify matplotlib is installed:
   ```bash
   pip list | findstr matplotlib
   ```
3. Try clearing browser cache
4. Check terminal for error messages

### Getting Help

If you're still stuck:

1. **Check the terminal/command prompt** for error messages
2. **Check browser console** (F12 → Console tab) for JavaScript errors
3. **Verify all files are present** in the project folder
4. **Try reinstalling dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall --no-cache-dir
   ```
5. **Check Python version:**
   ```bash
   python --version  # Must be 3.11+
   ```

---

## Advanced Configuration

### Modifying Classification Thresholds

Edit `core/config.py`:

```python
SCALE_THRESHOLDS = {
    "small_max_racks": 20,      # Change this
    "small_max_servers": 200,   # Change this
    "large_min_racks": 100,     # Change this
    "large_min_servers": 1000,   # Change this
}

BUDGET_THRESHOLDS = {
    "low_max": 100000,    # Change this
    "high_min": 500000,   # Change this
}

POWER_THRESHOLDS = {
    "low_max": 50,     # Change this
    "high_min": 200,   # Change this
}
```

**After changes, restart the app.**

### Modifying Scoring Weights

Edit `core/scoring.py`:

```python
SCORING_WEIGHTS = {
    "scale_match": 0.30,        # Change this (must sum to 1.0)
    "budget_match": 0.25,       # Change this
    "power_match": 0.20,        # Change this
    "workload_suitability": 0.15,  # Change this
    "scalability_match": 0.10,  # Change this
}
```

**Important:** Weights must sum to 1.0!

**After changes, restart the app.**

### Adding New Topologies

1. Add to `TopologyType` enum in `core/models.py`
2. Add characteristics in `core/topology.py`
3. Update decision rules in `core/decision_engine.py`
4. Add scoring logic in `core/scoring.py`
5. Create graph generator in `visualization/graphs.py`
6. Update UI in `app.py`

### Changing Port Number

**Temporary:**
```bash
streamlit run app.py --server.port 8502
```

**Permanent:** Create `.streamlit/config.toml`:
```toml
[server]
port = 8502
```

---

## Quick Reference

### Essential Commands

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Check Python version
python --version

# Check installed packages
pip list

# Deactivate virtual environment
deactivate
```

### File Locations

- **Main app:** `app.py`
- **Configuration:** `core/config.py`
- **Scoring weights:** `core/scoring.py`
- **Decision logic:** `core/decision_engine.py`
- **Dependencies:** `requirements.txt`

### Important URLs

- **Local app:** `http://localhost:8501`
- **Streamlit docs:** https://docs.streamlit.io/

---

## Summary

This system is a **decision-support tool** that helps you choose the right data center network topology based on your requirements. It uses:

- ✅ **Rule-based logic** for primary recommendations
- ✅ **Weighted scoring** for secondary analysis
- ✅ **Visualizations** for understanding
- ✅ **Detailed explanations** for transparency

**Remember:** This is NOT a network simulator. It's a decision-support system that uses heuristics and expert knowledge to make recommendations.

---

## Support

For questions or issues:
1. Check this guide first
2. Review the README.md
3. Check the code comments in relevant files
4. Verify your Python version and dependencies

**Good luck with your data center planning!** 🚀
