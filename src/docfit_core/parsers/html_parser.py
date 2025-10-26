"""
HTML Document Parser
===================

Pure NLP HTML parser without LLM dependencies.
"""

import re
from typing import Dict, List, Any
from .base_parser import BaseParser


class HTMLParser(BaseParser):
    """Parser for HTML documents"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.html', '.htm']
        
    def parse(self, content: str, filename: str = None) -> Dict[str, Any]:
        """Parse HTML content"""
        try:
            # Use BeautifulSoup if available, otherwise fallback to regex
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                text_content = soup.get_text()
            except ImportError:
                # Fallback to regex-based HTML parsing
                text_content = self._extract_text_with_regex(content)
            
            return {
                'content': text_content,
                'filename': filename,
                'file_type': 'html',
                'metadata': self._extract_metadata(content, text_content),
                'structure': self._extract_structure(content, text_content)
            }
        except Exception as e:
            # Fallback to basic text extraction
            text_content = self._extract_text_with_regex(content)
            return {
                'content': text_content,
                'filename': filename,
                'file_type': 'html',
                'metadata': self._extract_metadata(content, text_content),
                'structure': self._extract_structure(content, text_content)
            }
    
    def _extract_text_with_regex(self, content: str) -> str:
        """Extract text from HTML using regex (fallback method)"""
        # Remove script and style elements
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Decode HTML entities
        content = self._decode_html_entities(content)
        
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        return content.strip()
    
    def _decode_html_entities(self, text: str) -> str:
        """Decode common HTML entities"""
        entities = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' ',
            '&copy;': '©',
            '&reg;': '®',
            '&trade;': '™',
        }
        
        for entity, char in entities.items():
            text = text.replace(entity, char)
        
        return text
    
    def _extract_metadata(self, html_content: str, text_content: str) -> Dict[str, Any]:
        """Extract metadata from HTML content"""
        return {
            'line_count': len(text_content.split('\n')),
            'char_count': len(text_content),
            'word_count': len(text_content.split()),
            'has_headers': self._has_headers(html_content),
            'has_lists': self._has_lists(html_content),
            'has_tables': self._has_tables(html_content),
            'has_links': self._has_links(html_content),
            'has_images': self._has_images(html_content),
            'title': self._extract_title(html_content)
        }
    
    def _extract_structure(self, html_content: str, text_content: str) -> Dict[str, Any]:
        """Extract document structure"""
        return {
            'paragraphs': self._extract_paragraphs(text_content),
            'sentences': self._extract_sentences(text_content),
            'headers': self._extract_headers(html_content),
            'lists': self._extract_lists(html_content),
            'links': self._extract_links(html_content)
        }
    
    def _has_headers(self, content: str) -> bool:
        """Check if document has headers"""
        header_tags = re.findall(r'<h[1-6][^>]*>', content, re.IGNORECASE)
        return len(header_tags) > 0
    
    def _has_lists(self, content: str) -> bool:
        """Check if document has lists"""
        list_tags = re.findall(r'<(ul|ol)[^>]*>', content, re.IGNORECASE)
        return len(list_tags) > 0
    
    def _has_tables(self, content: str) -> bool:
        """Check if document has tables"""
        table_tags = re.findall(r'<table[^>]*>', content, re.IGNORECASE)
        return len(table_tags) > 0
    
    def _has_links(self, content: str) -> bool:
        """Check if document has links"""
        link_tags = re.findall(r'<a[^>]*href[^>]*>', content, re.IGNORECASE)
        return len(link_tags) > 0
    
    def _has_images(self, content: str) -> bool:
        """Check if document has images"""
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        return len(img_tags) > 0
    
    def _extract_title(self, content: str) -> str:
        """Extract document title"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return ""
    
    def _extract_paragraphs(self, content: str) -> List[str]:
        """Extract paragraphs from content"""
        paragraphs = re.split(r'\n\s*\n', content)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _extract_sentences(self, content: str) -> List[str]:
        """Extract sentences from content"""
        sentences = re.split(r'[.!?]+', content)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Extract headers from HTML content"""
        headers = []
        
        # Extract h1-h6 tags
        header_pattern = r'<h([1-6])[^>]*>(.*?)</h[1-6]>'
        header_matches = re.finditer(header_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in header_matches:
            level = int(match.group(1))
            text = self._extract_text_with_regex(match.group(2)).strip()
            if text:
                headers.append({'level': level, 'text': text, 'type': 'html'})
        
        return headers
    
    def _extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Extract lists from HTML content"""
        lists = []
        
        # Extract ul lists
        ul_pattern = r'<ul[^>]*>(.*?)</ul>'
        ul_matches = re.finditer(ul_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in ul_matches:
            ul_content = match.group(1)
            li_items = re.findall(r'<li[^>]*>(.*?)</li>', ul_content, re.IGNORECASE | re.DOTALL)
            items = [self._extract_text_with_regex(item).strip() for item in li_items if item.strip()]
            if items:
                lists.append({'type': 'bullet', 'items': items})
        
        # Extract ol lists
        ol_pattern = r'<ol[^>]*>(.*?)</ol>'
        ol_matches = re.finditer(ol_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in ol_matches:
            ol_content = match.group(1)
            li_items = re.findall(r'<li[^>]*>(.*?)</li>', ol_content, re.IGNORECASE | re.DOTALL)
            items = [self._extract_text_with_regex(item).strip() for item in li_items if item.strip()]
            if items:
                lists.append({'type': 'numbered', 'items': items})
        
        return lists
    
    def _extract_links(self, content: str) -> List[Dict[str, Any]]:
        """Extract links from HTML content"""
        links = []
        
        # Extract a tags with href
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        link_matches = re.finditer(link_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in link_matches:
            href = match.group(1)
            text = self._extract_text_with_regex(match.group(2)).strip()
            if text and href:
                links.append({'href': href, 'text': text})
        
        return links