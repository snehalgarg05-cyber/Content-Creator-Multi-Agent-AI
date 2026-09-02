import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
from pipeline import run_pipeline

st.set_page_config(
    page_title="Multi-Agent Content Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: #f8f7ff; }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6d28d9, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
    }
    .sub-text { color: #4b5563; text-align: center; font-size: 1rem; margin-top: 0.3rem; }
    p, li { color: #1f2937 !important; }
    h1, h2, h3 { color: #111827 !important; }
    label { color: #374151 !important; }
    .stTextInput input {
        background: #ffffff;
        color: #111827;
        border: 2px solid #7c3aed;
        border-radius: 10px;
        font-size: 1rem;
    }
    .stTextInput label { color: #374151 !important; font-weight: 600; }
    .stTextArea textarea {
        background: #ffffff;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 8px;
    }
    .stSelectbox label { color: #374151 !important; font-weight: 600; }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
    }
    .stButton > button:hover { opacity: 0.88; }
    .stTabs [data-baseweb="tab-list"] {
        background: #ede9fe;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] { color: #4b5563 !important; font-weight: 500; }
    .stTabs [aria-selected="true"] {
        background: #7c3aed !important;
        color: white !important;
        border-radius: 8px;
    }
    [data-testid="stSidebar"] { background: #ede9fe; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #1f2937 !important; }
    .stMetric label { color: #6b7280 !important; font-size: 0.85rem !important; }
    .stMetric [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.8rem;
    }
    .stDownloadButton button {
        background: #f3f4f6;
        color: #4f46e5 !important;
        border: 1px solid #4f46e5;
        border-radius: 8px;
        font-weight: 600;
    }
    .stSuccess { background: #f0fdf4 !important; color: #166534 !important; border: 1px solid #16a34a; border-radius: 8px; }
    .stError { background: #fef2f2 !important; color: #991b1b !important; border: 1px solid #dc2626; border-radius: 8px; }
    .stInfo { background: #eff6ff !important; color: #1e40af !important; border: 1px solid #3b82f6; border-radius: 8px; }
    .stExpander { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 Multi-Agent Content Creation Studio</div>', unsafe_allow_html=True)
st.markdown("<p class='sub-text'>5 AI Agents working together to create your complete content package</p>", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; justify-content:center; gap:8px; padding:1rem 0; flex-wrap:wrap;'>
<span style='background:#ecfeff; border:1.5px solid #06b6d4; color:#0e7490; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🔍 Researcher</span>
<span style='color:#9ca3af; font-size:1.2rem;'>→</span>
<span style='background:#ede9fe; border:1.5px solid #7c3aed; color:#6d28d9; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🎯 Strategist</span>
<span style='color:#9ca3af; font-size:1.2rem;'>→</span>
<span style='background:#fdf2f8; border:1.5px solid #db2777; color:#9d174d; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:600;'>✍️ Writer</span>
<span style='color:#9ca3af; font-size:1.2rem;'>→</span>
<span style='background:#ecfdf5; border:1.5px solid #059669; color:#065f46; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:600;'>📱 Adapter</span>
<span style='color:#9ca3af; font-size:1.2rem;'>→</span>
<span style='background:#fffbeb; border:1.5px solid #d97706; color:#92400e; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🔎 SEO</span>
</div>
""", unsafe_allow_html=True)

st.divider()

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    target_audience = st.selectbox("Target Audience", [
        "Tech Professionals",
        "Business Executives",
        "Students & Learners",
        "Entrepreneurs & Founders",
        "General Public",
        "Developers & Engineers"
    ])
    st.markdown("---")
    language = st.selectbox("🌐 Content Language", [
        "English",
        "Hindi",
        "Hinglish (Hindi + English)"
    ])
    st.divider()
    st.markdown("### 🤖 Agent Pipeline")
    st.markdown("**1. 🔍 Researcher** — Tavily web search")
    st.markdown("**2. 🎯 Strategist** — Content angle & tone")
    st.markdown("**3. ✍️ Writer** — Blog + YouTube script")
    st.markdown("**4. 📱 Adapter** — LinkedIn, Twitter, Instagram")
    st.markdown("**5. 🔎 SEO** — Keywords + optimization")
    st.divider()
    st.markdown("### 🛠️ Built With")
    st.markdown("LangGraph · Groq · Tavily · Streamlit")

col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "📝 Enter your topic",
        placeholder="e.g. Artificial Intelligence in Healthcare, LangGraph Tutorial..."
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("✨ Generate Content", use_container_width=True)

if generate_btn:
    if not topic.strip():
        st.error("Please enter a topic first!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        try:
            status_text.markdown("### 🔍 Agent 1: Searching the web for latest trends...")
            progress_bar.progress(10)
            result = run_pipeline(topic, target_audience, language)
            status_text.markdown("### 🎯 Agent 2: Planning content strategy...")
            progress_bar.progress(40)
            time.sleep(0.3)
            status_text.markdown("### ✍️ Agent 3: Writing blog post and YouTube script...")
            progress_bar.progress(60)
            time.sleep(0.3)
            status_text.markdown("### 📱 Agent 4: Adapting for all platforms...")
            progress_bar.progress(80)
            time.sleep(0.3)
            status_text.markdown("### 🔎 Agent 5: SEO optimization...")
            progress_bar.progress(95)
            time.sleep(0.3)
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            st.session_state["result"] = result
            st.session_state["topic"] = topic
            st.success(f"✅ Complete content package ready for: **{topic}**")
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error: {str(e)}")
            st.info("Check your API keys in the .env file")

if "result" in st.session_state:
    result = st.session_state["result"]
    st.divider()
    st.markdown(f"## 📦 Content Package: *{st.session_state['topic']}*")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Blog Words", f"{len(result.get('final_blog', '').split()):,}")
    with col2:
        st.metric("🔎 SEO Score", f"{result.get('seo_score', '0')}/100")
    with col3:
        st.metric("🐦 Tweets", str(result.get("twitter_thread", "").count("/")))
    with col4:
        st.metric("📱 Platforms", "4")

    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Blog Post",
        "🎬 YouTube Script",
        "💼 LinkedIn",
        "🐦 Twitter/X",
        "📸 Instagram",
        "⚙️ Pipeline Log"
    ])

    with tab1:
        st.markdown("### 📄 SEO-Optimized Blog Post")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(result.get("final_blog", "No blog post generated"))
        with c2:
            st.markdown("#### 🔎 SEO Details")
            st.info(result.get("meta_description", "No meta description"))
            st.markdown("**Top Keywords:**")
            for kw in result.get("seo_keywords", "").split(",")[:5]:
                if kw.strip():
                    st.markdown(f"• {kw.strip()}")
            st.metric("SEO Score", f"{result.get('seo_score', '0')}/100")
        st.download_button(
            "⬇️ Download Blog Post",
            data=result.get("final_blog", ""),
            file_name=f"blog_{st.session_state['topic'][:20].replace(' ','_')}.md",
            mime="text/markdown"
        )

    with tab2:
        st.markdown("### 🎬 YouTube Video Script")
        st.markdown(result.get("youtube_script", "No script generated"))
        st.download_button(
            "⬇️ Download Script",
            data=result.get("youtube_script", ""),
            file_name=f"youtube_{st.session_state['topic'][:20].replace(' ','_')}.txt",
            mime="text/plain"
        )

    with tab3:
        st.markdown("### 💼 LinkedIn Post")
        linkedin = result.get("linkedin_post", "No LinkedIn post generated")
        st.text_area("Ready to post on LinkedIn:", value=linkedin, height=380, key="li_ta")
        st.caption(f"Word count: {len(linkedin.split())} words")

    with tab4:
        st.markdown("### 🐦 Twitter/X Thread")
        twitter = result.get("twitter_thread", "")
        for line in twitter.split("\n"):
            if line.strip():
                char_count = len(line)
                color = "#065f46" if char_count <= 280 else "#991b1b"
                bg = "#ecfdf5" if char_count <= 280 else "#fef2f2"
                border = "#059669" if char_count <= 280 else "#dc2626"
                st.markdown(
                    f"<div style='background:{bg}; border:1px solid {border}; border-radius:8px; "
                    f"padding:10px 14px; margin:4px 0; color:#111827;'>"
                    f"{line}"
                    f"<br><small style='color:{color};font-weight:600;'>Characters: {char_count}/280</small></div>",
                    unsafe_allow_html=True
                )
        st.download_button(
            "⬇️ Download Thread",
            data=twitter,
            file_name=f"twitter_{st.session_state['topic'][:20].replace(' ','_')}.txt",
            mime="text/plain"
        )

    with tab5:
        st.markdown("### 📸 Instagram Caption")
        ig = result.get("instagram_caption", "No caption generated")
        st.text_area("Ready to post on Instagram:", value=ig, height=300, key="ig_ta")
        st.download_button(
            "⬇️ Download Caption",
            data=ig,
            file_name=f"instagram_{st.session_state['topic'][:20].replace(' ','_')}.txt",
            mime="text/plain"
        )

    with tab6:
        st.markdown("### ⚙️ Agent Processing Log")
        for entry in result.get("processing_log", []):
            st.markdown(
                f"<div style='padding:6px 0; border-bottom:1px solid #e5e7eb; "
                f"font-size:13px; color:#374151;'>{entry}</div>",
                unsafe_allow_html=True
            )
        st.divider()
        with st.expander("📊 View Research Data"):
            st.markdown(result.get("research_data", ""))
        with st.expander("🎯 View Content Strategy"):
            st.markdown(result.get("content_angle", ""))

st.divider()
st.markdown(
    "<div style='text-align:center; color:#6b7280; font-size:13px; padding:1rem 0;'>"
    "Built by <strong style='color:#7c3aed'>Snehal Garg</strong> &nbsp;|&nbsp; "
    "LangGraph · Groq · Tavily · Streamlit &nbsp;|&nbsp; "
    "<a href='https://github.com/snehalgarg05-cyber' style='color:#4f46e5; text-decoration:none; font-weight:600;'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)