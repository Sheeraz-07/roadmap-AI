"""
Streamlit web interface for the Multi-Agent Project Refiner AI System
"""
import streamlit as st
import os
from datetime import datetime
from multi_agent_orchestrator import ProjectRefinerAPI

# Page configuration
st.set_page_config(
    page_title="AI Project Refiner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🤖 Multi-Agent Project Refiner")
    st.markdown("### Transform your project ideas into comprehensive roadmaps using AI collaboration")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # System information
        st.subheader("System Info")
        st.info("""
        **Strategist**: GPT-4.1 (OpenAI)
        **Refiner**: Gemini Pro (Google)
        **Iterations**: 3 rounds of refinement
        **API Keys**: Loaded from .env file
        """)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Project Description")
        project_input = st.text_area(
            "Describe your project requirements, goals, and constraints:",
            height=300,
            placeholder="""Example:
I want to build a mobile app for fitness tracking that includes:
- User authentication and profiles
- Workout logging with exercise database
- Progress tracking with charts
- Social features for sharing achievements
- Integration with wearable devices
- Offline capability for workouts

Budget: $50,000
Timeline: 6 months
Team: 2 developers, 1 designer
Target platforms: iOS and Android
..."""
        )
        
        # Processing options
        col_a, col_b = st.columns(2)
        with col_a:
            show_detailed = st.checkbox("Show detailed processing info", value=False)
        with col_b:
            auto_process = st.checkbox("Auto-process on input change", value=False)
    
    with col2:
        st.subheader("Quick Examples")
        
        examples = {
            "Mobile App": "Build a social media mobile app with user profiles, photo sharing, messaging, and real-time notifications. Budget: $75k, Timeline: 8 months, Team: 3 developers.",
            "Web Platform": "Create an e-learning platform with course management, video streaming, quizzes, certificates, and payment processing. Target: 10k users, Budget: $100k.",
            "AI System": "Develop an AI-powered customer service chatbot with NLP, multi-language support, CRM integration, and analytics dashboard. Enterprise-grade security required."
        }
        
        for title, example in examples.items():
            if st.button(f"Load {title} Example", use_container_width=True):
                st.session_state.example_input = example
        
        if 'example_input' in st.session_state:
            project_input = st.session_state.example_input
            del st.session_state.example_input
    
    # Process button
    if st.button("🚀 Generate Refined Roadmap", type="primary", use_container_width=True):
        if not project_input.strip():
            st.error("Please provide a project description")
            return
        
        # Check if API keys are available from .env file
        try:
            from config import Config
            Config.validate_config()
        except ValueError as e:
            st.error(f"API Configuration Error: {str(e)}")
            st.info("Please ensure your .env file contains valid OPENAI_API_KEY and GEMINI_API_KEY")
            return
        
        # Processing
        with st.spinner("🤖 AI agents are collaborating on your roadmap..."):
            try:
                # Initialize API
                api = ProjectRefinerAPI()
                
                # Process project
                if show_detailed:
                    result = api.refine_project_detailed(project_input)
                    roadmap = result['roadmap']
                    metadata = result['metadata']
                else:
                    roadmap = api.refine_project(project_input)
                    metadata = None
                
                # Display results
                st.success("✅ Roadmap generated successfully!")
                
                # Show metadata if requested
                if metadata:
                    with st.expander("Processing Details"):
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("Processing Type", metadata['processing_type'].title())
                        with col_m2:
                            st.metric("Total Tokens", f"{metadata['total_tokens']:,}")
                        with col_m3:
                            st.metric("Processing Time", f"{metadata['processing_time']:.1f}s")
                
                # Display roadmap
                st.subheader("📋 Your Refined Project Roadmap")
                st.markdown(roadmap)
                
                # Download option
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"project_roadmap_{timestamp}.md"
                
                st.download_button(
                    label="📥 Download Roadmap",
                    data=roadmap,
                    file_name=filename,
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")
                st.info("Please check your API keys and try again")

if __name__ == "__main__":
    main()
