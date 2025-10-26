"""
DocFitLabs for AI - Version Information
===================================

Centralized version information for the DocFitLabs for AI platform.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__author__ = "DocFitLabs Team"
__email__ = "docfit4ai@outlook.com"
__description__ = "Unified Document Assessment Platform for AI Readiness, Security, and IP Protection"
__url__ = "https://github.com/docfitlabs/docfit4ai"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 DocFitLabs Team"

# Build information
__build_date__ = "2024-01-XX"
__python_version__ = "3.8+"
__streamlit_version__ = "1.25+"

# Feature flags
__features__ = {
    "readiness_assessment": True,
    "security_analysis": True,
    "obfuscation_scoring": True,
    "pii_detection": True,
    "custom_config": True,
    "streamlit_ui": True,
    "cli_tools": True,
    "docker_support": True,
    "llm_integration": False,  # Planned for NextPhase
    "ml_enhancements": False,  # Planned for NextPhase
    "advanced_analytics": False,  # Planned for NextPhase
}

# Supported formats
__supported_formats__ = [
    ".txt", ".md", ".rst",  # Text formats
    ".pdf",  # PDF format
    ".html", ".htm",  # HTML formats
]

# CLI tools
__cli_tools__ = {
    "ready4ai": {
        "command": "analyze",
        "description": "AI Readiness Assessment",
        "target_users": ["AI/ML Engineers", "Data Scientists"]
    },
    "security4ai": {
        "command": "scan", 
        "description": "Security and DLP Assessment",
        "target_users": ["CISO", "Compliance Officers", "Security Teams"]
    },
    "obfuscate4ai": {
        "command": "measure",
        "description": "IP Protection and Obfuscation Assessment", 
        "target_users": ["IP Strategy Leaders", "CTO", "Legal Teams"]
    }
}
