"""
Base Parser Class
================

Abstract base class for all document parsers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseParser(ABC):
    """Abstract base class for document parsers"""
    
    def __init__(self):
        self.supported_extensions = []
    
    @abstractmethod
    def parse(self, content: str, filename: str = None) -> Dict[str, Any]:
        """Parse document content"""
        pass
    
    def can_parse(self, filename: str) -> bool:
        """Check if parser can handle the file"""
        if not filename:
            return False
        
        extension = filename.lower().split('.')[-1]
        return f'.{extension}' in self.supported_extensions
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        return self.supported_extensions
