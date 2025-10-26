"""
DocFitLabs Configuration
===================

Configuration settings for all DocFitLabs tools.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import json
import os


@dataclass
class DocFitConfig:
    """Configuration class for DocFitLabs tools"""
    
    # Scoring thresholds
    readiness_thresholds: Dict[str, float] = None
    security_thresholds: Dict[str, float] = None
    obfuscation_thresholds: Dict[str, float] = None
    
    # Output settings
    output_format: str = 'json'
    verbose: bool = False
    save_results: bool = False
    
    # File processing
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    supported_formats: List[str] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.readiness_thresholds is None:
            self.readiness_thresholds = {
                'excellent': 0.9,
                'good': 0.7,
                'fair': 0.5,
                'poor': 0.3
            }
        
        if self.security_thresholds is None:
            self.security_thresholds = {
                'excellent': 0.8,
                'good': 0.6,
                'fair': 0.4,
                'poor': 0.2
            }
        
        if self.obfuscation_thresholds is None:
            self.obfuscation_thresholds = {
                'excellent': 0.9,
                'good': 0.7,
                'fair': 0.5,
                'poor': 0.3
            }
        
        if self.supported_formats is None:
            self.supported_formats = ['.txt', '.md', '.rst', '.pdf', '.html', '.htm']
    
    @classmethod
    def from_file(cls, config_path: str) -> 'DocFitConfig':
        """Load configuration from file"""
        if not os.path.exists(config_path):
            return cls()
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return cls(**config_data)
        except Exception:
            return cls()
    
    def to_file(self, config_path: str) -> None:
        """Save configuration to file"""
        config_data = {
            'readiness_thresholds': self.readiness_thresholds,
            'security_thresholds': self.security_thresholds,
            'obfuscation_thresholds': self.obfuscation_thresholds,
            'output_format': self.output_format,
            'verbose': self.verbose,
            'save_results': self.save_results,
            'max_file_size': self.max_file_size,
            'supported_formats': self.supported_formats
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def get_score_category(self, score_type: str, score: float) -> str:
        """Get score category based on thresholds"""
        if score_type == 'readiness':
            thresholds = self.readiness_thresholds
        elif score_type == 'security':
            thresholds = self.security_thresholds
        elif score_type == 'obfuscation':
            thresholds = self.obfuscation_thresholds
        else:
            return 'unknown'
        
        if score >= thresholds['excellent']:
            return 'excellent'
        elif score >= thresholds['good']:
            return 'good'
        elif score >= thresholds['fair']:
            return 'fair'
        elif score >= thresholds['poor']:
            return 'poor'
        else:
            return 'very_poor'
