import os
import json
import time
import streamlit as st
from streamlit_lottie import st_lottie
from dotenv import load_dotenv

from filter_regex import scan_code
from filter_ai import get_mentorship_feedback

load_dotenv()

st.set_page_config(
    page_title="VeriVibe | Enterprise Expertise Guardrail",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Elite Custom CSS Injection to override Streamlit defaults
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #F7F7F5 !important;
        font-family: 'Inter', sans-serif !important;
        color: #222222 !important;
    }
    
    /* Global Typography */
    h1, h2, h3, h4, h5, h6, p, span, label {
        font-family: 'Inter', sans-serif !important;
        color: #222222 !important;
    }

    /* Header styling */
    .app-header {
        padding: 1rem 0 0.5rem 0;
        border-bottom: 1px solid #E5E5E0;
        margin-bottom: 2rem;
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #111111;
        margin: 0;
    }
    .app-subtitle {
        font-size: 0.95rem;
        color: #666666;
        margin-top: 4px;
    }

    /* Card Containers */
    .glass-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E5E0;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* Badges */
    .status-error {
        background-color: #FDF2F2;
        color: #9E2A2B;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #F5C6CB;
        margin-bottom: 14px;
        display: inline-block;
    }
    .status-success {
        background-color: #EBF4F0;
        color: #2D7254;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #C3E6CB;
        margin-bottom: 14px;
        display: inline-block;
    }

    /* Custom Button Styling */
    .stButton>button {
        background-color: #B5A48B !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(181, 164, 139, 0.3);
    }
    .stButton>button:hover {
        background-color: #9C8C73 !important;
        box-shadow: 0 4px 12px rgba(156, 140, 115, 0.4);
    }

    /* Text area refinement */
    textarea {
        border-radius: 8px !important;
        border-color: #E5E5E0 !important;
        background-color: #FAFAFA !important;
    }
    </style>
""", unsafe_allow_html=True)

def load_lottiefile(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def load_samples():
    filepath = os.path.join(os.path.dirname(__file__), 'References', 'code_samples.txt')
    samples = {"Custom Workspace (Empty)": ""}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            blocks = content.split('[')
            for block in blocks:
                if ']' in block:
                    title, code = block.split(']', 1)
                    samples[title.strip()] = code.strip()
    return samples

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### **VeriVibe Control**")
    st.markdown("<p style='color: #666666; font-size: 0.85rem;'>Closing the technical expertise gap.</p>", unsafe_allow_html=True)
    
    samples_dict = load_samples()
    selected_sample = st.selectbox("Load Test Scenario:", list(samples_dict.keys()))
    
    st.markdown("---")
    st.markdown("#### **Architecture Overview**")
    st.markdown("""
    <p style='color: #666666; font-size: 0.8rem; line-height: 1.4;'>
    <b>Stage 1:</b> Local Regex Guardrail<br>
    <b>Stage 2:</b> GPT-OSS-120B Neural Mentorship
    </p>
    """, unsafe_allow_html=True)

if "code_input" not in st.session_state or st.session_state.get('last_sample') != selected_sample:
    st.session_state['code_input'] = samples_dict[selected_sample]
    st.session_state['last_sample'] = selected_sample

# --- MAIN APP HEADER ---
st.markdown("""
<div class="app-header">
    <p class="app-title">VeriVibe Mentorship Platform</p>
    <p class="app-subtitle">Translate raw code vulnerabilities and complex errors into clear, actionable guidance.</p>
</div>
""", unsafe_allow_html=True)

# Split Workspace Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("#### **Code Workspace**")
    code = st.text_area(
        "Paste your code or configuration snippet:",
        value=st.session_state['code_input'],
        height=340,
        key="editor"
    )
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("Run Security & Mentorship Audit")

with col2:
    st.markdown("#### **Real-Time Mentorship Output**")
    feedback_container = st.empty()
    
    if analyze_clicked:
        if not code.strip():
            feedback_container.warning("Please provide a valid code snippet to evaluate.")
        else:
            with feedback_container.container():
                st.markdown("<div class='glass-card' style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
                lottie_data = load_lottiefile("marketing.json")
                if lottie_data:
                    st_lottie(lottie_data, speed=1, height=120, key="loading")
                st.markdown("<p style='color: #666666; margin-top: 12px; font-size: 0.9rem;'>Running local AST scan & querying neural mentor...</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            violations = scan_code(code)
            time.sleep(1.2)  # Smooth transition for animation
            mentorship_response = get_mentorship_feedback(code, violations)
            
            # Parse out the AI status tag
            ai_status = "CLEAN"
            clean_response = mentorship_response
            if "STATUS:" in mentorship_response:
                lines = mentorship_response.split("\n", 1)
                status_line = lines[0].strip()
                if "CRITICAL" in status_line:
                    ai_status = "CRITICAL"
                elif "HIGH_RISK" in status_line:
                    ai_status = "HIGH_RISK"
                elif "WARNING" in status_line:
                    ai_status = "WARNING"
                else:
                    ai_status = "CLEAN"
                
                if len(lines) > 1:
                    clean_response = lines[1].strip()

            feedback_container.empty()
            
            with feedback_container.container():
                if ai_status == "CRITICAL":
                    status_class = "status-error"
                    status_text = "🚨 CRITICAL: Severe Security Vulnerability Detected"
                elif ai_status == "HIGH_RISK":
                    status_class = "status-error"
                    status_text = "⚠️ HIGH RISK: Vulnerability Pattern Identified by AI"
                elif ai_status == "WARNING":
                    status_class = "status-error"
                    status_text = "⚡ WARNING: Potential Security Code Smell"
                else:
                    status_class = "status-success"
                    status_text = "✨ AI Mentor: Clean Baseline Verified"
                
                st.markdown(f"""
                <div class='glass-card'>
                    <div><span class='{status_class}'>{status_text}</span></div>
                """, unsafe_allow_html=True)
                
                st.markdown(clean_response)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        feedback_container.markdown("""
        <div class='glass-card' style='text-align: center; padding: 70px 20px;'>
            <p style='color: #888888; font-size: 0.95rem;'>Awaiting code submission for evaluation...</p>
        </div>
        """, unsafe_allow_html=True)