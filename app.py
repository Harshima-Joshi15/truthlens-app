import streamlit as st
import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
import re

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="TruthLens | News Credibility Engine",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------
# Monochromatic Paper Background & Custom Styles
# ---------------------------
newspaper_bg = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
    /* Monochromatic Paper Tint Backdrop */
    .stApp {{
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.88) 0%, rgba(15, 23, 42, 0.93) 100%), 
                    url("{newspaper_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        backdrop-filter: grayscale(100%) contrast(105%);
        -webkit-backdrop-filter: grayscale(100%) contrast(105%);
        pointer-events: none;
        z-index: 0;
    }}
    
    /* Layout Alignment */
    .main .block-container {{
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        position: relative;
        z-index: 1;
    }}
    
    /* Dark Header Card */
    .hero-card {{
        background: rgba(10, 10, 14, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.15);
        margin-bottom: 2rem;
    }}
    .hero-left {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .lens-icon {{
        font-size: 2.6rem;
        filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.6));
    }}
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        line-height: 1;
        margin: 0;
    }}
    .hero-subtitle {{
        color: #38bdf8;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 6px;
        letter-spacing: 0.2px;
    }}
    .reader-img {{
        width: 85px;
        height: auto;
        opacity: 0.9;
        filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.5));
    }}
    
    /* Input Box Styling */
    .stTextArea textarea {{
        background-color: rgba(10, 10, 14, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 0.98rem !important;
        padding: 12px !important;
    }}
    .stTextArea textarea:focus {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.35) !important;
    }}
    
    /* Cyan Action Button */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(90deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
        margin-top: 0.5rem;
    }}
    .stButton>button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
    }}

    /* Monitored Network Badges */
    .domain-tag {{
        display: inline-block;
        background: rgba(10, 10, 14, 0.75);
        color: #e2e8f0;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        transition: border-color 0.2s ease, color 0.2s ease;
    }}
    .domain-tag:hover {{
        border-color: #38bdf8;
        color: #38bdf8;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: rgba(10, 10, 14, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Monitored Domains List
# ---------------------------
trusted_domains = [
    "bbc.com", "reuters.com", "ndtv.com", 
    "thehindu.com", "hindustantimes.com", "timesofindia.com",
    "indiatoday.in", "news18.com", "aljazeera.com", "cnn.com"
]

# ---------------------------
# Sidebar UI
# ---------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/search.png", width=50)
    st.title("TruthLens")
    st.caption("v2.0 • Credibility Engine")
    st.divider()
    
    st.markdown("### 🌐 Monitored Outlets")
    for d in trusted_domains:
        st.markdown(f'<span class="domain-tag">🟢 {d}</span>', unsafe_allow_html=True)
        
    st.divider()
    st.info("💡 Real-time news cross-checking database.")

# ---------------------------
# Hero Header Section
# ---------------------------
newspaper_reader_icon = "https://cdn-icons-png.flaticon.com/512/2965/2965879.png"

st.markdown(f"""
    <div class="hero-card">
        <div class="hero-left">
            <span class="lens-icon">🔍</span>
            <div>
                <div class="hero-title">TruthLens</div>
                <div class="hero-subtitle">Real-Time News Verification & Fact-Checking</div>
            </div>
        </div>
        <img src="{newspaper_reader_icon}" class="reader-img" alt="Reading Newspaper">
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# Backend Extraction & Analysis Logic
# ---------------------------
def extract_title_and_domain(url):
    """Extracts page title and base domain from news URLs."""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = soup.title.string if soup.title else ""
        if not title and soup.find("h1"):
            title = soup.find("h1").text
            
        title = re.sub(r'\s+', ' ', title).strip()
        return title, domain
    except:
        return "", ""

def clean_search_query(text):
    """Removes special characters/quotes and limits search key terms for valid RSS matching."""
    cleaned = re.sub(r'[^\w\s]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    words = cleaned.split()
    return " ".join(words[:8])

def search_live_news(query):
    """Queries live news feeds with URL encoding to prevent control character errors."""
    try:
        encoded_query = quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}"
        
        feed = feedparser.parse(url)
        
        results = []
        if hasattr(feed, 'entries'):
            for entry in feed.entries:
                results.append({
                    "title": entry.title,
                    "url": entry.link,
                    "published": getattr(entry, "published", "Recent")
                })
        return results
    except Exception as e:
        st.error(f"Error fetching live news: {e}")
        return []

def calculate_credibility_score(articles, input_domain):
    """Calculates credibility score based on verified outlet coverage."""
    if not articles:
        return 0, "No matching articles found in live news databases for this claim.", []

    trusted_matches = []
    other_matches = []

    for item in articles:
        link = item["url"].lower()
        if any(td in link for td in trusted_domains):
            trusted_matches.append(item)
        else:
            other_matches.append(item)

    trusted_count = len(trusted_matches)
    total_count = len(articles)

    if trusted_count > 0:
        score = (trusted_count * 25) + (total_count * 2)
        if input_domain and any(td in input_domain for td in trusted_domains):
            score += 15
    else:
        score = min(total_count * 3, 25)

    score = min(max(score, 5), 96)

    if score >= 70:
        reasoning = f"High probability of truth ({score}%). Found {trusted_count} verified report(s) from major news networks."
    elif score >= 40:
        reasoning = f"Moderate credibility ({score}%). Partial coverage found, but key tier-1 networks have not confirmed full details."
    else:
        reasoning = f"Low credibility score ({score}%). Found {trusted_count} verified reports from monitored news networks."

    combined_sources = trusted_matches + other_matches
    return score, reasoning, combined_sources[:6]

# ---------------------------
# Form Input Section
# ---------------------------
user_input = st.text_area(
    "Enter Article URL or Claim:",
    placeholder="Paste a link or news text here...",
    height=125
)

analyze = st.button("🔍 Run TruthLens Verification")

# Monitored Domain Display
st.write("")
st.markdown("<p style='color: #ffffff; font-size: 0.95rem; font-weight: 700;'>🌐 Monitored News Networks:</p>", unsafe_allow_html=True)
badges_html = "".join([f'<span class="domain-tag">🟢 {domain}</span>' for domain in trusted_domains])
st.markdown(f'<div style="margin-bottom: 2rem;">{badges_html}</div>', unsafe_allow_html=True)

# ---------------------------
# Output Results Section
# ---------------------------
if analyze and user_input:
    st.divider()
    
    with st.spinner("Analyzing claims and cross-checking live sources..."):
        input_domain = ""
        if user_input.startswith("http://") or user_input.startswith("https://"):
            extracted_title, input_domain = extract_title_and_domain(user_input)
            if extracted_title:
                search_term = clean_search_query(extracted_title)
                st.caption(f"**Extracted Article Title:** _{extracted_title}_")
            else:
                search_term = clean_search_query(user_input)
        else:
            search_term = clean_search_query(user_input)

        articles = search_live_news(search_term)
        score, reasoning, top_sources = calculate_credibility_score(articles, input_domain)

    # Display Metrics and Analysis Breakdown
    st.markdown("### 📊 Verification Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Truth/Credibility Score", f"{score}%")
    with col2:
        st.metric("Matching News Reports", len(top_sources))

    st.write("")
    if score >= 70:
        st.success(f"✅ **Verdict:** {reasoning}")
    elif score >= 40:
        st.warning(f"⚠️ **Verdict:** {reasoning}")
    else:
        st.error(f"❌ **Verdict:** {reasoning}")

    # Display Relevant Articles
    if top_sources:
        st.markdown("---")
        st.subheader("📰 Relevant Articles & Live Coverage")
        for idx, item in enumerate(top_sources, 1):
            st.markdown(f"**{idx}.** [{item['title']}]({item['url']})")
