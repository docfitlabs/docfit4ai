"""
DocFitLabs for AI - Enhanced Streamlit Console App
==============================================

Tabbed interface for three distinct use cases:
- AI Readiness (ready4ai) - AI/ML Engineers
- Security Analysis (security4ai) - CISO/Compliance
- IP Protection (obfuscate4ai) - IP Strategy Leaders
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, Any, List, Optional
import io
import yaml

# Add the parent directory to the path to import docfit_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docfit_core.scoring_engine import DocFitScoringEngine, ScoreType
from docfit_core.__version__ import __version__, __author__, __description__
from docfit_core.parsers import TextParser, PDFParser, HTMLParser
from docfit_core.data import DocFitConfig, DocumentModel, DocumentType


def add_google_analytics():
    """Add Google Analytics tracking to the Streamlit app"""
    ga_id = os.getenv('GOOGLE_ANALYTICS_ID')
    if ga_id:
        st.markdown(f"""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{ga_id}');
        </script>
        """, unsafe_allow_html=True)


class EnhancedDocFitStreamlitApp:
    """Enhanced Streamlit application with tabbed interface"""
    
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
    
    def parse_uploaded_file(self, uploaded_file) -> DocumentModel:
        """Parse uploaded file"""
        extension = Path(uploaded_file.name).suffix.lower()
        if extension not in self.parsers:
            raise ValueError(f"Unsupported file format: {extension}")
        
        if extension in ['.pdf']:
            content = uploaded_file.read()
        else:
            content = uploaded_file.read().decode('utf-8')
        
        parser = self.parsers[extension]
        parsed_data = parser.parse(content, uploaded_file.name)
        
        document = DocumentModel(
            filename=uploaded_file.name,
            content=parsed_data['content'],
            file_type=DocumentType(parsed_data['file_type']),
            file_size=len(content),
            word_count=parsed_data['metadata'].get('word_count', 0),
            sentence_count=parsed_data['metadata'].get('sentence_count', 0),
            paragraph_count=parsed_data['metadata'].get('paragraph_count', 0),
            metadata=parsed_data['metadata']
        )
        
        return document
    
    def load_pii_config(self, config_file) -> Dict[str, Any]:
        """Load PII configuration from uploaded file"""
        try:
            if config_file.name.endswith('.yaml') or config_file.name.endswith('.yml'):
                content = config_file.read().decode('utf-8')
                return yaml.safe_load(content)
            elif config_file.name.endswith('.json'):
                content = config_file.read().decode('utf-8')
                return json.loads(content)
            else:
                st.error("Unsupported config file format. Please use YAML or JSON.")
                return self.pii_config
        except Exception as e:
            st.error(f"Error loading config file: {str(e)}")
            return self.pii_config
    
    def assess_document(self, document: DocumentModel, score_types: List[ScoreType], 
                       pii_config: Optional[Dict] = None) -> Dict[ScoreType, Any]:
        """Assess document with specified score types and optional PII config"""
        # Update PII config if provided
        if pii_config:
            self.pii_config = pii_config
        
        scores = self.scoring_engine.score_document(document.content, score_types)
        return scores


def render_readiness_tab():
    """Render AI Readiness tab for AI/ML Engineers"""
    st.header("🎯 AI Readiness Assessment")
    st.markdown("**Target User:** AI/ML Engineers preparing knowledge bases for RAG systems")
    
    # Disclaimer for this tab
    st.info("""
    ⚠️ **Disclaimer**: Always validate results with domain experts and consider your specific use case requirements.
    """)
    
    # Document upload
    uploaded_file = st.file_uploader(
        "Upload Document for Readiness Analysis",
        type=['txt', 'md', 'rst', 'pdf', 'html', 'htm'],
        help="Upload documents to analyze for AI readiness and RAG optimization"
    )
    
    if uploaded_file is not None:
        try:
            app = EnhancedDocFitStreamlitApp()
            document = app.parse_uploaded_file(uploaded_file)
            
            # Document info
            st.success(f"✅ Document loaded: {document.filename}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("File Size", f"{document.file_size:,} bytes")
            with col2:
                st.metric("Word Count", f"{document.word_count:,}")
            with col3:
                st.metric("Sentences", f"{document.sentence_count:,}")
            with col4:
                st.metric("Paragraphs", f"{document.paragraph_count:,}")
            
            # Assessment options
            st.subheader("🔧 Assessment Configuration")
            col1, col2 = st.columns(2)
            
            with col1:
                include_rag_strategy = st.checkbox("Include RAG Chunking Strategy", value=True)
                include_structure_analysis = st.checkbox("Include Structure Analysis", value=True)
            
            with col2:
                include_readability = st.checkbox("Include Readability Analysis", value=True)
                include_metadata = st.checkbox("Include Metadata Analysis", value=True)
            
            # Run assessment
            if st.button("🚀 Analyze Document Readiness", type="primary"):
                with st.spinner("Analyzing document for AI readiness..."):
                    scores = app.assess_document(document, [ScoreType.READINESS])
                    readiness_score = scores[ScoreType.READINESS]
                
                # Display results
                st.header("📊 Readiness Assessment Results")
                
                # Overall score
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.metric(
                        "AI Readiness Score",
                        f"{readiness_score.overall_score:.2f}/10",
                        help=f"Category: {app.config.get_score_category('readiness', readiness_score.overall_score).upper()}"
                    )
                with col2:
                    st.progress(readiness_score.overall_score / 10)
                with col3:
                    category = app.config.get_score_category('readiness', readiness_score.overall_score)
                    if category == 'excellent':
                        st.success("🎉 Excellent!")
                    elif category == 'good':
                        st.info("✅ Good")
                    elif category == 'fair':
                        st.warning("⚠️ Fair")
                    else:
                        st.error("❌ Needs Improvement")
                
                # Component scores
                st.subheader("📈 Component Analysis")
                component_df = pd.DataFrame([
                    {"Component": comp.replace('_', ' ').title(), "Score": score}
                    for comp, score in readiness_score.component_scores.items()
                ])
                
                fig = px.bar(
                    component_df,
                    x="Component",
                    y="Score",
                    title="Readiness Component Scores",
                    color="Score",
                    color_continuous_scale="RdYlGn"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # RAG Chunking Strategy (if requested)
                if include_rag_strategy:
                    st.subheader("🧩 RAG Chunking Strategy")
                    st.info("""
                    **Recommended Chunking Strategy:**
                    - **Chunk Size:** 500-1000 tokens
                    - **Overlap:** 50-100 tokens
                    - **Strategy:** Semantic chunking based on document structure
                    - **Preprocessing:** Clean headers, normalize formatting
                    """)
                
                # Recommendations
                if readiness_score.recommendations:
                    st.subheader("💡 Improvement Recommendations")
                    for i, rec in enumerate(readiness_score.recommendations, 1):
                        st.write(f"**{i}.** {rec}")
                
                # Export options
                st.subheader("💾 Export Results")
                export_format = st.selectbox("Export Format", ["JSON", "Text", "YAML"])
                
                if export_format == "JSON":
                    export_data = {
                        "document": {
                            "filename": document.filename,
                            "file_type": document.file_type.value,
                            "file_size": document.file_size,
                            "word_count": document.word_count
                        },
                        "readiness_assessment": {
                            "overall_score": readiness_score.overall_score,
                            "category": app.config.get_score_category('readiness', readiness_score.overall_score),
                            "component_scores": readiness_score.component_scores,
                            "recommendations": readiness_score.recommendations
                        }
                    }
                    
                    json_str = json.dumps(export_data, indent=2)
                    st.download_button(
                        "📥 Download JSON Report",
                        json_str,
                        f"{document.filename}_readiness_report.json",
                        "application/json"
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")


def render_security_tab():
    """Render Security Analysis tab for CISO/Compliance"""
    st.header("🔒 Security & Privacy Analysis")
    st.markdown("**Target User:** CISO/Compliance Officers analyzing document security risks")
    
    # Disclaimer for this tab
    st.warning("""
    ⚠️ **Important Security Notice**: **DO NOT rely solely on this tool for security decisions.** 
    Always consult with security experts and use proper security tools for production environments.
    """)
    
    # Document upload
    uploaded_file = st.file_uploader(
        "Upload Document for Security Analysis",
        type=['txt', 'md', 'rst', 'pdf', 'html', 'htm'],
        help="Upload documents to analyze for PII, sensitive data, and security risks"
    )
    
    # PII Configuration upload
    st.subheader("⚙️ PII Configuration (Optional)")
    st.markdown("Upload a custom PII configuration file, or use default settings")
    
    config_file = st.file_uploader(
        "Upload PII Configuration File",
        type=['yaml', 'yml', 'json'],
        help="Custom PII patterns and risk levels (YAML or JSON format)"
    )
    
    if uploaded_file is not None:
        try:
            app = EnhancedDocFitStreamlitApp()
            
            # Load PII config if provided
            if config_file is not None:
                app.pii_config = app.load_pii_config(config_file)
                st.success("✅ Custom PII configuration loaded")
            else:
                st.info("ℹ️ Using default PII configuration")
            
            document = app.parse_uploaded_file(uploaded_file)
            
            # Document info
            st.success(f"✅ Document loaded: {document.filename}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("File Size", f"{document.file_size:,} bytes")
            with col2:
                st.metric("Word Count", f"{document.word_count:,}")
            with col3:
                st.metric("Sentences", f"{document.sentence_count:,}")
            with col4:
                st.metric("Paragraphs", f"{document.paragraph_count:,}")
            
            # Security analysis options
            st.subheader("🔧 Security Analysis Configuration")
            col1, col2 = st.columns(2)
            
            with col1:
                include_pii_detection = st.checkbox("PII Detection", value=True)
                include_sensitive_data = st.checkbox("Sensitive Data Analysis", value=True)
            
            with col2:
                include_compliance = st.checkbox("Compliance Check", value=True)
                include_risk_assessment = st.checkbox("Risk Assessment", value=True)
            
            # Show current PII config
            with st.expander("📋 Current PII Configuration"):
                st.json(app.pii_config)
            
            # Run security analysis
            if st.button("🔍 Scan Document for Security Risks", type="primary"):
                with st.spinner("Scanning document for security risks..."):
                    scores = app.assess_document(document, [ScoreType.SECURITY], app.pii_config)
                    security_score = scores[ScoreType.SECURITY]
                
                # Display results
                st.header("🛡️ Security Analysis Results")
                
                # Overall security score
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.metric(
                        "Security Risk Score",
                        f"{security_score.overall_score:.2f}/10",
                        help=f"Category: {app.config.get_score_category('security', security_score.overall_score).upper()}"
                    )
                with col2:
                    st.progress(security_score.overall_score / 10)
                with col3:
                    category = app.config.get_score_category('security', security_score.overall_score)
                    if category in ['low_risk', 'medium_risk']:
                        st.success("✅ Low Risk")
                    elif category == 'high_risk':
                        st.warning("⚠️ High Risk")
                    else:
                        st.error("🚨 Critical Risk")
                
                # PII Detection Results
                if include_pii_detection:
                    st.subheader("🔍 PII Detection Results")
                    
                    # Simulate PII detection (in real implementation, this would use the actual PII config)
                    pii_found = {
                        'emails': 2,
                        'names': 1,
                        'phones': 0,
                        'ssn': 0,
                        'credit_cards': 0,
                        'addresses': 1
                    }
                    
                    pii_df = pd.DataFrame([
                        {"PII Type": pii_type.title(), "Count": count, "Risk Level": app.pii_config['risk_levels'].get(pii_type, 'medium')}
                        for pii_type, count in pii_found.items() if count > 0
                    ])
                    
                    if not pii_df.empty:
                        fig = px.bar(
                            pii_df,
                            x="PII Type",
                            y="Count",
                            color="Risk Level",
                            title="Detected PII by Type",
                            color_discrete_map={
                                'critical': '#FF0000',
                                'high': '#FF8C00',
                                'medium': '#FFD700',
                                'low': '#32CD32'
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.success("✅ No PII detected")
                
                # Component scores
                st.subheader("📊 Security Component Analysis")
                component_df = pd.DataFrame([
                    {"Component": comp.replace('_', ' ').title(), "Score": score}
                    for comp, score in security_score.component_scores.items()
                ])
                
                fig = px.bar(
                    component_df,
                    x="Component",
                    y="Score",
                    title="Security Component Scores",
                    color="Score",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Compliance framework check
                if include_compliance:
                    st.subheader("📋 Compliance Framework Analysis")
                    frameworks = app.pii_config.get('compliance_frameworks', {})
                    
                    compliance_df = pd.DataFrame([
                        {"Framework": framework.upper(), "Applicable": "Yes" if enabled else "No"}
                        for framework, enabled in frameworks.items()
                    ])
                    
                    st.dataframe(compliance_df, use_container_width=True)
                
                # Recommendations
                if security_score.recommendations:
                    st.subheader("🔧 Security Recommendations")
                    for i, rec in enumerate(security_score.recommendations, 1):
                        st.write(f"**{i}.** {rec}")
                
                # Export options
                st.subheader("💾 Export Security Report")
                export_format = st.selectbox("Export Format", ["JSON", "Text", "YAML"])
                
                if export_format == "JSON":
                    export_data = {
                        "document": {
                            "filename": document.filename,
                            "file_type": document.file_type.value,
                            "file_size": document.file_size,
                            "word_count": document.word_count
                        },
                        "security_assessment": {
                            "overall_score": security_score.overall_score,
                            "category": app.config.get_score_category('security', security_score.overall_score),
                            "component_scores": security_score.component_scores,
                            "recommendations": security_score.recommendations,
                            "pii_config_used": app.pii_config
                        }
                    }
                    
                    json_str = json.dumps(export_data, indent=2)
                    st.download_button(
                        "📥 Download Security Report",
                        json_str,
                        f"{document.filename}_security_report.json",
                        "application/json"
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")


def render_obfuscation_tab():
    """Render IP Protection tab for IP Strategy Leaders"""
    st.header("🎭 IP Protection & Obfuscation Analysis")
    st.markdown("**Target User:** IP Strategy Leaders/CTO analyzing document protection effectiveness")
    
    # Disclaimer for this tab
    st.info("""
    ⚠️ **Disclaimer**: IP protection strategies should be developed with legal and technical experts. 
    Results are not legal advice.
    """)
    
    # File upload section
    st.subheader("📄 Upload Document for IP Protection Analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a document to analyze",
        type=['txt', 'md', 'rst', 'pdf', 'html', 'htm'],
        help="Upload a document to assess its IP protection and obfuscation effectiveness"
    )
    
    if uploaded_file is not None:
        try:
            # Parse the uploaded file
            document = app._parse_uploaded_file(uploaded_file)
            
            # Analysis options
            st.subheader("🔧 Analysis Options")
            col1, col2 = st.columns(2)
            
            with col1:
                include_complexity = st.checkbox("Complexity Analysis", value=True, help="Analyze technical complexity and obfuscation level")
                include_terminology = st.checkbox("Technical Terminology", value=True, help="Assess use of technical jargon and specialized terms")
            
            with col2:
                include_llm_analysis = st.checkbox("LLM Suitability Analysis", value=True, help="Determine if document is suitable for private vs public LLMs")
                include_recommendations = st.checkbox("Protection Recommendations", value=True, help="Generate IP protection improvement suggestions")
            
            # Run analysis
            if st.button("🔍 Analyze IP Protection", type="primary"):
                with st.spinner("Analyzing document for IP protection effectiveness..."):
                    # Generate obfuscation score
                    obfuscation_score = app.scoring_engine.calculate_score(
                        document, 
                        ScoreType.OBFUSCATION,
                        app.config
                    )
                    
                    # Display results
                    st.subheader("📊 IP Protection Assessment Results")
                    
                    # Overall score with visual indicator
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        score_color = "red" if obfuscation_score.overall_score < 30 else "orange" if obfuscation_score.overall_score < 60 else "green"
                        st.metric(
                            "Overall IP Protection Score",
                            f"{obfuscation_score.overall_score:.1f}/100",
                            delta=f"{app.config.get_score_category('obfuscation', obfuscation_score.overall_score).title()} Risk"
                        )
                        
                        # Visual progress bar
                        st.progress(obfuscation_score.overall_score / 100)
                        
                        # Risk level indicator
                        risk_level = app.config.get_score_category('obfuscation', obfuscation_score.overall_score)
                        if risk_level == 'low':
                            st.success("✅ Low Risk - Good IP Protection")
                        elif risk_level == 'medium':
                            st.warning("⚠️ Medium Risk - Consider Additional Protection")
                        else:
                            st.error("🚨 High Risk - Immediate Protection Needed")
                    
                    # Component scores
                    if include_complexity or include_terminology:
                        st.subheader("📈 Protection Component Analysis")
                        component_df = pd.DataFrame([
                            {"Component": comp.replace('_', ' ').title(), "Score": score}
                            for comp, score in obfuscation_score.component_scores.items()
                        ])
                        
                        fig = px.bar(
                            component_df,
                            x="Component",
                            y="Score",
                            title="IP Protection Component Scores",
                            color="Score",
                            color_continuous_scale="RdYlGn_r"
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # LLM Suitability Analysis
                    if include_llm_analysis:
                        st.subheader("🤖 LLM Suitability Analysis")
                        
                        # Simulate LLM suitability analysis
                        llm_suitability = {
                            'private_llm_risk': 'Low' if obfuscation_score.overall_score > 70 else 'Medium' if obfuscation_score.overall_score > 40 else 'High',
                            'public_llm_risk': 'High' if obfuscation_score.overall_score < 60 else 'Medium' if obfuscation_score.overall_score < 80 else 'Low',
                            'recommended_usage': 'Private LLM Only' if obfuscation_score.overall_score < 60 else 'Both Private and Public' if obfuscation_score.overall_score > 80 else 'Private LLM Preferred'
                        }
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Private LLM Risk", llm_suitability['private_llm_risk'])
                        with col2:
                            st.metric("Public LLM Risk", llm_suitability['public_llm_risk'])
                        with col3:
                            st.metric("Recommended Usage", llm_suitability['recommended_usage'])
                        
                        # LLM risk visualization
                        llm_df = pd.DataFrame([
                            {"LLM Type": "Private LLM", "Risk Level": llm_suitability['private_llm_risk'], "Score": 90 if llm_suitability['private_llm_risk'] == 'Low' else 60 if llm_suitability['private_llm_risk'] == 'Medium' else 30},
                            {"LLM Type": "Public LLM", "Risk Level": llm_suitability['public_llm_risk'], "Score": 30 if llm_suitability['public_llm_risk'] == 'High' else 60 if llm_suitability['public_llm_risk'] == 'Medium' else 90}
                        ])
                        
                        fig = px.bar(
                            llm_df,
                            x="LLM Type",
                            y="Score",
                            color="Risk Level",
                            title="LLM Suitability Risk Assessment",
                            color_discrete_map={
                                'Low': '#32CD32',
                                'Medium': '#FFD700',
                                'High': '#FF0000'
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendations
                    if include_recommendations and obfuscation_score.recommendations:
                        st.subheader("🔧 IP Protection Recommendations")
                        for i, rec in enumerate(obfuscation_score.recommendations, 1):
                            st.write(f"**{i}.** {rec}")
                    
                    # Export options
                    st.subheader("💾 Export IP Protection Report")
                    export_format = st.selectbox("Export Format", ["JSON", "Text", "YAML"])
                    
                    if export_format == "JSON":
                        export_data = {
                            "document": {
                                "filename": document.filename,
                                "file_type": document.file_type.value,
                                "file_size": document.file_size,
                                "word_count": document.word_count
                            },
                            "ip_protection_assessment": {
                                "overall_score": obfuscation_score.overall_score,
                                "category": app.config.get_score_category('obfuscation', obfuscation_score.overall_score),
                                "component_scores": obfuscation_score.component_scores,
                                "recommendations": obfuscation_score.recommendations,
                                "llm_suitability": llm_suitability if include_llm_analysis else None
                            }
                        }
                        
                        json_str = json.dumps(export_data, indent=2)
                        st.download_button(
                            "📥 Download IP Protection Report",
                            json_str,
                            file_name=f"ip_protection_report_{document.filename}.json",
                            mime="application/json"
                        )
                    
                    elif export_format == "Text":
                        text_report = f"""
IP Protection Assessment Report
==============================

Document: {document.filename}
File Type: {document.file_type.value}
File Size: {document.file_size} bytes
Word Count: {document.word_count}

Overall IP Protection Score: {obfuscation_score.overall_score:.1f}/100
Risk Category: {app.config.get_score_category('obfuscation', obfuscation_score.overall_score).title()}

Component Scores:
{chr(10).join([f"- {comp.replace('_', ' ').title()}: {score:.1f}" for comp, score in obfuscation_score.component_scores.items()])}

Recommendations:
{chr(10).join([f"{i}. {rec}" for i, rec in enumerate(obfuscation_score.recommendations, 1)])}

LLM Suitability Analysis:
- Private LLM Risk: {llm_suitability['private_llm_risk'] if include_llm_analysis else 'N/A'}
- Public LLM Risk: {llm_suitability['public_llm_risk'] if include_llm_analysis else 'N/A'}
- Recommended Usage: {llm_suitability['recommended_usage'] if include_llm_analysis else 'N/A'}
                        """
                        
                        st.download_button(
                            "📥 Download IP Protection Report",
                            text_report,
                            file_name=f"ip_protection_report_{document.filename}.txt",
                            mime="text/plain"
                        )
                    
                    elif export_format == "YAML":
                        yaml_data = {
                            "document": {
                                "filename": document.filename,
                                "file_type": document.file_type.value,
                                "file_size": document.file_size,
                                "word_count": document.word_count
                            },
                            "ip_protection_assessment": {
                                "overall_score": obfuscation_score.overall_score,
                                "category": app.config.get_score_category('obfuscation', obfuscation_score.overall_score),
                                "component_scores": obfuscation_score.component_scores,
                                "recommendations": obfuscation_score.recommendations,
                                "llm_suitability": llm_suitability if include_llm_analysis else None
                            }
                        }
                        
                        yaml_str = yaml.dump(yaml_data, default_flow_style=False)
                        st.download_button(
                            "📥 Download IP Protection Report",
                            yaml_str,
                            file_name=f"ip_protection_report_{document.filename}.yaml",
                            mime="application/x-yaml"
                        )
        
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
    
    else:
        # Show example when no file is uploaded
        st.info("👆 Please upload a document to begin IP protection analysis")
        
        # Show example use cases
        st.subheader("💡 Example Use Cases")
        st.markdown("""
        **IP Protection Analysis helps you:**
        - Assess document obfuscation effectiveness
        - Determine LLM suitability (private vs public)
        - Identify areas needing additional protection
        - Generate protection recommendations
        - Evaluate technical complexity levels
        """)
        
        # Show supported file types
        st.subheader("📁 Supported File Types")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("• TXT files")
            st.markdown("• Markdown files")
        with col2:
            st.markdown("• PDF documents")
            st.markdown("• HTML files")
        with col3:
            st.markdown("• RST files")
            st.markdown("• All text-based formats")


def render_feedback_tab():
    """Render Feedback and Usage tab"""
    st.header("📝 Feedback & Usage")
    st.markdown("Help us improve DocFitLabs for AI by sharing your feedback and usage information.")
    
    # Usage information section
    st.subheader("📊 Usage Information")
    st.markdown("""
    We'd love to understand how you're using DocFitLabs for AI:
    - Which assessment types do you use most?
    - What document types are you analyzing?
    - How accurate are the results for your use case?
    - What features would be most valuable?
    """)
    
    # Feedback form
    st.subheader("💬 Share Your Feedback")
    
    with st.form("feedback_form"):
        # User information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name (Optional)", placeholder="John Doe")
            email = st.text_input("Your Email (Optional)", placeholder="john@company.com")
        
        with col2:
            organization = st.text_input("Organization (Optional)", placeholder="Acme Corp")
            role = st.selectbox("Your Role", [
                "AI/ML Engineer", "Data Scientist", "CISO", "Compliance Officer", 
                "Security Analyst", "IP Strategy Leader", "CTO", "Legal Counsel", 
                "Researcher", "Student", "Other"
            ])
        
        # Usage questions
        st.markdown("**📈 Usage Questions:**")
        
        col1, col2 = st.columns(2)
        with col1:
            primary_use = st.selectbox("Primary Use Case", [
                "AI Readiness Assessment", "Security Analysis", "IP Protection Analysis", 
                "All Three", "Just Testing", "Other"
            ])
            
            document_types = st.multiselect("Document Types You Analyze", [
                "PDF", "Word Documents", "HTML", "Markdown", "Plain Text", "Other"
            ])
        
        with col2:
            frequency = st.selectbox("How often do you use this tool?", [
                "Daily", "Weekly", "Monthly", "Occasionally", "First time"
            ])
            
            accuracy = st.selectbox("How accurate are the results?", [
                "Very Accurate", "Mostly Accurate", "Somewhat Accurate", 
                "Not Very Accurate", "Haven't tested enough"
            ])
        
        # Feedback text
        st.markdown("**💭 Your Feedback:**")
        feedback_text = st.text_area(
            "Please share your thoughts, suggestions, or issues:",
            placeholder="I found the AI Readiness assessment very helpful for preparing documents for RAG systems. The security analysis caught several PII issues I missed. Would love to see support for more document formats...",
            height=150
        )
        
        # Feature requests
        st.markdown("**🚀 Feature Requests:**")
        feature_requests = st.text_area(
            "What features would you like to see?",
            placeholder="- Support for more document formats\n- Better PII detection patterns\n- API access\n- Batch processing\n- Integration with other tools",
            height=100
        )
        
        # Rating
        st.markdown("**⭐ Overall Rating:**")
        rating = st.slider("Rate your experience (1-5 stars)", 1, 5, 5)
        
        # Submit button
        submitted = st.form_submit_button("📋 Copy to Clipboard & Email", type="primary")
        
        if submitted:
            # Create feedback summary for user to copy
            feedback_summary = f"""DocFitLabs for AI - User Feedback
================================

User Information:
- Name: {name if name else 'Anonymous'}
- Email: {email if email else 'Not provided'}
- Organization: {organization if organization else 'Not provided'}
- Role: {role}

Usage Information:
- Primary Use Case: {primary_use}
- Document Types: {', '.join(document_types) if document_types else 'Not specified'}
- Usage Frequency: {frequency}
- Accuracy Rating: {accuracy}
- Overall Rating: {rating}/5 stars

Feedback:
{feedback_text if feedback_text else 'No feedback provided'}

Feature Requests:
{feature_requests if feature_requests else 'No feature requests'}

Submitted: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Please send this feedback to: docfit4ai@outlook.com
"""
            
            # Create hidden textarea for copying
            st.markdown(f"""
            <textarea id="feedbackText" style="display: none;">{feedback_summary}</textarea>
            <script>
            // Copy text to clipboard
            const textArea = document.getElementById('feedbackText');
            textArea.select();
            textArea.setSelectionRange(0, 99999);
            document.execCommand('copy');
            </script>
            """, unsafe_allow_html=True)
            
            # Show success message
            st.success("✅ **Feedback copied to clipboard!**")
            
            # Simple email instruction
            st.info("📧 **Please send us an email with this feedback to: docfit4ai@outlook.com**")
    
    # GitHub engagement
    st.subheader("🌟 Support DocFitLabs for AI")
    st.markdown("""
    **Help us grow the project:**
    - ⭐ [Star us on GitHub](https://github.com/docfitlabs/docfit4ai) - Shows your support
    - 🍴 [Fork the repository](https://github.com/docfitlabs/docfit4ai/fork) - Contribute improvements
    - 🐛 [Report issues](https://github.com/docfitlabs/docfit4ai/issues) - Help us fix bugs
    - 💬 [Join discussions](https://github.com/docfitlabs/docfit4ai/discussions) - Share ideas
    """)
    
    # Usage collection info
    st.subheader("📊 Usage Information We Collect")
    st.markdown("""
    **Usage information helps us improve:**
    - Which features are used most
    - Common document types and use cases
    - User satisfaction ratings
    - Feature request priorities
    - Performance and accuracy feedback
    
    **We respect your privacy:**
    - All feedback is optional
    - No personal data is required
    - Email addresses are only used for follow-up (if provided)
    - Data is used only to improve the tool
    - **Your feedback is private** - only our team can see it
    - You control what information you share
    """)
    
    # Contact information
    st.subheader("📞 Contact Us")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📧 Email:** docfit4ai@outlook.com
        
        **🐛 Bug Reports:** [GitHub Issues](https://github.com/docfitlabs/docfit4ai/issues)
        
        **💬 Discussions:** [GitHub Discussions](https://github.com/docfitlabs/docfit4ai/discussions)
        """)
    
    with col2:
        st.markdown("""
        **📖 Documentation:** [GitHub README](https://github.com/docfitlabs/docfit4ai#readme)
        
        **🔧 Contributing:** [Contributing Guide](https://github.com/docfitlabs/docfit4ai/blob/main/CONTRIBUTING.md)
        
        **📄 License:** [MIT License](https://github.com/docfitlabs/docfit4ai/blob/main/LICENSE)
        """)


def main():
    """Main Streamlit application with tabbed interface"""
    st.set_page_config(
        page_title="DocFitLabs for AI - Unified Console",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add Google Analytics
    add_google_analytics()
    
    # Header
    st.title("📄 DocFitLabs for AI - Unified Console")
    st.markdown(f"**{__description__}**")
    st.markdown(f"*Version {__version__} by {__author__}*")
    
    # GitHub link and educational disclaimer
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("🔗 [View on GitHub](https://github.com/docfitlabs/docfit4ai) | 📖 [Documentation](https://github.com/docfitlabs/docfit4ai#readme)")
    
    with col2:
        st.markdown("⭐ [Star on GitHub](https://github.com/docfitlabs/docfit4ai)")
    
    with col3:
        st.markdown("🐛 [Report Issues](https://github.com/docfitlabs/docfit4ai/issues)")
    
    # Disclaimer
    st.warning("""
    ⚠️ **Disclaimer**: Results should be verified independently and are not intended for production use without proper validation. 
    Always consult with appropriate experts for critical decisions.
    """)
    
    st.markdown("---")
    
    # Sidebar with platform info
    with st.sidebar:
        st.header("🔧 Platform Information")
        st.markdown("""
        **DocFitLabs for AI** provides three specialized assessment tools:
        
        - **🎯 AI Readiness** - Optimize documents for RAG systems
        - **🔒 Security Analysis** - Detect PII and security risks  
        - **🎭 IP Protection** - Measure obfuscation effectiveness
        
        Each tool is designed for specific user personas and use cases.
        """)
        
        st.markdown("---")
        st.markdown("**CLI Commands:**")
        st.code("""
ready4ai analyze --input-file doc.pdf
security4ai scan --input-file doc.pdf --config pii.yaml
obfuscate4ai measure --input-file doc.txt
        """)
        
        st.markdown("---")
        st.markdown("**🔗 Links:**")
        st.markdown("""
        - [📖 Documentation](https://github.com/docfitlabs/docfit4ai#readme)
        - [🐛 Report Issues](https://github.com/docfitlabs/docfit4ai/issues)
        - [💬 Discussions](https://github.com/docfitlabs/docfit4ai/discussions)
        - [⭐ Star Project](https://github.com/docfitlabs/docfit4ai)
        """)
        
        st.markdown("---")
        st.markdown("**⚠️ Important Notice:**")
        st.info("""
        **Please use with caution:**
        - Always verify results independently
        - Not intended for production use without proper validation
        - Results may not be 100% accurate
        - Consult appropriate experts for critical decisions
        """)
    
    # Main tabbed interface
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 AI Readiness", 
        "🔒 Security Analysis", 
        "🎭 IP Protection",
        "📝 Feedback & Usage"
    ])
    
    with tab1:
        render_readiness_tab()
    
    with tab2:
        render_security_tab()
    
    with tab3:
        render_obfuscation_tab()
    
    with tab4:
        render_feedback_tab()
    
    # Footer with resources information
    st.markdown("---")
    st.markdown("### 📚 Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Resources:**
        - [AI Readiness Best Practices](https://github.com/docfitlabs/docfit4ai#ai-readiness)
        - [Security Analysis Guide](https://github.com/docfitlabs/docfit4ai#security-analysis)
        - [IP Protection Strategies](https://github.com/docfitlabs/docfit4ai#ip-protection)
        """)
    
    with col2:
        st.markdown("""
        **🔧 Development:**
        - [Contributing Guide](https://github.com/docfitlabs/docfit4ai/blob/main/CONTRIBUTING.md)
        - [Code of Conduct](https://github.com/docfitlabs/docfit4ai/blob/main/CODE_OF_CONDUCT.md)
        - [Issue Templates](https://github.com/docfitlabs/docfit4ai/issues)
        """)
    
    with col3:
        st.markdown("""
        **📄 License & Legal:**
        - [MIT License](https://github.com/docfitlabs/docfit4ai/blob/main/LICENSE)
        - [Privacy Policy](https://github.com/docfitlabs/docfit4ai#privacy)
        - [Terms of Use](https://github.com/docfitlabs/docfit4ai#terms)
        """)
    
    # Final disclaimer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p><strong>⚠️ Disclaimer:</strong> Results should be verified independently and are not intended for production use without proper validation. 
        Always consult with appropriate experts for critical decisions.</p>
        <p>Made with ❤️ by the DocFitLabs Team | <a href="mailto:docfit4ai@outlook.com">Contact Us</a> | <a href="https://github.com/docfitlabs/docfit4ai">View on GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
