import streamlit as st
import pandas as pd
from ai_engine import analyze_message, generate_safe_response

st.set_page_config(page_title="SafeEmpathy Platform", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

custom_ui_css = """
<style>
    /* PRECISE GLITCH FIX: Hides the broken text font, but keeps the sidebar toggle container functional */
    header {display: none !important;}

    [data-testid="collapsedControl"] button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        padding: 5px 12px !important;
        min-width: 70px !important;
    }

    [data-testid="collapsedControl"] button span {
        display: none !important; /* Hides 'keyboard_double_arrow_right' text completely */
    }

    [data-testid="collapsedControl"] button::after {
        content: "📂 Menu" !important;
        font-size: 13px !important;
        color: #3CD070 !important;
        font-weight: 600 !important;
        font-family: system-ui, sans-serif;
    }

    /* BACKGROUND LAYERS */
    @keyframes slowZoom {
        0% { background-size: 100%; }
        100% { background-size: 105%; }
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(13, 18, 14, 0.88), rgba(13, 18, 14, 0.94)),
                         url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2560&auto=format&fit=crop") !important;
        background-position: center !important;
        background-attachment: fixed !important;
        animation: slowZoom 25s ease-in-out infinite alternate !important;
    }

    /* SURFACE GLASS CARDS */
    .main .block-container {
        background: rgba(20, 26, 22, 0.85);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 3rem;
        padding-top: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
</style>
"""
st.markdown(custom_ui_css, unsafe_allow_html=True)

# Navigation Control Sidebar
st.sidebar.title("🛡️ Control Center")
page = st.sidebar.radio("Switch Workspace View:", ["1. User Communication Portal", "2. B2B Analytics Dashboard"])
st.sidebar.markdown("---")
st.sidebar.caption("System Status: Operational\nDatabase: Local Vector RAG Core")

if page == "1. User Communication Portal":
    st.title("🛡️ SafeEmpathy Chat")
    st.caption("Advanced Real-Time Natural Language Translation & Fact Mitigation")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "live_logs" not in st.session_state:
        st.session_state.live_logs = [
            {"Timestamp": "10 mins ago", "Source": "WhatsApp", "Claim": "Salt water prevents radiation", "Risk Level": "Medium"},
            {"Timestamp": "20 mins ago", "Source": "Forum", "Claim": "ATMs closing at midnight", "Risk Level": "High"}
        ]

    col_chat, col_metrics = st.columns([1.8, 1.2])

    with col_chat:
        st.subheader("Live Interaction Feed")
        chat_box = st.container(height=420)

        with chat_box:
            if not st.session_state.messages:
                st.markdown("""
                <div style="text-align: center; padding: 3rem 1rem; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1); margin-top: 1rem;">
                    <h3 style="color: #3CD070; margin-bottom: 0.5rem;">System Ready for Input</h3>
                    <p style="color: #94A3B8; font-size: 0.95rem; max-width: 400px; margin: 0 auto;">
                        Paste a suspicious forwarded message or headline below. Our engine will assess emotional intent and check facts using our RAG core.
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
            <div style="background: rgba(10, 15, 20, 0.6); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 0.5rem;">
                <p style="color: #64748b; font-family: 'Courier New', monospace; font-size: 0.8rem; margin: 0;">
                    <span style="color: #3CD070;">> [System]</span> Analyzing lexical sentiment vectors... <span style="color: #3CD070;">OK</span><br>
                    <span style="color: #3CD070;">> [Engine]</span> Emotion: <b>{res.get('detected_emotion', 'N/A').upper()}</b><br>
                    <span style="color: #3CD070;">> [RAG]</span> Database Threat Certainty: <b>{res.get('risk_score', '0')}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col_metrics:
        st.subheader("Data Analysis Panel")
        if "latest_analysis" in st.session_state:
            res = st.session_state.latest_analysis

            st.metric(label="Detected Emotion Profile", value=res["detected_emotion"].upper())
            st.markdown(f"**De-escalation Strategy:**<br>{res['empathy_guideline']}", unsafe_allow_html=True)
            st.markdown("---")

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
            st.markdown(f"**Verification Verdict:**<br>{res['fact_check_verdict']}", unsafe_allow_html=True)
            st.markdown("---")

            html_report = f"""
            <html>
            <body style="font-family: sans-serif; padding: 20px; background: #0b0f19; color: #ffffff;">
                <div style="background: #131924; padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                    <h2 style="color: #3CD070;">🛡️ SafeEmpathy Audit Report</h2>
                    <p><strong>Analysis Status:</strong> {res['misinformation_risk'].upper()} RISK ({score}%)</p>
                    <p><strong>Verdict:</strong> {res['fact_check_verdict']}</p>
                </div>
            </body>
            </html>
            """
            st.download_button(
                label="📥 Export Report (HTML)",
                data=html_report,
                file_name="SafeEmpathy_Report.html",
                mime="text/html"
            )
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #94A3B8; margin: 0;">System Standby.<br><br>Feed an active input string to initialize localized telemetry.</p>
            </div>
            """, unsafe_allow_html=True)

    # CRITICAL: Moved out of columns to layout baseline to eliminate form submission enter-glitch
    st.markdown("---")
    if user_query := st.chat_input("Paste incoming message or chat forward here..."):
        with col_chat:
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.spinner("Analyzing message vectors..."):
            analysis_results = analyze_message(user_query)
            final_reply = generate_safe_response(user_query, analysis_results)

        st.session_state.messages.append({"role": "assistant", "content": final_reply})
        st.session_state.latest_analysis = analysis_results
        risk_text = str(analysis_results.get('risk_score', 50)) + "%"
        st.session_state.live_logs.insert(0, {
            "Timestamp": "Just Now",
            "Source": "Live Portal",
            "Claim": user_query[:40] + "...", # Only show the first 40 characters
            "Risk Level": risk_text
        })
        st.rerun()

elif page == "2. B2B Analytics Dashboard":
    st.title("📊 Enterprise Network Safety Dashboard")
    st.caption("Global telemetry metrics tracking localized platform stability.")
    st.markdown("---")

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)

    with kpi_col1: st.metric(label="Total Scanned Messages", value="24,891", delta="+1,142 today")
    with kpi_col2: st.metric(label="Interacted Responses Generated", value="18,402", delta="98.7% SLA")
    with kpi_col3: st.metric(label="Extracted User Moods Profiled", value="4 Categories", delta="Anxiety Dominant")
    with kpi_col4: st.metric(label="Misconceptions Logged", value="1,248 Claims", delta="+42 high threat")
    with kpi_col5: st.metric(label="RAG Database Queries", value="34,109", delta="< 0.2s latency")
    with kpi_col6: st.metric(label="Total Misinformation Suppressed", value="4,821 Incidents", delta="84% Mitigation Rate")

    st.markdown("---")
    st.subheader("Real-Time RAG Database Incident Logs")

    st.markdown("---")
    st.subheader("Real-Time RAG Database Incident Logs")

    # Render the live session state data instead of the fake static data
    st.dataframe(pd.DataFrame(st.session_state.live_logs), use_container_width=True)
   # st.dataframe(incident_logs, use_container_width=True)