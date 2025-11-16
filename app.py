import streamlit as st
import os
from dotenv import load_dotenv
from agents.literature_scout import LiteratureScoutAgent
from agents.paper_analyzer import PaperAnalyzerAgent
from agents.research_gap_analyzer import ResearchGapAnalyzerAgent
import datetime

# Page config
st.set_page_config(
    page_title="ScholarSync AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal, smooth CSS
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Smooth background */
    .stApp {
        background: #FFFFFF;
    }

    .block-container {
        padding: 2rem 1rem;
        max-width: 1100px;
    }

    /* Minimal hero */
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.10);
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #666;
        font-weight: 400;
        max-width: 0 auto;
        margin: 0 auto;
        line-height: 1.6;
        text-align: center;
    }

    /* Smooth feature cards */
    .feature-card {
        background: #FAFAFA;
        padding: 1.75rem 1.5rem;
        border-radius: 10px;
        border: 1px solid #EAEAEA;
        min-height: 200px;
        transition: all 0.2s ease-out;
        text-align: center;
    }

    .feature-card:hover {
        background: #F0F0F0;
        border-color: #D0D0D0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-3px);
    }

    .feature-emoji {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        opacity: 0.9;
    }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        font-size: 0.95rem;
        color: #666;
        line-height: 1.5;
        text-align: center;
    }

    /* Smooth minimal button */
    .stButton>button {
        background: #1a1a1a;
        color: white;
        font-size: 1rem;
        font-weight: 500;
        padding: 0.75rem 2rem;
        border-radius: 50px; /* Fully rounded/pill shape */
        border: none;
        transition: all 0.2s ease;
        box-shadow: none;
    }

    .stButton>button:hover {
        background: #333;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    }

    /* Clean form */
    .form-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .form-subtitle {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* Smooth inputs */
    .stTextInput>div>div>input {
        background: #FAFAFA !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        color: #1a1a1a !important;
        transition: all 0.15s ease !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #999 !important;
        background: #FFF !important;
    }

    .stTextInput>div>div>input::placeholder {
        color: #999 !important;
    }

    .stNumberInput>div>div>input {
        background: #FAFAFA !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        color: #1a1a1a !important;
    }

    label {
        color: #666 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Smooth progress */
    .stProgress>div>div {
        background: #1a1a1a !important;
        height: 4px !important;
        border-radius: 2px !important;
        transition: width 0.3s ease-out !important;
    }

    /* Clean status */
    .status-text {
        text-align: center;
        color: #666;
        font-size: 1rem;
        padding: 0.5rem;
    }

    /* Minimal expander */
    .streamlit-expanderHeader {
        background: #FAFAFA !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        color: #1a1a1a !important;
    }

    .streamlit-expanderHeader:hover {
        background: #F5F5F5 !important;
    }

    .streamlit-expanderContent {
        background: #FFF !important;
        border: 1px solid #E0E0E0 !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }

    /* Smooth download */
    .stDownloadButton>button {
        background: #1a1a1a !important;
        color: white !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.75rem !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.15s ease !important;
    }

    .stDownloadButton>button:hover {
        background: #333 !important;
    }

    /* Clean messages */
    .element-container .stSuccess {
        background: #F0F9F4 !important;
        border: 1px solid #D1F2E0 !important;
        color: #1a7a3e !important;
        border-radius: 6px !important;
    }

    /* Paper items */
    .paper-item {
        padding: 1rem;
        border-bottom: 1px solid #F0F0F0;
    }

    .paper-item:hover {
        background: #FAFAFA;
    }

    .paper-number {
        color: #1a1a1a;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .paper-title {
        color: #1a1a1a;
        font-weight: 500;
        font-size: 1rem;
    }

    .paper-meta {
        color: #666;
        font-size: 0.875rem;
    }

    /* Section headers */
    .section-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1rem 0 0.5rem 0;
    }

    .section-text {
        color: #333;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Links */
    a {
        color: #1a1a1a !important;
        text-decoration: underline !important;
    }

    a:hover {
        color: #666 !important;
    }

    /* Clean spacing */
    h1, h2, h3 {
        color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)


class ScholarSyncApp:

    def __init__(self):
        load_dotenv()
        # NOTE: Since this is a Streamlit app run outside of the Canvas environment, 
        # we assume os.getenv('GEMINI_API_KEY') is used.
        self.api_key = os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            st.error("⚠️ Add GEMINI_API_KEY to .env file")
            st.stop()

        if 'page' not in st.session_state:
            st.session_state.page = 'home'
        
        # --- FIX: Initialize topic_error in session state ---
        # This prevents the AttributeError on reruns.
        if 'topic_error' not in st.session_state:
            st.session_state.topic_error = False
        # ----------------------------------------------------

        self.scout, self.analyzer, self.gap_analyzer = self.init_agents()

    @st.cache_resource
    def init_agents(_self):
        # NOTE: These classes (LiteratureScoutAgent, PaperAnalyzerAgent, etc.) 
        # are assumed to exist in the 'agents' directory as per the original code.
        return (
            LiteratureScoutAgent(_self.api_key),
            PaperAnalyzerAgent(_self.api_key),
            ResearchGapAnalyzerAgent(_self.api_key)
        )

    def home_page(self):
        """Minimal landing page"""

        st.markdown("""
            <div class="hero">
                <h1 class="hero-title">ScholarSync AI</h1>
                <p class="hero-subtitle" style="text-align: center;"> 
                    Automate literature review with AI agents. Find papers, extract insights, identify research gaps. 
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-emoji">📚</div>
                    <div class="feature-title">Smart Discovery</div>
                    <div class="feature-desc">Search and rank papers from arxiv by relevance</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-emoji">🔍</div>
                    <div class="feature-title">Deep Analysis</div>
                    <div class="feature-desc">Extract questions, methods, findings, limitations</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-emoji">💡</div>
                    <div class="feature-title">Gap Identification</div>
                    <div class="feature-desc">Discover research opportunities and contributions</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.25, 0.5, 1.25])
        with col2:
            if st.button("Start", key="start", use_container_width=True):
                st.session_state.page = 'workflow'
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; color: #999; font-size: 0.85rem;'>
                Multi-Agent Architecture • Kaggle AI Agents Capstone
            </div>
        """, unsafe_allow_html=True)

    def workflow_page(self):
        """Workflow page with topic validation and red border error."""

        if st.button("← Back", key="back"):
            st.session_state.page = 'home'
            st.session_state.topic_error = False # Reset error state when leaving
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h2 class="form-title">Research Analysis</h2>', unsafe_allow_html=True)
        st.markdown('<p class="form-subtitle">Enter your research topic to begin</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.5, 1, 0.5])

        with col2:
            
            # --- CONDITIONAL CSS INJECTION ---
            if st.session_state.topic_error:
                st.markdown("""
                <style>
                /* Apply red border to the text input when the error state is true */
                .stTextInput > div > div > input {
                    border-color: #EF4444 !important; /* Red color */
                    box-shadow: 0 0 0 1px #EF4444 !important;
                }
                </style>
                """, unsafe_allow_html=True)
            # ---------------------------------

            query = st.text_input(
                "Topic",
                placeholder="e.g., transformer models in NLP",
                label_visibility="collapsed",
                key="topic_input" # Added key for session state access
            )
            
            # --- LIVE VALIDATION RESET ---
            # If the user starts typing after an error, reset the flag for the next rerun
            if 'topic_input' in st.session_state and st.session_state.topic_error and st.session_state.topic_input:
                st.session_state.topic_error = False
                st.rerun()
            # -----------------------------

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                num_papers = st.number_input("Papers to Find", 3, 10, 5)
            with c2:
                num_analyze = st.number_input("Papers to Analyze", 1, 3, 2)

            st.markdown("<br>", unsafe_allow_html=True)

            start = st.button("Run Analysis", use_container_width=True) 

        # --- VALIDATION LOGIC ---
        if start:
            if query:
                # Successful run
                st.session_state.topic_error = False
                st.markdown("<br>", unsafe_allow_html=True)
                self.run_analysis(query, num_papers, num_analyze)
            else:
                # Empty query, set error state and show warning
                st.session_state.topic_error = True
                st.warning("Please enter a research topic before running the analysis.")
                st.rerun() # Rerun to apply the conditional CSS
        # ------------------------


    def run_analysis(self, query, max_papers, analyze_top):
        """Run analysis"""

        progress = st.progress(0)
        status = st.empty()

        # Helper function to update both the bar and the status text with the percentage
        def update_status(message, percent):
            progress.progress(percent)
            status.markdown(f'<p class="status-text">{message} ({percent}%)</p>', unsafe_allow_html=True)

        # Search
        with status:
            st.markdown('<p class="status-text">Searching papers...</p>', unsafe_allow_html=True)
        progress.progress(25)

        papers = self.scout.search_papers(query, max_results=max_papers)
        if not papers:
            st.error("No papers found")
            return

        # Rank
        with status:
            st.markdown('<p class="status-text">Ranking...</p>', unsafe_allow_html=True)
        progress.progress(40)

        ranked = self.scout.rank_papers_with_gemini(papers, query)

        # Analyze
        with status:
            st.markdown('<p class="status-text">Analyzing...</p>', unsafe_allow_html=True)
        progress.progress(60)

        analyzed = []
        for i, p in enumerate(ranked[:analyze_top], 1):
            analysis = self.analyzer.analyze_paper(p['url'], p['title'])
            if analysis:
                analyzed.append(analysis)
            progress.progress(60 + (i * 15))

        # Gap
        gap = None
        if len(analyzed) >= 2:
            with status:
                st.markdown('<p class="status-text">Finding gaps...</p>', unsafe_allow_html=True)
            progress.progress(90)
            gap = self.gap_analyzer.analyze_gaps(analyzed, query)

        progress.progress(100)
        status.empty()

        self.show_results(query, ranked, analyzed, gap)

    def show_results(self, query, ranked, analyzed, gap):
        """Show results"""

        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✓ Complete")

        # Papers
        with st.expander("📚 Ranked Papers", expanded=False):
            for i, p in enumerate(ranked, 1):
                st.markdown(f"""
                    <div class="paper-item">
                        <span class="paper-number">{i}.</span>
                        <span class="paper-title">{p['title']}</span><br>
                        <span class="paper-meta">{', '.join(p['authors'][:2])} • <a href="{p['url']}">PDF</a></span>
                    </div>
                """, unsafe_allow_html=True)

        # Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📄 Analysis", expanded=True):
            for i, a in enumerate(analyzed, 1):
                s = a['summary']
                st.markdown(f"**{i}. {a['title']}**")

                st.markdown('<p class="section-label">Research Question</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{s.get("research_question", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Methodology</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{s.get("methodology", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Key Findings</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{s.get("key_findings", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Limitations</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{s.get("limitations", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Future Work</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{s.get("future_work", "N/A")}</p>', unsafe_allow_html=True)

                if i < len(analyzed):
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.divider()

        # Gaps
        if gap:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("💡 Research Gaps", expanded=True):
                st.markdown('<p class="section-label">Common Themes</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{gap.get("common_themes", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Divergent Approaches</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{gap.get("divergent_approaches", "N/A")}</p>',
                            unsafe_allow_html=True)

                st.markdown('<p class="section-label">Research Gaps</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{gap.get("research_gaps", "N/A")}</p>', unsafe_allow_html=True)

                st.markdown('<p class="section-label">Proposed Directions</p>', unsafe_allow_html=True)
                for idx, d in enumerate(gap.get("proposed_directions", []), 1):
                    st.markdown(f'<p class="section-text">{idx}. {d.lstrip("0123456789.• ")}</p>',
                                unsafe_allow_html=True)

                st.markdown('<p class="section-label">Novel Contribution</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="section-text">{gap.get("novel_contribution", "N/A")}</p>',
                            unsafe_allow_html=True)

        # Download
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.25, 0.5, 1.25])
        with col2:
            report = self.gen_report(query, ranked, analyzed, gap)
            st.download_button(
                "Download",
                report,
                f"report_{datetime.datetime.now().strftime('%Y%m%d')}.md",
                "text/markdown",
                use_container_width=True
            )

    def gen_report(self, query, ranked, analyzed, gap):
        """Generate report"""
        r = f"# {query}\n\n**Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n## Papers\n\n"
        for i, p in enumerate(ranked, 1):
            r += f"{i}. {p['title']} - {', '.join(p['authors'][:2])}\n   {p['url']}\n\n"
        r += "\n## Analysis\n\n"
        for a in analyzed:
            s = a['summary']
            r += f"### {a['title']}\n\n"
            r += f"**Question:** {s.get('research_question', 'N/A')}\n\n"
            r += f"**Method:** {s.get('methodology', 'N/A')}\n\n"
            r += f"**Findings:** {s.get('key_findings', 'N/A')}\n\n"
            r += f"**Limits:** {s.get('limitations', 'N/A')}\n\n"
            r += f"**Future:** {s.get('future_work', 'N/A')}\n\n"
        if gap:
            r += "\n## Gaps\n\n"
            r += f"**Themes:** {gap.get('common_themes', 'N/A')}\n\n"
            r += f"**Approaches:** {gap.get('divergent_approaches', 'N/A')}\n\n"
            r += f"**Gaps:** {gap.get('research_gaps', 'N/A')}\n\n"
            r += "**Directions:**\n"
            for idx, d in enumerate(gap.get('proposed_directions', []), 1):
                r += f"{idx}. {d.lstrip('0123456789.• ')}\n"
            r += f"\n**Contribution:** {gap.get('novel_contribution', 'N/A')}\n"
        return r

    def run(self):
        if st.session_state.page == 'home':
            self.home_page()
        else:
            self.workflow_page()


def main():
    app = ScholarSyncApp()
    app.run()


if __name__ == "__main__":
    main()
