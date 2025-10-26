#!/usr/bin/env python3
"""
Security4AI Enhanced CLI Tool
============================

Command-line interface for security and DLP assessment with proper command structure.
Matches specification: security4ai scan --input-file policy.docx --config pii_us.yaml
"""

import argparse
import sys
import json
import yaml
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the parent directory to the path to import docfit_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docfit_core.scoring_engine import DocFitScoringEngine, ScoreType

# Import version information
from docfit_core.__version__ import __version__, __author__, __email__
from docfit_core.parsers import TextParser, PDFParser, HTMLParser
from docfit_core.data import DocFitConfig, DocumentModel, DocumentType


class Security4AIEnhancedCLI:
    """Enhanced CLI for security and DLP assessment"""
    
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
        self.pii_config = self._load_default_pii_config()
    
    def _load_default_pii_config(self) -> Dict[str, Any]:
        """Load default PII configuration"""
        return {
            'patterns': {
                'names': [
                    r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Full names
                    r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b',  # Names with middle initial
                ],
                'emails': [
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                ],
                'phones': [
                    r'\b\d{3}-\d{3}-\d{4}\b',  # 123-456-7890
                    r'\(\d{3}\) \d{3}-\d{4}',  # (123) 456-7890
                ],
                'ssn': [
                    r'\b\d{3}-\d{2}-\d{4}\b',  # 123-45-6789
                ],
                'credit_cards': [
                    r'\b\d{4} \d{4} \d{4} \d{4}\b',  # 1234 5678 9012 3456
                    r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',  # 1234-5678-9012-3456
                ],
                'addresses': [
                    r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
                ]
            },
            'risk_levels': {
                'names': 'medium',
                'emails': 'high',
                'phones': 'high',
                'ssn': 'critical',
                'credit_cards': 'critical',
                'addresses': 'medium'
            },
            'compliance_frameworks': {
                'gdpr': True,
                'ccpa': True,
                'hipaa': False,
                'sox': False
            }
        }
    
    def load_pii_config(self, config_path: str) -> Dict[str, Any]:
        """Load PII configuration from file"""
        try:
            with open(config_path, 'r') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif config_path.endswith('.json'):
                    return json.load(f)
                else:
                    print(f"Warning: Unsupported config file format: {config_path}", file=sys.stderr)
                    return self.pii_config
        except Exception as e:
            print(f"Error loading config file: {str(e)}", file=sys.stderr)
            return self.pii_config
    
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
    
    def scan_document(self, file_path: str, config_path: Optional[str] = None, 
                     output_format: str = 'json') -> Dict[str, Any]:
        """Scan document for security risks"""
        try:
            # Load PII config if provided
            if config_path:
                self.pii_config = self.load_pii_config(config_path)
            
            # Parse document
            document = self.parse_file(file_path)
            
            # Score document
            scores = self.scoring_engine.score_document(
                document.content, 
                [ScoreType.SECURITY]
            )
            
            security_score = scores[ScoreType.SECURITY]
            
            # Simulate PII detection using the loaded config
            pii_detection = self._detect_pii_with_config(document.content)
            
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
                },
                'pii_detection': pii_detection,
                'pii_config_used': self.pii_config
            }
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'document': {'filename': file_path}
            }
    
    def _detect_pii_with_config(self, content: str) -> Dict[str, Any]:
        """Detect PII using the loaded configuration"""
        import re
        
        pii_found = {}
        total_risk_score = 0
        
        for pii_type, patterns in self.pii_config['patterns'].items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, content, re.IGNORECASE))
            
            if matches:
                pii_found[pii_type] = {
                    'count': len(matches),
                    'matches': matches[:5],  # Limit to first 5 matches
                    'risk_level': self.pii_config['risk_levels'].get(pii_type, 'medium')
                }
                
                # Calculate risk score
                risk_multiplier = {
                    'critical': 4,
                    'high': 3,
                    'medium': 2,
                    'low': 1
                }.get(pii_found[pii_type]['risk_level'], 1)
                
                total_risk_score += len(matches) * risk_multiplier
        
        return {
            'pii_found': pii_found,
            'total_risk_score': total_risk_score,
            'risk_level': self._get_risk_level(total_risk_score)
        }
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Get risk level based on score"""
        if risk_score >= 20:
            return 'critical'
        elif risk_score >= 10:
            return 'high'
        elif risk_score >= 5:
            return 'medium'
        else:
            return 'low'
    
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
        pii = result['pii_detection']
        
        print(f"\n🔒 Document: {doc['filename']}")
        print(f"📊 File Type: {doc['file_type']}")
        print(f"📏 Size: {doc['file_size']} bytes")
        print(f"📝 Words: {doc['word_count']}")
        print(f"📄 Sentences: {doc['sentence_count']}")
        print(f"📑 Paragraphs: {doc['paragraph_count']}")
        
        print(f"\n🛡️ Security Risk Score: {score['overall_score']:.2f}")
        print(f"📈 Risk Level: {score['category'].upper()}")
        
        print(f"\n📊 Component Scores:")
        for component, comp_score in score['component_scores'].items():
            risk_level = "HIGH" if comp_score > 0.7 else "MEDIUM" if comp_score > 0.4 else "LOW"
            print(f"  • {component.replace('_', ' ').title()}: {comp_score:.2f} ({risk_level})")
        
        # PII Detection Results
        print(f"\n🔍 PII Detection Results:")
        print(f"  • Total Risk Score: {pii['total_risk_score']}")
        print(f"  • Risk Level: {pii['risk_level'].upper()}")
        
        if pii['pii_found']:
            print(f"  • PII Types Found:")
            for pii_type, data in pii['pii_found'].items():
                print(f"    - {pii_type.title()}: {data['count']} instances ({data['risk_level']} risk)")
                if data['matches']:
                    print(f"      Examples: {', '.join(data['matches'][:3])}")
        else:
            print("  ✅ No PII detected")
        
        # Compliance frameworks
        frameworks = result['pii_config_used'].get('compliance_frameworks', {})
        print(f"\n📋 Compliance Frameworks:")
        for framework, enabled in frameworks.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            print(f"  • {framework.upper()}: {status}")
        
        if score['recommendations']:
            print(f"\n🔧 Security Recommendations:")
            for i, rec in enumerate(score['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Security4AI - Security and DLP Assessment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  security4ai scan --input-file policy.docx
  security4ai scan --input-file document.pdf --config pii_us.yaml
  security4ai scan --input-file report.html --output text --config custom_pii.json

Disclaimer:
  DO NOT rely solely on this tool for security decisions. Always consult
  with security experts and use proper security tools for production.
        """
    )
    
    # Add version argument
    parser.add_argument('--version', '-v', action='version', 
                       version=f'%(prog)s {__version__} by {__author__} <{__email__}>')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan document for security risks')
    scan_parser.add_argument('--input-file', '-i', required=True, help='Input document file')
    scan_parser.add_argument('--config', '-c', help='PII configuration file (YAML or JSON)')
    scan_parser.add_argument('--output', '-o', choices=['json', 'text'], default='text',
                            help='Output format (default: text)')
    scan_parser.add_argument('--verbose', '-v', action='store_true',
                            help='Verbose output')
    
    args = parser.parse_args()
    
    if args.command != 'scan':
        parser.print_help()
        sys.exit(1)
    
    # Initialize CLI
    cli = Security4AIEnhancedCLI()
    
    # Scan document
    result = cli.scan_document(
        args.input_file,
        args.config,
        args.output
    )
    
    # Print results
    cli.print_results(result, args.output)
    
    # Exit with error code if assessment failed
    if 'error' in result:
        sys.exit(1)


if __name__ == '__main__':
    main()
