@echo off
echo ========================================
echo DCN Topology Planner - Starting App
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the Streamlit app
echo Starting Streamlit application...
echo.
streamlit run app.py

pause
