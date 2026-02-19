# 📐 The Levelerr — Construction Bid Intelligence Platform

> **AI-Powered Drawing-to-Bid Gap Detection | Bid Leveling | Risk Mitigation**

---

## What It Does

The Levelerr uses Claude (Anthropic's AI) to:

1. **Read your drawing set** (PDF) and extract a required scope per trade
2. **Parse subcontractor bid PDFs** — extracting price, inclusions, and exclusions
3. **Detect gaps** — items in scope but missing from the bid, flagged by risk level
4. **Level bids side-by-side** so you're comparing apples to apples

---

## Deploy on Streamlit Cloud (Free)

### Step 1: Fork or clone this repo to your GitHub account

### Step 2: Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click **"New app"**
- Select your repo, branch `main`, file `app.py`
- Click **Deploy**

### Step 3: Enter your Anthropic API key in the sidebar when the app loads

Get an API key at [console.anthropic.com](https://console.anthropic.com)

---

## Usage

1. **Add trades** in the sidebar (Drywall, MEP, Glazing, etc.)
2. **Upload drawings PDF** → "Drawings & Scope" tab → click "Extract Scope"
3. **Upload bid PDFs** in each trade tab → Claude auto-extracts everything
4. **Review gaps** (red items = critical missing scope)
5. **Edit scope** anytime with the ✏️ Edit button — save to re-run all gap analysis

---

## Files

| File | Purpose |
|---|---|
| `app.py` | Full Streamlit application |
| `requirements.txt` | Python dependencies |

---

## Tech Stack

- **Streamlit** — UI framework
- **Anthropic Claude** — PDF reading, scope extraction, gap detection
- **Pandas** — Data handling
- **Plotly** — Visualizations
