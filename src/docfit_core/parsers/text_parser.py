"""
Text Document Parser
===================

Pure NLP text parser for various text formats without LLM dependencies.
"""

import re
from typing import Dict, List, Any
from .base_parser import BaseParser


class TextParser(BaseParser):
    """Parser for plain text documents"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.txt', '.md', '.rst', '.text']
        
    def parse(self, content: str, filename: str = None) -> Dict[str, Any]:
        """Parse text content"""
        return {
            'content': content,
            'filename': filename,
            'file_type': 'text',
            'metadata': self._extract_metadata(content),
            'structure': self._extract_structure(content)
        }
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from text content"""
        lines = content.split('\n')
        
        return {
            'line_count': len(lines),
            'char_count': len(content),
            'word_count': len(content.split()),
            'has_headers': self._has_headers(content),
            'has_lists': self._has_lists(content),
            'has_code_blocks': self._has_code_blocks(content)
        }
    
    def _extract_structure(self, content: str) -> Dict[str, Any]:
        """Extract document structure"""
        return {
            'paragraphs': self._extract_paragraphs(content),
            'sentences': self._extract_sentences(content),
            'headers': self._extract_headers(content),
            'lists': self._extract_lists(content)
        }
    
    def _has_headers(self, content: str) -> bool:
        """Check if document has headers"""
        # Markdown headers
        markdown_headers = re.findall(r'^#{1,6}\s+', content, re.MULTILINE)
        # RST headers
        rst_headers = re.findall(r'^[=#-]{3,}$', content, re.MULTILINE)
        return len(markdown_headers) > 0 or len(rst_headers) > 0
    
    def _has_lists(self, content: str) -> bool:
        """Check if document has lists"""
        # Bullet points
        bullets = re.findall(r'^\s*[-*+]\s+', content, re.MULTILINE)
        # Numbered lists
        numbers = re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE)
        return len(bullets) > 0 or len(numbers) > 0
    
    def _has_code_blocks(self, content: str) -> bool:
        """Check if document has code blocks"""
        # Markdown code blocks
        markdown_code = re.findall(r'```', content)
        # Indented code
        indented_code = re.findall(r'^\s{4,}', content, re.MULTILINE)
        return len(markdown_code) > 0 or len(indented_code) > 0
    
    def _extract_paragraphs(self, content: str) -> List[str]:
        """Extract paragraphs from content"""
        paragraphs = re.split(r'\n\s*\n', content)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _extract_sentences(self, content: str) -> List[str]:
        """Extract sentences from content"""
        sentences = re.split(r'[.!?]+', content)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Extract headers from content"""
        headers = []
        
        # Markdown headers
        markdown_headers = re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        for match in markdown_headers:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append({'level': level, 'text': text, 'type': 'markdown'})
        
        # RST headers
        rst_headers = re.finditer(r'^(.+)\n([=#-]{3,})$', content, re.MULTILINE)
        for match in rst_headers:
            text = match.group(1).strip()
            level = 1 if match.group(2)[0] == '=' else 2
            headers.append({'level': level, 'text': text, 'type': 'rst'})
        
        return headers
    
    def _extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Extract lists from content"""
        lists = []
        
        # Bullet lists
        bullet_items = re.findall(r'^\s*[-*+]\s+(.+)$', content, re.MULTILINE)
        if bullet_items:
            lists.append({'type': 'bullet', 'items': bullet_items})
        
        # Numbered lists
        numbered_items = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
        if numbered_items:
            lists.append({'type': 'numbered', 'items': numbered_items})
        
        return lists
