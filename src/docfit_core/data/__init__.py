"""
DocFitLabs for AI - Data Module
==========================

This module contains shared data, models, and configuration for all DocFitLabs tools.
"""

from .config import DocFitConfig
from .models import DocumentModel, ScoreModel, DocumentType, ScoreCategory, AnalysisResult

__all__ = ['DocFitConfig', 'DocumentModel', 'ScoreModel', 'DocumentType', 'ScoreCategory', 'AnalysisResult']
