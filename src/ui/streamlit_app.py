"""
DocFitLabs for AI - Streamlit Console App
====================================

Unified Streamlit interface for all DocFitLabs tools:
- Readiness Scorecard (ready4ai)
- Security Scorecard (security4ai) 
- Obfuscation Scorecard (obfuscate4ai)
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, Any, List
import io

# Add the parent directory to the path to import docfit_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docfit_core.scoring_engine import DocFitScoringEngine, ScoreType
from docfit_core.parsers import TextParser, PDFParser, HTMLParser
from docfit_core.data import DocFitConfig, DocumentModel, DocumentType


class DocFitStreamlitApp:
    """Streamlit application for DocFitLabs tools"""
    
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
    
    def parse_uploaded_file(self, uploaded_file) -> DocumentModel:
        """Parse uploaded file"""
        # Determine file type
        extension = Path(uploaded_file.name).suffix.lower()
        if extension not in self.parsers:
            raise ValueError(f"Unsupported file format: {extension}")
        
        # Read file content
        if extension in ['.pdf']:
            content = uploaded_file.read()
        else:
            content = uploaded_file.read().decode('utf-8')
        
        # Parse document
        parser = self.parsers[extension]
        parsed_data = parser.parse(content, uploaded_file.name)
        
        # Create document model
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
    
    def assess_document(self, document: DocumentModel, score_types: List[ScoreType]) -> Dict[ScoreType, Any]:
        """Assess document with specified score types"""
        scores = self.scoring_engine.score_document(document.content, score_types)
        return scores
    
    def create_score_visualization(self, scores: Dict[ScoreType, Any]) -> go.Figure:
        """Create score visualization"""
        score_data = []
        for score_type, score_result in scores.items():
            score_data.append({
                'Score Type': score_type.value.title(),
                'Overall Score': score_result.overall_score,
                'Category': self.config.get_score_category(score_type.value, score_result.overall_score)
            })
        
        df = pd.DataFrame(score_data)
        
        fig = px.bar(
            df, 
            x='Score Type', 
            y='Overall Score',
            color='Category',
            title='Document Assessment Scores',
            color_discrete_map={
                'excellent': '#2E8B57',
                'good': '#32CD32', 
                'fair': '#FFD700',
                'poor': '#FF8C00',
                'very_poor': '#FF4500'
            }
        )
        
        fig.update_layout(
            yaxis_title="Score",
            xaxis_title="Assessment Type",
            height=400
        )
        
        return fig
    
    def create_component_scores_chart(self, scores: Dict[ScoreType, Any]) -> go.Figure:
        """Create component scores radar chart"""
        fig = go.Figure()
        
        for score_type, score_result in scores.items():
            components = list(score_result.component_scores.keys())
            values = list(score_result.component_scores.values())
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=components,
                fill='toself',
                name=score_type.value.title()
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            title="Component Scores Comparison",
            height=400
        )
        
        return fig


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="DocFitLabs for AI",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize app
    app = DocFitStreamlitApp()
    
    # Header
    st.title("📄 DocFitLabs for AI")
    st.markdown("**Unified Document Assessment Platform**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("🔧 Configuration")
    
    # Assessment type selection
    assessment_types = st.sidebar.multiselect(
        "Select Assessment Types",
        ["Readiness", "Security", "Obfuscation"],
        default=["Readiness"]
    )
    
    # Output format
    output_format = st.sidebar.selectbox(
        "Output Format",
        ["Text", "JSON"],
        index=0
    )
    
    # File upload
    st.header("📁 Document Upload")
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['txt', 'md', 'rst', 'pdf', 'html', 'htm'],
        help="Supported formats: TXT, MD, RST, PDF, HTML"
    )
    
    if uploaded_file is not None:
        try:
            # Parse document
            with st.spinner("Parsing document..."):
                document = app.parse_uploaded_file(uploaded_file)
            
            # Display document info
            st.success(f"✅ Document parsed successfully: {document.filename}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("File Size", f"{document.file_size:,} bytes")
            with col2:
                st.metric("Word Count", f"{document.word_count:,}")
            with col3:
                st.metric("Sentences", f"{document.sentence_count:,}")
            with col4:
                st.metric("Paragraphs", f"{document.paragraph_count:,}")
            
            # Convert assessment types to ScoreType enum
            score_types = []
            if "Readiness" in assessment_types:
                score_types.append(ScoreType.READINESS)
            if "Security" in assessment_types:
                score_types.append(ScoreType.SECURITY)
            if "Obfuscation" in assessment_types:
                score_types.append(ScoreType.OBFUSCATION)
            
            if score_types:
                # Assess document
                with st.spinner("Assessing document..."):
                    scores = app.assess_document(document, score_types)
                
                st.header("📊 Assessment Results")
                
                # Display results
                for score_type, score_result in scores.items():
                    with st.expander(f"🔍 {score_type.value.title()} Assessment", expanded=True):
                        # Overall score
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.metric(
                                "Overall Score",
                                f"{score_result.overall_score:.2f}",
                                help=f"Category: {app.config.get_score_category(score_type.value, score_result.overall_score).upper()}"
                            )
                        
                        with col2:
                            # Progress bar for overall score
                            st.progress(score_result.overall_score)
                        
                        # Component scores
                        st.subheader("📈 Component Scores")
                        component_df = pd.DataFrame([
                            {"Component": comp.replace('_', ' ').title(), "Score": score}
                            for comp, score in score_result.component_scores.items()
                        ])
                        
                        # Create component scores bar chart
                        fig_components = px.bar(
                            component_df,
                            x="Component",
                            y="Score",
                            title=f"{score_type.value.title()} Component Scores",
                            color="Score",
                            color_continuous_scale="RdYlGn"
                        )
                        fig_components.update_layout(height=300)
                        st.plotly_chart(fig_components, use_container_width=True)
                        
                        # Recommendations
                        if score_result.recommendations:
                            st.subheader("💡 Recommendations")
                            for i, rec in enumerate(score_result.recommendations, 1):
                                st.write(f"{i}. {rec}")
                        
                        # Metadata
                        if score_result.metadata:
                            st.subheader("📋 Additional Information")
                            metadata_df = pd.DataFrame([
                                {"Metric": key.replace('_', ' ').title(), "Value": str(value)}
                                for key, value in score_result.metadata.items()
                            ])
                            st.dataframe(metadata_df, use_container_width=True)
                
                # Overall visualization
                if len(scores) > 1:
                    st.header("📊 Overall Assessment")
                    
                    # Score comparison
                    fig_overall = app.create_score_visualization(scores)
                    st.plotly_chart(fig_overall, use_container_width=True)
                    
                    # Component comparison
                    fig_components = app.create_component_scores_chart(scores)
                    st.plotly_chart(fig_components, use_container_width=True)
                
                # Export results
                st.header("💾 Export Results")
                
                if output_format == "JSON":
                    # Prepare JSON export
                    export_data = {
                        "document": {
                            "filename": document.filename,
                            "file_type": document.file_type.value,
                            "file_size": document.file_size,
                            "word_count": document.word_count,
                            "sentence_count": document.sentence_count,
                            "paragraph_count": document.paragraph_count
                        },
                        "assessments": {}
                    }
                    
                    for score_type, score_result in scores.items():
                        export_data["assessments"][score_type.value] = {
                            "overall_score": score_result.overall_score,
                            "category": app.config.get_score_category(score_type.value, score_result.overall_score),
                            "component_scores": score_result.component_scores,
                            "recommendations": score_result.recommendations,
                            "metadata": score_result.metadata
                        }
                    
                    json_str = json.dumps(export_data, indent=2)
                    
                    st.download_button(
                        label="📥 Download JSON Results",
                        data=json_str,
                        file_name=f"{document.filename}_assessment.json",
                        mime="application/json"
                    )
                
                else:  # Text format
                    # Prepare text export
                    text_export = f"DocFitLabs for AI - Assessment Results\n"
                    text_export += f"Document: {document.filename}\n"
                    text_export += f"File Type: {document.file_type.value}\n"
                    text_export += f"File Size: {document.file_size:,} bytes\n"
                    text_export += f"Word Count: {document.word_count:,}\n"
                    text_export += f"Sentences: {document.sentence_count:,}\n"
                    text_export += f"Paragraphs: {document.paragraph_count:,}\n\n"
                    
                    for score_type, score_result in scores.items():
                        text_export += f"{score_type.value.title()} Assessment:\n"
                        text_export += f"  Overall Score: {score_result.overall_score:.2f}\n"
                        text_export += f"  Category: {app.config.get_score_category(score_type.value, score_result.overall_score).upper()}\n"
                        text_export += f"  Component Scores:\n"
                        for comp, score in score_result.component_scores.items():
                            text_export += f"    - {comp.replace('_', ' ').title()}: {score:.2f}\n"
                        if score_result.recommendations:
                            text_export += f"  Recommendations:\n"
                            for i, rec in enumerate(score_result.recommendations, 1):
                                text_export += f"    {i}. {rec}\n"
                        text_export += "\n"
                    
                    st.download_button(
                        label="📥 Download Text Results",
                        data=text_export,
                        file_name=f"{document.filename}_assessment.txt",
                        mime="text/plain"
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
    
    else:
        # Show instructions when no file is uploaded
        st.info("👆 Please upload a document to begin assessment")
        
        st.markdown("### 📋 Supported Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎯 Readiness Assessment**
            - Document structure analysis
            - Clarity and readability scoring
            - Completeness evaluation
            - Formatting assessment
            """)
        
        with col2:
            st.markdown("""
            **🔒 Security Assessment**
            - PII detection and risk scoring
            - Sensitive data pattern analysis
            - Classification risk evaluation
            - DLP compliance checking
            """)
        
        with col3:
            st.markdown("""
            **🎭 Obfuscation Assessment**
            - Complexity analysis
            - IP protection scoring
            - Technical terminology assessment
            - Obfuscation effectiveness
            """)
        
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. **Upload a document** using the file uploader above
        2. **Select assessment types** from the sidebar
        3. **Choose output format** (Text or JSON)
        4. **View results** and recommendations
        5. **Export results** for further analysis
        """)


if __name__ == "__main__":
    main()
