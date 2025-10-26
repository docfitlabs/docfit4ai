"""
Tests for DocFitLabs scoring engine
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from docfit_core.scoring_engine import DocFitScoringEngine, ScoreType


class TestScoringEngine:
    """Test cases for the scoring engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scoring_engine = DocFitScoringEngine()
        self.sample_text = """
        This is a sample document for testing.
        It contains multiple sentences and paragraphs.
        The content is structured and readable.
        """
    
    def test_readiness_scoring(self):
        """Test AI readiness scoring"""
        scores = self.scoring_engine.score_document(
            self.sample_text, 
            [ScoreType.READINESS]
        )
        
        assert ScoreType.READINESS in scores
        readiness_score = scores[ScoreType.READINESS]
        
        assert hasattr(readiness_score, 'overall_score')
        assert hasattr(readiness_score, 'component_scores')
        assert hasattr(readiness_score, 'recommendations')
        
        assert 0 <= readiness_score.overall_score <= 1
        assert isinstance(readiness_score.component_scores, dict)
        assert isinstance(readiness_score.recommendations, list)
    
    def test_security_scoring(self):
        """Test security scoring"""
        scores = self.scoring_engine.score_document(
            self.sample_text, 
            [ScoreType.SECURITY]
        )
        
        assert ScoreType.SECURITY in scores
        security_score = scores[ScoreType.SECURITY]
        
        assert hasattr(security_score, 'overall_score')
        assert hasattr(security_score, 'component_scores')
        assert hasattr(security_score, 'recommendations')
        
        assert 0 <= security_score.overall_score <= 1
        assert isinstance(security_score.component_scores, dict)
        assert isinstance(security_score.recommendations, list)
    
    def test_obfuscation_scoring(self):
        """Test obfuscation scoring"""
        scores = self.scoring_engine.score_document(
            self.sample_text, 
            [ScoreType.OBFUSCATION]
        )
        
        assert ScoreType.OBFUSCATION in scores
        obfuscation_score = scores[ScoreType.OBFUSCATION]
        
        assert hasattr(obfuscation_score, 'overall_score')
        assert hasattr(obfuscation_score, 'component_scores')
        assert hasattr(obfuscation_score, 'recommendations')
        
        assert 0 <= obfuscation_score.overall_score <= 1
        assert isinstance(obfuscation_score.component_scores, dict)
        assert isinstance(obfuscation_score.recommendations, list)
    
    def test_multiple_score_types(self):
        """Test scoring multiple types at once"""
        scores = self.scoring_engine.score_document(
            self.sample_text, 
            [ScoreType.READINESS, ScoreType.SECURITY, ScoreType.OBFUSCATION]
        )
        
        assert len(scores) == 3
        assert ScoreType.READINESS in scores
        assert ScoreType.SECURITY in scores
        assert ScoreType.OBFUSCATION in scores
    
    def test_empty_text(self):
        """Test handling of empty text"""
        scores = self.scoring_engine.score_document("", [ScoreType.READINESS])
        
        assert ScoreType.READINESS in scores
        readiness_score = scores[ScoreType.READINESS]
        assert readiness_score.overall_score == 0.0
    
    def test_very_short_text(self):
        """Test handling of very short text"""
        short_text = "Hi."
        scores = self.scoring_engine.score_document(short_text, [ScoreType.READINESS])
        
        assert ScoreType.READINESS in scores
        readiness_score = scores[ScoreType.READINESS]
        assert 0 <= readiness_score.overall_score <= 1
