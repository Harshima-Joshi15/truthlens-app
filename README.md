# 🔍 TruthLens — Real-Time News Verification & Fact-Checking Engine

> **A real-time news credibility analysis system that cross-references claims and article links against live news feeds and monitored news sources.**

TruthLens is a Streamlit-based news verification application designed to help users evaluate the credibility of online news claims and article URLs.

The system accepts either a **news article URL** or a **text-based claim**, extracts and cleans the relevant information, searches live Google News RSS results, compares the retrieved coverage against a predefined set of monitored news networks, and generates a **rule-based credibility assessment** along with supporting reports.

---

## 🎯 Problem Statement

The rapid spread of misleading headlines, unverified claims, and manipulated information makes it difficult to determine whether a piece of news is being independently reported.

TruthLens addresses this problem by using **live news-source corroboration** rather than relying only on the content of a single article.

Instead of asking:

> "Does this article look real?"

TruthLens asks:

> "Are independent monitored news sources currently reporting the same information?"

---

## 💡 How TruthLens Works

The verification pipeline follows these major stages:

1. **Input Collection**
   - Accepts a complete article URL
   - OR accepts a text-based news claim

2. **Input Processing**
   - For URLs, the system extracts the article title and domain.
   - For claims, the text is cleaned and converted into a searchable query.

3. **Live News Retrieval**
   - The processed query is sent to Google News RSS.
   - Current matching news articles are retrieved.

4. **Source Verification**
   - Retrieved articles are compared against monitored news networks.
   - Source names and article titles are checked for relevant matches.

5. **Evidence Matching**
   - Multiple matching reports increase the confidence of the assessment.
   - Specific action-related claims such as deaths, arrests, resignations, etc. receive stricter matching.

6. **Credibility Assessment**
   - A rule-based scoring system generates the final credibility assessment.

7. **Result Presentation**
   - Displays the credibility score
   - Shows the number of matching reports
   - Provides the matched news sources for further verification

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["👤 User Input"] --> B{"Input Type?"}

    B -->|Article URL| C["🌐 Extract Article Title & Domain"]
    B -->|Text Claim| D["📝 Clean & Process Claim"]

    C --> E["🔎 Generate Search Query"]
    D --> E

    E --> F["📰 Google News RSS"]
    F --> G["📚 Retrieve Live News Results"]

    G --> H["🔍 Match Against Monitored Sources"]

    H --> I{"Corroborating Reports Found?"}

    I -->|Yes| J["📊 Calculate Rule-Based Credibility Score"]
    I -->|No| K["⚠️ Low / Uncertain Confidence"]

    J --> L["📋 Generate Verification Verdict"]
    K --> L

    L --> M["🖥️ Streamlit Dashboard"]
    M --> N["📈 Score + Matching Reports + Sources"]
