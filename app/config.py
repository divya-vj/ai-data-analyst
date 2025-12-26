"""Configuration Settings"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"

# Create directories
DATA_DIR.mkdir(exist_ok=True)

# App Settings
APP_TITLE = "AI Data Analyst Pro"
APP_ICON = "📊"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional AI-Powered Data Analysis"

# File Settings
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = ["csv", "xlsx", "xls", "json"]
MAX_ROWS_DISPLAY = 1000

# Visualization
CHART_DPI = 150
PRIMARY_COLOR = "#1f77b4"

# Analysis
OUTLIER_THRESHOLD = 3
MAX_CATEGORIES = 50