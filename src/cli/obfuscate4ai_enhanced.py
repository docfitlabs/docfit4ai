#!/usr/bin/env python3
"""
Obfuscate4AI Enhanced CLI Tool
=============================

Command-line interface for obfuscation and IP protection assessment with proper command structure.
Matches specification: obfuscate4ai measure --input-file trade_secret_doc.txt
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


class Obfuscate4AIEnhancedCLI:
    """Enhanced CLI for obfuscation and IP protection assessment"""
    
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
    
    def measure_document(self, file_path: str, output_format: str = 'json',
                        include_llm_analysis: bool = True) -> Dict[str, Any]:
        """Measure document obfuscation effectiveness"""
        try:
            # Parse document
            document = self.parse_file(file_path)
            
            # Score document
            scores = self.scoring_engine.score_document(
                document.content, 
                [ScoreType.OBFUSCATION]
            )
            
            obfuscation_score = scores[ScoreType.OBFUSCATION]
            
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
                'obfuscation_score': {
                    'overall_score': obfuscation_score.overall_score,
                    'category': self.config.get_score_category('obfuscation', obfuscation_score.overall_score),
                    'component_scores': obfuscation_score.component_scores,
                    'recommendations': obfuscation_score.recommendations,
                    'metadata': obfuscation_score.metadata
                }
            }
            
            # Add LLM suitability analysis if requested
            if include_llm_analysis:
                result['llm_suitability'] = self._analyze_llm_suitability(document, obfuscation_score)
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'document': {'filename': file_path}
            }
    
    def _analyze_llm_suitability(self, document: DocumentModel, obfuscation_score: Any) -> Dict[str, Any]:
        """Analyze document suitability for private vs public LLMs"""
        overall_score = obfuscation_score.overall_score
        
        # Calculate suitability scores
        private_llm_suitability = overall_score / 10  # Higher obfuscation = better for private LLM
        public_llm_risk = 1 - (overall_score / 10)    # Higher obfuscation = lower public LLM risk
        
        # Determine complexity level
        complexity_level = obfuscation_score.metadata.get('complexity_level', 'medium')
        
        # Analyze technical content
        technical_indicators = self._analyze_technical_content(document.content)
        
        # Generate recommendations
        recommendations = []
        if private_llm_suitability < 0.7:
            recommendations.append("Consider increasing document complexity for better private LLM suitability")
        if public_llm_risk > 0.3:
            recommendations.append("Document may be too accessible for public LLMs - consider additional obfuscation")
        
        return {
            'private_llm_suitability': private_llm_suitability,
            'public_llm_risk': public_llm_risk,
            'complexity_level': complexity_level,
            'technical_indicators': technical_indicators,
            'recommendations': recommendations,
            'suitability_summary': self._get_suitability_summary(private_llm_suitability, public_llm_risk)
        }
    
    def _analyze_technical_content(self, content: str) -> Dict[str, Any]:
        """Analyze technical content indicators"""
        import re
        
        # Technical terminology patterns
        technical_patterns = [
            r'\b(?:algorithm|methodology|framework|architecture|implementation)\b',
            r'\b(?:API|SDK|SDLC|CI/CD|DevOps)\b',
            r'\b(?:machine learning|artificial intelligence|neural network)\b',
            r'\b(?:database|repository|deployment|infrastructure)\b'
        ]
        
        technical_count = 0
        for pattern in technical_patterns:
            technical_count += len(re.findall(pattern, content, re.IGNORECASE))
        
        # Jargon density
        words = content.split()
        jargon_density = technical_count / max(len(words), 1)
        
        # Acronym count
        acronym_count = len(re.findall(r'\b[A-Z]{2,}\b', content))
        
        return {
            'technical_terms_found': technical_count,
            'jargon_density': jargon_density,
            'acronym_count': acronym_count,
            'technical_level': 'high' if jargon_density > 0.05 else 'medium' if jargon_density > 0.02 else 'low'
        }
    
    def _get_suitability_summary(self, private_suitability: float, public_risk: float) -> str:
        """Get suitability summary"""
        if private_suitability >= 0.8 and public_risk <= 0.2:
            return "Excellent for private LLM, low public LLM risk"
        elif private_suitability >= 0.6 and public_risk <= 0.4:
            return "Good for private LLM, moderate public LLM risk"
        elif private_suitability >= 0.4 and public_risk <= 0.6:
            return "Moderate private LLM suitability, moderate public LLM risk"
        else:
            return "Limited private LLM suitability, high public LLM risk"
    
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
        score = result['obfuscation_score']
        
        print(f"\n🎭 Document: {doc['filename']}")
        print(f"📊 File Type: {doc['file_type']}")
        print(f"📏 Size: {doc['file_size']} bytes")
        print(f"📝 Words: {doc['word_count']}")
        print(f"📄 Sentences: {doc['sentence_count']}")
        print(f"📑 Paragraphs: {doc['paragraph_count']}")
        
        print(f"\n🛡️ IP Protection Score: {score['overall_score']:.2f}")
        print(f"📈 Protection Level: {score['category'].upper()}")
        
        print(f"\n📊 Protection Components:")
        for component, comp_score in score['component_scores'].items():
            level = "HIGH" if comp_score > 0.7 else "MEDIUM" if comp_score > 0.4 else "LOW"
            print(f"  • {component.replace('_', ' ').title()}: {comp_score:.2f} ({level})")
        
        # LLM Suitability Analysis
        if 'llm_suitability' in result:
            llm = result['llm_suitability']
            print(f"\n🤖 LLM Suitability Analysis:")
            print(f"  • Private LLM Suitability: {llm['private_llm_suitability']:.1%}")
            print(f"  • Public LLM Risk: {llm['public_llm_risk']:.1%}")
            print(f"  • Complexity Level: {llm['complexity_level'].title()}")
            print(f"  • Summary: {llm['suitability_summary']}")
            
            # Technical indicators
            tech = llm['technical_indicators']
            print(f"\n🔧 Technical Content Analysis:")
            print(f"  • Technical Terms: {tech['technical_terms_found']}")
            print(f"  • Jargon Density: {tech['jargon_density']:.2%}")
            print(f"  • Acronyms: {tech['acronym_count']}")
            print(f"  • Technical Level: {tech['technical_level'].title()}")
            
            if llm['recommendations']:
                print(f"\n💡 LLM Suitability Recommendations:")
                for i, rec in enumerate(llm['recommendations'], 1):
                    print(f"  {i}. {rec}")
        
        if score['recommendations']:
            print(f"\n🛡️ Protection Recommendations:")
            for i, rec in enumerate(score['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Obfuscate4AI - IP Protection and Obfuscation Assessment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  obfuscate4ai measure --input-file trade_secret_doc.txt
  obfuscate4ai measure --input-file technical_spec.pdf --output text
  obfuscate4ai measure --input-file internal_doc.html --output json --no-llm-analysis

Disclaimer:
  IP protection strategies should be developed with legal and technical experts.
  Results are not legal advice and should be verified independently.
        """
    )
    
    # Add version argument
    parser.add_argument('--version', '-v', action='version', 
                       version=f'%(prog)s {__version__} by {__author__} <{__email__}>')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Measure command
    measure_parser = subparsers.add_parser('measure', help='Measure document obfuscation effectiveness')
    measure_parser.add_argument('--input-file', '-i', required=True, help='Input document file')
    measure_parser.add_argument('--output', '-o', choices=['json', 'text'], default='text',
                               help='Output format (default: text)')
    measure_parser.add_argument('--no-llm-analysis', action='store_true',
                               help='Skip LLM suitability analysis')
    measure_parser.add_argument('--verbose', '-v', action='store_true',
                               help='Verbose output')
    measure_parser.add_argument('--config', '-c', help='Configuration file path')
    
    args = parser.parse_args()
    
    if args.command != 'measure':
        parser.print_help()
        sys.exit(1)
    
    # Initialize CLI
    cli = Obfuscate4AIEnhancedCLI()
    
    # Load config if provided
    if args.config:
        cli.config = DocFitConfig.from_file(args.config)
    
    # Set verbose mode
    cli.config.verbose = args.verbose
    
    # Measure document
    result = cli.measure_document(
        args.input_file,
        args.output,
        include_llm_analysis=not args.no_llm_analysis
    )
    
    # Print results
    cli.print_results(result, args.output)
    
    # Exit with error code if assessment failed
    if 'error' in result:
        sys.exit(1)


if __name__ == '__main__':
    main()
