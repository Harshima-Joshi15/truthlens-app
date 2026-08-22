# 🔍 TruthLens — Real-Time News Verification & Fact-Checking Engine

TruthLens is a Streamlit-powered news credibility tool designed to analyze claims, headlines, and article links in real time. It extracts core search intent, queries live RSS news databases, cross-checks reporting across trusted global outlets, and provides a dynamic truth/credibility score with matched coverage sources.

---

## ✨ Features

* **URL & Text Claim Verification:** Accepts full article URLs or raw claim text inputs.
* **Smart Search Query Cleaning:** Automatically strips special characters, quotes, and filler words to prevent feed syntax errors.
* **Live RSS News Matching:** Scans active Google News feeds for concurrent coverage.
* **Source Trust Analysis:** Dynamically weights scores based on matches against major verified networks (BBC, Reuters, NDTV, etc.).
* **Responsive Newspaper Aesthetic:** Features a customized dark-mode paper backdrop and styled UI components.

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit, Custom HTML/CSS
* **Web Scraping & Parsing:** BeautifulSoup4, Feedparser, Requests
* **Language:** Python 3.10+

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Harshima-Joshi15/fake-news-detection-app.git](https://github.com/Harshima-Joshi15/fake-news-detection-app.git)
   cd fake-news-detection-app
