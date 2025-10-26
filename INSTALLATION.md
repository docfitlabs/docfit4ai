# DocFitLabs for AI - Installation Guide

## 🏗️ Build from Source

```bash
# Clone repository
git clone https://github.com/docfitlabs/docfit4ai.git
cd docfit4ai

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run CLI tools
python src/cli/ready4ai_enhanced.py analyze --input-file document.txt
python src/cli/security4ai_enhanced.py scan --input-file document.pdf --config pii.yaml
python src/cli/obfuscate4ai_enhanced.py measure --input-file document.html

# Run web interface
streamlit run src/ui/enhanced_streamlit_app.py
```

## 🚀 Quick Start Examples

### AI Readiness Assessment
```bash
# Analyze document for AI readiness
ready4ai analyze --input-file contract.pdf --output text

# Include RAG chunking strategy
ready4ai analyze --input-file document.txt --output json
```

### Security Analysis
```bash
# Scan document for security risks
security4ai scan --input-file policy.docx --output text

# Use custom PII configuration
security4ai scan --input-file document.pdf --config pii_us.yaml --output json
```

### IP Protection Analysis
```bash
# Measure obfuscation effectiveness
obfuscate4ai measure --input-file trade_secret.txt --output text

# Include LLM suitability analysis
obfuscate4ai measure --input-file technical_doc.pdf --output json
```

### Web Interface
```bash
# Start Streamlit web interface
streamlit run src/ui/enhanced_streamlit_app.py

# Or use Docker
docker run -p 8501:8501 docfit/docfit4ai
```

## 🔧 Configuration

### PII Configuration File
Create a `pii_config.yaml` file for custom PII detection:

```yaml
patterns:
  names:
    - '\b[A-Z][a-z]+ [A-Z][a-z]+\b'
  emails:
    - '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

risk_levels:
  names: medium
  emails: high

compliance_frameworks:
  gdpr: true
  ccpa: true
```

## 🆘 Troubleshooting

### Common Issues

1. **Permission denied errors**
   ```bash
   # Fix executable permissions
   chmod +x $(which ready4ai)
   chmod +x $(which security4ai)
   chmod +x $(which obfuscate4ai)
   ```

2. **Python dependencies missing**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

### Getting Help

- 🐛 **Issues**: [GitHub Issues](https://github.com/docfitlabs/docfit4ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/docfitlabs/docfit4ai/discussions)
- 📧 **Email**: docfit4ai@outlook.com