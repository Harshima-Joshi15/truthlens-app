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
