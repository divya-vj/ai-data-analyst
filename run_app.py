"""Launcher script for the Streamlit app"""
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    sys.argv = [
        "streamlit",
        "run",
        str(root_dir / "app" / "main.py"),
        "--server.port=8501",
        "--server.address=localhost"
    ]
    
    sys.exit(stcli.main())