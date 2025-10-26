"""
DocFitLabs for AI - Core Scoring Engine
====================================

This module provides the core scoring logic used by all three DocFitLabs tools:
- Readiness Scorecard (ready4ai)
- Security Scorecard (security4ai) 
- Obfuscation Scorecard (obfuscate4ai)

The scoring engine uses pure NLP techniques without LLM dependencies.
"""

import re
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ScoreType(Enum):
    """Types of scores that can be calculated"""
    READINESS = "readiness"
    SECURITY = "security"
    OBFUSCATION = "obfuscation"


@dataclass
class ScoreResult:
    """Result of a scoring operation"""
    score_type: ScoreType
    overall_score: float
    component_scores: Dict[str, float]
    recommendations: List[str]
    metadata: Dict[str, Any]


class DocumentParser:
    """Pure NLP document parser without LLM dependencies"""
    
    def __init__(self):
        self.sentence_endings = r'[.!?]+'
        self.word_pattern = r'\b\w+\b'
        self.paragraph_pattern = r'\n\s*\n'
        
    def parse_document(self, text: str) -> Dict[str, Any]:
        """Parse document into structured components"""
        return {
            'raw_text': text,
            'sentences': self._extract_sentences(text),
            'words': self._extract_words(text),
            'paragraphs': self._extract_paragraphs(text),
            'word_count': len(self._extract_words(text)),
            'sentence_count': len(self._extract_sentences(text)),
            'paragraph_count': len(self._extract_paragraphs(text))
        }
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences using regex"""
        sentences = re.split(self.sentence_endings, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words using regex"""
        return re.findall(self.word_pattern, text.lower())
    
    def _extract_paragraphs(self, text: str) -> List[str]:
        """Extract paragraphs"""
        paragraphs = re.split(self.paragraph_pattern, text)
        return [p.strip() for p in paragraphs if p.strip()]


class ReadinessScorer:
    """Scoring engine for AI readiness assessment"""
    
    def __init__(self):
        self.parser = DocumentParser()
        
    def calculate_readiness_score(self, document: Dict[str, Any]) -> ScoreResult:
        """Calculate AI readiness score using pure NLP"""
        
        # Extract metrics
        word_count = document['word_count']
        sentence_count = document['sentence_count']
        paragraph_count = document['paragraph_count']
        
        # Calculate component scores
        structure_score = self._calculate_structure_score(document)
        clarity_score = self._calculate_clarity_score(document)
        completeness_score = self._calculate_completeness_score(document)
        formatting_score = self._calculate_formatting_score(document)
        
        # Calculate overall score
        overall_score = (
            structure_score * 0.3 +
            clarity_score * 0.3 +
            completeness_score * 0.25 +
            formatting_score * 0.15
        )
        
        # Generate recommendations
        recommendations = self._generate_readiness_recommendations(
            structure_score, clarity_score, completeness_score, formatting_score
        )
        
        return ScoreResult(
            score_type=ScoreType.READINESS,
            overall_score=overall_score,
            component_scores={
                'structure': structure_score,
                'clarity': clarity_score,
                'completeness': completeness_score,
                'formatting': formatting_score
            },
            recommendations=recommendations,
            metadata={
                'word_count': word_count,
                'sentence_count': sentence_count,
                'paragraph_count': paragraph_count
            }
        )
    
    def _calculate_structure_score(self, document: Dict[str, Any]) -> float:
        """Calculate document structure score"""
        paragraphs = document['paragraphs']
        sentences = document['sentences']
        
        # Check for proper paragraph structure
        avg_sentences_per_paragraph = len(sentences) / max(len(paragraphs), 1)
        structure_score = min(avg_sentences_per_paragraph / 3.0, 1.0)  # Optimal: 3 sentences per paragraph
        
        return min(structure_score, 1.0)
    
    def _calculate_clarity_score(self, document: Dict[str, Any]) -> float:
        """Calculate document clarity score"""
        words = document['words']
        sentences = document['sentences']
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # Optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            clarity_score = 1.0
        else:
            # Penalize very short or very long sentences
            clarity_score = max(0.3, 1.0 - abs(avg_sentence_length - 17.5) / 17.5)
        
        return clarity_score
    
    def _calculate_completeness_score(self, document: Dict[str, Any]) -> float:
        """Calculate document completeness score"""
        word_count = document['word_count']
        
        # Minimum word count for AI processing
        if word_count < 100:
            return 0.2
        elif word_count < 500:
            return 0.5
        elif word_count < 1000:
            return 0.8
        else:
            return 1.0
    
    def _calculate_formatting_score(self, document: Dict[str, Any]) -> float:
        """Calculate document formatting score"""
        text = document['raw_text']
        
        # Check for basic formatting elements
        has_paragraphs = '\n\n' in text
        has_proper_spacing = not re.search(r'[a-z][A-Z]', text)  # No missing spaces between sentences
        
        score = 0.0
        if has_paragraphs:
            score += 0.5
        if has_proper_spacing:
            score += 0.5
            
        return score
    
    def _generate_readiness_recommendations(self, structure: float, clarity: float, 
                                          completeness: float, formatting: float) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        
        if structure < 0.7:
            recommendations.append("Improve document structure with better paragraph organization")
        if clarity < 0.7:
            recommendations.append("Simplify sentence structure for better clarity")
        if completeness < 0.7:
            recommendations.append("Add more content to make the document more comprehensive")
        if formatting < 0.7:
            recommendations.append("Improve document formatting and spacing")
            
        return recommendations


class SecurityScorer:
    """Scoring engine for security and DLP assessment"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.sensitive_patterns = [
            r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',  # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b',        # SSN
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:password|passwd|pwd)\s*[:=]\s*\w+',  # Password patterns
        ]
        
    def calculate_security_score(self, document: Dict[str, Any]) -> ScoreResult:
        """Calculate security risk score"""
        
        text = document['raw_text']
        
        # Calculate component scores
        pii_score = self._calculate_pii_score(text)
        sensitive_data_score = self._calculate_sensitive_data_score(text)
        classification_score = self._calculate_classification_score(text)
        
        # Overall security score (lower is better for security)
        overall_score = 1.0 - (
            pii_score * 0.4 +
            sensitive_data_score * 0.4 +
            classification_score * 0.2
        )
        
        recommendations = self._generate_security_recommendations(
            pii_score, sensitive_data_score, classification_score
        )
        
        return ScoreResult(
            score_type=ScoreType.SECURITY,
            overall_score=max(overall_score, 0.0),
            component_scores={
                'pii_risk': pii_score,
                'sensitive_data_risk': sensitive_data_score,
                'classification_risk': classification_score
            },
            recommendations=recommendations,
            metadata={
                'pii_detected': pii_score > 0.5,
                'sensitive_patterns_found': len(self._find_sensitive_patterns(text))
            }
        )
    
    def _calculate_pii_score(self, text: str) -> float:
        """Calculate PII risk score"""
        pii_indicators = [
            r'\b(?:name|address|phone|ssn|social security)\b',
            r'\b(?:birth|born|age)\b',
            r'\b(?:personal|private|confidential)\b'
        ]
        
        pii_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in pii_indicators)
        return min(pii_count / 10.0, 1.0)  # Normalize to 0-1
    
    def _calculate_sensitive_data_score(self, text: str) -> float:
        """Calculate sensitive data risk score"""
        sensitive_count = len(self._find_sensitive_patterns(text))
        return min(sensitive_count / 5.0, 1.0)  # Normalize to 0-1
    
    def _calculate_classification_score(self, text: str) -> float:
        """Calculate classification risk score"""
        classification_indicators = [
            r'\b(?:confidential|secret|classified|proprietary)\b',
            r'\b(?:internal|restricted|private)\b'
        ]
        
        classification_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                                 for pattern in classification_indicators)
        return min(classification_count / 3.0, 1.0)
    
    def _find_sensitive_patterns(self, text: str) -> List[str]:
        """Find sensitive data patterns in text"""
        matches = []
        for pattern in self.sensitive_patterns:
            matches.extend(re.findall(pattern, text))
        return matches
    
    def _generate_security_recommendations(self, pii: float, sensitive: float, 
                                         classification: float) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if pii > 0.3:
            recommendations.append("Remove or mask personally identifiable information")
        if sensitive > 0.3:
            recommendations.append("Remove sensitive data patterns (SSN, credit cards, etc.)")
        if classification > 0.3:
            recommendations.append("Review document classification and remove sensitive indicators")
            
        return recommendations


class ObfuscationScorer:
    """Scoring engine for obfuscation and IP protection assessment"""
    
    def __init__(self):
        self.parser = DocumentParser()
        
    def calculate_obfuscation_score(self, document: Dict[str, Any]) -> ScoreResult:
        """Calculate obfuscation effectiveness score"""
        
        text = document['raw_text']
        
        # Calculate component scores
        complexity_score = self._calculate_complexity_score(document)
        obfuscation_score = self._calculate_obfuscation_effectiveness(text)
        ip_protection_score = self._calculate_ip_protection_score(text)
        
        # Overall obfuscation score
        overall_score = (
            complexity_score * 0.4 +
            obfuscation_score * 0.4 +
            ip_protection_score * 0.2
        )
        
        recommendations = self._generate_obfuscation_recommendations(
            complexity_score, obfuscation_score, ip_protection_score
        )
        
        return ScoreResult(
            score_type=ScoreType.OBFUSCATION,
            overall_score=overall_score,
            component_scores={
                'complexity': complexity_score,
                'obfuscation': obfuscation_score,
                'ip_protection': ip_protection_score
            },
            recommendations=recommendations,
            metadata={
                'complexity_level': 'high' if complexity_score > 0.7 else 'medium' if complexity_score > 0.4 else 'low'
            }
        )
    
    def _calculate_complexity_score(self, document: Dict[str, Any]) -> float:
        """Calculate document complexity score"""
        words = document['words']
        sentences = document['sentences']
        
        # Calculate lexical diversity
        unique_words = len(set(words))
        total_words = len(words)
        lexical_diversity = unique_words / max(total_words, 1)
        
        # Calculate sentence complexity
        avg_sentence_length = total_words / max(len(sentences), 1)
        
        # Combine metrics
        complexity_score = (lexical_diversity * 0.6 + min(avg_sentence_length / 30.0, 1.0) * 0.4)
        
        return min(complexity_score, 1.0)
    
    def _calculate_obfuscation_effectiveness(self, text: str) -> float:
        """Calculate obfuscation effectiveness"""
        # Check for obfuscation techniques
        obfuscation_indicators = [
            r'[A-Z]{2,}',  # Acronyms
            r'\b\w{10,}\b',  # Long technical terms
            r'\b(?:algorithm|methodology|framework|architecture)\b',  # Technical jargon
        ]
        
        obfuscation_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                              for pattern in obfuscation_indicators)
        
        return min(obfuscation_count / 10.0, 1.0)
    
    def _calculate_ip_protection_score(self, text: str) -> float:
        """Calculate intellectual property protection score"""
        ip_indicators = [
            r'\b(?:patent|copyright|trademark|proprietary)\b',
            r'\b(?:intellectual property|IP|trade secret)\b',
            r'\b(?:confidential|restricted|internal)\b'
        ]
        
        ip_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                      for pattern in ip_indicators)
        
        return min(ip_count / 5.0, 1.0)
    
    def _generate_obfuscation_recommendations(self, complexity: float, obfuscation: float, 
                                             ip_protection: float) -> List[str]:
        """Generate obfuscation recommendations"""
        recommendations = []
        
        if complexity < 0.5:
            recommendations.append("Increase document complexity with technical terminology")
        if obfuscation < 0.5:
            recommendations.append("Add more technical jargon and acronyms")
        if ip_protection < 0.5:
            recommendations.append("Add intellectual property protection indicators")
            
        return recommendations


class DocFitScoringEngine:
    """Main scoring engine that coordinates all scoring types"""
    
    def __init__(self):
        self.readiness_scorer = ReadinessScorer()
        self.security_scorer = SecurityScorer()
        self.obfuscation_scorer = ObfuscationScorer()
        self.parser = DocumentParser()
    
    def score_document(self, text: str, score_types: List[ScoreType] = None) -> Dict[ScoreType, ScoreResult]:
        """Score document for specified score types"""
        if score_types is None:
            score_types = [ScoreType.READINESS, ScoreType.SECURITY, ScoreType.OBFUSCATION]
        
        # Parse document once
        document = self.parser.parse_document(text)
        
        results = {}
        
        for score_type in score_types:
            if score_type == ScoreType.READINESS:
                results[score_type] = self.readiness_scorer.calculate_readiness_score(document)
            elif score_type == ScoreType.SECURITY:
                results[score_type] = self.security_scorer.calculate_security_score(document)
            elif score_type == ScoreType.OBFUSCATION:
                results[score_type] = self.obfuscation_scorer.calculate_obfuscation_score(document)
        
        return results
