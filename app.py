import os
import time
import streamlit as st
from dotenv import load_dotenv

from filter_regex import scan_code
from filter_ai import get_mentorship_feedback

load_dotenv()

st.set_page_config(
    page_title="VeriVibe | Enterprise AI Mentorship",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI CSS Overhaul
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Page & Main Background */
    .stApp {
        background: #090D16 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F3F4F6 !important;
    }

    /* Style Upper Header Bar to Match Background */
    header[data-testid="stHeader"] {
        background-color: #090D16 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Matching Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0D1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] *:not([data-testid^="stIcon"]):not([class*="material" i]) {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Typography Override */
    h1, h2, h3, h4, h5, h6, p,
    span:not([data-testid^="stIcon"]):not([class*="material" i]),
    label:not([data-testid^="stIcon"]):not([class*="material" i]) {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid^="stIcon"],
    [class*="material" i] {
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Sidebar toggle controls */
    [data-testid="stSidebarCollapsedControl"] [data-testid^="stIcon"],
    [data-testid="stSidebarCollapseButton"] [data-testid^="stIcon"],
    [data-testid="collapsedControl"] [data-testid^="stIcon"],
    [data-testid="collapsedControl"] svg {
        color: #090D16 !important;
        fill: #090D16 !important;
    }

    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button {
        opacity: 1 !important;
        visibility: visible !important;
        background: #FFFFFF !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebarCollapsedControl"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="collapsedControl"] button:hover {
        background: #E5E7EB !important;
    }

    header[data-testid="stHeader"] button:first-of-type {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    header[data-testid="stHeader"] button:first-of-type [data-testid^="stIcon"],
    header[data-testid="stHeader"] button:first-of-type svg {
        color: #090D16 !important;
        fill: #090D16 !important;
    }

    header[data-testid="stHeader"] button:first-of-type:hover {
        background: #E5E7EB !important;
    }

    div[data-testid="stTextArea"] label {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] label,
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] label p {
        color: #FFFFFF !important;
    }

    textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    textarea::placeholder {
        color: #FFFFFF !important;
        opacity: 0.9 !important;
        font-weight: 500 !important;
    }

    textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 1px #6366F1 !important;
    }

    .radar-container {
        position: relative;
        width: 100px;
        height: 100px;
        margin: 0 auto;
    }
    
    .radar-sweep {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px solid rgba(99, 102, 241, 0.3);
        background: conic-gradient(from 0deg, rgba(99, 102, 241, 0.4), transparent 60%);
        animation: radar-spin 1.5s linear infinite;
    }

    .radar-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2rem;
    }

    @keyframes radar-spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .app-header {
        padding: 2.5rem 2.5rem;
        background: radial-gradient(100% 100% at 0% 0%, rgba(99, 102, 241, 0.15) 0%, rgba(17, 24, 39, 0.4) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .title-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 20px;
        color: #818CF8;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .app-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.15;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #9CA3AF;
        margin-top: 10px;
        max-width: 750px;
        line-height: 1.5;
    }

    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
        color: #FFFFFF !important;
    }
    .glass-card * {
        color: #FFFFFF !important;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }

    .status-badge {
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        letter-spacing: 0.02em;
    }
    .status-critical {
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5 !important;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .status-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #FDE047 !important;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .status-success {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7 !important;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .metric-container {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
    }
    .metric-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 12px 16px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-val {
        font-size: 1.2rem;
        font-weight: 700;
        color: #6366F1 !important;
    }
    .metric-lbl {
        font-size: 0.75rem;
        color: #9CA3AF !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    }

    .stTabs [role="tablist"] {
        gap: 8px;
    }
    .stTabs [role="tab"] {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .stTabs [role="tab"],
    .stTabs [role="tab"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    .stTabs [role="tab"][aria-selected="false"],
    .stTabs [role="tab"][aria-selected="false"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.2) !important;
        border-color: #6366F1 !important;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #090D16;
    }
    ::-webkit-scrollbar-thumb {
        background: #1F2937;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

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
    st.markdown("<h2 style='font-size: 1.2rem; font-weight: 700; margin-bottom: 4px; color: #FFFFFF;'>🛡️ VeriVibe Control</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF; font-size: 0.85rem;'>Bridge the tech expertise gap automatically.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    samples_dict = load_samples()
    selected_sample = st.selectbox("Select Test Scenario:", list(samples_dict.keys()))
    
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 0.9rem; letter-spacing: 0.05em; color: #9CA3AF;'>ENGINE PIPELINE</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); font-size: 0.82rem; color: #D1D5DB;'>
        <p style='margin-bottom: 6px;'><b>⚡ Stage 1:</b> Local AST & Regex Guard</p>
        <p style='margin: 0;'><b>🧠 Stage 2:</b> GPT-OSS Neural Mentorship</p>
    </div>
    """, unsafe_allow_html=True)

# --- SAFE SESSION STATE INITIALIZATION ---
if "last_sample" not in st.session_state:
    st.session_state["last_sample"] = selected_sample

if "code_input" not in st.session_state or st.session_state.get("last_sample") != selected_sample:
    st.session_state["code_input"] = samples_dict[selected_sample]
    st.session_state["last_sample"] = selected_sample

# --- ENHANCED MAIN APP HEADER ---
st.markdown("""
<div class="app-header">
    <span class="title-badge">🛡️ Enterprise Code Intelligence</span>
    <p class="app-title">VeriVibe Mentorship Platform</p>
    <p class="app-subtitle">Identify vulnerabilities, decode complex tracebacks, and receive real-time actionable code improvements through AI mentorship.</p>
</div>
""", unsafe_allow_html=True)

# Split Workspace Layout
col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.markdown("<h4 style='font-size: 1rem; font-weight: 600; margin-bottom: 12px; color: #FFFFFF;'>💻 Code Workspace</h4>", unsafe_allow_html=True)
    code = st.text_area(
        label="Code Input Area",
        value=st.session_state['code_input'],
        placeholder="Paste your code snippet here...",
        height=380,
        key="editor"
    )
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Run Security & Mentorship Audit", use_container_width=True)

with col2:
    st.markdown("<h4 style='font-size: 1rem; font-weight: 600; margin-bottom: 12px; color: #FFFFFF;'>🧠 Real-Time Insights</h4>", unsafe_allow_html=True)
    feedback_container = st.empty()
    
    if analyze_clicked:
        if not code.strip():
            feedback_container.warning("Please provide a valid code snippet to evaluate.")
        else:
            with feedback_container.container():
                st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 40px 20px;'>
                    <div class='radar-container'>
                        <div class='radar-sweep'></div>
                        <div class='radar-icon'>🔍</div>
                    </div>
                    <p style='color: #9CA3AF !important; margin-top: 16px; font-size: 0.9rem;'>Running local AST scan & querying neural mentor...</p>
                </div>
                """, unsafe_allow_html=True)
            
            violations = scan_code(code)
            time.sleep(1.0)  
            mentorship_response = get_mentorship_feedback(code, violations)
            
            # Parse AI status tag (separating HIGH_RISK and WARNING accurately)
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
                    status_class = "status-critical"
                    status_text = "🚨 CRITICAL: Severe Vulnerability Identified"
                elif ai_status == "HIGH_RISK":
                    status_class = "status-critical"
                    status_text = "⚠️ HIGH RISK: Major Security Flaw Detected"
                elif ai_status == "WARNING":
                    status_class = "status-warning"
                    status_text = "⚡ WARNING: Code Smell / Minor Anti-Pattern"
                else:
                    status_class = "status-success"
                    status_text = "✨ CLEAN: Security Baseline Verified"
                
                # Dynamic Metric Summary Grid
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-box'>
                        <div class='metric-val'>{len(violations)}</div>
                        <div class='metric-lbl'>Local Violations</div>
                    </div>
                    <div class='metric-box'>
                        <div class='metric-val'>{len(code.splitlines())}</div>
                        <div class='metric-lbl'>Lines Scanned</div>
                    </div>
                    <div class='metric-box'>
                        <div class='metric-val'>{ai_status}</div>
                        <div class='metric-lbl'>AI Risk Level</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tabbed Output Container
                tab1, tab2 = st.tabs(["💬 Mentor Feedback", "🔍 Detected Patterns"])
                
                with tab1:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div><span class='status-badge {status_class}'>{status_text}</span></div>
                    """, unsafe_allow_html=True)
                    st.markdown(clean_response)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    if violations:
                        st.markdown("**Rule Engine Flags:**")
                        for v in violations:
                            st.error(f"• {v}")
                    else:
                        st.info("No static rule violations triggered by regex scan.")
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        feedback_container.markdown("""
        <div class='glass-card' style='text-align: center; padding: 90px 20px;'>
            <div style='font-size: 2.5rem; margin-bottom: 12px;'>🛡️</div>
            <p style='color: #FFFFFF !important; font-size: 0.95rem; margin: 0;'>Awaiting code submission for security evaluation...</p>
        </div>
        """, unsafe_allow_html=True)