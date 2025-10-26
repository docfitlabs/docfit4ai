#!/usr/bin/env python3
"""
Security4AI CLI Tool
===================

Command-line interface for security and DLP assessment using pure NLP techniques.
"""

import argparse
import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Any

# Add the parent directory to the path to import docfit_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docfit_core.scoring_engine import DocFitScoringEngine, ScoreType
from docfit_core.parsers import TextParser, PDFParser, HTMLParser
from docfit_core.data import DocFitConfig, DocumentModel, DocumentType


class Security4AICLI:
    """CLI for security and DLP assessment"""
    
    def __init__(self):
        self.scoring_engine = DocFitScoringEngine()
        self.config = DocFitConfig()
        self.parsers = {
            '.txt': TextParser(),
            '.md': TextParser(),
            '.rst': TextParser(),
            '.pdf': PDFParser(),
            '.html': HTMLParser(),
            '.htm': HTMLParser()
        }
    
    def parse_file(self, file_path: str) -> DocumentModel:
        """Parse a document file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.stat().st_size > self.config.max_file_size:
            raise ValueError(f"File too large: {path.stat().st_size} bytes (max: {self.config.max_file_size})")
        
        # Determine file type
        extension = path.suffix.lower()
        if extension not in self.parsers:
            raise ValueError(f"Unsupported file format: {extension}")
        
        # Read file content
        if extension in ['.pdf']:
            with open(file_path, 'rb') as f:
                content = f.read()
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Parse document
        parser = self.parsers[extension]
        parsed_data = parser.parse(content, str(path))
        
        # Create document model
        document = DocumentModel(
            filename=str(path),
            content=parsed_data['content'],
            file_type=DocumentType(parsed_data['file_type']),
            file_size=path.stat().st_size,
            word_count=parsed_data['metadata'].get('word_count', 0),
            sentence_count=parsed_data['metadata'].get('sentence_count', 0),
            paragraph_count=parsed_data['metadata'].get('paragraph_count', 0),
            metadata=parsed_data['metadata']
        )
        
        return document
    
    def assess_security(self, file_path: str, output_format: str = 'json') -> Dict[str, Any]:
        """Assess security risk of a document"""
        try:
            # Parse document
            document = self.parse_file(file_path)
            
            # Score document
            scores = self.scoring_engine.score_document(
                document.content, 
                [ScoreType.SECURITY]
            )
            
            security_score = scores[ScoreType.SECURITY]
            
            # Prepare result
            result = {
                'document': {
                    'filename': document.filename,
                    'file_type': document.file_type.value,
                    'file_size': document.file_size,
                    'word_count': document.word_count,
                    'sentence_count': document.sentence_count,
                    'paragraph_count': document.paragraph_count
                },
                'security_score': {
                    'overall_score': security_score.overall_score,
                    'category': self.config.get_score_category('security', security_score.overall_score),
                    'component_scores': security_score.component_scores,
                    'recommendations': security_score.recommendations,
                    'metadata': security_score.metadata
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'document': {'filename': file_path}
            }
    
    def print_results(self, result: Dict[str, Any], output_format: str):
        """Print results in specified format"""
        if 'error' in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            return
        
        if output_format == 'json':
            print(json.dumps(result, indent=2))
        elif output_format == 'text':
            self._print_text_results(result)
        else:
            print(json.dumps(result, indent=2))
    
    def _print_text_results(self, result: Dict[str, Any]):
        """Print results in human-readable text format"""
        doc = result['document']
        score = result['security_score']
        
        print(f"\n🔒 Document: {doc['filename']}")
        print(f"📊 File Type: {doc['file_type']}")
        print(f"📏 Size: {doc['file_size']} bytes")
        print(f"📝 Words: {doc['word_count']}")
        print(f"📄 Sentences: {doc['sentence_count']}")
        print(f"📑 Paragraphs: {doc['paragraph_count']}")
        
        print(f"\n🛡️ Security Score: {score['overall_score']:.2f}")
        print(f"📈 Risk Level: {score['category'].upper()}")
        
        print(f"\n📊 Risk Components:")
        for component, comp_score in score['component_scores'].items():
            risk_level = "HIGH" if comp_score > 0.7 else "MEDIUM" if comp_score > 0.4 else "LOW"
            print(f"  • {component.replace('_', ' ').title()}: {comp_score:.2f} ({risk_level})")
        
        if score['recommendations']:
            print(f"\n🔧 Security Recommendations:")
            for i, rec in enumerate(score['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Additional security insights
        metadata = score['metadata']
        if metadata.get('pii_detected'):
            print(f"\n⚠️  WARNING: Personally Identifiable Information detected!")
        if metadata.get('sensitive_patterns_found', 0) > 0:
            print(f"⚠️  WARNING: {metadata['sensitive_patterns_found']} sensitive data patterns found!")
        
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Security4AI - Security and DLP Assessment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  security4ai document.txt
  security4ai document.pdf --output text
  security4ai document.html --output json --verbose
        """
    )
    
    parser.add_argument('file', help='Document file to assess')
    parser.add_argument('--output', '-o', choices=['json', 'text'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--config', '-c', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = Security4AICLI()
    
    # Load config if provided
    if args.config:
        cli.config = DocFitConfig.from_file(args.config)
    
    # Set verbose mode
    cli.config.verbose = args.verbose
    
    # Assess document
    result = cli.assess_security(args.file, args.output)
    
    # Print results
    cli.print_results(result, args.output)
    
    # Exit with error code if assessment failed
    if 'error' in result:
        sys.exit(1)


if __name__ == '__main__':
    main()
