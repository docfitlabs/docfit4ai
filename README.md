# DocFitLabs for AI

[![GitHub stars](https://img.shields.io/github/stars/docfitlabs/docfit4ai?style=social)](https://github.com/docfitlabs/docfit4ai)
[![GitHub forks](https://img.shields.io/github/forks/docfitlabs/docfit4ai?style=social)](https://github.com/docfitlabs/docfit4ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-green.svg)](https://docfit4ai-pky7c2plckscap9eesfkba.streamlit.app/)

**Unified Document Assessment Platform**

DocFitLabs for AI is a comprehensive suite of tools for assessing document readiness, security, and obfuscation for AI processing. Built with pure NLP techniques, it provides fast, reliable assessments without LLM dependencies.

## 🌐 Live Demo

**[🚀 Try DocFitLabs for AI Now](https://docfit4ai-pky7c2plckscap9eesfkba.streamlit.app/)**

Experience the full platform with our interactive web application. Upload documents, run assessments, and explore all features in real-time.

## 🎯 Features

### 📊 Three Assessment Tools

1. **Ready4AI** - AI Readiness Scorecard
   - Document structure analysis
   - Clarity and readability scoring
   - Completeness evaluation
   - Formatting assessment

2. **Security4AI** - Security & DLP Scorecard
   - PII detection and risk scoring
   - Sensitive data pattern analysis
   - Classification risk evaluation
   - DLP compliance checking

3. **Obfuscate4AI** - Obfuscation & IP Protection Scorecard
   - Complexity analysis
   - IP protection scoring
   - Technical terminology assessment
   - Obfuscation effectiveness

### 🚀 Key Benefits

- **Pure NLP**: No LLM dependencies, fast and reliable
- **Multiple Formats**: Supports TXT, MD, RST, PDF, HTML
- **Unified Interface**: Single platform for all assessments
- **CLI & Web UI**: Command-line tools and Streamlit interface
- **Enhanced Features**: Advanced CLI commands and tabbed web interface
- **PII Configuration**: Customizable PII detection patterns
- **RAG Optimization**: Built-in chunking strategy recommendations
- **LLM Suitability**: Private vs public LLM risk analysis
- **Extensible**: Modular design for easy customization

## 📁 Project Structure

```
docfit4ai/
├── src/
│   ├── docfit_core/           # Core scoring engine and parsers
│   │   ├── scoring_engine.py  # Main scoring logic
│   │   ├── parsers/           # Document parsers (TXT, PDF, HTML)
│   │   └── data/              # Data models and config
│   ├── cli/                   # Command-line tools
│   │   ├── ready4ai.py       # Basic readiness CLI
│   │   ├── ready4ai_enhanced.py # Enhanced readiness CLI
│   │   ├── security4ai.py     # Basic security CLI
│   │   ├── security4ai_enhanced.py # Enhanced security CLI
│   │   ├── obfuscate4ai.py    # Basic obfuscation CLI
│   │   └── obfuscate4ai_enhanced.py # Enhanced obfuscation CLI
│   └── ui/                    # User interface
│       ├── streamlit_app.py  # Basic Streamlit app
│       └── enhanced_streamlit_app.py # Enhanced tabbed Streamlit app
├── README.md
├── requirements.txt
├── setup.py
├── Makefile
└── Dockerfile
```

## ⚠️ Disclaimer

**Results should be verified independently and are not intended for production use without proper validation.** Always consult with appropriate experts for critical decisions.
**This tool is for initial research purpose only.**

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/docfitlabs/docfit4ai.git
cd docfit4ai

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
make test
```

## 🚀 Usage

### Command Line Interface

DocFitLabs provides both basic and enhanced CLI tools. The enhanced versions offer better command structure and additional features.

#### Readiness Assessment
```bash
# Basic assessment (original CLI)
ready4ai document.txt

# Enhanced CLI with proper command structure
ready4ai analyze --input-file document.pdf --output text

# JSON output with RAG strategy
ready4ai analyze --input-file document.html --output json --verbose

# Skip RAG strategy generation
ready4ai analyze --input-file document.txt --no-rag-strategy
```

#### Security Assessment
```bash
# Security risk assessment
security4ai document.txt

# JSON output with verbose logging
security4ai document.pdf --output json --verbose

# With custom PII configuration
security4ai document.txt --config pii_config.yaml
```

#### Obfuscation Assessment
```bash
# IP protection assessment
obfuscate4ai document.txt

# Text output
obfuscate4ai document.html --output text

# JSON output with verbose mode
obfuscate4ai document.pdf --output json --verbose
```

#### Enhanced CLI Commands (Recommended)

The enhanced CLI commands provide better structure and additional features:

```bash
# Enhanced Readiness Assessment
ready4ai-enhanced analyze --input-file document.pdf --output text
ready4ai-enhanced analyze --input-file document.html --output json --verbose
ready4ai-enhanced analyze --input-file document.txt --no-rag-strategy

# Enhanced Security Assessment  
security4ai-enhanced scan --input-file document.pdf --config pii_config.yaml
security4ai-enhanced scan --input-file document.html --output json --verbose

# Enhanced Obfuscation Assessment
obfuscate4ai-enhanced measure --input-file document.txt --output text
obfuscate4ai-enhanced measure --input-file document.pdf --output json --verbose
```

### Web Interface

```bash
# Start basic Streamlit app
streamlit run src/ui/streamlit_app.py

# Start enhanced Streamlit app (recommended)
streamlit run src/ui/enhanced_streamlit_app.py

# Or use the Makefile
make ui

# For Streamlit Cloud deployment
streamlit run streamlit_app.py
```

#### Enhanced Web Interface (Recommended)

The enhanced Streamlit app provides a tabbed interface for different user personas:

```bash
# Start enhanced Streamlit app
streamlit run src/ui/enhanced_streamlit_app.py

# Or use the enhanced UI command
docfit4ai-enhanced-ui
```

**Features:**
- **Tabbed Interface**: Separate tabs for AI Readiness, Security Analysis, and IP Protection
- **User Persona Focused**: Each tab is designed for specific user types
- **PII Configuration**: Upload custom PII detection patterns
- **Interactive Visualizations**: Enhanced charts and graphs
- **Feedback System**: Built-in feedback collection
- **Export Options**: Multiple export formats (JSON, Text, YAML)

### Docker

```bash
# Build Docker image
make build

# Run container
make run

# Run with custom port
docker run -p 8501:8501 docfit4ai
```

## 📊 Output Formats

### Text Output
```
📄 Document: document.txt
📊 File Type: text
📏 Size: 1,234 bytes
📝 Words: 250
📄 Sentences: 15
📑 Paragraphs: 5

🎯 AI Readiness Score: 0.85
📈 Category: GOOD

📊 Component Scores:
  • Structure: 0.90
  • Clarity: 0.80
  • Completeness: 0.85
  • Formatting: 0.75

💡 Recommendations:
  1. Improve document formatting and spacing
```

### JSON Output
```json
{
  "document": {
    "filename": "document.txt",
    "file_type": "text",
    "file_size": 1234,
    "word_count": 250,
    "sentence_count": 15,
    "paragraph_count": 5
  },
  "readiness_score": {
    "overall_score": 0.85,
    "category": "good",
    "component_scores": {
      "structure": 0.90,
      "clarity": 0.80,
      "completeness": 0.85,
      "formatting": 0.75
    },
    "recommendations": [
      "Improve document formatting and spacing"
    ]
  }
}
```

## 🔧 Configuration

### Custom Configuration

#### Basic Configuration

Create a `config.json` file:

```json
{
  "readiness_thresholds": {
    "excellent": 0.9,
    "good": 0.7,
    "fair": 0.5,
    "poor": 0.3
  },
  "security_thresholds": {
    "low_risk": 0.8,
    "medium_risk": 0.6,
    "high_risk": 0.4,
    "critical_risk": 0.2
  },
  "output_format": "json",
  "verbose": false,
  "max_file_size": 10485760
}
```

Use with CLI:
```bash
ready4ai document.txt --config config.json
```

#### PII Configuration (Security Analysis)

For security analysis, you can customize PII detection patterns using YAML or JSON:

```yaml
# pii_config.yaml
patterns:
  names:
    - '\b[A-Z][a-z]+ [A-Z][a-z]+\b'  # Full names
    - '\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b'  # Names with middle initial
  emails:
    - '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  phones:
    - '\b\d{3}-\d{3}-\d{4}\b'  # 123-456-7890
    - '\(\d{3}\) \d{3}-\d{4}'  # (123) 456-7890
  ssn:
    - '\b\d{3}-\d{2}-\d{4}\b'  # 123-45-6789
  credit_cards:
    - '\b\d{4} \d{4} \d{4} \d{4}\b'  # 1234 5678 9012 3456
    - '\b\d{4}-\d{4}-\d{4}-\d{4}\b'  # 1234-5678-9012-3456

risk_levels:
  names: medium
  emails: high
  phones: high
  ssn: critical
  credit_cards: critical

compliance_frameworks:
  gdpr: true
  ccpa: true
  hipaa: false
  sox: false
```

Use with enhanced security CLI:
```bash
security4ai-enhanced scan --input-file document.pdf --config pii_config.yaml
```

## 🧪 Testing

```bash
# Run all tests
make test

# Test all CLI tools
make test-cli

# Run specific test
python -m pytest tests/test_scoring_engine.py

# Run with coverage
make test-coverage

# Test enhanced CLI tools
python src/cli/ready4ai_enhanced.py analyze --input-file test_documents/technical_spec.md
python src/cli/security4ai_enhanced.py scan --input-file test_documents/technical_spec.md
python src/cli/obfuscate4ai_enhanced.py measure --input-file test_documents/technical_spec.md
```

## 🚀 Enhanced Features

### Advanced CLI Commands
- **Structured Commands**: `ready4ai analyze`, `security4ai scan`, `obfuscate4ai measure`
- **RAG Optimization**: Built-in chunking strategy recommendations
- **PII Configuration**: Customizable PII detection patterns
- **LLM Suitability**: Private vs public LLM risk analysis
- **Enhanced Output**: Detailed analysis with recommendations

### Enhanced Web Interface
- **Tabbed Interface**: Separate tabs for different user personas
- **Interactive Visualizations**: Charts and graphs for better insights
- **PII Configuration Upload**: Custom PII pattern configuration
- **Feedback System**: Built-in user feedback collection
- **Multiple Export Formats**: JSON, Text, and YAML export options

## 📈 Performance

- **Fast Processing**: Pure NLP algorithms, no external API calls
- **Low Memory**: Efficient document parsing and scoring
- **Scalable**: Handles documents up to 10MB by default
- **Reliable**: No network dependencies or rate limits

## 🚀 Deployment

### Streamlit Cloud (Live)

**🌐 [Try the Live Demo](https://docfit4ai-pky7c2plckscap9eesfkba.streamlit.app/)**

The app is already deployed and ready to use! Simply visit the link above to start assessing your documents.

### Docker Deployment

```bash
# Build and run
docker build -t docfit4ai .
docker run -p 8501:8501 -e GOOGLE_ANALYTICS_ID="G-XXXXXXXXXX" docfit4ai
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📋 Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 📈 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and releases.

## 🆘 Support

- **Documentation**: Check the README and inline comments
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions
- **Email**: docfit4ai@outlook.com

## 🔮 Roadmap

See [NextPhase.md](NextPhase.md) for upcoming features including:
- LLM integration for advanced scoring
- Advanced suggestion system
- Batch processing capabilities
- API endpoints
- Enterprise features
