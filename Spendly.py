import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import base64
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

.banner-title {
    font-size: 15px;
    font-weight: 700;
}

.banner-date {
    font-size: 13px;
    color: #6b7280;
    margin: 6px 0 10px;
}

.banner-features {
    font-size: 13px;
    color: #4b5563;
}
</style>

<div class="banner">
    <div class="banner-title">🚀 Upcoming Release</div>
    <div class="banner-date">Scheduled for July 10, 2026</div>
    <div class="banner-features">
        UI refinements • Improved user experience • Feature enhancements
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- APPLE & NOTION THEME CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Main App Styles */
.stApp { background-color: #191919 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background-color: #202020 !important; border-right: 1px solid #2f2f2f !important; }

/* Header Action Group Styling */
.action-group { display: flex; gap: 10px; justify-content: flex-end; align-items: center; padding-top: 5px; }
.action-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 16px; 
    height: 38px; 
    border-radius: 8px; 
    font-size: 14px; 
    font-weight: 500;
    text-decoration: none !important; 
    color: #efefef !important;
    background: rgba(255, 255, 255, 0.05); 
    border: 1px solid #2f2f2f;
    transition: all 0.2s ease;
}
.action-link:hover { background: rgba(255, 255, 255, 0.1); border-color: #3a3a3a; color: #ffffff !important; }
.action-link-primary { background: #007aff !important; border: none !important; color: white !important; }
.action-link-primary:hover { background: #0063cc !important; box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3); }

/* Sidebar & Layout Elements */
.sidebar-spacer { margin-top: 25px; margin-bottom: 10px; border-top: 1px solid #2f2f2f; }
.apple-badge {
    padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 600;
    display: inline-flex; align-items: center; margin-left: 10px;
}
.warning-active { background-color: rgba(255, 159, 10, 0.15); color: #ff9f0a; border: 1px solid rgba(255, 159, 10, 0.3); }
.warning-neutral { background-color: rgba(0, 122, 255, 0.1); color: #007aff; border: 1px solid rgba(0, 122, 255, 0.2); }
.metric-container { background: #202020; border: 1px solid #2f2f2f; border-radius: 12px; padding: 20px; }

/* Notion-style Tags */
.tag { padding: 3px 10px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase;}
.tag-food { background: #452219; color: #e07941; }
.tag-rent { background: #222b35; color: #529cca; }
.tag-transport { background: #282e26; color: #6fb169; }
.tag-fun { background: #352230; color: #b44f99; }
.tag-bills { background: #352c1e; color: #dfab01; }
.tag-other { background: #2f2f2f; color: #9b9b9b; }

/* OVERRIDE NATIVE STREAMLIT BUTTONS */
div[data-testid="stButton"] button {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #f2f2f2 !important;
    border: 1px solid #2f2f2f !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: 38px !important; 
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-color: #3a3a3a !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- INITIALIZATION ----------------
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "envelopes" not in st.session_state:
    st.session_state.envelopes = {"Food": 5000.0, "Rent": 20000.0, "Transport": 2000.0, "Entertainment": 3000.0, "Utilities": 10000.0, "Miscellaneous": 5000.0}
if "income" not in st.session_state:
    st.session_state.income = 50000.0

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
    else: daily_sums = [0] * 30
    
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
