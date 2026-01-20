"""
Data Center Network Topology Planner

A decision-support system for selecting optimal network topologies
based on scale, budget, power, and workload requirements.
"""

import streamlit as st
import pandas as pd
from typing import Optional

# Core modules
from core.models import (
    UserInputs,
    WorkloadType,
    TopologyType,
    TopologyRecommendation
)
from core.decision_engine import (
    classify_inputs,
    suggest_topology_by_rules,
    generate_explanation,
    explain_rule_application
)
from core.scoring import rank_topologies
from core.topology import get_topology_characteristics, get_topology_comparison
from utils.validators import validate_all_inputs
from visualization.graphs import draw_topology_graph
from visualization.charts import (
    create_comparison_dataframe,
    create_score_comparison_chart,
    create_score_breakdown_chart
)


# Page configuration
st.set_page_config(
    page_title="DC Topology Planner",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Optimized CSS for maximum visibility
st.markdown("""
<style>
/* FORCE LIGHT THEME - ESSENTIAL STYLES ONLY */

/* GLOBAL OVERRIDES - FORCE LIGHT THEME */
* {
    color: #000000 !important;
}

html, body {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stApp {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.main {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.block-container {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* HEADERS - ALL LEVELS */
h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

h1 {
    border-bottom: 2px solid #2E86AB !important;
    padding-bottom: 12px !important;
    margin-bottom: 15px !important;
}

h2 {
    color: #2E86AB !important;
    border-left: 3px solid #2E86AB !important;
    padding-left: 10px !important;
    margin-top: 25px !important;
    margin-bottom: 15px !important;
}

h3 {
    color: #4a4a4a !important;
    margin-top: 15px !important;
}

h4 {
    color: #495057 !important;
}

/* TEXT ELEMENTS - COMPREHENSIVE */
p, span, div, label, li, td, th, a, em, strong, b, i, small, code {
    color: #000000 !important;
}

.stMarkdown, .stMarkdown * {
    color: #000000 !important;
}

.stText, .stText * {
    color: #000000 !important;
}

/* LABELS - ALL INPUT TYPES */
label, .stLabel, [data-testid*="label"] {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label,
.stDateInput label,
.stTimeInput label,
.stFileUploader label,
.stColorPicker label,
.stSlider label,
.stCheckbox label,
.stRadio label,
.stMultiSelect label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* INPUT FIELDS - ALL TYPES */
input, textarea, select {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #ced4da !important;
    border-radius: 4px !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #ced4da !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #2E86AB !important;
    box-shadow: 0 0 0 2px rgba(46, 134, 171, 0.15) !important;
    color: #000000 !important;
}

/* SELECTBOX - ULTRA COMPREHENSIVE FIX */
.stSelectbox {
    color: #000000 !important;
}

.stSelectbox > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stSelectbox [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stSelectbox [data-baseweb="select"] > div > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stSelectbox [data-baseweb="select"] span {
    color: #000000 !important;
}

.stSelectbox [data-baseweb="select"] div {
    color: #000000 !important;
}

/* DROPDOWN MENUS */
[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

[data-baseweb="popover"] * {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] [role="menuitem"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] li:hover {
    background-color: #e7f3ff !important;
    color: #000000 !important;
}

[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="menu"] li {
    color: #000000 !important;
}

/* BUTTONS - ALL STATES */
.stButton > button {
    background-color: #2E86AB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 12px 28px !important;
    font-weight: 500 !important;
    font-size: 15px !important;
}

.stButton > button:hover {
    background-color: #1e5f7a !important;
    color: #FFFFFF !important;
}

/* NUMBER INPUT +/- BUTTONS */
.stNumberInput button {
    background-color: #333333 !important;
    color: #FFFFFF !important;
    border: 1px solid #555555 !important;
    border-radius: 3px !important;
}

.stNumberInput button:hover {
    background-color: #dc3545 !important;
    color: #FFFFFF !important;
}

.stNumberInput button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

.stButton > button:focus {
    background-color: #1e5f7a !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="secondary"] {
    background-color: #6c757d !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="secondary"]:hover {
    background-color: #545b62 !important;
    color: #FFFFFF !important;
}

/* EXPANDERS */
.streamlit-expanderHeader {
    background-color: #f8f9fa !important;
    color: #2E86AB !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
}

.streamlit-expanderHeader * {
    color: #2E86AB !important;
}

.streamlit-expanderHeader p {
    color: #2E86AB !important;
    font-weight: 500 !important;
}

.streamlit-expanderHeader span {
    color: #2E86AB !important;
}

.streamlit-expanderHeader svg {
    color: #2E86AB !important;
    fill: #2E86AB !important;
}

.streamlit-expanderContent {
    background-color: #FFFFFF !important;
    border: 1px solid #dee2e6 !important;
    border-top: none !important;
    padding: 18px !important;
}

.streamlit-expanderContent * {
    color: #000000 !important;
}

.streamlit-expanderContent p,
.streamlit-expanderContent li,
.streamlit-expanderContent div,
.streamlit-expanderContent span {
    color: #000000 !important;
}

/* METRICS */
[data-testid="stMetricValue"] {
    color: #2E86AB !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #495057 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

[data-testid="stMetricDelta"] {
    color: #495057 !important;
}

/* HELP/INFO ICONS */
[data-testid="stTooltipIcon"] {
    background-color: #e9ecef !important;
    border: 1px solid #ced4da !important;
    border-radius: 50% !important;
    color: #000000 !important;
    width: 20px !important;
    height: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 12px !important;
    font-weight: bold !important;
}

[data-testid="stTooltipIcon"]:before {
    content: "i" !important;
    color: #000000 !important;
    font-style: italic !important;
    font-weight: bold !important;
}

[data-testid="stTooltipIcon"] svg {
    display: none !important;
}

/* Alternative tooltip icon selectors */
.stTooltip [data-testid="stTooltipIcon"],
.element-container [data-testid="stTooltipIcon"],
[role="button"][aria-label*="help"] {
    background-color: #e9ecef !important;
    border: 1px solid #ced4da !important;
    border-radius: 50% !important;
    color: #000000 !important;
}

/* ALERT BOXES */
.stAlert, [data-testid="stAlert"] {
    color: #000000 !important;
}

.stAlert *, [data-testid="stAlert"] * {
    color: #000000 !important;
}

.stInfo {
    background-color: #e7f3ff !important;
    border-left: 4px solid #2E86AB !important;
}

.stInfo * {
    color: #0c5460 !important;
}

.stSuccess {
    background-color: #d4edda !important;
}

.stSuccess * {
    color: #155724 !important;
}

.stWarning {
    background-color: #fff3cd !important;
}

.stWarning * {
    color: #856404 !important;
}

.stError {
    background-color: #f8d7da !important;
}

.stError * {
    color: #721c24 !important;
}

/* DATAFRAMES AND TABLES */
.stDataFrame, [data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}

.stTable {
    background-color: #FFFFFF !important;
}

table {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

table th {
    background-color: #2E86AB !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

table td {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

table tr {
    background-color: #FFFFFF !important;
}

table tr:nth-child(even) {
    background-color: #f8f9fa !important;
}

/* CAPTIONS */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #6c757d !important;
}

.stCaption * {
    color: #6c757d !important;
}

/* SIDEBAR */
.css-1d391kg, .css-1cypcdb {
    background-color: #FFFFFF !important;
}

.sidebar .sidebar-content {
    background-color: #FFFFFF !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FFFFFF !important;
}

.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86AB !important;
    background-color: #FFFFFF !important;
}

/* MULTISELECT */
.stMultiSelect {
    color: #000000 !important;
}

.stMultiSelect [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stMultiSelect span {
    color: #000000 !important;
}

.stMultiSelect [data-baseweb="tag"] {
    background-color: #e7f3ff !important;
    color: #000000 !important;
}

/* CHECKBOX AND RADIO */
.stCheckbox {
    color: #000000 !important;
}

.stRadio {
    color: #000000 !important;
}

.stCheckbox > label {
    color: #000000 !important;
}

.stRadio > label {
    color: #000000 !important;
}

/* SLIDER */
.stSlider {
    color: #000000 !important;
}

.stSlider > label {
    color: #000000 !important;
}

/* FILE UPLOADER */
.stFileUploader {
    color: #000000 !important;
}

.stFileUploader > label {
    color: #000000 !important;
}

[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
}

/* DATE AND TIME INPUTS */
.stDateInput {
    color: #000000 !important;
}

.stTimeInput {
    color: #000000 !important;
}

.stDateInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.stTimeInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* COLOR PICKER */
.stColorPicker {
    color: #000000 !important;
}

.stColorPicker > label {
    color: #000000 !important;
}

/* SPINNER */
.stSpinner {
    color: #2E86AB !important;
}

.stSpinner > div {
    color: #2E86AB !important;
}

/* TOOLTIPS */
[data-testid="stTooltipIcon"] {
    color: #6c757d !important;
}

/* PROGRESS BAR */
.stProgress > div > div {
    background-color: #2E86AB !important;
}

/* JSON */
.stJson {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* CODE BLOCKS */
.stCode {
    background-color: #f8f9fa !important;
    color: #000000 !important;
}

code {
    background-color: #f8f9fa !important;
    color: #e83e8c !important;
    padding: 2px 6px !important;
    border-radius: 3px !important;
}

pre {
    background-color: #f8f9fa !important;
    color: #000000 !important;
}

/* LINKS */
a, a:visited, a:hover {
    color: #2E86AB !important;
}

/* STRONG AND EMPHASIS */
strong, b {
    color: inherit !important;
    font-weight: 600 !important;
}

em, i {
    color: inherit !important;
}

/* DIVIDERS */
hr {
    border-color: #dee2e6 !important;
    margin: 30px 0 !important;
}

/* PLOTLY CHARTS */
.js-plotly-plot {
    background-color: #FFFFFF !important;
}

/* MATPLOTLIB FIGURES */
.stPlotlyChart {
    background-color: #FFFFFF !important;
}

/* HIDE STREAMLIT BRANDING */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stDeployButton {visibility: hidden !important;}

/* SCROLLBARS */
::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
}

::-webkit-scrollbar-track {
    background: #f1f1f1 !important;
}

::-webkit-scrollbar-thumb {
    background: #2E86AB !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #1e5f7a !important;
}

/* CONTAINER SPACING */
.element-container {
    margin-bottom: 1.5rem !important;
}

/* CUSTOM CARDS */
.metric-card {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    padding: 20px !important;
    border-radius: 8px !important;
    border: 1px solid #dee2e6 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

/* FORCE VISIBILITY FOR ANY MISSED ELEMENTS */
[class*="st"] {
    color: #000000 !important;
}

[data-testid*="st"] {
    color: #000000 !important;
}

/* DATAFRAME CONTROLS - SHOW/HIDE COLUMNS BUTTON */
[data-testid="stDataFrameResizeHandle"] {
    color: #FFFFFF !important;
    background-color: #2E86AB !important;
}

[data-testid="stDataFrame"] button {
    background-color: #2E86AB !important;
    color: #FFFFFF !important;
    border: none !important;
}

[data-testid="stDataFrame"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

[data-testid="stDataFrame"] [role="button"] {
    background-color: #2E86AB !important;
    color: #FFFFFF !important;
}

[data-testid="stDataFrame"] [role="button"] svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* DATAFRAME TOOLBAR BUTTONS */
.dataframe-toolbar button,
.dataframe-controls button,
[class*="dataframe"] button {
    background-color: #2E86AB !important;
    color: #FFFFFF !important;
}

[class*="dataframe"] button svg,
.dataframe-toolbar button svg,
.dataframe-controls button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* GENERIC ICON FIXES */
svg {
    fill: currentColor !important;
    stroke: currentColor !important;
}

button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* FULLSCREEN BUTTON - BLACK BACKGROUND, WHITE ICON */
[data-testid="stFullScreenFrame"] button,
[title="View fullscreen"],
[aria-label="View fullscreen"],
button[title*="fullscreen"],
button[aria-label*="fullscreen"],
.stPlotlyChart button,
.element-container button[title*="View"],
[data-testid="stPlotlyChart"] button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 4px !important;
    padding: 4px !important;
}

[data-testid="stFullScreenFrame"] button svg,
[title="View fullscreen"] svg,
[aria-label="View fullscreen"] svg,
button[title*="fullscreen"] svg,
button[aria-label*="fullscreen"] svg,
.stPlotlyChart button svg,
.element-container button[title*="View"] svg,
[data-testid="stPlotlyChart"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* CHART CONTROL BUTTONS */
.js-plotly-plot .modebar {
    background-color: rgba(0, 0, 0, 0.8) !important;
}

.js-plotly-plot .modebar-btn {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
}

.js-plotly-plot .modebar-btn svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

.js-plotly-plot .modebar-btn:hover {
    background-color: #333333 !important;
}

/* MATPLOTLIB TOOLBAR BUTTONS */
.toolbar button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
}

.toolbar button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* STREAMLIT CONTROL BUTTONS */
[data-testid*="button"] svg,
[data-testid*="Button"] svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* ULTIMATE FALLBACK */
div, span, p, label, input, textarea, select, button, a, li, td, th {
    color: #000000 !important;
}
</style>

<script>
// Simplified JavaScript fix
function fixVisibility() {
    // Fix selectboxes
    document.querySelectorAll('[data-baseweb="select"] *').forEach(el => {
        el.style.setProperty('color', '#000000', 'important');
        el.style.setProperty('background-color', '#FFFFFF', 'important');
    });
    
    // Fix dropdowns
    document.querySelectorAll('[data-baseweb="popover"] *').forEach(el => {
        el.style.setProperty('color', '#000000', 'important');
        el.style.setProperty('background-color', '#FFFFFF', 'important');
    });
    
    // Fix number input +/- buttons
    document.querySelectorAll('.stNumberInput button').forEach(button => {
        button.style.setProperty('background-color', '#333333', 'important');
        button.style.setProperty('color', '#FFFFFF', 'important');
        button.style.setProperty('border', '1px solid #555555', 'important');
        
        // Add hover effect
        button.addEventListener('mouseenter', function() {
            this.style.setProperty('background-color', '#dc3545', 'important');
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.setProperty('background-color', '#333333', 'important');
        });
        
        const svg = button.querySelector('svg');
        if (svg) {
            svg.style.setProperty('fill', '#FFFFFF', 'important');
            svg.style.setProperty('stroke', '#FFFFFF', 'important');
            svg.style.setProperty('color', '#FFFFFF', 'important');
        }
    });
    
    // Fix help/info icons
    document.querySelectorAll('[data-testid="stTooltipIcon"]').forEach(icon => {
        icon.style.setProperty('background-color', '#e9ecef', 'important');
        icon.style.setProperty('border', '1px solid #ced4da', 'important');
        icon.style.setProperty('border-radius', '50%', 'important');
        icon.style.setProperty('color', '#000000', 'important');
        icon.style.setProperty('width', '20px', 'important');
        icon.style.setProperty('height', '20px', 'important');
        icon.style.setProperty('display', 'flex', 'important');
        icon.style.setProperty('align-items', 'center', 'important');
        icon.style.setProperty('justify-content', 'center', 'important');
        icon.style.setProperty('font-size', '12px', 'important');
        icon.style.setProperty('font-weight', 'bold', 'important');
        
        // Hide the SVG and add text "i"
        const svg = icon.querySelector('svg');
        if (svg) {
            svg.style.display = 'none';
        }
        
        // Add "i" text if not already present
        if (!icon.textContent || icon.textContent.trim() === '') {
            icon.textContent = 'i';
            icon.style.setProperty('font-style', 'italic', 'important');
        }
    });
    
    // Fix control button icons
    document.querySelectorAll('button svg').forEach(svg => {
        const button = svg.closest('button');
        if (button && (button.title?.includes('fullscreen') || button.closest('[data-testid="stDataFrame"]'))) {
            svg.style.setProperty('fill', '#FFFFFF', 'important');
            svg.style.setProperty('stroke', '#FFFFFF', 'important');
        }
    });
}

// Run fix
fixVisibility();
setTimeout(fixVisibility, 500);
new MutationObserver(fixVisibility).observe(document.body, { childList: true, subtree: true });
document.addEventListener('click', () => setTimeout(fixVisibility, 50));
setInterval(fixVisibility, 2000);
</script>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'recommendation' not in st.session_state:
        st.session_state.recommendation = None
    if 'inputs' not in st.session_state:
        st.session_state.inputs = None


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header with clean minimal styling
    st.markdown("""
    <div style='padding: 20px 0; margin-bottom: 30px; border-bottom: 2px solid #e9ecef;'>
        <h1 style='color: #1a1a1a; margin: 0; padding: 0; border: none; font-size: 2rem; font-weight: 600;'>
            🌐 Adaptive Topology Selection in Data Center Networks
        </h1>
        <p style='color: #6c757d; margin-top: 8px; font-size: 1rem; margin-bottom: 0;'>
            Academic Decision-Support System for Network Topology Planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Reset button in header area
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🔄 Reset All", use_container_width=True, type="secondary"):
            st.session_state.recommendation = None
            st.session_state.inputs = None
            st.session_state.rule_explanation = None
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input Section with clean minimal layout
    st.markdown("""
    <div style='margin-bottom: 25px;'>
        <h2 style='margin-top: 0; padding-left: 8px; border-left: 3px solid #2E86AB; color: #2E86AB; font-size: 1.5rem;'>
            📊 Input Parameters
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 Enter Data Center Requirements", expanded=True):
        st.markdown("""
        <p style='color: #495057; font-size: 14px; margin-bottom: 20px;'>
            Please provide the following information about your data center deployment:
        </p>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p style='color: #495057; font-weight: 600; font-size: 14px; margin-bottom: 12px;'>
                Infrastructure Scale
            </p>
            """, unsafe_allow_html=True)
            racks = st.number_input(
                "Number of Racks",
                min_value=1,
                max_value=10000,
                value=12,
                step=1,
                help="Total number of server racks in the data center",
                key="racks_input"
            )
            
            servers = st.number_input(
                "Number of Servers",
                min_value=1,
                max_value=1000000,
                value=480,
                step=1,
                help="Total number of servers to be deployed",
                key="servers_input"
            )
        
        with col2:
            st.markdown("""
            <p style='color: #495057; font-weight: 600; font-size: 14px; margin-bottom: 12px;'>
                Resource Constraints
            </p>
            """, unsafe_allow_html=True)
            budget_usd = st.number_input(
                "Budget (USD)",
                min_value=0.0,
                max_value=1000000000.0,
                value=250000.0,
                step=10000.0,
                format="%.0f",
                help="Total budget available for network infrastructure",
                key="budget_input"
            )
            
            power_kw = st.number_input(
                "Power Limit (kW)",
                min_value=0.1,
                max_value=100000.0,
                value=30.0,
                step=1.0,
                format="%.1f",
                help="Maximum power consumption limit in kilowatts",
                key="power_input"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
         <p style='color: #495057; font-weight: 600; font-size: 14px; margin-bottom: 12px;'>
             Workload Configuration
         </p>
         """, unsafe_allow_html=True)
        workload_type = st.selectbox(
            "**Workload Type**",
            options=[wt.value for wt in WorkloadType],
            help="Type of workload that will run on the infrastructure",
            key="workload_input"
        )
        
        # Validation
        is_valid, error_msg = validate_all_inputs(racks, servers, budget_usd, power_kw)
        
        if not is_valid:
            st.error(f"❌ Validation Error: {error_msg}")
            return
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Process inputs with improved button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze & Recommend Topology", type="primary", use_container_width=True):
                try:
                    inputs = UserInputs(
                        racks=int(racks),
                        servers=int(servers),
                        budget_usd=float(budget_usd),
                        power_kw=float(power_kw),
                        workload_type=WorkloadType(workload_type)
                    )
                    
                    # Classify inputs
                    classification = classify_inputs(inputs)
                    
                    # Rule-based recommendation
                    rule_topology = suggest_topology_by_rules(classification)
                    
                    # Scoring-based ranking
                    scores = rank_topologies(inputs, classification)
                    
                    # Get top-scoring topology
                    scored_topology = scores[0].topology
                    
                    # Use rule-based if it matches top score, otherwise use top score
                    # (Rule-based takes precedence as per requirements)
                    final_topology = rule_topology
                    confidence = 0.8 if rule_topology == scored_topology else 0.7
                    
                    # Generate explanation
                    explanation = generate_explanation(final_topology, classification, rule_based=True)
                    
                    # Get rule explanation for explainability
                    rule_explanation = explain_rule_application(classification)
                    
                    # Create recommendation
                    recommendation = TopologyRecommendation(
                        topology=final_topology,
                        confidence=confidence,
                        explanation=explanation,
                        scores=scores,
                        classification=classification
                    )
                    
                    st.session_state.recommendation = recommendation
                    st.session_state.inputs = inputs
                    st.session_state.rule_explanation = rule_explanation
                    
                except Exception as e:
                    st.error(f"❌ Error processing inputs: {str(e)}")
                    return
    
    # Display results if available
    if st.session_state.recommendation is not None:
        recommendation = st.session_state.recommendation
        inputs = st.session_state.inputs
        
        st.markdown("---")
        
        # Recommendation Section - Clean minimal design
        st.markdown("""
        <div style='margin-bottom: 25px;'>
            <h2 style='margin-top: 0; padding-left: 8px; border-left: 3px solid #2E86AB; color: #2E86AB; font-size: 1.5rem;'>
                🎯 Topology Recommendation
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Highlight recommended topology - Clean card design
        st.markdown(f"""
        <div style='background-color: #ffffff; 
                    padding: 20px; 
                    border-radius: 4px; 
                    border: 1px solid #28a745;
                    margin-bottom: 20px;'>
            <h3 style='color: #28a745; margin-top: 0; font-size: 1.3rem; font-weight: 600;'>
                ✅ Recommended: {recommendation.topology.value}
            </h3>
            <p style='font-size: 15px; color: #495057; margin-bottom: 0;'>
                <strong>Confidence:</strong> <span style='color: #28a745; font-weight: 600;'>{recommendation.confidence:.0%}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics in a row
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            st.metric("Scale Classification", recommendation.classification.scale.value)
        
        with rec_col2:
            st.metric("Budget Classification", recommendation.classification.budget.value)
        
        with rec_col3:
            st.metric("Power Classification", recommendation.classification.power.value)
        
        # Classification Results (Prominently Displayed) with enhanced cards
        st.subheader("📋 Input Classification Results")
        st.markdown("**Your inputs have been classified into the following categories:**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        class_col1, class_col2, class_col3 = st.columns(3)
        with class_col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e7f3ff 0%, #d0e7ff 100%); 
                        padding: 20px; 
                        border-radius: 8px; 
                        border-left: 5px solid #2E86AB;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 100%;'>
                <h4 style='margin: 0 0 10px 0; color: #2E86AB; font-size: 16px;'>📏 Scale Classification</h4>
                <p style='font-size: 24px; font-weight: 700; margin: 15px 0; color: #1e5f7a;'>{recommendation.classification.scale.value}</p>
                <p style='font-size: 13px; color: #666; margin: 0; line-height: 1.5;'>
                    <strong>Based on:</strong><br>
                    {inputs.racks} racks<br>
                    {inputs.servers} servers
                </p>
            </div>
            """, unsafe_allow_html=True)
        with class_col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fff4e6 0%, #ffe8cc 100%); 
                        padding: 20px; 
                        border-radius: 8px; 
                        border-left: 5px solid #F77F00;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 100%;'>
                <h4 style='margin: 0 0 10px 0; color: #F77F00; font-size: 16px;'>💰 Budget Classification</h4>
                <p style='font-size: 24px; font-weight: 700; margin: 15px 0; color: #cc6600;'>{recommendation.classification.budget.value}</p>
                <p style='font-size: 13px; color: #666; margin: 0; line-height: 1.5;'>
                    <strong>Budget:</strong><br>
                    ${inputs.budget_usd:,.0f} USD
                </p>
            </div>
            """, unsafe_allow_html=True)
        with class_col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                        padding: 20px; 
                        border-radius: 8px; 
                        border-left: 5px solid #06B6D4;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 100%;'>
                <h4 style='margin: 0 0 10px 0; color: #06B6D4; font-size: 16px;'>⚡ Power Classification</h4>
                <p style='font-size: 24px; font-weight: 700; margin: 15px 0; color: #0891b2;'>{recommendation.classification.power.value}</p>
                <p style='font-size: 13px; color: #666; margin: 0; line-height: 1.5;'>
                    <strong>Power Limit:</strong><br>
                    {inputs.power_kw:.1f} kW
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Explain Decision Section (MANDATORY for viva)
        st.markdown("""
        <div style='background-color: #ffffff; 
                    padding: 20px; 
                    border-radius: 8px; 
                    border: 1px solid #dee2e6;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    margin-bottom: 20px;'>
            <h2 style='margin-top: 0; padding-left: 0; border-left: none; color: #2E86AB;'>
                🔍 Explain Decision
            </h2>
            <p style='color: #6c757d; margin-bottom: 0;'>
                Detailed explanation of the decision-making process for academic evaluation
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📖 Decision Logic Explanation", expanded=True):
            rule_expl = st.session_state.get('rule_explanation', {})
            
            if rule_expl:
                st.markdown("""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2E86AB;'>
                    <h3 style='color: #2E86AB; margin-top: 0; font-weight: 600;'>Rule-Based Decision Process</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Show which rule fired
                st.markdown(f"""
                <div style='background-color: #e7f3ff; padding: 15px; border-radius: 6px; margin-bottom: 15px;'>
                    <p style='color: #212529; margin: 0; font-size: 15px;'>
                        <strong style='color: #2E86AB;'>Rule Applied:</strong> 
                        <span style='color: #212529; font-weight: 600;'>Rule #{rule_expl.get('fired_rule', 'N/A')}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show conditions
                conditions = rule_expl.get('rule_conditions', [])
                if conditions:
                    st.markdown("""
                    <p style='color: #212529; font-weight: 600; font-size: 15px; margin-bottom: 10px;'>
                        Conditions that triggered this rule:
                    </p>
                    """, unsafe_allow_html=True)
                    for condition in conditions:
                        st.markdown(f"""
                        <div style='background-color: #ffffff; padding: 10px 15px; border-radius: 5px; margin-bottom: 8px; border-left: 3px solid #28a745;'>
                            <p style='color: #212529; margin: 0; font-size: 14px;'>
                                ✓ <strong style='color: #212529;'>{condition}</strong>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Why other topologies were not selected
                st.markdown("""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #F77F00;'>
                    <h3 style='color: #F77F00; margin-top: 0; font-weight: 600;'>Why Other Topologies Were Not Selected</h3>
                </div>
                """, unsafe_allow_html=True)
                why_not = rule_expl.get('why_not_others', {})
                for topology_name, reason in why_not.items():
                    st.markdown(f"""
                    <div style='background-color: #ffffff; padding: 15px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #dee2e6;'>
                        <p style='color: #212529; margin: 0 0 8px 0; font-weight: 600; font-size: 15px;'>
                            <strong style='color: #2E86AB;'>{topology_name}:</strong>
                        </p>
                        <p style='color: #495057; margin: 0; font-size: 14px; line-height: 1.6;'>
                            {reason}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;'>
                <h3 style='color: #28a745; margin-top: 0; font-weight: 600;'>Plain-English Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background-color: #ffffff; padding: 20px; border-radius: 6px; border: 1px solid #dee2e6;'>
                <p style='color: #212529; margin: 0; font-size: 15px; line-height: 1.7;'>
                    {recommendation.explanation}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Topology Characteristics
        characteristics = get_topology_characteristics(recommendation.topology)
        
        with st.expander("📋 Topology Characteristics", expanded=False):
            st.markdown(f"**Description:** {characteristics.description}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Advantages:**")
                for adv in characteristics.advantages:
                    st.markdown(f"- {adv}")
            
            with col2:
                st.markdown("**Disadvantages:**")
                for disadv in characteristics.disadvantages:
                    st.markdown(f"- {disadv}")
            
            st.markdown("**Typical Use Cases:**")
            for use_case in characteristics.typical_use_cases:
                st.markdown(f"- {use_case}")
        
        st.markdown("---")
        
        # Visualization Section
        st.markdown("""
        <div style='background-color: #ffffff; 
                    padding: 20px; 
                    border-radius: 8px; 
                    border: 1px solid #dee2e6;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    margin-bottom: 20px;'>
            <h2 style='margin-top: 0; padding-left: 0; border-left: none; color: #2E86AB;'>
                📈 Analysis & Visualization
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Topology Graph
        st.subheader("Network Topology Diagram")
        st.caption("**Note:** These diagrams are logical abstractions showing network structure, not physical hardware layouts. They represent the connectivity patterns and hierarchical relationships between network layers.")
        with st.spinner("Generating topology diagram..."):
            fig = draw_topology_graph(recommendation.topology, inputs.racks)
            st.pyplot(fig, use_container_width=True)
        
        # Score Comparison
        st.subheader("Topology Score Comparison")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            score_fig = create_score_comparison_chart(recommendation.scores)
            st.pyplot(score_fig, use_container_width=True)
        
        with col2:
            st.markdown("**Score Ranking:**")
            for i, score in enumerate(recommendation.scores, 1):
                marker = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                st.markdown(f"{marker} **{i}.** {score.topology.value}: {score.score:.2f}")
        
        # Score Breakdown for recommended topology
        st.subheader(f"Score Breakdown: {recommendation.topology.value}")
        breakdown_fig = create_score_breakdown_chart(
            next(s for s in recommendation.scores if s.topology == recommendation.topology)
        )
        st.pyplot(breakdown_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Comparison Table
        st.markdown("""
        <div style='background-color: #ffffff; 
                    padding: 20px; 
                    border-radius: 8px; 
                    border: 1px solid #dee2e6;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    margin-bottom: 20px;'>
            <h2 style='margin-top: 0; padding-left: 0; border-left: none; color: #2E86AB;'>
                📊 Topology Comparison
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        comparison_df = create_comparison_dataframe()
        
        # Highlight recommended topology
        def highlight_recommended(row):
            if row['Topology'] == recommendation.topology.value:
                return ['background-color: #d4edda'] * len(row)
            return [''] * len(row)
        
        styled_df = comparison_df.style.apply(highlight_recommended, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Detailed Score Table (Transparency for Academic Evaluation)
        st.subheader("📊 Weighted Scoring Transparency")
        st.markdown("**Complete score breakdown for all topologies (MCDA/AHP-inspired approach)**")
        
        # Create comprehensive score table
        score_data = []
        for score in recommendation.scores:
            row = {
                "Topology": score.topology.value,
                "Scale Score": None,
                "Budget Score": None,
                "Power Score": None,
                "Workload Score": None,
                "Scalability Score": None,
                "Total Score": f"{score.score:.3f}"
            }
            
            # Extract individual scores from breakdown
            for key, value in score.breakdown.items():
                if key == "Scale Match":
                    row["Scale Score"] = value.split()[0]
                elif key == "Budget Match":
                    row["Budget Score"] = value.split()[0]
                elif key == "Power Match":
                    row["Power Score"] = value.split()[0]
                elif key == "Workload Suitability":
                    row["Workload Score"] = value.split()[0]
                elif key == "Scalability Match":
                    row["Scalability Score"] = value.split()[0]
            
            score_data.append(row)
        
        score_df = pd.DataFrame(score_data)
        
        # Highlight recommended topology
        def highlight_recommended_score(row):
            if row['Topology'] == recommendation.topology.value:
                return ['background-color: #d4edda'] * len(row)
            return [''] * len(row)
        
        styled_score_df = score_df.style.apply(highlight_recommended_score, axis=1)
        st.dataframe(styled_score_df, use_container_width=True, hide_index=True)
        
        # Show weights
        st.markdown("**Scoring Weights (configurable in `core/scoring.py`):**")
        from core.scoring import SCORING_WEIGHTS
        weight_data = {
            "Criterion": ["Scale Match", "Budget Match", "Power Match", "Workload Suitability", "Scalability Match"],
            "Weight": [
                f"{SCORING_WEIGHTS['scale_match']*100:.0f}%",
                f"{SCORING_WEIGHTS['budget_match']*100:.0f}%",
                f"{SCORING_WEIGHTS['power_match']*100:.0f}%",
                f"{SCORING_WEIGHTS['workload_suitability']*100:.0f}%",
                f"{SCORING_WEIGHTS['scalability_match']*100:.0f}%"
            ]
        }
        weight_df = pd.DataFrame(weight_data)
        st.dataframe(weight_df, use_container_width=True, hide_index=True)
        st.caption("Note: Weights are expert-assigned heuristics inspired by MCDA/AHP principles. They can be adjusted in `core/scoring.py`.")
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style='text-align: center; color: #6c757d; padding: 20px;'>
            <p><em>Academic Decision-Support System for Data Center Network Planning</em></p>
            <p style='font-size: 0.9em;'>This tool uses rule-based logic and weighted scoring for topology recommendation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Show instruction when no recommendation yet
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e7f3ff 0%, #d0e7ff 100%); 
                    padding: 30px; 
                    border-radius: 10px; 
                    border-left: 5px solid #2E86AB;
                    margin: 40px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E86AB; margin-top: 0;'>
                👆 Get Started
            </h3>
            <p style='font-size: 16px; color: #495057; line-height: 1.6; margin-bottom: 0;'>
                Enter the required parameters above and click <strong>'Analyze & Recommend Topology'</strong> to get 
                personalized topology suggestions based on your data center requirements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick info cards
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 What This Tool Does")
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.markdown("""
            <div style='background-color: #ffffff; 
                        padding: 20px; 
                        border-radius: 8px; 
                        border: 1px solid #dee2e6;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        height: 100%;'>
                <h4 style='color: #2E86AB; margin-top: 0;'>🎯 Smart Recommendations</h4>
                <p style='color: #6c757d; font-size: 14px; margin-bottom: 0;'>
                    Get topology recommendations based on rule-based logic and weighted scoring analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with info_col2:
            st.markdown("""
            <div style='background-color: #ffffff; 
                        padding: 20px; 
                        border-radius: 8px; 
                        border: 1px solid #dee2e6;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        height: 100%;'>
                <h4 style='color: #2E86AB; margin-top: 0;'>📊 Detailed Analysis</h4>
                <p style='color: #6c757d; font-size: 14px; margin-bottom: 0;'>
                    View comprehensive score breakdowns, comparisons, and visualizations for all topologies.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with info_col3:
            st.markdown("""
            <div style='background-color: #ffffff; 
                        padding: 20px; 
                        border-radius: 8px; 
                        border: 1px solid #dee2e6;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        height: 100%;'>
                <h4 style='color: #2E86AB; margin-top: 0;'>🔍 Explainable Decisions</h4>
                <p style='color: #6c757d; font-size: 14px; margin-bottom: 0;'>
                    Understand why each topology was recommended with detailed explanations and rule breakdowns.
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
