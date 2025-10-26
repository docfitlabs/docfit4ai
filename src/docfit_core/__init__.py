"""
DocFitLabs for AI - Core Module
===========================

Core functionality for DocFitLabs for AI platform.
"""

from .scoring_engine import DocFitScoringEngine, ScoreType
from .data import DocFitConfig, DocumentModel, ScoreModel, DocumentType, ScoreCategory, AnalysisResult
from .parsers import TextParser, PDFParser, HTMLParser
from .__version__ import __version__, __author__, __email__, __description__

__all__ = [
    'DocFitScoringEngine', 'ScoreType',
    'DocFitConfig', 'DocumentModel', 'ScoreModel', 'DocumentType', 'ScoreCategory', 'AnalysisResult',
    'TextParser', 'PDFParser', 'HTMLParser',
    '__version__', '__author__', '__email__', '__description__'
]
