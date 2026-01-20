@echo off
echo Starting DC Topology Planner...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Install dependencies if needed
python -c "import streamlit" 2>nul || pip install -r requirements.txt

REM Run the app
streamlit run app.py

pause
