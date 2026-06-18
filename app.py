import streamlit as st
import pandas as pd
from ai_engine import analyze_message, generate_safe_response

st.set_page_config(page_title="SafeEmpathy Platform", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

custom_ui_css = """
<style>
    /* 1. NUKE THE 'KEYBOARD_DOUBLE' GLITCH */
    /* This completely removes the top-left sidebar control and the header */
    header {display: none !important;}
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* 2. THE BREATHING BACKGROUND ANIMATION */
    @keyframes slowZoom {
        0% { background-size: 100%; }
        100% { background-size: 105%; }
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(13, 18, 14, 0.85), rgba(13, 18, 14, 0.92)),
                         url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2560&auto=format&fit=crop") !important;
        background-position: center !important;
        background-attachment: fixed !important;
        animation: slowZoom 25s ease-in-out infinite alternate !important;
    }

    /* 3. DYNAMIC GLASS PANEL */
    .main .block-container {
        background: rgba(20, 26, 22, 0.85);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 3rem;
        padding-top: 1rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }

    /* 4. TYPOGRAPHY */
    h1 {
        font-family: 'SF Pro Display', 'Inter', sans-serif !important;
        font-size: clamp(2.2rem, 4vw, 3.8rem) !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.03em;
    }
    h2, h3 {
        font-family: 'SF Pro Display', 'Inter', sans-serif !important;
        color: #F8FAFC !important;
    }
    p, span, label {
        font-family: 'SF Pro Text', 'Inter', sans-serif !important;
        color: #E2E8F0 !important;
        line-height: 1.6;
    }

    [data-testid="stChatInput"] {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(1.8rem, 3vw, 2.5rem) !important;
        font-weight: 700 !important;
        color: #3CD070 !important;
    }
</style>
"""
st.markdown(custom_ui_css, unsafe_allow_html=True)

# Navigation Control Sidebar
st.sidebar.title("🛡️ Control Center")
page = st.sidebar.radio("Switch Workspace View:", ["1. User Communication Portal", "2. B2B Analytics Dashboard"])
st.sidebar.markdown("---")
st.sidebar.caption("System Status: Operational\n\nDatabase: Local Vector RAG Core")

if page == "1. User Communication Portal":
    st.title("🛡️ SafeEmpathy Chat")
    st.caption("Advanced Real-Time Natural Language Translation & Fact Mitigation")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    col_chat, col_metrics = st.columns([2, 1])

    with col_chat:
        st.subheader("Live Interaction Feed")

        chat_box = st.container(height=450)

        with chat_box:
            if not st.session_state.messages:
                st.markdown("""
                <div style="text-align: center; padding: 4rem 2rem; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1); margin-top: 1rem;">
                    <h2 style="font-size: 2.2rem; color: #3CD070; margin-bottom: 1rem;">System Ready for Input</h2>
                    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 400px; margin: 0 auto;">
                        Paste a suspicious forwarded message or headline below. <br><br>
                        Our RAG-powered engine will instantly extract the emotional intent and cross-reference the claims against our trusted database.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.messages:
                    avatar_icon = "👤" if msg["role"] == "user" else "🛡️"
                    with st.chat_message(msg["role"], avatar=avatar_icon):
                        st.markdown(msg["content"])

        if st.session_state.messages and "latest_analysis" in st.session_state:
            res = st.session_state.latest_analysis
            st.markdown(f"""
            <div style="background: rgba(10, 15, 20, 0.6); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 1rem;">
                <p style="color: #64748b; font-family: 'Courier New', monospace; font-size: 0.85rem; margin: 0; line-height: 1.6;">
                    <span style="color: #3CD070;">> [System]</span> Analyzing lexical sentiment vectors... <span style="color: #3CD070;">OK</span><br>
                    <span style="color: #3CD070;">> [Engine]</span> Emotion identified: <b>{res.get('detected_emotion', 'N/A').upper()}</b><br>
                    <span style="color: #3CD070;">> [RAG]</span> Querying FAISS vector database... <b>{res.get('risk_score', '0')}% Threat Probability</b><br>
                    <span style="color: #3CD070;">> [Output]</span> Empathy-first mitigation response generated.
                </p>
            </div>
            """, unsafe_allow_html=True)

        if user_query := st.chat_input("Paste incoming message or chat forward here..."):
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})

            with st.spinner("Analyzing message vectors and emotional states..."):
                analysis_results = analyze_message(user_query)
                final_reply = generate_safe_response(user_query, analysis_results)

            st.session_state.messages.append({
                "role": "assistant",
                "content": final_reply
            })
            st.session_state.latest_analysis = analysis_results
            st.rerun()

    with col_metrics:
        st.subheader("Data Analysis Panel")
        if "latest_analysis" in st.session_state:
            res = st.session_state.latest_analysis

            st.metric(label="Detected Emotion Profile", value=res["detected_emotion"].upper())
            st.markdown(f"**De-escalation Strategy:**<br>{res['empathy_guideline']}", unsafe_allow_html=True)
            st.markdown("---")

            # --- RESTORED MISINFORMATION STATUS BLOCKS ---
            st.markdown("### Misinformation Status")
            score = res.get("risk_score", 50)

            if score > 70:
                st.error(f"🚨 HIGH RISK DETECTED: {score}%")
            elif score > 30:
                st.warning(f"⚠️ MEDIUM RISK DETECTED: {score}%")
            else:
                st.success(f"✅ VERIFIED SAFE: {score}%")

            st.progress(score / 100)
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"**RAG Verification Verdict:**<br>{res['fact_check_verdict']}", unsafe_allow_html=True)
            st.markdown("---")

            html_report = f"""
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: -apple-system, sans-serif; padding: 30px; background: #0b0f19; color: #ffffff; }}
                    .card {{ background: #131924; padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); max-width: 600px; margin: 0 auto; }}
                    h2 {{ color: #3CD070; margin-bottom: 5px; font-weight: 600; }}
                    .risk {{ font-size: 1.15em; font-weight: bold; color: {'#ff4b4b' if score > 50 else '#3CD070'}; text-transform: uppercase; }}
                    .verdict {{ line-height: 1.6; margin-top: 20px; background: rgba(255,255,255,0.03); padding: 18px; border-radius: 10px; border-left: 4px solid #3CD070; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>🛡️ SafeEmpathy Verification Audit</h2>
                    <p class="risk">Analysis: {res['misinformation_risk'].upper()} THREAT ({score}% Certainty)</p>
                    <div class="verdict"><strong>Verified Fact Check Summary:</strong> {res['fact_check_verdict']}</div>
                    <p style="color: #64748B; font-size: 0.85em; margin-top: 25px; text-align: center;">Generated securely via SafeEmpathy Enterprise RAG Architecture Engine.</p>
                </div>
            </body>
            </html>
            """

            st.download_button(
                label="📥 Export Report (Mobile Web HTML)",
                data=html_report,
                file_name="SafeEmpathy_Verification_Report.html",
                mime="text/html"
            )
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #94A3B8; margin: 0;">System Standby.<br><br>Feed an active user message string to view real-time vector extractions and telemetry.</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "2. B2B Analytics Dashboard":
    st.title("📊 Enterprise Network Safety Dashboard")
    st.caption("Global telemetry metrics tracking localized platform stability.")
    st.markdown("---")

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)

    with kpi_col1:
        st.metric(label="Total Scanned Messages", value="24,891", delta="+1,142 today")
    with kpi_col2:
        st.metric(label="Interacted Responses Generated", value="18,402", delta="98.7% SLA")
    with kpi_col3:
        st.metric(label="Extracted User Moods Profiled", value="4 Categories", delta="Anxiety Dominant")

    st.markdown("<br>", unsafe_allow_html=True)

    with kpi_col4:
        st.metric(label="Misconceptions Logged & Refuted", value="1,248 Claims", delta="+42 high threat")
    with kpi_col5:
        st.metric(label="RAG Database Queries", value="34,109", delta="< 0.2s latency")
    with kpi_col6:
        st.metric(label="Total Misinformation Suppressed", value="4,821 Incidents", delta="84% Mitigation Rate")

    st.markdown("---")
    st.subheader("Real-Time RAG Database Incident Logs")

    incident_logs = pd.DataFrame({
        "Timestamp Cluster": ["22:11", "21:54", "21:30", "20:15"],
        "Target Platform Feed": ["WhatsApp India Forward", "Community Forum Input", "Public Slack Channel", "WhatsApp Bengal Cluster"],
        "Identified Misconception": ["ATM closures at midnight", "Boiling water kills system virus", "Salt water prevents fallout radiation", "Bank validation locks"],
        "Suppression Response Status": ["Mitigated via RAG", "Resolved (Low Risk)", "Mitigated via RAG", "Resolved (Medium Risk)"]
    })
    st.dataframe(incident_logs, use_container_width=True)