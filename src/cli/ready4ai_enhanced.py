#!/usr/bin/env python3
"""
Ready4AI Enhanced CLI Tool
==========================

Command-line interface for AI readiness assessment with proper command structure.
Matches specification: ready4ai analyze --input-file contract.pdf
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

# Import version information
from docfit_core.__version__ import __version__, __author__, __email__
from docfit_core.parsers import TextParser, PDFParser, HTMLParser
from docfit_core.data import DocFitConfig, DocumentModel, DocumentType


class Ready4AIEnhancedCLI:
    """Enhanced CLI for AI readiness assessment"""
    
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
    
    def analyze_document(self, file_path: str, output_format: str = 'json', 
                        include_rag_strategy: bool = True) -> Dict[str, Any]:
        """Analyze document for AI readiness"""
        try:
            # Parse document
            document = self.parse_file(file_path)
            
            # Score document
            scores = self.scoring_engine.score_document(
                document.content, 
                [ScoreType.READINESS]
            )
            
            readiness_score = scores[ScoreType.READINESS]
            
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
                'readiness_score': {
                    'overall_score': readiness_score.overall_score,
                    'category': self.config.get_score_category('readiness', readiness_score.overall_score),
                    'component_scores': readiness_score.component_scores,
                    'recommendations': readiness_score.recommendations,
                    'metadata': readiness_score.metadata
                }
            }
            
            # Add RAG chunking strategy if requested
            if include_rag_strategy:
                result['rag_chunking_strategy'] = self._generate_rag_strategy(document, readiness_score)
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'document': {'filename': file_path}
            }
    
    def _generate_rag_strategy(self, document: DocumentModel, readiness_score: Any) -> Dict[str, Any]:
        """Generate RAG chunking strategy based on document analysis"""
        word_count = document.word_count
        paragraph_count = document.paragraph_count
        
        # Calculate optimal chunk size based on document characteristics
        if word_count < 500:
            chunk_size = 200
            overlap = 50
        elif word_count < 2000:
            chunk_size = 500
            overlap = 100
        else:
            chunk_size = 1000
            overlap = 150
        
        # Determine chunking strategy
        if paragraph_count > 10:
            strategy = "paragraph_based"
        elif readiness_score.component_scores.get('structure', 0) > 0.7:
            strategy = "structure_based"
        else:
            strategy = "semantic_based"
        
        return {
            'recommended_chunk_size': chunk_size,
            'recommended_overlap': overlap,
            'chunking_strategy': strategy,
            'preprocessing_steps': [
                'Clean headers and normalize formatting',
                'Remove excessive whitespace',
                'Standardize list formatting',
                'Ensure consistent paragraph breaks'
            ],
            'optimization_tips': [
                'Use semantic chunking for better context preservation',
                'Maintain overlap to prevent information loss at boundaries',
                'Consider document structure for logical chunk boundaries'
            ]
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
        score = result['readiness_score']
        
        print(f"\n📄 Document: {doc['filename']}")
        print(f"📊 File Type: {doc['file_type']}")
        print(f"📏 Size: {doc['file_size']} bytes")
        print(f"📝 Words: {doc['word_count']}")
        print(f"📄 Sentences: {doc['sentence_count']}")
        print(f"📑 Paragraphs: {doc['paragraph_count']}")
        
        print(f"\n🎯 AI Readiness Score: {score['overall_score']:.2f}")
        print(f"📈 Category: {score['category'].upper()}")
        
        print(f"\n📊 Component Scores:")
        for component, comp_score in score['component_scores'].items():
            print(f"  • {component.title()}: {comp_score:.2f}")
        
        # RAG Chunking Strategy
        if 'rag_chunking_strategy' in result:
            rag = result['rag_chunking_strategy']
            print(f"\n🧩 RAG Chunking Strategy:")
            print(f"  • Chunk Size: {rag['recommended_chunk_size']} tokens")
            print(f"  • Overlap: {rag['recommended_overlap']} tokens")
            print(f"  • Strategy: {rag['chunking_strategy']}")
            print(f"  • Preprocessing Steps:")
            for step in rag['preprocessing_steps']:
                print(f"    - {step}")
        
        if score['recommendations']:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(score['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Ready4AI - AI Readiness Assessment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ready4ai analyze --input-file contract.pdf
  ready4ai analyze --input-file document.txt --output text
  ready4ai analyze --input-file report.html --output json --no-rag-strategy

Disclaimer:
  Results should be verified independently and are not intended for 
  production use without proper validation.
        """
    )
    
    # Add version argument
    parser.add_argument('--version', '-v', action='version', 
                       version=f'%(prog)s {__version__} by {__author__} <{__email__}>')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze document for AI readiness')
    analyze_parser.add_argument('--input-file', '-i', required=True, help='Input document file')
    analyze_parser.add_argument('--output', '-o', choices=['json', 'text'], default='text',
                               help='Output format (default: text)')
    analyze_parser.add_argument('--no-rag-strategy', action='store_true',
                               help='Skip RAG chunking strategy generation')
    analyze_parser.add_argument('--verbose', '-v', action='store_true',
                               help='Verbose output')
    analyze_parser.add_argument('--config', '-c', help='Configuration file path')
    
    args = parser.parse_args()
    
    if args.command != 'analyze':
        parser.print_help()
        sys.exit(1)
    
    # Initialize CLI
    cli = Ready4AIEnhancedCLI()
    
    # Load config if provided
    if args.config:
        cli.config = DocFitConfig.from_file(args.config)
    
    # Set verbose mode
    cli.config.verbose = args.verbose
    
    # Analyze document
    result = cli.analyze_document(
        args.input_file, 
        args.output,
        include_rag_strategy=not args.no_rag_strategy
    )
    
    # Print results
    cli.print_results(result, args.output)
    
    # Exit with error code if assessment failed
    if 'error' in result:
        sys.exit(1)


if __name__ == '__main__':
    main()
