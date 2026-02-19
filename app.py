"""
The Levelerr — Construction Bid Intelligence Platform
Drawing-to-Bid Gap Detection | AI-Powered Scope Extraction | Multi-Sub Leveling
"""

import streamlit as st
import anthropic
import base64
import json
import re
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Levelerr | Construction Bid Intelligence",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# MIDNIGHT PROFESSIONAL THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }
.stApp {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid #1E293B !important;
}
[data-testid="stSidebar"] * { color: #F8FAFC; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #38BDF8 !important; }
[data-testid="stSidebar"] label { color: #94A3B8 !important; font-size: 0.8rem !important; }

/* ── Main content ── */
[data-testid="stMainBlockContainer"] { padding-top: 1.5rem; }

/* ── Headings ── */
h1 { color: #F8FAFC !important; }
h2, h3 { color: #CBD5E1 !important; }
p, li { color: #94A3B8; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 0;
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: #263348 !important;
    color: #F8FAFC !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0EA5E9, #38BDF8) !important;
    color: #0F172A !important;
    font-weight: 800 !important;
    border-color: #38BDF8 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #0F172A;
    padding-top: 20px;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
}
textarea { color: #F8FAFC !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0EA5E9, #38BDF8) !important;
    color: #0F172A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #38BDF8, #7DD3FC) !important;
    box-shadow: 0 0 20px rgba(56,189,248,0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary buttons */
button[kind="secondary"] {
    background: #1E293B !important;
    color: #94A3B8 !important;
    border: 1px solid #334155 !important;
}
button[kind="secondary"]:hover {
    background: #263348 !important;
    color: #F8FAFC !important;
    box-shadow: none !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E293B, #162032) !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 800 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: #1E293B !important;
    border: 1px dashed #334155 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #38BDF8 !important; }
[data-testid="stFileUploader"] * { color: #94A3B8 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: #94A3B8 !important; font-weight: 600 !important; }
[data-testid="stExpander"] summary:hover { color: #38BDF8 !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] iframe { border-radius: 8px; }

/* ── Success / Error / Info ── */
[data-testid="stAlert"] { border-radius: 8px !important; }
.stSuccess { background-color: rgba(52,211,153,0.1) !important; border: 1px solid rgba(52,211,153,0.3) !important; }
.stError { background-color: rgba(251,113,133,0.1) !important; border: 1px solid rgba(251,113,133,0.3) !important; }
.stInfo { background-color: rgba(56,189,248,0.1) !important; border: 1px solid rgba(56,189,248,0.3) !important; }
.stWarning { background-color: rgba(251,191,36,0.1) !important; border: 1px solid rgba(251,191,36,0.3) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ── Divider ── */
hr { border-color: #1E293B !important; margin: 16px 0 !important; }

/* ── Custom component classes ── */
.scope-item-included {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    border-left: 3px solid #34D399;
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.83rem;
    color: #A7F3D0;
}
.scope-item-gap {
    background: rgba(251,113,133,0.08);
    border: 1px solid rgba(251,113,133,0.25);
    border-left: 3px solid #FB7185;
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.83rem;
    color: #FDA4AF;
    font-weight: 600;
}
.scope-item-gap::before { content: "⚠ CRITICAL GAP — "; color: #FB7185; font-weight: 800; }

.card {
    background: linear-gradient(135deg, #1E293B 0%, #162032 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.card-accent {
    background: linear-gradient(135deg, #1E293B 0%, #162032 100%);
    border: 1px solid #334155;
    border-top: 2px solid #38BDF8;
    border-radius: 0 0 12px 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.section-header {
    background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%);
    border-left: 3px solid #38BDF8;
    padding: 10px 18px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0 14px 0;
}
.section-header h4 {
    color: #38BDF8 !important;
    margin: 0 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
.section-header p {
    color: #64748B !important;
    margin: 2px 0 0 0 !important;
    font-size: 0.76rem !important;
}
.winner-pill {
    display: inline-block;
    background: linear-gradient(90deg, #0EA5E9, #38BDF8);
    color: #0F172A;
    font-weight: 800;
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    vertical-align: middle;
    margin-left: 8px;
}
.price-tag {
    font-size: 1.6rem;
    font-weight: 900;
    color: #F8FAFC;
    line-height: 1;
}
.sub-label {
    font-size: 0.72rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}
.gap-count-badge {
    background: rgba(251,113,133,0.15);
    border: 1px solid rgba(251,113,133,0.4);
    color: #FB7185;
    font-weight: 700;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
}
.help-box {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    padding: 20px 24px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font=dict(family="Inter, Segoe UI, sans-serif", color="#F8FAFC", size=12),
    xaxis=dict(gridcolor="#334155", linecolor="#334155", tickfont=dict(color="#94A3B8")),
    yaxis=dict(gridcolor="#334155", linecolor="#334155", tickfont=dict(color="#94A3B8")),
    legend=dict(bgcolor="#0F172A", bordercolor="#334155", borderwidth=1, font=dict(color="#94A3B8")),
    margin=dict(l=20, r=20, t=50, b=20),
)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "trades": ["Drywall", "MEP", "Interiors", "Site Work"],
    "drawing_pdf_bytes": None,
    "drawing_filename": "",
    "master_scopes": {},       # {trade: [str, ...]}
    "scope_edit_mode": {},     # {trade: bool}
    "scope_edit_buffer": {},   # {trade: str}
    "sub_bids": {},            # {trade: [{name, filename, pdf_bytes, price, inclusions, exclusions, gaps, raw_text}]}
    "api_key": "",
    "project_name": "My Project",
    "extraction_status": {},   # {trade: "pending"|"done"|"error"}
    "ai_suggested_trades": [],
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def ensure_trade_state(trade: str):
    if trade not in st.session_state.master_scopes:
        st.session_state.master_scopes[trade] = []
    if trade not in st.session_state.scope_edit_mode:
        st.session_state.scope_edit_mode[trade] = False
    if trade not in st.session_state.scope_edit_buffer:
        st.session_state.scope_edit_buffer[trade] = ""
    if trade not in st.session_state.sub_bids:
        st.session_state.sub_bids[trade] = []
    if trade not in st.session_state.extraction_status:
        st.session_state.extraction_status[trade] = "pending"

for t in st.session_state.trades:
    ensure_trade_state(t)

# ─────────────────────────────────────────────────────────────────────────────
# ANTHROPIC HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_client():
    key = st.session_state.api_key.strip()
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)

def pdf_to_base64(pdf_bytes: bytes) -> str:
    return base64.standard_b64encode(pdf_bytes).decode("utf-8")

def extract_scope_from_drawings(pdf_bytes: bytes, trades: list[str]) -> dict:
    """Send drawing PDF to Claude, get back {trade: [scope items]} + suggested trades."""
    client = get_client()
    if not client:
        return {}
    
    b64 = pdf_to_base64(pdf_bytes)
    trades_str = ", ".join(trades)
    
    prompt = f"""You are a senior construction estimator reviewing architectural and engineering drawings.

Analyze these construction drawings and do the following:

1. For each of these trades: {trades_str}
   — Extract a detailed list of required scope items (materials, systems, specifications)
   — Be specific: include dimensions, quantities where visible, product types, finishes

2. Additionally, suggest any OTHER trades that appear required based on the drawings but are NOT in the list above.

Respond ONLY with valid JSON in this exact format:
{{
  "trades": {{
    "TradeNameExact": [
      "Scope item 1",
      "Scope item 2"
    ]
  }},
  "suggested_trades": [
    {{
      "name": "Trade Name",
      "reason": "Why this trade is needed",
      "scope_items": ["item 1", "item 2"]
    }}
  ]
}}

Use the exact trade names as provided. If a trade has no visible scope in the drawings, return an empty array for it.
Be thorough. A missed scope item becomes a change order."""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": b64,
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        st.error(f"AI returned invalid JSON: {e}")
        return {}
    except Exception as e:
        st.error(f"API error: {e}")
        return {}

def parse_bid_pdf(pdf_bytes: bytes, trade: str, master_scope: list[str], sub_name: str) -> dict:
    """Extract bid data from a subcontractor PDF."""
    client = get_client()
    if not client:
        return {}
    
    b64 = pdf_to_base64(pdf_bytes)
    scope_list = "\n".join(f"- {item}" for item in master_scope) if master_scope else "No master scope defined."
    
    prompt = f"""You are a construction bid analyst reviewing a subcontractor bid for the {trade} trade.

MASTER SCOPE (the required items for this trade):
{scope_list}

Analyze this bid document and extract:
1. The total bid price (numeric, USD)
2. All explicit inclusions mentioned
3. All explicit exclusions mentioned
4. Compare EVERY item in the Master Scope against the inclusions — identify what is MISSING (gaps)
5. Key notes, clarifications, or assumptions

Respond ONLY with valid JSON:
{{
  "subcontractor_name": "{sub_name}",
  "total_price": 0,
  "price_display": "$0",
  "inclusions": [
    "Included item 1",
    "Included item 2"
  ],
  "exclusions": [
    "Excluded item 1"
  ],
  "gaps": [
    {{
      "master_scope_item": "Missing item from master scope",
      "risk": "HIGH|MEDIUM|LOW",
      "estimated_value": "Rough cost estimate or Unknown",
      "note": "Why this matters"
    }}
  ],
  "key_notes": [
    "Clarification or assumption 1"
  ],
  "bid_confidence": "HIGH|MEDIUM|LOW",
  "bid_confidence_reason": "Why you scored it this way"
}}

Be precise. A gap = something in the master scope that is NOT clearly included in this bid.
For risk: HIGH = likely major change order, MEDIUM = worth discussing, LOW = minor/admin."""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": b64,
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        st.error(f"Bid parse error (invalid JSON): {e}")
        return {}
    except Exception as e:
        st.error(f"API error parsing bid: {e}")
        return {}

# ─────────────────────────────────────────────────────────────────────────────
# FORMATTING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_usd(val) -> str:
    try:
        return f"${float(val):,.0f}"
    except:
        return "—"

def risk_color(risk: str) -> str:
    return {"HIGH": "#FB7185", "MEDIUM": "#FBBF24", "LOW": "#34D399"}.get(risk.upper(), "#94A3B8")

def confidence_color(conf: str) -> str:
    return {"HIGH": "#34D399", "MEDIUM": "#FBBF24", "LOW": "#FB7185"}.get(conf.upper(), "#94A3B8")

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / Title
    st.markdown("""
    <div style='padding:16px 0 12px 0;'>
        <div style='font-size:1.5rem; font-weight:900; color:#38BDF8; letter-spacing:0.04em;'>
            📐 THE LEVELERR
        </div>
        <div style='font-size:0.7rem; color:#475569; letter-spacing:0.14em; text-transform:uppercase; margin-top:2px;'>
            Bid Intelligence Platform
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

    if st.session_state.api_key:
        st.markdown("<p style='color:#34D399; font-size:0.78rem;'>✓ API Key loaded</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#FB7185; font-size:0.78rem;'>⚠ API Key required for AI features</p>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Project Name
    st.markdown("### 🏗 Project Settings")
    proj_name = st.text_input("Project Name", value=st.session_state.project_name)
    st.session_state.project_name = proj_name

    st.markdown("<hr>", unsafe_allow_html=True)

    # Trade Management
    st.markdown("### 🏷 Trade Management")
    st.markdown("<p style='font-size:0.78rem; color:#64748B;'>Trades define your bid tabs. Changes persist.</p>", unsafe_allow_html=True)

    # Show current trades with delete buttons
    trades_to_delete = []
    for trade in st.session_state.trades:
        col_t, col_del = st.columns([3, 1])
        with col_t:
            st.markdown(f"<div style='padding:6px 0; color:#CBD5E1; font-size:0.82rem;'>📁 {trade}</div>", unsafe_allow_html=True)
        with col_del:
            if st.button("✕", key=f"del_trade_{trade}", help=f"Delete {trade}"):
                trades_to_delete.append(trade)

    for trade in trades_to_delete:
        st.session_state.trades.remove(trade)
        for d in ["master_scopes", "scope_edit_mode", "scope_edit_buffer", "sub_bids", "extraction_status"]:
            st.session_state[d].pop(trade, None)
        st.rerun()

    # Add new trade
    with st.form("add_trade_form", clear_on_submit=True):
        new_trade = st.text_input("New Trade Name", placeholder="e.g. Glazing, Roofing...")
        if st.form_submit_button("➕ Add Trade"):
            if new_trade.strip() and new_trade.strip() not in st.session_state.trades:
                st.session_state.trades.append(new_trade.strip())
                ensure_trade_state(new_trade.strip())
                st.rerun()

    # AI Suggested trades
    if st.session_state.ai_suggested_trades:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🤖 AI-Suggested Trades")
        st.markdown("<p style='font-size:0.76rem; color:#64748B;'>Found in your drawings:</p>", unsafe_allow_html=True)
        for sug in st.session_state.ai_suggested_trades:
            s_col1, s_col2 = st.columns([3, 1])
            with s_col1:
                st.markdown(f"<div style='color:#94A3B8; font-size:0.78rem; padding:3px 0;'>💡 {sug['name']}</div>", unsafe_allow_html=True)
            with s_col2:
                if st.button("Add", key=f"add_sug_{sug['name']}"):
                    if sug["name"] not in st.session_state.trades:
                        st.session_state.trades.append(sug["name"])
                        ensure_trade_state(sug["name"])
                        st.session_state.master_scopes[sug["name"]] = sug.get("scope_items", [])
                    st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    # Quick stats
    total_subs = sum(len(v) for v in st.session_state.sub_bids.values())
    total_gaps = sum(
        sum(len(b.get("gaps", [])) for b in bids)
        for bids in st.session_state.sub_bids.values()
    )
    st.metric("Trades", len(st.session_state.trades))
    st.metric("Bids Loaded", total_subs)
    st.metric("Total Gaps", total_gaps)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex; align-items:flex-end; gap:16px; margin-bottom:4px;'>
    <div>
        <h1 style='margin:0; font-size:2rem; font-weight:900;
            background:linear-gradient(90deg,#F8FAFC 0%,#38BDF8 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            {st.session_state.project_name}
        </h1>
        <p style='margin:4px 0 0 0; color:#475569; font-size:0.82rem;'>
            The Levelerr · Drawing-to-Bid Gap Detection · AI-Powered Bid Intelligence
        </p>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL TABS
# ─────────────────────────────────────────────────────────────────────────────
main_tabs = st.tabs(["📋 Drawings & Scope", "📊 Analytics", "❓ Help"] + [f"🔧 {t}" for t in st.session_state.trades])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: DRAWINGS & SCOPE
# ═════════════════════════════════════════════════════════════════════════════
with main_tabs[0]:
    st.markdown("""
    <div class='section-header'>
        <h4>Drawing Set Ingestion</h4>
        <p>Upload your full drawing set PDF. Claude will extract the Master Scope for each trade.</p>
    </div>
    """, unsafe_allow_html=True)

    upload_col, status_col = st.columns([3, 2])
    with upload_col:
        drawing_file = st.file_uploader(
            "Upload Full Drawing Set (PDF)",
            type=["pdf"],
            key="drawing_upload",
            help="Architectural, structural, MEP drawings — all in one PDF is fine."
        )

    if drawing_file is not None:
        st.session_state.drawing_pdf_bytes = drawing_file.read()
        st.session_state.drawing_filename = drawing_file.name
        with status_col:
            st.markdown(f"""
            <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25);
                        border-radius:8px; padding:14px 16px; margin-top:24px;'>
                <div style='color:#34D399; font-weight:700; font-size:0.85rem;'>✓ Drawing Loaded</div>
                <div style='color:#64748B; font-size:0.78rem; margin-top:4px;'>{drawing_file.name}</div>
                <div style='color:#64748B; font-size:0.75rem;'>{len(st.session_state.drawing_pdf_bytes)/1024:.0f} KB</div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.drawing_pdf_bytes:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        extract_col1, extract_col2 = st.columns([2, 3])
        with extract_col1:
            if st.button("🤖 Extract Scope from Drawings", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("Please enter your Anthropic API Key in the sidebar.")
                else:
                    with st.spinner("Claude is reading your drawings… This takes 30–60 seconds for large PDFs."):
                        result = extract_scope_from_drawings(
                            st.session_state.drawing_pdf_bytes,
                            st.session_state.trades
                        )
                    if result:
                        # Populate master scopes
                        for trade, items in result.get("trades", {}).items():
                            if trade in st.session_state.master_scopes:
                                st.session_state.master_scopes[trade] = items
                                st.session_state.extraction_status[trade] = "done"

                        # Store suggested trades
                        suggested = result.get("suggested_trades", [])
                        existing = st.session_state.trades
                        st.session_state.ai_suggested_trades = [
                            s for s in suggested if s["name"] not in existing
                        ]
                        st.success(f"✓ Scope extracted for {len(result.get('trades', {}))} trades. "
                                   f"{len(st.session_state.ai_suggested_trades)} additional trades suggested in sidebar.")
                        st.rerun()

        with extract_col2:
            st.markdown("""
            <div style='background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.15);
                        border-radius:8px; padding:12px 16px; font-size:0.79rem; color:#94A3B8;'>
                <strong style='color:#38BDF8;'>What happens:</strong>
                Claude reads every page of your drawings and extracts all required scope items per trade.
                Results populate the Master Scope in each trade tab as the baseline for gap detection.
            </div>
            """, unsafe_allow_html=True)

    # Master scope overview
    st.markdown("""
    <div class='section-header' style='margin-top:28px;'>
        <h4>Master Scope Overview</h4>
        <p>Review extracted scopes. Use the Edit button in each trade tab to modify individual items.</p>
    </div>
    """, unsafe_allow_html=True)

    if not any(st.session_state.master_scopes.values()):
        st.markdown("""
        <div class='card' style='text-align:center; padding:40px;'>
            <div style='font-size:2.5rem; margin-bottom:10px;'>📋</div>
            <div style='color:#38BDF8; font-weight:700; margin-bottom:6px;'>No Scope Loaded Yet</div>
            <div style='color:#475569; font-size:0.83rem;'>Upload drawings above or add scope manually in each trade tab.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        overview_cols = st.columns(min(len(st.session_state.trades), 4))
        for i, trade in enumerate(st.session_state.trades):
            with overview_cols[i % 4]:
                items = st.session_state.master_scopes.get(trade, [])
                status = st.session_state.extraction_status.get(trade, "pending")
                status_icon = "✓" if status == "done" else "○"
                status_color = "#34D399" if status == "done" else "#475569"
                st.markdown(f"""
                <div class='card' style='min-height:120px;'>
                    <div style='color:{status_color}; font-size:0.7rem; font-weight:700;
                                text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px;'>
                        {status_icon} {trade}
                    </div>
                    <div style='color:#F8FAFC; font-size:1.6rem; font-weight:900; margin-bottom:4px;'>
                        {len(items)}
                    </div>
                    <div style='color:#64748B; font-size:0.76rem;'>scope items</div>
                    {"".join(f"<div style='color:#475569; font-size:0.72rem; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>· {item[:35]}...</div>" for item in items[:3])}
                    {"" if len(items) <= 3 else f"<div style='color:#334155; font-size:0.7rem; margin-top:4px;'>+{len(items)-3} more</div>"}
                </div>
                """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TRADE TABS (dynamic)
# ═════════════════════════════════════════════════════════════════════════════
for trade_idx, trade in enumerate(st.session_state.trades):
    tab_offset = 3  # "Drawings", "Analytics", "Help" come first
    with main_tabs[tab_offset + trade_idx]:
        ensure_trade_state(trade)
        scope_items = st.session_state.master_scopes.get(trade, [])
        sub_bids = st.session_state.sub_bids.get(trade, [])

        # Trade header
        total_gaps_trade = sum(len(b.get("gaps", [])) for b in sub_bids)
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:4px;'>
            <div>
                <h2 style='margin:0; font-size:1.4rem;'>{trade}</h2>
                <p style='margin:2px 0 0 0; color:#475569; font-size:0.8rem;'>
                    {len(scope_items)} scope items · {len(sub_bids)} bid(s) loaded
                    {"&nbsp;&nbsp;<span class='gap-count-badge'>⚠ " + str(total_gaps_trade) + " total gaps</span>" if total_gaps_trade else ""}
                </p>
            </div>
        </div>
        <hr>
        """, unsafe_allow_html=True)

        # ── LEFT / RIGHT SPLIT ──
        scope_col, bids_col = st.columns([1, 2], gap="large")

        # ────────────────────────────────────
        # LEFT: MASTER SCOPE
        # ────────────────────────────────────
        with scope_col:
            st.markdown("""
            <div class='section-header'>
                <h4>AI-Generated Master Scope</h4>
                <p>Baseline for gap detection</p>
            </div>
            """, unsafe_allow_html=True)

            edit_mode = st.session_state.scope_edit_mode.get(trade, False)

            if not edit_mode:
                # View mode
                if scope_items:
                    scope_display = ""
                    for item in scope_items:
                        scope_display += f"<div style='padding:6px 10px; margin:3px 0; background:#1E293B; border:1px solid #334155; border-radius:6px; font-size:0.8rem; color:#CBD5E1;'>· {item}</div>"
                    st.markdown(scope_display, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='padding:24px; text-align:center; background:#1E293B; border:1px dashed #334155; border-radius:8px;'>
                        <div style='color:#475569; font-size:0.82rem;'>No scope items yet.</div>
                        <div style='color:#334155; font-size:0.75rem; margin-top:4px;'>Upload drawings or click Edit to add manually.</div>
                    </div>
                    """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("✏️ Edit Scope", key=f"edit_scope_{trade}", use_container_width=True):
                        st.session_state.scope_edit_buffer[trade] = "\n".join(scope_items)
                        st.session_state.scope_edit_mode[trade] = True
                        st.rerun()
                with btn_col2:
                    if st.button("🗑 Clear", key=f"clear_scope_{trade}", use_container_width=True):
                        st.session_state.master_scopes[trade] = []
                        st.rerun()
            else:
                # Edit mode
                st.markdown("""
                <div style='background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.2);
                            border-radius:6px; padding:8px 12px; font-size:0.76rem; color:#38BDF8; margin-bottom:8px;'>
                    ✏️ Edit mode — one item per line
                </div>
                """, unsafe_allow_html=True)

                buffer = st.text_area(
                    "Scope Items (one per line)",
                    value=st.session_state.scope_edit_buffer.get(trade, ""),
                    height=300,
                    key=f"scope_textarea_{trade}",
                    label_visibility="collapsed",
                    placeholder="5/8\" Type X GWB\nMetal stud framing\nAcoustic insulation..."
                )
                st.session_state.scope_edit_buffer[trade] = buffer

                save_col, cancel_col = st.columns(2)
                with save_col:
                    if st.button("💾 Save & Update All Bids", key=f"save_scope_{trade}", use_container_width=True):
                        new_items = [l.strip() for l in buffer.split("\n") if l.strip()]
                        st.session_state.master_scopes[trade] = new_items
                        st.session_state.scope_edit_mode[trade] = False
                        # Clear cached gaps so they re-run against new scope
                        for bid in st.session_state.sub_bids.get(trade, []):
                            bid["gaps"] = []
                            bid["stale"] = True
                        st.success(f"Scope updated — {len(new_items)} items. Re-run gap analysis on bids.")
                        st.rerun()
                with cancel_col:
                    if st.button("✕ Cancel", key=f"cancel_scope_{trade}", use_container_width=True):
                        st.session_state.scope_edit_mode[trade] = False
                        st.rerun()

        # ────────────────────────────────────
        # RIGHT: SUB BIDS
        # ────────────────────────────────────
        with bids_col:
            st.markdown("""
            <div class='section-header'>
                <h4>Subcontractor Bid Analysis</h4>
                <p>Upload PDFs · Claude extracts price, inclusions, gaps</p>
            </div>
            """, unsafe_allow_html=True)

            # Upload new bid
            with st.expander("➕ Upload New Subcontractor Bid", expanded=len(sub_bids) == 0):
                u1, u2 = st.columns(2)
                with u1:
                    sub_name_input = st.text_input("Subcontractor Name", key=f"sub_name_{trade}", placeholder="ABC Drywall Co.")
                with u2:
                    bid_pdf = st.file_uploader("Bid PDF", type=["pdf"], key=f"bid_upload_{trade}")

                if bid_pdf and sub_name_input and st.button(f"🤖 Parse Bid with Claude", key=f"parse_bid_{trade}", use_container_width=True):
                    if not st.session_state.api_key:
                        st.error("API Key required.")
                    else:
                        with st.spinner(f"Claude is reading {sub_name_input}'s bid…"):
                            pdf_bytes = bid_pdf.read()
                            parsed = parse_bid_pdf(pdf_bytes, trade, scope_items, sub_name_input)
                        if parsed:
                            parsed["filename"] = bid_pdf.name
                            parsed["pdf_bytes"] = pdf_bytes
                            parsed["stale"] = False
                            parsed["timestamp"] = datetime.now().strftime("%b %d, %Y %H:%M")
                            # Use user-provided name if AI didn't find one
                            if not parsed.get("subcontractor_name") or parsed["subcontractor_name"] == sub_name_input:
                                parsed["subcontractor_name"] = sub_name_input
                            st.session_state.sub_bids[trade].append(parsed)
                            st.success(f"✓ {sub_name_input} parsed — {len(parsed.get('gaps', []))} gap(s) detected.")
                            st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

            # Display bids
            if not sub_bids:
                st.markdown("""
                <div class='card' style='text-align:center; padding:32px;'>
                    <div style='font-size:2rem; margin-bottom:8px;'>📄</div>
                    <div style='color:#475569; font-size:0.83rem;'>No bids uploaded yet. Add one above.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Price comparison metrics
                if len(sub_bids) > 1:
                    m_cols = st.columns(len(sub_bids) + 1)
                    prices = [float(b.get("total_price", 0)) for b in sub_bids if b.get("total_price", 0)]
                    min_price = min(prices) if prices else 0
                    for mi, bid in enumerate(sub_bids):
                        price = float(bid.get("total_price", 0))
                        is_low = price == min_price and price > 0
                        delta_pct = ((price - min_price) / min_price * 100) if min_price and price > min_price else None
                        with m_cols[mi]:
                            st.metric(
                                bid.get("subcontractor_name", f"Sub {mi+1}"),
                                fmt_usd(price) if price else "—",
                                delta=f"+{delta_pct:.1f}% vs low" if delta_pct else ("Lowest" if is_low else None),
                                delta_color="inverse" if delta_pct else "normal"
                            )
                    with m_cols[-1]:
                        total_scope_budget = 0
                        st.metric("Gap Count", sum(len(b.get("gaps", [])) for b in sub_bids), delta="total risk items")

                st.markdown("<hr>", unsafe_allow_html=True)

                # Bid cards — up to 3 side-by-side
                bid_display_cols = st.columns(min(len(sub_bids), 3))
                for bi, bid in enumerate(sub_bids[:3]):
                    col_idx = bi % len(bid_display_cols)
                    with bid_display_cols[col_idx]:
                        name = bid.get("subcontractor_name", f"Sub {bi+1}")
                        price = bid.get("total_price", 0)
                        inclusions = bid.get("inclusions", [])
                        exclusions = bid.get("exclusions", [])
                        gaps = bid.get("gaps", [])
                        notes = bid.get("key_notes", [])
                        confidence = bid.get("bid_confidence", "")
                        conf_reason = bid.get("bid_confidence_reason", "")
                        stale = bid.get("stale", False)
                        timestamp = bid.get("timestamp", "")

                        # Determine accent color
                        prices_list = [float(b.get("total_price", 0)) for b in sub_bids if b.get("total_price", 0)]
                        is_winner = float(price) == min(prices_list) if prices_list else False
                        accent = "#38BDF8" if is_winner else "#334155"

                        st.markdown(f"""
                        <div style='border:1px solid {accent}; border-top:3px solid {accent};
                                    background:linear-gradient(135deg,#1E293B,#162032);
                                    border-radius:0 0 12px 12px; padding:16px; margin-bottom:8px;'>
                            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;'>
                                <div>
                                    <div style='color:#F8FAFC; font-weight:800; font-size:0.9rem;'>
                                        {name}
                                        {"<span class='winner-pill'>✓ LOWEST</span>" if is_winner else ""}
                                    </div>
                                    <div class='sub-label' style='margin-top:2px;'>{bid.get("filename", "")[:30]}</div>
                                </div>
                                <div style='text-align:right;'>
                                    <div class='price-tag'>{fmt_usd(price)}</div>
                                    <div style='font-size:0.7rem; color:#475569; margin-top:1px;'>{timestamp}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        # Confidence badge
                        if confidence:
                            cc = confidence_color(confidence)
                            st.markdown(f"""
                            <div style='background:rgba(0,0,0,0.2); border-radius:6px; padding:6px 10px; margin-bottom:10px;'>
                                <span style='font-size:0.7rem; color:#64748B;'>Bid Confidence: </span>
                                <span style='color:{cc}; font-weight:700; font-size:0.78rem;'>{confidence}</span>
                                <div style='color:#475569; font-size:0.7rem; margin-top:2px;'>{conf_reason[:80]}{"..." if len(conf_reason)>80 else ""}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        if stale:
                            st.markdown("""
                            <div style='background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3);
                                        border-radius:6px; padding:5px 10px; font-size:0.72rem; color:#FBBF24; margin-bottom:8px;'>
                                ⟳ Scope changed — re-run gap analysis
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                        # Inclusions / Exclusions / Gaps in expanders
                        if inclusions:
                            with st.expander(f"✅ Inclusions ({len(inclusions)})", expanded=False):
                                for item in inclusions:
                                    st.markdown(f"<div class='scope-item-included'>{item}</div>", unsafe_allow_html=True)

                        if exclusions:
                            with st.expander(f"❌ Exclusions ({len(exclusions)})", expanded=False):
                                for item in exclusions:
                                    st.markdown(f"""
                                    <div style='background:rgba(251,146,60,0.08); border-left:3px solid #FB923C;
                                                border-radius:0 6px 6px 0; padding:6px 10px; margin:3px 0;
                                                font-size:0.8rem; color:#FED7AA;'>{item}</div>
                                    """, unsafe_allow_html=True)

                        if gaps:
                            with st.expander(f"⚠ GAPS ({len(gaps)}) — Click to Review", expanded=True):
                                for gap in gaps:
                                    risk = gap.get("risk", "MEDIUM")
                                    rc = risk_color(risk)
                                    scope_item = gap.get("master_scope_item", "Unknown")
                                    est_val = gap.get("estimated_value", "Unknown")
                                    note = gap.get("note", "")
                                    st.markdown(f"""
                                    <div style='background:rgba(251,113,133,0.07); border:1px solid rgba(251,113,133,0.2);
                                                border-left:3px solid {rc}; border-radius:0 8px 8px 0;
                                                padding:8px 12px; margin:5px 0;'>
                                        <div style='color:#FB7185; font-weight:700; font-size:0.8rem;'>⚠ CRITICAL GAP</div>
                                        <div style='color:#F8FAFC; font-weight:600; font-size:0.82rem; margin:2px 0;'>{scope_item}</div>
                                        <div style='display:flex; gap:12px; margin-top:4px;'>
                                            <span style='background:rgba(0,0,0,0.3); border:1px solid {rc}; color:{rc};
                                                         font-size:0.68rem; font-weight:700; border-radius:4px; padding:1px 7px;'>
                                                {risk} RISK
                                            </span>
                                            <span style='color:#64748B; font-size:0.73rem;'>Est: {est_val}</span>
                                        </div>
                                        {"<div style='color:#64748B; font-size:0.73rem; margin-top:4px;'>" + note + "</div>" if note else ""}
                                    </div>
                                    """, unsafe_allow_html=True)
                        elif not gaps and price:
                            st.markdown("""
                            <div style='background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.2);
                                        border-radius:6px; padding:8px 12px; font-size:0.78rem; color:#6EE7B7;'>
                                ✓ No critical gaps detected
                            </div>
                            """, unsafe_allow_html=True)

                        if notes:
                            with st.expander(f"📝 Notes & Clarifications ({len(notes)})", expanded=False):
                                for note in notes:
                                    st.markdown(f"<div style='color:#94A3B8; font-size:0.78rem; padding:4px 0; border-bottom:1px solid #1E293B;'>{note}</div>", unsafe_allow_html=True)

                        # Re-run gap analysis button
                        if stale and bid.get("pdf_bytes"):
                            if st.button(f"↻ Re-run Gap Analysis", key=f"rerun_{trade}_{bi}", use_container_width=True):
                                if not st.session_state.api_key:
                                    st.error("API Key required.")
                                else:
                                    with st.spinner("Re-running analysis…"):
                                        new_parsed = parse_bid_pdf(bid["pdf_bytes"], trade, st.session_state.master_scopes.get(trade, []), name)
                                    if new_parsed:
                                        new_parsed["filename"] = bid.get("filename", "")
                                        new_parsed["pdf_bytes"] = bid["pdf_bytes"]
                                        new_parsed["stale"] = False
                                        new_parsed["timestamp"] = datetime.now().strftime("%b %d, %Y %H:%M")
                                        st.session_state.sub_bids[trade][bi] = new_parsed
                                        st.rerun()

                        # Remove bid button
                        if st.button(f"🗑 Remove Bid", key=f"remove_bid_{trade}_{bi}", use_container_width=True):
                            st.session_state.sub_bids[trade].pop(bi)
                            st.rerun()

                # Side-by-side gap contrast table (if 2+ bids)
                if len(sub_bids) >= 2:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("""
                    <div class='section-header'>
                        <h4>Gap Contrast Matrix</h4>
                        <p>Scope item coverage comparison across all subs</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if scope_items:
                        table_data = []
                        for item in scope_items:
                            row = {"Scope Item": item}
                            item_lower = item.lower()
                            for bid in sub_bids[:3]:
                                bname = bid.get("subcontractor_name", "Sub")[:15]
                                inclusions = [i.lower() for i in bid.get("inclusions", [])]
                                gap_items = [g.get("master_scope_item", "").lower() for g in bid.get("gaps", [])]
                                exclusions = [e.lower() for e in bid.get("exclusions", [])]

                                is_excl = any(item_lower in e or e in item_lower for e in exclusions)
                                is_gap = any(item_lower in g or g in item_lower for g in gap_items)
                                is_incl = any(item_lower in i or i in item_lower for i in inclusions)

                                if is_excl:
                                    row[bname] = "❌ Excluded"
                                elif is_gap:
                                    row[bname] = "⚠️ GAP"
                                elif is_incl:
                                    row[bname] = "✅ Included"
                                else:
                                    row[bname] = "— Unknown"
                            table_data.append(row)

                        if table_data:
                            df = pd.DataFrame(table_data)

                            def style_cell(val):
                                if "GAP" in str(val):
                                    return "color: #FB7185; font-weight: bold; background-color: rgba(251,113,133,0.1);"
                                elif "✅" in str(val):
                                    return "color: #34D399; background-color: rgba(52,211,153,0.05);"
                                elif "❌" in str(val):
                                    return "color: #FB923C; background-color: rgba(251,146,60,0.05);"
                                return "color: #64748B;"

                            styled_df = df.style.map(
                                style_cell,
                                subset=[c for c in df.columns if c != "Scope Item"]
                            )
                            st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("Add a Master Scope to enable the gap contrast matrix.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: ANALYTICS
# ═════════════════════════════════════════════════════════════════════════════
with main_tabs[1]:
    st.markdown("""
    <div class='section-header'>
        <h4>Portfolio Analytics</h4>
        <p>Cross-trade bid comparison · Risk heatmap · Price delta visualization</p>
    </div>
    """, unsafe_allow_html=True)

    has_data = any(st.session_state.sub_bids.get(t) for t in st.session_state.trades)

    if not has_data:
        st.markdown("""
        <div class='card' style='text-align:center; padding:48px;'>
            <div style='font-size:2.5rem; margin-bottom:12px;'>📊</div>
            <div style='color:#38BDF8; font-weight:700; margin-bottom:6px;'>No Bid Data Yet</div>
            <div style='color:#475569; font-size:0.83rem;'>Upload and parse bids in the trade tabs to see analytics.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Price comparison bar chart
        st.markdown("#### 💰 Bid Price Comparison by Trade")

        chart_data = {}
        all_sub_names = set()
        for trade in st.session_state.trades:
            for bid in st.session_state.sub_bids.get(trade, []):
                all_sub_names.add(bid.get("subcontractor_name", "Unknown"))

        sub_colors = ["#38BDF8", "#A78BFA", "#34D399", "#FB923C", "#FBBF24"]
        bar_fig = go.Figure()

        for si, sub_name in enumerate(list(all_sub_names)[:5]):
            trade_prices = []
            trade_names = []
            for trade in st.session_state.trades:
                bids = st.session_state.sub_bids.get(trade, [])
                matching = [b for b in bids if b.get("subcontractor_name") == sub_name]
                price = float(matching[0].get("total_price", 0)) if matching else 0
                trade_prices.append(price)
                trade_names.append(trade)

            if any(p > 0 for p in trade_prices):
                bar_fig.add_trace(go.Bar(
                    name=sub_name,
                    x=trade_names,
                    y=trade_prices,
                    marker_color=sub_colors[si % len(sub_colors)],
                    text=[f"${p:,.0f}" if p else "—" for p in trade_prices],
                    textposition="outside",
                    textfont=dict(size=10, color=sub_colors[si % len(sub_colors)]),
                ))

        bar_fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Trade Bid Comparison",
            barmode="group",
            height=380,
            yaxis_tickprefix="$",
            yaxis_tickformat=",",
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        # Gap Risk Heatmap
        st.markdown("#### 🌡 Risk Heatmap — Gaps by Trade & Subcontractor")

        heat_trades = []
        heat_subs = []
        heat_values = []
        heat_texts = []

        for trade in st.session_state.trades:
            for bid in st.session_state.sub_bids.get(trade, []):
                high = sum(1 for g in bid.get("gaps", []) if g.get("risk") == "HIGH")
                med = sum(1 for g in bid.get("gaps", []) if g.get("risk") == "MEDIUM")
                low = sum(1 for g in bid.get("gaps", []) if g.get("risk") == "LOW")
                score = high * 3 + med * 2 + low
                heat_trades.append(trade)
                heat_subs.append(bid.get("subcontractor_name", "Sub")[:20])
                heat_values.append(score)
                heat_texts.append(f"{len(bid.get('gaps', []))} gaps<br>H:{high} M:{med} L:{low}")

        if heat_trades:
            heat_df = pd.DataFrame({"Trade": heat_trades, "Sub": heat_subs, "Score": heat_values, "Text": heat_texts})
            try:
                pivot = heat_df.pivot_table(index="Sub", columns="Trade", values="Score", aggfunc="first").fillna(0)
                text_pivot = heat_df.pivot_table(index="Sub", columns="Trade", values="Text", aggfunc="first").fillna("No bid")

                heat_fig = go.Figure(data=go.Heatmap(
                    z=pivot.values,
                    x=pivot.columns.tolist(),
                    y=pivot.index.tolist(),
                    text=text_pivot.values,
                    texttemplate="%{text}",
                    textfont=dict(size=11, color="#F8FAFC"),
                    colorscale=[[0, "#34D399"], [0.4, "#FBBF24"], [0.7, "#FB923C"], [1.0, "#FB7185"]],
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="Risk Score", font=dict(color="#94A3B8")),
                        tickfont=dict(color="#94A3B8"),
                        bgcolor="#1E293B", bordercolor="#334155",
                    ),
                    hovertemplate="<b>%{y}</b> — %{x}<br>%{text}<extra></extra>",
                ))
                heat_fig.update_layout(**PLOTLY_LAYOUT, title="Gap Risk Heatmap", height=320)
                st.plotly_chart(heat_fig, use_container_width=True)
            except Exception:
                st.info("Add more bids across trades to see the heatmap.")

        # Summary table
        st.markdown("#### 📋 Bid Leveling Summary Table")
        summary_rows = []
        for trade in st.session_state.trades:
            for bid in st.session_state.sub_bids.get(trade, []):
                gaps = bid.get("gaps", [])
                high_gaps = sum(1 for g in gaps if g.get("risk") == "HIGH")
                summary_rows.append({
                    "Trade": trade,
                    "Subcontractor": bid.get("subcontractor_name", "—"),
                    "Bid Total": fmt_usd(bid.get("total_price", 0)),
                    "Inclusions": len(bid.get("inclusions", [])),
                    "Exclusions": len(bid.get("exclusions", [])),
                    "Total Gaps": len(gaps),
                    "HIGH Risk Gaps": high_gaps,
                    "Confidence": bid.get("bid_confidence", "—"),
                })

        if summary_rows:
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: HELP
# ═════════════════════════════════════════════════════════════════════════════
with main_tabs[2]:
    st.markdown("""
    <div class='section-header'>
        <h4>How To Use The Levelerr</h4>
        <p>A guide to bid transparency and gap detection</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='help-box'>
        <h3 style='color:#38BDF8; margin-top:0;'>📐 What Is "The Levelerr"?</h3>
        <p style='color:#CBD5E1;'>
            The Levelerr is a construction bid intelligence tool that solves the #1 problem in procurement:
            <strong style='color:#F8FAFC;'>you can't compare bids that are quoting different scopes.</strong>
        </p>
        <p style='color:#94A3B8;'>
            Sub A might be $80,000 cheaper than Sub B — but only because Sub A excluded $95,000 of required work.
            Without leveling, you don't have a cheaper bid. You have a future change order waiting to happen.
        </p>
    </div>

    <div style='height:16px;'></div>

    <div class='card'>
        <h3 style='color:#38BDF8; margin-top:0;'>🔄 The 4-Step Workflow</h3>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:12px;'>
            <div style='background:#0F172A; border:1px solid #334155; border-radius:8px; padding:16px;'>
                <div style='color:#38BDF8; font-weight:800; font-size:1.1rem; margin-bottom:6px;'>1️⃣ Define Your Trades</div>
                <p style='color:#94A3B8; font-size:0.83rem; margin:0;'>
                    In the sidebar, add all trades for your project (Drywall, MEP, Glazing, etc.).
                    These become your bid leveling tabs.
                </p>
            </div>
            <div style='background:#0F172A; border:1px solid #334155; border-radius:8px; padding:16px;'>
                <div style='color:#38BDF8; font-weight:800; font-size:1.1rem; margin-bottom:6px;'>2️⃣ Upload Your Drawings</div>
                <p style='color:#94A3B8; font-size:0.83rem; margin:0;'>
                    Go to "Drawings & Scope" and upload your full drawing set PDF.
                    Claude reads every page and builds a Master Scope per trade automatically.
                </p>
            </div>
            <div style='background:#0F172A; border:1px solid #334155; border-radius:8px; padding:16px;'>
                <div style='color:#38BDF8; font-weight:800; font-size:1.1rem; margin-bottom:6px;'>3️⃣ Upload Sub Bids</div>
                <p style='color:#94A3B8; font-size:0.83rem; margin:0;'>
                    In each trade tab, upload subcontractor bid PDFs. Claude extracts the total price,
                    inclusions, and exclusions — then cross-references them against the Master Scope.
                </p>
            </div>
            <div style='background:#0F172A; border:1px solid #334155; border-radius:8px; padding:16px;'>
                <div style='color:#38BDF8; font-weight:800; font-size:1.1rem; margin-bottom:6px;'>4️⃣ Review Gaps & Decide</div>
                <p style='color:#94A3B8; font-size:0.83rem; margin:0;'>
                    Every item in the Master Scope but <em>not</em> in the bid is flagged as a Critical Gap in red.
                    Use the Analytics tab to see the full risk picture across all trades.
                </p>
            </div>
        </div>
    </div>

    <div class='card'>
        <h3 style='color:#FB7185; margin-top:0;'>⚠ Understanding the Gap Detector</h3>
        <p style='color:#94A3B8; font-size:0.85rem;'>
            The gap detector compares every item in your AI-generated Master Scope against the bid's stated inclusions.
            If a scope item is not clearly covered by the bid, it's flagged as a <strong style='color:#FB7185;'>Critical Gap</strong>.
        </p>
        <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:12px;'>
            <div style='background:rgba(251,113,133,0.08); border:1px solid rgba(251,113,133,0.25); border-radius:8px; padding:12px;'>
                <div style='color:#FB7185; font-weight:700; font-size:0.82rem;'>🔴 HIGH Risk Gap</div>
                <p style='color:#94A3B8; font-size:0.78rem; margin:6px 0 0 0;'>
                    Major scope item clearly absent. Likely a significant change order if awarded. Requires immediate clarification.
                </p>
            </div>
            <div style='background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25); border-radius:8px; padding:12px;'>
                <div style='color:#FBBF24; font-weight:700; font-size:0.82rem;'>🟡 MEDIUM Risk Gap</div>
                <p style='color:#94A3B8; font-size:0.78rem; margin:6px 0 0 0;'>
                    Item may be implied or covered elsewhere in the bid. Worth discussing with the sub before award.
                </p>
            </div>
            <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25); border-radius:8px; padding:12px;'>
                <div style='color:#34D399; font-weight:700; font-size:0.82rem;'>🟢 LOW Risk Gap</div>
                <p style='color:#94A3B8; font-size:0.78rem; margin:6px 0 0 0;'>
                    Minor or administrative item. Low dollar impact but should still be confirmed in the contract.
                </p>
            </div>
        </div>
    </div>

    <div class='card'>
        <h3 style='color:#38BDF8; margin-top:0;'>✏️ Editing the Master Scope</h3>
        <p style='color:#94A3B8; font-size:0.84rem;'>
            The AI-generated scope is a <em>starting point</em>, not gospel. Use the <strong style='color:#F8FAFC;'>Edit Scope</strong> button
            in any trade tab to add, modify, or remove items.
        </p>
        <p style='color:#94A3B8; font-size:0.84rem;'>
            When you click <strong style='color:#38BDF8;'>Save & Update All Bids</strong>, the system marks all existing bids
            as "stale" so you can re-run gap analysis against the updated scope. This ensures your gap data
            is always synchronized with your latest scope definition.
        </p>
    </div>

    <div class='card'>
        <h3 style='color:#38BDF8; margin-top:0;'>🔑 API Key & Privacy</h3>
        <p style='color:#94A3B8; font-size:0.84rem;'>
            Your Anthropic API key is entered in the sidebar and stored only in your browser session —
            it is never saved to disk or transmitted anywhere except directly to Anthropic's API.
            Your drawing and bid PDFs are also only processed in-memory for the current session.
        </p>
        <p style='color:#94A3B8; font-size:0.84rem;'>
            Get an API key at <strong style='color:#38BDF8;'>console.anthropic.com</strong>.
            The claude-opus-4-6 model is used for highest accuracy on complex documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='margin:40px 0 16px 0;'>
<div style='text-align:center; color:#1E293B; font-size:0.72rem; padding-bottom:20px;'>
    The Levelerr · Construction Bid Intelligence Platform ·
    Risk Mitigation & Financial Transparency
</div>
""", unsafe_allow_html=True)
