import streamlit as st
import pandas as pd
import plotly.express as px

# 1. INITIALIZE STORAGE
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "tip_index" not in st.session_state:
    st.session_state.tip_index = 0
if "budget_goal" not in st.session_state:
    st.session_state.budget_goal = 1000.0

# 2. PAGE CONFIG
st.set_page_config(page_title="Spendly Pro", page_icon="💰", layout="wide")

# Custom CSS for that "High-End" feel
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #eef0f2; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); }
    [data-testid="stMetricValue"] { color: #1b5e20; font-weight: 800; }
    .stButton>button { border-radius: 12px; height: 3em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("💰 Spendly Pro")
st.caption("Simplified Financial Intelligence")

# 3. PREP DATA
df = pd.DataFrame(st.session_state.expense_history)
total_spent = df["Amount"].sum() if not df.empty else 0.0
budget_left = max(0.0, st.session_state.budget_goal - total_spent)

# Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Total Spending", f"${total_spent:,.2f}")
m2.metric("Budget Remaining", f"${budget_left:,.2f}")
m3.metric("Goal", f"${st.session_state.budget_goal:,.0f}")

st.progress(min(1.0, total_spent / st.session_state.budget_goal))
st.divider()

# --- INPUT SECTION (THE FIXED FORM) ---
with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_in = st.text_input("Date", placeholder="DD/MM/YYYY")
        desc_in = st.text_input("Description", placeholder="E.g. Starbucks")
    
    with col2:
        cat_in = st.selectbox("Category", ["Groceries", "Dining", "Transport", "Housing", "Entertainment", "Misc"])
        amt_in = st.number_input("Amount ($)", min_value=0.0, step=1.0)
    
    with col3:
        st.write("Confirm Entry")
        # THIS IS THE SUBMIT BUTTON - MUST STAY INSIDE THE FORM BLOCK
        submitted = st.form_submit_button("🚀 Save Expense", type="primary")

    if submitted:
        if date_in and desc_in and amt_in > 0:
            st.session_state.expense_history.append({
                "Date": date_in, "Description": desc_in, "Category": cat_in, "Amount": amt_in
            })
            st.toast("Saved!", icon="✅")
            st.rerun() # Refresh to update charts immediately
        else:
            st.error("Please fill in all fields!")

# --- BUDGET CONTROLS (OUTSIDE FORM) ---
c1, c2, _ = st.columns([1, 1, 4])
with c1:
    if st.button("➖ $100"):
        st.session_state.budget_goal -= 100
        st.rerun()
with c2:
    if st.button("➕ $100"):
        st.session_state.budget_goal += 100
        st.rerun()

st.divider()

# --- ANALYTICS (ATTRACTIVE CHARTS) ---
if not df.empty:
    st.subheader("📊 Visual Analytics")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # VERY ATTRACTIVE BAR GRAPH
        daily_data = df.groupby("Date")["Amount"].sum().reset_index()
        fig_bar = px.bar(
            daily_data, x="Date", y="Amount",
            title="➤ Spending Trend",
            color="Amount",
            color_continuous_scale="Viridis", # Stunning gradient
            text_auto='.2s'
        )
        fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        # CLEAN DONUT CHART
        fig_pie = px.pie(
            df, values='Amount', names='Category',
            hole=0.5,
            title="➤ Allocation",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📋 Expense Log")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ Clear Last Entry"):
        if st.session_state.expense_history:
            st.session_state.expense_history.pop()
            st.rerun()
else:
    st.info("Your analytics will appear here once you log an expense.")

# --- WISDOM SECTION ---
st.divider()
tips = ["Save 20% first.", "Track every dollar.", "Invest the rest.", "Emergency funds are key."]
st.subheader("💡 Wisdom")
if st.button("➤ Next Tip"):
    st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)
st.success(f"➤ {tips[st.session_state.tip_index]}")