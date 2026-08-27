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

# Custom Styles
newspaper_bg = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
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
        top: 0; left: 0; width: 100%; height: 100%;
        backdrop-filter: grayscale(100%) contrast(105%);
        -webkit-backdrop-filter: grayscale(100%) contrast(105%);
        pointer-events: none;
        z-index: 0;
    }}
    .main .block-container {{
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        position: relative;
        z-index: 1;
    }}
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
    .hero-left {{ display: flex; align-items: center; gap: 15px; }}
    .lens-icon {{ font-size: 2.6rem; filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.6)); }}
    .hero-title {{ font-size: 2.8rem; font-weight: 800; color: #ffffff; margin: 0; line-height: 1; }}
    .hero-subtitle {{ color: #38bdf8; font-size: 0.95rem; font-weight: 600; margin-top: 6px; }}
    .reader-img {{ width: 85px; height: auto; opacity: 0.9; }}
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
    .stButton>button {{
        width: 100%;
        background: linear-gradient(90deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        border: none;
        margin-top: 0.5rem;
    }}
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
    }}
    section[data-testid="stSidebar"] {{
        background-color: rgba(10, 10, 14, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Monitored Outlets & Keywords
# ---------------------------
trusted_domains = [
    "bbc.com", "reuters.com", "ndtv.com", "thehindu.com", 
    "hindustantimes.com", "timesofindia.com", "indiatoday.in", 
    "news18.com", "aljazeera.com", "cnn.com"
]

trusted_brands = [
    "bbc", "reuters", "ndtv", "the hindu", "hindustan times", 
    "times of india", "india today", "news18", "al jazeera", 
    "cnn", "economist", "dw", "boom", "indian express"
]

STOP_WORDS = {
    "is", "are", "was", "were", "did", "does", "do", "the", "a", "an",
    "really", "true", "false", "fake", "news", "what", "where", "who", "when", "how", "why"
}

# Expanded list of action words to check for rumor validation
SENSITIVE_ACTIONS = [
    "die", "died", "dead", "death", "killed", "kill", "passed away", 
    "arrested", "arrest", "resigned", "resign", "hospitalized", "crash", "crashed"
]

# ---------------------------
# Sidebar UI
# ---------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/search.png", width=50)
    st.title("TruthLens")
    st.caption("v2.0 • Real-Time Engine")
    st.divider()
    st.markdown("### 🌐 Monitored Outlets")
    for d in trusted_domains:
        st.markdown(f'<span class="domain-tag">🟢 {d}</span>', unsafe_allow_html=True)

# ---------------------------
# Hero Section
# ---------------------------
st.markdown("""
    <div class="hero-card">
        <div class="hero-left">
            <span class="lens-icon">🔍</span>
            <div>
                <div class="hero-title">TruthLens</div>
                <div class="hero-subtitle">Real-Time News Verification & Fact-Checking</div>
            </div>
        </div>
        <img src="https://cdn-icons-png.flaticon.com/512/2965/2965879.png" class="reader-img" alt="Newspaper">
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# Processing Helpers
# ---------------------------
def scrape_article_data(url):
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        title = soup.title.string if soup.title else ""
        if not title and soup.find("h1"):
            title = soup.find("h1").text
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title, domain
    except Exception:
        return "", ""

def fetch_rss_feed(query):
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    results = []
    if hasattr(feed, 'entries'):
        for entry in feed.entries:
            source_name = getattr(entry, 'source', {}).get('title', '')
            results.append({
                "title": entry.title,
                "url": entry.link,
                "source": source_name
            })
    return results

def clean_query(text):
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    keywords = [w for w in words if w not in STOP_WORDS]
    return " ".join(keywords) if keywords else text

# ---------------------------
# Analysis Engine
# ---------------------------
def analyze_url(url):
    title, domain = scrape_article_data(url)
    if not title:
        return 0, "Unable to reach or read the provided URL.", []

    is_monitored_domain = any(td in domain for td in trusted_domains)
    search_query = clean_query(title)
    related = fetch_rss_feed(search_query)

    trusted_matches = [
        item for item in related 
        if any(brand in item['source'].lower() or brand in item['title'].lower() for brand in trusted_brands)
    ]

    if is_monitored_domain:
        score = 95 if len(trusted_matches) >= 2 else 85
        verdict = f"High Reality Score ({score}%). Published by monitored outlet '{domain}' and supported by live news feeds."
    elif len(trusted_matches) >= 3:
        score = 78
        verdict = f"Moderate-High Reality Score ({score}%). Published externally, but corroborated by major news networks."
    elif len(trusted_matches) >= 1:
        score = 50
        verdict = f"Partial Reality Score ({score}%). Limited matching coverage found across verified outlets."
    else:
        score = 15
        verdict = f"Low Reality Score ({score}%). Unverified source with zero matching reports found in verified outlets."

    return score, verdict, title, related[:5]

def analyze_claim(claim):
    claim_lower = claim.lower()
    
    # Check if user claim contains any action word (die, dead, arrested, etc.)
    found_actions = [act for act in SENSITIVE_ACTIONS if act in claim_lower]
    
    search_query = clean_query(claim)
    articles = fetch_rss_feed(search_query)

    if not articles:
        return 10, "Claim Unverified (10%). No live news reports found matching this query.", []

    # Strict strict matching: Articles MUST match the action word if the claim contained one
    exact_claim_matches = []
    
    for item in articles:
        t_lower = item['title'].lower()
        s_lower = item['source'].lower()
        
        is_trusted = any(brand in t_lower or brand in s_lower for brand in trusted_brands)
        
        if found_actions:
            # Must contain at least one of the target action words in the article title
            has_action_in_title = any(act in t_lower for act in found_actions)
        else:
            has_action_in_title = True

        if is_trusted and has_action_in_title:
            exact_claim_matches.append(item)

    # Score Assignment
    if len(exact_claim_matches) >= 3:
        score = 92
        verdict = f"Claim Verified ({score}%). Confirmed by multiple monitored news networks."
    elif len(exact_claim_matches) >= 1:
        score = 75
        verdict = f"Claim Likely True ({score}%). Confirmed by verified news reports."
    elif found_actions:
        # If the claim was about death/arrest but 0 verified articles confirm that specific action
        score = 15
        verdict = f"Claim False / Unverified ({score}%). Monitored news networks do NOT report this claim."
    else:
        # General query with no specific sensitive action
        score = 35
        verdict = f"Uncertain Claim ({score}%). Missing direct confirmation from monitored networks."

    display_sources = exact_claim_matches if exact_claim_matches else []
    return score, verdict, display_sources

# ---------------------------
# UI Input & Display
# ---------------------------
user_input = st.text_area(
    "Enter Article URL or Claim:",
    placeholder="Paste news link (e.g., https://...) OR enter a claim (e.g., Did PM Modi die?)...",
    height=125
)

analyze = st.button("🔍 Run TruthLens Verification")

st.write("")
st.markdown("<p style='color: #ffffff; font-size: 0.95rem; font-weight: 700;'>🌐 Monitored News Networks:</p>", unsafe_allow_html=True)
badges_html = "".join([f'<span class="domain-tag">🟢 {domain}</span>' for domain in trusted_domains])
st.markdown(f'<div style="margin-bottom: 2rem;">{badges_html}</div>', unsafe_allow_html=True)

if analyze and user_input.strip():
    st.divider()
    input_str = user_input.strip()
    is_url = input_str.startswith("http://") or input_str.startswith("https://")

    with st.spinner("Processing input and cross-referencing news databases..."):
        if is_url:
            score, verdict, extracted_title, related_news = analyze_url(input_str)
            if extracted_title:
                st.caption(f"**Read Article Title:** _{extracted_title}_")
        else:
            score, verdict, related_news = analyze_claim(input_str)

    st.markdown("### 📊 Verification Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Reality / Credibility Score", f"{score}%")
    with col2:
        st.metric("Matching Verified Reports", len(related_news))

    st.write("")
    if score >= 70:
        st.success(f"✅ **Verdict:** {verdict}")
    elif score >= 40:
        st.warning(f"⚠️ **Verdict:** {verdict}")
    else:
        st.error(f"❌ **Verdict:** {verdict}")

    if related_news:
        st.markdown("---")
        st.subheader("📰 Matching Verified Reports")
        for idx, item in enumerate(related_news, 1):
            st.markdown(f"**{idx}.** [{item['title']}]({item['url']})")
