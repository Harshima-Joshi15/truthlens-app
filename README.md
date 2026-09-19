# 🔍 TruthLens — Real-Time News Verification & Fact-Checking Engine

> A real-time news credibility analysis system that cross-references claims and article links against live news feeds and monitored news sources.

TruthLens is a Streamlit-based news verification application that helps users evaluate online news claims and article URLs.

The system accepts an **article URL or text-based claim**, retrieves relevant live news results, compares them against monitored news sources, and generates a **rule-based credibility assessment** with supporting reports.

---

## 🎯 Problem Statement

The rapid spread of misleading headlines and unverified claims makes it difficult to determine whether information circulating online is being independently reported.

TruthLens addresses this by cross-referencing claims with **live news coverage from monitored sources** instead of relying only on a single article.

---

## 💡 How TruthLens Works

1. **User Input** — Accepts an article URL or text-based claim.
2. **Input Processing** — Extracts article titles/domains or cleans the submitted claim.
3. **Live News Search** — Queries Google News RSS for relevant coverage.
4. **Source Matching** — Compares retrieved reports against monitored news networks.
5. **Evidence Analysis** — Checks for corroborating reports and relevant event keywords.
6. **Credibility Assessment** — Generates a rule-based credibility score.
7. **Result Display** — Shows the score, verdict, and matching reports.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["👤 User Input"] --> B{"Input Type?"}

    B -->|Article URL| C["🌐 Extract Title & Domain"]
    B -->|Text Claim| D["📝 Clean & Process Claim"]

    C --> E["🔎 Generate Search Query"]
    D --> E

    E --> F["📰 Google News RSS"]
    F --> G["📚 Retrieve Live News Results"]

    G --> H["🔍 Match Monitored Sources"]

    H --> I{"Corroborating Reports?"}

    I -->|Yes| J["📊 Calculate Credibility Score"]
    I -->|No| K["⚠️ Low / Uncertain Confidence"]

    J --> L["📋 Generate Verification Verdict"]
    K --> L

    L --> M["🖥️ Streamlit Dashboard"]
    M --> N["📊 Score + Matching Reports + Sources"]

    N --> O["👤 User Reviews Evidence"]
    O --> P["✅ Verification Complete"]
---
## 🚧 Limitations

TruthLens is currently a **news-source corroboration system** rather than a complete automated fact-checking model.

The reliability of its assessment can be affected by:

- 📰 Availability and freshness of live RSS results
- 🔎 Search-result quality and relevance
- ⏱️ Delays between an event occurring and news outlets reporting it
- 📝 Differences in wording between articles covering the same event
- 🌐 Coverage limitations of the monitored news sources
- 📋 The predefined source and keyword matching rules

> **Note:** The credibility score represents the level of available supporting evidence. It should not be interpreted as an absolute determination that a claim is true or false.

---

## 🔮 Future Improvements

The current system provides a foundation that can be extended with more advanced AI and NLP capabilities.

Planned improvements include:

- 🤖 **Semantic Similarity** — Compare claims and articles based on meaning rather than exact keywords.
- 🧠 **NLP-Based Verification** — Use transformer-based models for deeper claim analysis.
- 📰 **News Clustering** — Group multiple reports covering the same event.
- 🌍 **Multilingual Verification** — Support claims and news sources in multiple languages.
- 🔗 **Evidence Graphs** — Connect claims with their supporting and contradicting reports.
- 🧩 **Named Entity Recognition** — Identify people, organizations, locations, and events within claims.
- 📈 **Historical Analytics** — Track news coverage and credibility patterns over time.
- 🧪 **Model Evaluation** — Evaluate future ML-based verification models using labeled fact-checking datasets.

---

## 📝 Conclusion

TruthLens demonstrates how **real-time web data, news-source corroboration, and explainable rule-based analysis** can be combined to build a practical news verification system.

Instead of relying on a single article, the system searches for supporting coverage across multiple monitored news sources and presents the available evidence alongside its credibility assessment.

The current implementation provides a foundation for extending the system toward **NLP, semantic analysis, and machine-learning-based fact verification**.

---

## 👩‍💻 Author

**Harshima Joshi**

B.Tech — VLSI / Electronics

Interested in **AI, Data Science, VLSI, and intelligent information systems.**

---

## ⭐ Project

If you find TruthLens interesting, consider giving the repository a ⭐ on GitHub.
