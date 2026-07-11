import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import base64
import re
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Spendly Pro | Financial Management", page_icon="💳", layout="wide")

# ---------------- Consolidated CSS and HTML Banner for Upcoming Releases ----------------
st.markdown("""
<style>
.banner {
    background: #f8f9fa;
    color: #31333F;
    padding: 14px 18px;
    text-align: center;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-bottom: 25px;
    line-height: 1.6;
}
.banner-title { font-size: 15px; font-weight: 700; }
.banner-date { font-size: 13px; color: #6b7280; margin: 6px 0 10px; }
.banner-features { font-size: 13px; color: #4b5563; }
</style>

<div class="banner">
    <div class="banner-title">🚀 Upcoming Release</div>
    <div class="banner-date">Scheduled for July 20, 2026</div>
    <div class="banner-features">
        Smart Bank CSV Import &bull;
        Multi-bank support &bull;
        Inline transaction editing &bull;
        Budget progress bars &bull;
        Visual envelope alerts &bull;
        Full UI redesign
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- APPLE & NOTION THEME CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp { background-color: #191919 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background-color: #202020 !important; border-right: 1px solid #2f2f2f !important; }

.action-group { display: flex; gap: 10px; justify-content: flex-end; align-items: center; padding-top: 5px; }
.action-link {
    display: inline-flex; align-items: center; justify-content: center;
    padding: 0 16px; height: 38px; border-radius: 8px; font-size: 14px; font-weight: 500;
    text-decoration: none !important; color: #efefef !important;
    background: rgba(255,255,255,0.05); border: 1px solid #2f2f2f; transition: all 0.2s ease;
}
.action-link:hover { background: rgba(255,255,255,0.1); border-color: #3a3a3a; color: #ffffff !important; }
.action-link-primary { background: #007aff !important; border: none !important; color: white !important; }
.action-link-primary:hover { background: #0063cc !important; box-shadow: 0 4px 12px rgba(0,122,255,0.3); }

.sidebar-spacer { margin-top: 25px; margin-bottom: 10px; border-top: 1px solid #2f2f2f; }
.apple-badge { padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; margin-left: 10px; }
.warning-active { background-color: rgba(255,159,10,0.15); color: #ff9f0a; border: 1px solid rgba(255,159,10,0.3); }
.warning-neutral { background-color: rgba(0,122,255,0.1); color: #007aff; border: 1px solid rgba(0,122,255,0.2); }
.metric-container { background: #202020; border: 1px solid #2f2f2f; border-radius: 12px; padding: 20px; }

.tag { padding: 3px 10px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
.tag-food { background: #452219; color: #e07941; }
.tag-rent { background: #222b35; color: #529cca; }
.tag-transport { background: #282e26; color: #6fb169; }
.tag-fun { background: #352230; color: #b44f99; }
.tag-bills { background: #352c1e; color: #dfab01; }
.tag-other { background: #2f2f2f; color: #9b9b9b; }

div[data-testid="stButton"] button {
    background-color: rgba(255,255,255,0.05) !important; color: #f2f2f2 !important;
    border: 1px solid #2f2f2f !important; border-radius: 8px !important;
    font-size: 13px !important; font-weight: 500 !important; height: 38px !important; transition: all 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
    background-color: rgba(255,255,255,0.1) !important; border-color: #3a3a3a !important; color: #ffffff !important;
}

/* NEW FEATURE STYLES */
.new-feature-badge {
    display: inline-block; background: rgba(0,122,255,0.15); color: #007aff;
    border: 1px solid rgba(0,122,255,0.25); border-radius: 4px;
    font-size: 10px; font-weight: 700; padding: 2px 7px;
    text-transform: uppercase; letter-spacing: 0.04em; margin-left: 8px;
    vertical-align: middle;
}
.goal-card {
    background: #202020; border: 1px solid #2f2f2f; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
}
.goal-bar-bg { height: 6px; background: #2f2f2f; border-radius: 99px; overflow: hidden; margin: 10px 0 6px; }
.goal-bar-fill { height: 100%; border-radius: 99px; background: #34c759; }
.goal-bar-fill.warn { background: #ff9f0a; }
.history-card {
    background: #202020; border: 1px solid #2f2f2f; border-radius: 10px;
    padding: 14px 18px; margin-bottom: 10px;
}
.import-info { background: #1a1f2e; border: 1px solid #2a3550; border-radius: 8px; padding: 12px 16px; font-size: 12px; color: #8a8aaa; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------------- INITIALIZATION ----------------
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "envelopes" not in st.session_state:
    st.session_state.envelopes = {"Food": 5000.0, "Rent": 20000.0, "Transport": 2000.0, "Entertainment": 3000.0, "Utilities": 10000.0, "Miscellaneous": 5000.0}
if "income" not in st.session_state:
    st.session_state.income = 50000.0
if "goals" not in st.session_state:
    st.session_state.goals = []
if "monthly_history" not in st.session_state:
    st.session_state.monthly_history = []

df = pd.DataFrame(st.session_state.expense_history)

# ---------------- HELPER FUNCTIONS ----------------
def generate_pdf(dataframe, income, total_spent, total_savings):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "Transaction Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Financial Summary", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(50, 8, f"Total Capital: {income:,.2f}", ln=True)
    pdf.cell(50, 8, f"Total Expenditure: {total_spent:,.2f}", ln=True)
    if total_savings >= 0:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(50, 8, f"Net Surplus: {total_savings:,.2f}", ln=True)
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(50, 8, f"Deficit: {abs(total_savings):,.2f}", ln=True)
    pdf.set_text_color(0, 0, 0); pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 8, "Date", 1); pdf.cell(40, 8, "Classification", 1); pdf.cell(80, 8, "Description", 1); pdf.cell(40, 8, "Amount", 1, 1)
    pdf.set_font("Arial", '', 9)
    for _, row in dataframe.iterrows():
        pdf.cell(30, 8, str(row['Date']), 1)
        pdf.cell(40, 8, str(row['Category']), 1)
        pdf.cell(80, 8, str(row['Description'])[:35], 1)
        pdf.cell(40, 8, f"{row['Amount']:,.2f}", 1, 1)
    try:
        pdf_out = pdf.output(dest='S')
        if isinstance(pdf_out, str):
            return pdf_out.encode('latin-1')
        return pdf_out
    except:
        return pdf.output()

def archive_current_month():
    if not st.session_state.expense_history:
        return False
    df_all = pd.DataFrame(st.session_state.expense_history)
    df_all['Date'] = pd.to_datetime(df_all['Date'])
    now = datetime.now()
    label = now.strftime("%B %Y")
    existing_labels = [h['month'] for h in st.session_state.monthly_history]
    if label in existing_labels:
        return False
    total_spent = float(df_all['Amount'].sum())
    cat_breakdown = df_all.groupby('Category')['Amount'].sum().to_dict()
    st.session_state.monthly_history.append({
        "month": label,
        "income": st.session_state.income,
        "spent": total_spent,
        "saved": st.session_state.income - total_spent,
        "breakdown": cat_breakdown,
        "tx_count": len(df_all),
    })
    st.session_state.expense_history = []
    return True

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 🏦 Administration")
    st.session_state.income = st.number_input("Monthly Income", value=float(st.session_state.income), step=1000.0)
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
    st.markdown("### 📦 Budget Allocation")
    for cat in st.session_state.envelopes.keys():
        st.session_state.envelopes[cat] = st.number_input(f"{cat}", value=float(st.session_state.envelopes[cat]), step=500.0, key=f"v10_{cat}")

# ---------------- HEADER & ACTION GROUP ----------------
header_col1, header_col2 = st.columns([1, 1])
with header_col1:
    st.markdown('<h2 style="margin:0; font-weight:700; letter-spacing:-1px;">Spendly Pro</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#71717a; font-size:13px; margin:0;">Personal Expense Tracker & Budget Manager</p>', unsafe_allow_html=True)

with header_col2:
    if not df.empty:
        total_spent = df['Amount'].sum()
        total_savings = st.session_state.income - total_spent
        csv_data = df.to_csv(index=False).encode('utf-8')
        b64_csv = base64.b64encode(csv_data).decode()
        pdf_data = generate_pdf(df, st.session_state.income, total_spent, total_savings)
        b64_pdf = base64.b64encode(pdf_data).decode()
        st.markdown(f'''
            <div class="action-group">
                <a href="data:file/csv;base64,{b64_csv}" download="ledger_export.csv" class="action-link">Download CSV</a>
                <a href="data:application/pdf;base64,{b64_pdf}" download="financial_report.pdf" class="action-link action-link-primary">Generate PDF Report</a>
            </div>
        ''', unsafe_allow_html=True)

st.write("##")

# ---------------- METRICS ----------------
total_budget = sum(st.session_state.envelopes.values())
total_spent = df['Amount'].sum() if not df.empty else 0.0
total_savings = st.session_state.income - total_spent

if total_savings >= 0:
    savings_label, savings_color, display_value = "RETAINED CAPITAL", "#34c759", total_savings
else:
    savings_label, savings_color, display_value = "BUDGET OVERAGE", "#ff3b30", abs(total_savings)

m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">AGGREGATE BUDGET</small><br><h2 style="margin:0">₹{total_budget:,.0f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">TOTAL EXPENDITURE</small><br><h2 style="margin:0; color:#ffffff">₹{total_spent:,.0f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">{savings_label}</small><br><h2 style="margin:0; color:{savings_color}">₹{display_value:,.0f}</h2></div>', unsafe_allow_html=True)

# ---------------- ENTRY FORM ----------------
st.write("##")
with st.container():
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 2.5, 1])
    d_in = c1.date_input("Transaction Date")
    cat_in = c2.selectbox("Classification", list(st.session_state.envelopes.keys()))
    desc_in = c3.text_input("Description", placeholder="Enter transaction details")
    amt_in = c4.number_input("Amount (₹)", min_value=0.0)
    is_today = d_in == datetime.now().date()
    badge_html = f'<div class="apple-badge warning-neutral">⦿ Current</div>' if is_today else f'<div class="apple-badge warning-active">⚠️ {d_in.strftime("%b %d")}</div>'
    btn_col, warn_col = st.columns([1, 4])
    with btn_col:
        if st.button("Confirm Entry", use_container_width=True):
            if desc_in and amt_in > 0:
                st.session_state.expense_history.insert(0, {"id": str(uuid.uuid4()), "Date": d_in, "Category": cat_in, "Description": desc_in, "Amount": amt_in})
                st.rerun()
    with warn_col:
        st.markdown(f'<div style="height:45px; display:flex; align-items:center;">{badge_html}</div>', unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
st.write("##")
col_pie, col_heat = st.columns([1, 2])
with col_pie:
    st.markdown("### 🍩 Categorical Distribution")
    if not df.empty:
        cat_sums = df.groupby('Category')['Amount'].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(labels=cat_sums['Category'], values=cat_sums['Amount'], hole=.72, marker=dict(colors=['#007aff', '#34c759', '#ff9500', '#ff3b30', '#af52de'], line=dict(color='#191919', width=2)))])
        fig_pie.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No data available for analysis.")

with col_heat:
    st.markdown("### 🗓️ Expenditure Frequency (30 Days)")
    today = datetime.now().date()
    last_30 = [today - timedelta(days=i) for i in range(30)]
    if not df.empty:
        df_c = df.copy()
        df_c['Date'] = pd.to_datetime(df_c['Date']).dt.date
        daily_sums = df_c.groupby('Date')['Amount'].sum().reindex(last_30, fill_value=0).values
    else:
        daily_sums = [0] * 30
    fig_h = go.Figure(data=go.Heatmap(
        z=[daily_sums[i:i+6] for i in range(0, 30, 6)],
        colorscale=['#242424', '#0e4429', '#006d32', '#26a641', '#39d353'],
        showscale=False, xgap=4, ygap=4
    ))
    fig_h.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='#191919', plot_bgcolor='#191919')
    fig_h.update_xaxes(visible=False); fig_h.update_yaxes(visible=False)
    st.plotly_chart(fig_h, use_container_width=True, config={'displayModeBar': False})

# ---------------- SEARCH & HISTORY ----------------
st.write("##")
hist_col1, hist_col2 = st.columns([4, 1])
with hist_col1:
    st.markdown("### 📜 Transaction Ledger")
    q = st.text_input("", placeholder="Search records...", label_visibility="collapsed")
with hist_col2:
    st.markdown('<div style="height:61px"></div>', unsafe_allow_html=True)
    if st.button("Reset Database", use_container_width=True):
        st.session_state.expense_history = []
        st.rerun()

if not df.empty:
    filtered = df[df['Description'].str.contains(q, case=False) | df['Category'].str.contains(q, case=False)]
    for item in filtered.to_dict('records'):
        c_item, c_del = st.columns([8, 1.2])
        with c_item:
            tag_class = f"tag tag-{item['Category'].lower() if item['Category'] != 'Entertainment' else 'fun'}"
            st.markdown(f'''
                <div style="border-bottom: 1px solid #2f2f2f; padding: 15px 0; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center;">
                        <span class="{tag_class}">{item['Category']}</span>
                        <div style="margin-left:15px;">
                            <div style="font-weight:500; font-size:14px; color: white;">{item['Description']}</div>
                            <div style="font-size:11px; color:#8a8a8a;">{item['Date']}</div>
                        </div>
                    </div>
                    <div style="font-weight:600; font-size:15px; margin-right: 20px;">₹{item['Amount']:,}</div>
                </div>
            ''', unsafe_allow_html=True)
        with c_del:
            st.markdown('<div style="margin-top: 22px;"></div>', unsafe_allow_html=True)
            if st.button("Delete", key=f"del_{item['id']}", use_container_width=True):
                st.session_state.expense_history = [x for x in st.session_state.expense_history if x["id"] != item["id"]]
                st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# NEW FEATURES
# ════════════════════════════════════════════════════════════════════════════

st.write("---")

# ── FEATURE 1: FINANCIAL GOALS ────────────────────────────────────────────
st.markdown(
    '### 🎯 Financial Goals'
    '<span class="new-feature-badge">New</span>',
    unsafe_allow_html=True
)
st.caption("Set a savings target, track progress month by month. No AI needed — pure math.")

with st.expander("ℹ️ How goals work", expanded=False):
    st.markdown("""
    - Set a **name**, **target amount**, and **deadline month**.
    - Spendly calculates how much you need to save per month to hit it.
    - Progress is tracked against your **Retained Capital** (income minus spending) each month.
    - Delete a goal anytime once achieved.
    """)

with st.container():
    ga, gb, gc, gd = st.columns([2, 1.2, 1.2, 0.8])
    goal_name   = ga.text_input("Goal Name", placeholder="e.g. Trip to Bali, Emergency Fund", key="gname")
    goal_target = gb.number_input("Target (₹)", min_value=0.0, step=1000.0, key="gtarget")
    goal_saved  = gc.number_input("Already Saved (₹)", min_value=0.0, step=500.0, key="gsaved")
    goal_months = gd.number_input("Months Left", min_value=1, max_value=60, value=6, key="gmonths")
    if st.button("Add Goal", key="add_goal"):
        if goal_name.strip() and goal_target > 0:
            st.session_state.goals.append({
                "id": str(uuid.uuid4()),
                "name": goal_name.strip(),
                "target": goal_target,
                "saved": goal_saved,
                "months_left": goal_months,
                "created": datetime.now().strftime("%b %Y"),
            })
            st.rerun()

if st.session_state.goals:
    g_cols = st.columns(min(len(st.session_state.goals), 3))
    for i, goal in enumerate(st.session_state.goals):
        pct = min((goal['saved'] / goal['target'] * 100) if goal['target'] > 0 else 0, 100)
        remaining = max(goal['target'] - goal['saved'], 0)
        per_month = remaining / goal['months_left'] if goal['months_left'] > 0 else remaining
        bar_class = "goal-bar-fill warn" if pct < 40 else "goal-bar-fill"
        on_track = per_month <= total_savings if total_savings > 0 else False
        track_txt = "✅ On track" if on_track else "⚠️ Needs attention"
        with g_cols[i % 3]:
            st.markdown(f"""
            <div class="goal-card">
                <div style="font-weight:600; font-size:14px; color:#fff;">{goal['name']}</div>
                <div style="font-size:11px; color:#8a8a8a; margin-top:2px;">Since {goal['created']} &bull; {goal['months_left']} months left</div>
                <div class="goal-bar-bg"><div class="{bar_class}" style="width:{pct:.1f}%"></div></div>
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#8a8a8a;">
                    <span>₹{goal['saved']:,.0f} saved</span><span>₹{goal['target']:,.0f} goal</span>
                </div>
                <div style="margin-top:8px; font-size:12px; color:#a0a0b0;">
                    Need <b style="color:#fff;">₹{per_month:,.0f}/mo</b> &nbsp;&bull;&nbsp; {track_txt}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Remove", key=f"del_goal_{goal['id']}"):
                st.session_state.goals = [g for g in st.session_state.goals if g['id'] != goal['id']]
                st.rerun()
else:
    st.markdown('<p style="color:#555; font-size:13px;">No goals yet. Add one above to start tracking.</p>', unsafe_allow_html=True)

st.write("---")

# ── FEATURE 2: MONTHLY HISTORY & RESET ───────────────────────────────────
st.markdown(
    '### 📅 Monthly History'
    '<span class="new-feature-badge">New</span>',
    unsafe_allow_html=True
)
st.caption("Archive this month's data before the 1st so you can compare months without losing records.")

with st.expander("ℹ️ How monthly archiving works", expanded=False):
    st.markdown("""
    - Click **Archive This Month** to save a snapshot of all current transactions.
    - Your ledger is then cleared, ready for a fresh month.
    - Archived months are shown below as read-only summaries.
    - Export the full CSV before archiving if you need raw transaction data.
    """)

arc_col, _ = st.columns([1, 4])
with arc_col:
    if st.button("📦 Archive This Month", key="archive_month"):
        did_archive = archive_current_month()
        if did_archive:
            st.success(f"Archived {datetime.now().strftime('%B %Y')} successfully. Ledger cleared.")
            st.rerun()
        else:
            st.warning("Nothing to archive, or this month is already saved.")

if st.session_state.monthly_history:
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    for record in reversed(st.session_state.monthly_history):
        saved_color = "#34c759" if record['saved'] >= 0 else "#ff3b30"
        saved_label = f"Saved ₹{record['saved']:,.0f}" if record['saved'] >= 0 else f"Over by ₹{abs(record['saved']):,.0f}"
        top_cat = max(record['breakdown'], key=record['breakdown'].get) if record['breakdown'] else "—"
        st.markdown(f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600; font-size:14px; color:#fff;">{record['month']}</div>
                    <div style="font-size:11px; color:#8a8a8a; margin-top:3px;">
                        {record['tx_count']} transactions &bull; Top spend: {top_cat}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:15px; font-weight:600; color:#fff;">₹{record['spent']:,.0f} <span style="color:#8a8a8a; font-weight:400; font-size:12px;">spent</span></div>
                    <div style="font-size:12px; color:{saved_color}; margin-top:2px;">{saved_label}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<p style="color:#555; font-size:13px;">No archived months yet.</p>', unsafe_allow_html=True)

st.write("---")

# ════════════════════════════════════════════════════════════════════════════
# FEATURE 3: BANK CSV IMPORT (fully upgraded)
# ════════════════════════════════════════════════════════════════════════════

# ------------------------------------------------------------------
# ALIASES FOR AUTO-DETECTION
# ------------------------------------------------------------------
DATE_ALIASES = [
    "date", "txn date", "transaction date", "value date", "posting date",
]
DESC_ALIASES = [
    "description", "narration", "remarks", "remark",
    "particulars", "details", "transaction details",
]
DEBIT_ALIASES = [
    "debit", "withdrawal", "withdrawal amt",
    "withdrawal amount", "dr", "debit amount",
]
CREDIT_ALIASES = [
    "credit", "deposit", "credit amt", "credit amount", "cr",
]
AMOUNT_ALIASES = [
    "amount", "transaction amount", "txn amount",
]

CATEGORY_OPTIONS = list(st.session_state.envelopes.keys())


def clean_amount(value) -> float | None:
    """Strip currency symbols, commas, CR/DR suffixes and return float or None."""
    if pd.isna(value):
        return None
    s = str(value).strip()
    if s == "" or s.lower() in ("nan", "none", "-"):
        return None
    # Remove currency symbols and labels
    s = re.sub(r"[₹,]", "", s)
    s = re.sub(r"\bINR\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\bRs\.?\b", "", s, flags=re.IGNORECASE)
    # Strip trailing/leading CR DR (keep the number)
    s = re.sub(r"\bCR\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\bDR\b", "", s, flags=re.IGNORECASE)
    s = s.strip()
    try:
        return float(s)
    except ValueError:
        return None


def detect_column(columns, aliases) -> str | None:
    """Return the first column name that matches any alias (exact then substring)."""
    col_lower = {c.lower().strip(): c for c in columns}
    for alias in aliases:
        if alias in col_lower:
            return col_lower[alias]
    for alias in aliases:
        for col_key, col_orig in col_lower.items():
            if alias in col_key:
                return col_orig
    return None


def detect_bank_columns(columns) -> dict:
    return {
        "date":   detect_column(columns, DATE_ALIASES),
        "desc":   detect_column(columns, DESC_ALIASES),
        "debit":  detect_column(columns, DEBIT_ALIASES),
        "credit": detect_column(columns, CREDIT_ALIASES),
        "amount": detect_column(columns, AMOUNT_ALIASES),
    }


def read_csv_robust(uploaded_file) -> pd.DataFrame:
    """Try UTF-8 then latin-1; strip column whitespace."""
    uploaded_file.seek(0)
    try:
        raw = pd.read_csv(uploaded_file, encoding="utf-8", dtype=str)
    except Exception:
        uploaded_file.seek(0)
        raw = pd.read_csv(uploaded_file, encoding="latin-1", dtype=str)
    raw.columns = raw.columns.str.strip()
    return raw


def build_existing_keys() -> set:
    """Return a set of (date_str, desc_lower, rounded_amount) for duplicate detection."""
    return {
        (
            str(x["Date"]),
            str(x["Description"]).lower().strip(),
            round(float(x["Amount"]), 2),
        )
        for x in st.session_state.expense_history
    }


def parse_rows_to_preview(
    raw: pd.DataFrame,
    date_col: str,
    desc_col: str,
    amount_col: str | None,
    debit_col: str | None,
    credit_col: str | None,
    default_category: str,
) -> tuple[pd.DataFrame, int, int, int]:
    """
    Parse raw CSV rows into a preview DataFrame ready for st.data_editor.

    Returns (preview_df, skipped_credits, skipped_duplicates, skipped_invalid)
    """
    existing_keys = build_existing_keys()
    rows = []
    skipped_credits = 0
    skipped_duplicates = 0
    skipped_invalid = 0

    has_debit_credit = bool(debit_col and credit_col)

    for _, row in raw.iterrows():
        try:
            # ── Date ──────────────────────────────────────────────────────
            raw_date = row.get(date_col, "")
            parsed_date = pd.to_datetime(raw_date, errors="coerce", dayfirst=True)
            if pd.isna(parsed_date):
                skipped_invalid += 1
                continue

            # ── Description ───────────────────────────────────────────────
            description = str(row.get(desc_col, "")).strip()
            if not description or description.lower() in ("nan", "none", ""):
                skipped_invalid += 1
                continue

            # ── Amount / Debit / Credit logic ─────────────────────────────
            amount = None

            if has_debit_credit:
                # Skip rows where credit column has a value (it's a credit, not debit)
                credit_val = clean_amount(row.get(credit_col, ""))
                if credit_val is not None and credit_val > 0:
                    skipped_credits += 1
                    continue
                amount = clean_amount(row.get(debit_col, ""))
            elif debit_col:
                amount = clean_amount(row.get(debit_col, ""))
            elif amount_col:
                amount = clean_amount(row.get(amount_col, ""))

            if amount is None or amount <= 0:
                skipped_invalid += 1
                continue

            # ── Duplicate check ───────────────────────────────────────────
            key = (
                str(parsed_date.date()),
                description.lower(),
                round(amount, 2),
            )
            if key in existing_keys:
                skipped_duplicates += 1
                continue

            rows.append({
                "Import":       True,
                "Date":         str(parsed_date.date()),
                "Description":  description[:80],
                "Amount":       round(amount, 2),
                "Category":     default_category,
                "_key":         key,
            })

        except Exception:
            skipped_invalid += 1
            continue

    preview_df = pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=["Import", "Date", "Description", "Amount", "Category", "_key"]
    )
    return preview_df, skipped_credits, skipped_duplicates, skipped_invalid


# ------------------------------------------------------------------
# FEATURE 3 UI
# ------------------------------------------------------------------

st.markdown(
    '### 📥 Import Bank Statement'
    '<span class="new-feature-badge">New</span>',
    unsafe_allow_html=True,
)
st.caption(
    "Upload a CSV exported from your bank — SBI, HDFC, ICICI, Axis, Kotak, Canara, BoB, PNB, Union, IDFC, Yes Bank."
)

with st.expander("ℹ️ How to export from your bank", expanded=False):
    st.markdown("""
| Bank | Steps |
|---|---|
| **HDFC** | NetBanking → Accounts → Download Statement → CSV |
| **ICICI** | iMobile / NetBanking → Account Statement → Export as CSV |
| **SBI** | YONO / NetBanking → Account → e-Statement → CSV |
| **Axis** | Internet Banking → Account → Statement → Download CSV |
| **Kotak** | Net Banking → Account → Statement → Download CSV |
| **Canara / BoB / PNB / Union** | NetBanking → Account → Statement → Export CSV |
| **IDFC / Yes Bank** | App or NetBanking → Statements → Download CSV |

Columns are **auto-detected**. You can still adjust them manually before importing.  
Only debit/withdrawal rows are imported. Credits are skipped automatically.
    """)

uploaded_csv = st.file_uploader(
    "Upload Bank CSV",
    type=["csv"],
    key="bank_csv_upload",
    label_visibility="collapsed",
)

if uploaded_csv:
    try:
        raw = read_csv_robust(uploaded_csv)

        if raw.empty:
            st.warning("The uploaded CSV appears to be empty.")
            st.stop()

        detected = detect_bank_columns(raw.columns)
        columns  = raw.columns.tolist()

        # ── Helper: safe selectbox index ──────────────────────────────────
        def safe_index(col_name):
            if col_name and col_name in columns:
                return columns.index(col_name)
            return 0

        # ── Column selectors (pre-filled from auto-detection) ─────────────
        st.markdown(
            f'<div class="import-info">📄 <b>{len(raw)}</b> rows detected &bull; '
            f'Columns: <b>{", ".join(columns)}</b></div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4, c5 = st.columns(5)
        date_col   = c1.selectbox("Date Column",        columns, index=safe_index(detected["date"]),   key="imp_date")
        desc_col   = c2.selectbox("Description Column", columns, index=safe_index(detected["desc"]),   key="imp_desc")
        debit_col  = c3.selectbox("Debit / Amount Col", columns, index=safe_index(detected["debit"] or detected["amount"]), key="imp_debit")
        credit_col_opts = ["(none)"] + columns
        credit_default  = detected["credit"] if detected["credit"] else "(none)"
        credit_col_sel  = c4.selectbox("Credit Col (optional)", credit_col_opts,
                                       index=credit_col_opts.index(credit_default), key="imp_credit")
        credit_col = None if credit_col_sel == "(none)" else credit_col_sel
        default_cat = c5.selectbox("Default Category", CATEGORY_OPTIONS, key="imp_cat")

        # ── Parse & build preview ─────────────────────────────────────────
        preview_df, n_credits, n_dupes, n_invalid = parse_rows_to_preview(
            raw, date_col, desc_col, debit_col, debit_col, credit_col, default_cat
        )

        # ── Stats banner ──────────────────────────────────────────────────
        total_parsed = len(raw)
        n_valid = len(preview_df)
        st.markdown(
            f'<div class="import-info">'
            f'✅ <b>{n_valid}</b> importable rows &nbsp;|&nbsp; '
            f'⏭ <b>{n_credits}</b> credits skipped &nbsp;|&nbsp; '
            f'🔁 <b>{n_dupes}</b> duplicates &nbsp;|&nbsp; '
            f'⚠️ <b>{n_invalid}</b> invalid rows'
            f'</div>',
            unsafe_allow_html=True,
        )

        if preview_df.empty:
            st.info("No importable debit transactions found. Adjust the column selections above.")
        else:
            st.caption("Review below — uncheck rows you don't want to import. You can also change the category per row.")

            # ── Editable preview ──────────────────────────────────────────
            edited = st.data_editor(
                preview_df.drop(columns=["_key"]),
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                column_config={
                    "Import": st.column_config.CheckboxColumn(
                        "Import",
                        help="Uncheck to skip this row",
                        default=True,
                    ),
                    "Date": st.column_config.TextColumn("Date", disabled=True),
                    "Description": st.column_config.TextColumn("Description", disabled=True),
                    "Amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f", disabled=True),
                    "Category": st.column_config.SelectboxColumn(
                        "Category",
                        options=CATEGORY_OPTIONS,
                        required=True,
                    ),
                },
                key="import_editor",
            )

            checked_rows = edited[edited["Import"] == True]
            st.caption(f"{len(checked_rows)} of {n_valid} rows selected for import.")

            if st.button("⬆️ Import Selected Transactions", key="do_import"):
                if checked_rows.empty:
                    st.warning("No rows selected. Tick at least one row to import.")
                else:
                    existing_keys = build_existing_keys()
                    imported_rows = []
                    final_dupes   = 0

                    # Re-attach _key from original preview_df by position
                    preview_df_reset = preview_df.reset_index(drop=True)
                    edited_reset     = edited.reset_index(drop=True)

                    for idx, erow in edited_reset.iterrows():
                        if not erow.get("Import", False):
                            continue
                        key = preview_df_reset.loc[idx, "_key"] if idx < len(preview_df_reset) else None
                        if key and key in existing_keys:
                            final_dupes += 1
                            continue
                        try:
                            date_val = datetime.strptime(str(erow["Date"]), "%Y-%m-%d").date()
                        except Exception:
                            date_val = pd.to_datetime(erow["Date"], errors="coerce", dayfirst=True).date()
                        new_tx = {
                            "id":          str(uuid.uuid4()),
                            "Date":        date_val,
                            "Category":    erow["Category"],
                            "Description": str(erow["Description"])[:80],
                            "Amount":      float(erow["Amount"]),
                        }
                        imported_rows.append(new_tx)
                        if key:
                            existing_keys.add(key)

                    if imported_rows:
                        st.session_state.expense_history = imported_rows + st.session_state.expense_history
                        summary_parts = [f"✅ Imported: **{len(imported_rows)}**"]
                        if n_credits:   summary_parts.append(f"⏭ Credits skipped: **{n_credits}**")
                        if n_dupes + final_dupes: summary_parts.append(f"🔁 Duplicates: **{n_dupes + final_dupes}**")
                        if n_invalid:   summary_parts.append(f"⚠️ Invalid rows: **{n_invalid}**")
                        st.success("   |   ".join(summary_parts))
                        st.rerun()
                    else:
                        st.warning("All selected rows were duplicates or invalid.")

    except Exception as e:
        st.error(f"Error reading file: {e}")