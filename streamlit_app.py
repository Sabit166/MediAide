"""
MediAide Streamlit UI
A beautiful web interface for the MediAide AI-Powered Medical Assistant
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import the main application
try:
    from src.main.app import MediAide
except ImportError as e:
    st.error(f"Failed to import MediAide application: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="MediAide - AI Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .status-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .tool-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .response-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin-top: 1rem;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'app' not in st.session_state:
    st.session_state.app = None
    st.session_state.initialized = False
    st.session_state.conversation_history = []

def initialize_app():
    """Initialize the MediAide application."""
    if not st.session_state.initialized:
        with st.spinner("🚀 Initializing MediAide application..."):
            try:
                st.session_state.app = MediAide()
                success = st.session_state.app.initialize()
                if success:
                    st.session_state.initialized = True
                    st.success("✅ MediAide initialized successfully!")
                    return True
                else:
                    st.error("❌ Failed to initialize MediAide")
                    return False
            except Exception as e:
                st.error(f"❌ Error initializing MediAide: {e}")
                return False
    return True

def display_header():
    """Display the main header."""
    st.markdown('<div class="main-header">🏥 MediAide</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Medical Assistant</div>', unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with navigation and status."""
    st.sidebar.title("🔧 Control Panel")
    
    # Status section
    st.sidebar.subheader("📊 System Status")
    
    if st.session_state.initialized and st.session_state.app:
        status = st.session_state.app.get_status()
        
        # Display status indicators
        st.sidebar.markdown("**Initialization:**")
        st.sidebar.markdown(f"✅ {'Initialized' if status['initialized'] else '❌ Not Initialized'}")
        
        st.sidebar.markdown("**Available Tools:**")
        tools_status = status['tools']
        for tool, available in tools_status.items():
            icon = "✅" if available else "❌"
            tool_name = tool.replace('_', ' ').title()
            st.sidebar.markdown(f"{icon} {tool_name}")
        
        st.sidebar.markdown("**Environment:**")
        env_status = status['environment']
        for env, available in env_status.items():
            icon = "✅" if available else "❌"
            env_name = env.replace('_', ' ').title()
            st.sidebar.markdown(f"{icon} {env_name}")
    else:
        st.sidebar.warning("Application not initialized")
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧭 Navigation")
    
    return st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "🔍 Query Tools", "📊 Analytics", "📋 History", "⚙️ Settings"]
    )

def display_query_interface():
    """Display the main query interface."""
    st.subheader("🤖 Ask MediAide")
    
    # Query input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your medical question:",
            placeholder="e.g., What are the symptoms of diabetes?",
            key="main_query"
        )
    
    with col2:
        query_type = st.selectbox(
            "Query Type:",
            ["🌐 Web Search", "📈 Diabetes DB", "🩺 Cancer DB", "❤️ Heart Disease DB", "🔄 All Sources"]
        )
    
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if query:
            process_query(query, query_type)
        else:
            st.warning("Please enter a question first!")

def process_query(query: str, query_type: str):
    """Process the user query and display results."""
    if not st.session_state.initialized or not st.session_state.app:
        st.error("Application not initialized. Please refresh the page.")
        return
    
    start_time = time.time()
    
    with st.spinner(f"Processing your query: {query}"):
        try:
            # Route query based on type
            if query_type == "🌐 Web Search":
                response = st.session_state.app.search_web(query)
            elif query_type == "📈 Diabetes DB":
                response = st.session_state.app.query_diabetes(query)
            elif query_type == "🩺 Cancer DB":
                response = st.session_state.app.query_cancer(query)
            elif query_type == "❤️ Heart Disease DB":
                response = st.session_state.app.query_heart_disease(query)
            elif query_type == "🔄 All Sources":
                response = st.session_state.app.get_comprehensive_answer(query)
                display_comprehensive_response(query, response, time.time() - start_time)
                return
            else:
                st.error("Unknown query type")
                return
            
            # Display single response
            display_single_response(query, response, query_type, time.time() - start_time)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "timestamp": datetime.now(),
                "query": query,
                "query_type": query_type,
                "response": response,
                "response_time": time.time() - start_time
            })
            
        except Exception as e:
            st.error(f"Error processing query: {e}")

def display_single_response(query: str, response: dict, query_type: str, response_time: float):
    """Display a single response."""
    st.markdown("---")
    st.subheader(f"🔍 Results for: *{query}*")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Source:** {query_type}")
    with col2:
        st.markdown(f"**Time:** {response_time:.2f}s")
    with col3:
        status_icon = "✅" if response.get('success', True) else "❌"
        st.markdown(f"**Status:** {status_icon}")
    
    if response.get('success', True):
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.markdown(response.get('answer', 'No answer provided'))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown(f"Error: {response.get('answer', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_comprehensive_response(query: str, response: dict, response_time: float):
    """Display comprehensive response from multiple sources."""
    st.markdown("---")
    st.subheader(f"🔍 Comprehensive Results for: *{query}*")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**Sources:** {len(response.get('responses', {}))}")
    with col2:
        st.markdown(f"**Total Time:** {response_time:.2f}s")
    
    # Display each source response
    responses = response.get('responses', {})
    
    for source, result in responses.items():
        with st.expander(f"📝 {source.replace('_', ' ').title()}", expanded=True):
            if result.get('success', True):
                st.markdown(result.get('answer', 'No answer provided'))
            else:
                st.error(f"Error: {result.get('answer', 'Unknown error')}")
    
    # Add to conversation history
    st.session_state.conversation_history.append({
        "timestamp": datetime.now(),
        "query": query,
        "query_type": "🔄 All Sources",
        "response": response,
        "response_time": response_time
    })

def display_analytics():
    """Display analytics and visualizations."""
    st.subheader("📊 Analytics Dashboard")
    
    if not st.session_state.conversation_history:
        st.info("No conversation history available yet. Start asking questions to see analytics!")
        return
    
    # Create analytics from conversation history
    df = pd.DataFrame(st.session_state.conversation_history)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Query types distribution
        query_type_counts = df['query_type'].value_counts()
        fig_pie = px.pie(
            values=query_type_counts.values,
            names=query_type_counts.index,
            title="Query Types Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Response times over time
        df['timestamp_str'] = df['timestamp'].dt.strftime('%H:%M:%S')
        fig_line = px.line(
            df,
            x='timestamp_str',
            y='response_time',
            title="Response Times Over Time",
            labels={'response_time': 'Response Time (s)', 'timestamp_str': 'Time'}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Statistics
    st.subheader("📈 Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queries", len(df))
    with col2:
        st.metric("Avg Response Time", f"{df['response_time'].mean():.2f}s")
    with col3:
        st.metric("Fastest Response", f"{df['response_time'].min():.2f}s")
    with col4:
        st.metric("Slowest Response", f"{df['response_time'].max():.2f}s")

def display_history():
    """Display conversation history."""
    st.subheader("📋 Conversation History")
    
    if not st.session_state.conversation_history:
        st.info("No conversation history available yet.")
        return
    
    # Display history in reverse chronological order
    for i, entry in enumerate(reversed(st.session_state.conversation_history)):
        with st.expander(f"🕒 {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {entry['query'][:50]}..."):
            st.markdown(f"**Query:** {entry['query']}")
            st.markdown(f"**Type:** {entry['query_type']}")
            st.markdown(f"**Response Time:** {entry['response_time']:.2f}s")
            
            if entry['query_type'] == "🔄 All Sources":
                st.markdown("**Responses:**")
                for source, result in entry['response'].get('responses', {}).items():
                    st.markdown(f"- **{source.title()}:** {result.get('answer', 'No answer')[:100]}...")
            else:
                st.markdown(f"**Answer:** {entry['response'].get('answer', 'No answer')[:200]}...")

def display_settings():
    """Display settings and configuration."""
    st.subheader("⚙️ Settings & Configuration")
    
    # System information
    st.markdown("### 🖥️ System Information")
    if st.session_state.initialized and st.session_state.app:
        status = st.session_state.app.get_status()
        st.json(status)
    
    # Clear history
    st.markdown("### 🗑️ Data Management")
    if st.button("Clear Conversation History", type="secondary"):
        st.session_state.conversation_history = []
        st.success("Conversation history cleared!")
        st.experimental_rerun()
    
    # Re-initialize
    if st.button("🔄 Re-initialize Application", type="secondary"):
        st.session_state.initialized = False
        st.session_state.app = None
        initialize_app()
        st.experimental_rerun()

def main():
    """Main Streamlit application."""
    display_header()
    
    # Initialize application
    if not initialize_app():
        st.stop()
    
    # Sidebar navigation
    selected_section = display_sidebar()
    
    # Main content area
    if selected_section == "🏠 Home":
        st.markdown("### Welcome to MediAide!")
        st.markdown("""
        MediAide is an AI-powered medical assistant that can help you with:
        
        - 📈 **Diabetes Information**: Query our diabetes database for insights
        - 🩺 **Cancer Research**: Access cancer-related data and information
        - ❤️ **Heart Disease**: Get information about cardiovascular health
        - 🌐 **Web Search**: Search the internet for latest medical information
        - 🔄 **Comprehensive Analysis**: Get answers from multiple sources
        
        **How to use:**
        1. Navigate to the "🔍 Query Tools" section
        2. Enter your medical question
        3. Choose the type of search you want
        4. Click "Search" to get your answer
        
        **Note:** This tool is for informational purposes only and should not replace professional medical advice.
        """)
        
        # Quick start
        st.markdown("### 🚀 Quick Start")
        display_query_interface()
    
    elif selected_section == "🔍 Query Tools":
        display_query_interface()
    
    elif selected_section == "📊 Analytics":
        display_analytics()
    
    elif selected_section == "📋 History":
        display_history()
    
    elif selected_section == "⚙️ Settings":
        display_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        MediAide v1.0 | AI-Powered Medical Assistant | 
        ⚠️ For informational purposes only - consult healthcare professionals for medical advice
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
