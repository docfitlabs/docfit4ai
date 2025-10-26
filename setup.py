"""
DocFitLabsfor AI - Setup Configuration
==================================

Setup script for DocFitLabsfor AI package.
"""

from setuptools import setup, find_packages
import os
import sys

# Add src to path to import version
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from docfit_core.__version__ import (
    __version__, __author__, __email__, __description__, 
    __url__, __license__, __python_version__
)

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="docfit4ai",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=__url__,
    license=__license__,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "llm": [
            "transformers>=4.25.0",
            "torch>=1.13.0",
            "openai>=0.27.0",
            "anthropic>=0.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ready4ai=cli.ready4ai:main",
            "ready4ai-enhanced=cli.ready4ai_enhanced:main",
            "security4ai=cli.security4ai:main",
            "security4ai-enhanced=cli.security4ai_enhanced:main", 
            "obfuscate4ai=cli.obfuscate4ai:main",
            "obfuscate4ai-enhanced=cli.obfuscate4ai_enhanced:main",
            "docfit4ai-ui=ui.streamlit_app:main",
            "docfit4ai-enhanced-ui=ui.enhanced_streamlit_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "docfit_core": ["data/*.json", "data/*.txt"],
    },
    keywords=[
        "ai", "document", "assessment", "readiness", "security", "obfuscation",
        "nlp", "text-processing", "dlp", "compliance", "scoring"
    ],
    project_urls={
        "Bug Reports": "https://github.com/docfitlabs/docfit4ai/issues",
        "Source": "https://github.com/docfitlabs/docfit4ai",
        "Documentation": "https://docfit.readthedocs.io/",
    },
)
