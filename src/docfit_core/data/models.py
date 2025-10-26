"""
DocFitLabs Data Models
==================

Data models for DocFitLabs tools.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class DocumentType(Enum):
    """Document types"""
    TEXT = "text"
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    RST = "rst"


class ScoreCategory(Enum):
    """Score categories"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    VERY_POOR = "very_poor"


@dataclass
class DocumentModel:
    """Document data model"""
    
    # Basic properties
    filename: str
    content: str
    file_type: DocumentType
    file_size: int
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    
    # Parsed content
    word_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    char_count: int = 0
    
    # Structure
    headers: List[Dict[str, Any]] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    sentences: List[str] = field(default_factory=list)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate basic metrics after initialization"""
        if self.content:
            self.char_count = len(self.content)
            self.word_count = len(self.content.split())
            self.sentence_count = len(self.content.split('.'))
            self.paragraph_count = len(self.content.split('\n\n'))


@dataclass
class ScoreModel:
    """Score data model"""
    
    # Score properties
    score_type: str
    overall_score: float
    category: ScoreCategory
    
    # Component scores
    component_scores: Dict[str, float] = field(default_factory=dict)
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    document_id: Optional[str] = None
    
    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'score_type': self.score_type,
            'overall_score': self.overall_score,
            'category': self.category.value,
            'component_scores': self.component_scores,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat(),
            'document_id': self.document_id,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScoreModel':
        """Create from dictionary"""
        return cls(
            score_type=data['score_type'],
            overall_score=data['overall_score'],
            category=ScoreCategory(data['category']),
            component_scores=data.get('component_scores', {}),
            recommendations=data.get('recommendations', []),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            document_id=data.get('document_id'),
            metadata=data.get('metadata', {})
        )


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    
    document: DocumentModel
    scores: Dict[str, ScoreModel]
    
    # Analysis metadata
    analysis_id: str
    created_at: datetime = field(default_factory=datetime.now)
    
    # Summary
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'analysis_id': self.analysis_id,
            'created_at': self.created_at.isoformat(),
            'document': {
                'filename': self.document.filename,
                'file_type': self.document.file_type.value,
                'file_size': self.document.file_size,
                'word_count': self.document.word_count,
                'sentence_count': self.document.sentence_count,
                'paragraph_count': self.document.paragraph_count
            },
            'scores': {score_type: score.to_dict() for score_type, score in self.scores.items()},
            'summary': self.summary
        }
    
    def get_overall_summary(self) -> Dict[str, Any]:
        """Get overall analysis summary"""
        return {
            'total_scores': len(self.scores),
            'average_score': sum(score.overall_score for score in self.scores.values()) / len(self.scores) if self.scores else 0,
            'best_score': max(self.scores.values(), key=lambda x: x.overall_score).score_type if self.scores else None,
            'worst_score': min(self.scores.values(), key=lambda x: x.overall_score).score_type if self.scores else None,
            'total_recommendations': sum(len(score.recommendations) for score in self.scores.values())
        }
