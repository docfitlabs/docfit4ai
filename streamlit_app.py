"""
DocFitLabs for AI - Main Streamlit App
=====================================

This is the main entry point for Streamlit Cloud deployment.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the enhanced app
from ui.enhanced_streamlit_app import main

if __name__ == "__main__":
    main()