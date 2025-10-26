"""
PDF Document Parser
==================

Pure NLP PDF parser without LLM dependencies.
"""

import re
from typing import Dict, List, Any
from .base_parser import BaseParser


class PDFParser(BaseParser):
    """Parser for PDF documents"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.pdf']
        
    def parse(self, content: bytes, filename: str = None) -> Dict[str, Any]:
        """Parse PDF content"""
        try:
            # For now, we'll use a simple text extraction approach
            # In a real implementation, you'd use PyPDF2 or similar
            text_content = self._extract_text_from_pdf(content)
            
            return {
                'content': text_content,
                'filename': filename,
                'file_type': 'pdf',
                'metadata': self._extract_metadata(text_content),
                'structure': self._extract_structure(text_content)
            }
        except Exception as e:
            # Fallback to basic text extraction
            text_content = content.decode('utf-8', errors='ignore')
            return {
                'content': text_content,
                'filename': filename,
                'file_type': 'pdf',
                'metadata': self._extract_metadata(text_content),
                'structure': self._extract_structure(text_content)
            }
    
    def _extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            import PyPDF2
            import io
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except ImportError:
            # Fallback if PyPDF2 is not available
            return content.decode('utf-8', errors='ignore')
        except Exception:
            # Fallback for any other PDF parsing errors
            return content.decode('utf-8', errors='ignore')
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from PDF content"""
        lines = content.split('\n')
        
        return {
            'line_count': len(lines),
            'char_count': len(content),
            'word_count': len(content.split()),
            'has_headers': self._has_headers(content),
            'has_lists': self._has_lists(content),
            'has_tables': self._has_tables(content),
            'page_count': self._estimate_page_count(content)
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
        # Look for common header patterns
        header_patterns = [
            r'^[A-Z][A-Z\s]{10,}$',  # All caps headers
            r'^\d+\.\s+[A-Z]',  # Numbered headers
            r'^[A-Z][a-z]+\s+[A-Z]',  # Title case headers
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return True
        return False
    
    def _has_lists(self, content: str) -> bool:
        """Check if document has lists"""
        # Bullet points
        bullets = re.findall(r'^\s*[-*•]\s+', content, re.MULTILINE)
        # Numbered lists
        numbers = re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE)
        return len(bullets) > 0 or len(numbers) > 0
    
    def _has_tables(self, content: str) -> bool:
        """Check if document has tables"""
        # Look for table-like patterns
        table_patterns = [
            r'\|\s*.*\s*\|',  # Pipe-separated tables
            r'\s{3,}.*\s{3,}',  # Space-separated columns
        ]
        
        for pattern in table_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return True
        return False
    
    def _estimate_page_count(self, content: str) -> int:
        """Estimate page count based on content length"""
        # Rough estimation: ~500 words per page
        word_count = len(content.split())
        return max(1, word_count // 500)
    
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
        
        # All caps headers
        caps_headers = re.finditer(r'^([A-Z][A-Z\s]{10,})$', content, re.MULTILINE)
        for match in caps_headers:
            text = match.group(1).strip()
            headers.append({'level': 1, 'text': text, 'type': 'caps'})
        
        # Numbered headers
        numbered_headers = re.finditer(r'^(\d+\.\s+[A-Z].+)$', content, re.MULTILINE)
        for match in numbered_headers:
            text = match.group(1).strip()
            level = 1
            headers.append({'level': level, 'text': text, 'type': 'numbered'})
        
        return headers
    
    def _extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Extract lists from content"""
        lists = []
        
        # Bullet lists
        bullet_items = re.findall(r'^\s*[-*•]\s+(.+)$', content, re.MULTILINE)
        if bullet_items:
            lists.append({'type': 'bullet', 'items': bullet_items})
        
        # Numbered lists
        numbered_items = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
        if numbered_items:
            lists.append({'type': 'numbered', 'items': numbered_items})
        
        return lists