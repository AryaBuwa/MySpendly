import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Spendly Pro", page_icon="💳", layout="wide")

# ---------------- APPLE & NOTION THEME CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Main App Styles */
.stApp { background-color: #191919 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background-color: #202020 !important; border-right: 1px solid #2f2f2f !important; }

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

/* Custom Download Link Button */
.download-btn {
    display: flex; align-items: center; justify-content: center;
    background-color: #007aff !important; color: #ffffff !important;
    width: 100%; height: 38px; border-radius: 8px;
    text-decoration: none !important; font-weight: 500; font-size: 14px;
    margin-top: 20px;
}

/* OVERRIDE NATIVE STREAMLIT BUTTONS TO MATCH NOTION */
div[data-testid="stButton"] button {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #f2f2f2 !important;
    border: 1px solid #2f2f2f !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: 34px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] button:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-color: #3a3a3a !important;
    color: #ffffff !important;
}

/* Primary Button (Log Transaction) Specific Styling */
div[data-testid="column"]:nth-of-type(1) button[kind="secondary"] {
    background-color: #007aff !important;
    border: none !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- INITIALIZATION ----------------
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "envelopes" not in st.session_state:
    st.session_state.envelopes = {"Food": 5000.0, "Rent": 20000.0, "Transport": 2000.0, "Fun": 3000.0, "Bills": 10000.0, "Other": 5000.0}
if "income" not in st.session_state:
    st.session_state.income = 50000.0

df = pd.DataFrame(st.session_state.expense_history)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 💵 Financials")
    st.session_state.income = st.number_input("Monthly Income", value=float(st.session_state.income), step=1000.0)
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ Envelopes")
    for cat in st.session_state.envelopes.keys():
        st.session_state.envelopes[cat] = st.number_input(f"{cat}", value=float(st.session_state.envelopes[cat]), step=500.0, key=f"v10_{cat}")
    
    if not df.empty:
        csv_data = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv_data).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="spendly_ledger.csv" class="download-btn">Download CSV</a>', unsafe_allow_html=True)
    
    if st.button("🗑️ Reset All Data", use_container_width=True):
        st.session_state.expense_history = []
        st.rerun()

# ---------------- TOP METRICS ----------------
st.title("Spendly Pro")
total_budget = sum(st.session_state.envelopes.values())
total_spent = df['Amount'].sum() if not df.empty else 0.0
total_savings = st.session_state.income - total_spent
savings_color = "#34c759" if total_savings >= 0 else "#ff3b30"

m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">CAPACITY</small><br><h2 style="margin:0">₹{total_budget:,.0f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">EXPENDITURE</small><br><h2 style="margin:0; color:#ffffff">₹{total_spent:,.0f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-container"><small style="color:#8a8a8a">SAVINGS</small><br><h2 style="margin:0; color:{savings_color}">₹{total_savings:,.0f}</h2></div>', unsafe_allow_html=True)

# ---------------- ENTRY FORM ----------------
st.write("##")
with st.container():
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 2.5, 1])
    d_in = c1.date_input("Date")
    cat_in = c2.selectbox("Category", list(st.session_state.envelopes.keys()))
    desc_in = c3.text_input("Description", placeholder="Purchase details...")
    amt_in = c4.number_input("Amount (₹)", min_value=0.0)
    
    is_today = d_in == datetime.now().date()
    badge_html = f'<div class="apple-badge warning-neutral">⦿ Today</div>' if is_today else f'<div class="apple-badge warning-active">⚠️ {d_in.strftime("%b %d")}</div>'
    
    btn_col, warn_col = st.columns([1, 4])
    with btn_col:
        # This button is styled as blue/primary in the CSS
        if st.button("＋ Log Transaction", use_container_width=True):
            if desc_in and amt_in > 0:
                st.session_state.expense_history.insert(0, {"id": str(uuid.uuid4()), "Date": d_in, "Category": cat_in, "Description": desc_in, "Amount": amt_in})
                st.rerun()
    with warn_col:
        st.markdown(f'<div style="height:45px; display:flex; align-items:center;">{badge_html}</div>', unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
st.write("##")
col_pie, col_heat = st.columns([1, 2])
with col_pie:
    st.markdown("### 🍩 Allocation")
    if not df.empty:
        cat_sums = df.groupby('Category')['Amount'].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(labels=cat_sums['Category'], values=cat_sums['Amount'], hole=.72, marker=dict(colors=['#007aff', '#34c759', '#ff9500', '#ff3b30', '#af52de'], line=dict(color='#191919', width=2)))])
        fig_pie.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

with col_heat:
    st.markdown("### 🗓️ Activity (30 Days)")
    today = datetime.now().date()
    last_30 = [today - timedelta(days=i) for i in range(30)]
    if not df.empty:
        df_c = df.copy()
        df_c['Date'] = pd.to_datetime(df_c['Date']).dt.date
        daily_sums = df_c.groupby('Date')['Amount'].sum().reindex(last_30, fill_value=0).values
    else:
        daily_sums = [0] * 30
    fig_h = go.Figure(data=go.Heatmap(z=[daily_sums[i:i+6] for i in range(0, 30, 6)], colorscale=['#1d1d1d', '#0e4429', '#006d32', '#26a641', '#39d353'], showscale=False, xgap=3, ygap=3))
    fig_h.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_h.update_xaxes(visible=False); fig_h.update_yaxes(visible=False)
    st.plotly_chart(fig_h, use_container_width=True, config={'displayModeBar': False})

# ---------------- SEARCH & HISTORY ----------------
st.write("##")
st.markdown("### 🔍 Search & History")
q = st.text_input("", placeholder="Filter list...", label_visibility="collapsed")

if not df.empty:
    filtered = df[df['Description'].str.contains(q, case=False) | df['Category'].str.contains(q, case=False)]
    for item in filtered.to_dict('records'):
        c_item, c_del = st.columns([8, 1.2])
        with c_item:
            tag_class = f"tag tag-{item['Category'].lower()}"
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
            # Vertical alignment spacer
            st.markdown('<div style="margin-top: 22px;"></div>', unsafe_allow_html=True)
            # Native streamlit button with custom CSS styling applied above
            if st.button("Delete", key=f"del_{item['id']}", use_container_width=True):
                st.session_state.expense_history = [x for x in st.session_state.expense_history if x["id"] != item["id"]]
                st.rerun()