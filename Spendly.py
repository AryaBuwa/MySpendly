import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PERSISTENT STORAGE
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "tip_index" not in st.session_state:
    st.session_state.tip_index = 0
if "budget_goal" not in st.session_state:
    st.session_state.budget_goal = 1000.0

# 2. PAGE CONFIG
st.set_page_config(page_title="Spendly Pro", page_icon="💰", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #eef0f2; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); }
    [data-testid="stMetricValue"] { color: #2e7d32; font-weight: 700; }
    div[data-testid="stForm"] { border: none; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATE VALIDATION CALLBACK
def validate_date():
    raw = st.session_state.date_input.replace("/", "")
    clean = "".join(filter(str.isdigit, raw))
    formatted = ""
    if len(clean) >= 2:
        dd = min(max(1, int(clean[:2])), 31)
        formatted += f"{dd:02d}/"
        if len(clean) >= 4:
            mm = min(max(1, int(clean[2:4])), 12)
            formatted += f"{mm:02d}/"
            if len(clean) >= 8:
                yyyy = min(max(1900, int(clean[4:8])), 2099)
                formatted += str(yyyy)
            else: formatted += clean[4:]
        else: formatted += clean[2:]
    else: formatted = clean
    st.session_state.date_input = formatted

# --- HEADER & METRICS ---
st.title("💰 Spendly Pro")
st.caption("Simplified Financial Intelligence")

# Data Prep
df = pd.DataFrame(st.session_state.expense_history)
total_spent = df["Amount"].sum() if not df.empty else 0.0
top_cat = df["Category"].mode()[0] if not df.empty else "N/A"
budget_left = max(0.0, st.session_state.budget_goal - total_spent)

m1, m2, m3 = st.columns(3)
m1.metric("Total Spending", f"${total_spent:,.2f}")
m2.metric("Top Category", top_cat)
m3.metric("Budget Remaining", f"${budget_left:,.2f}")

# Progress Bar
progress = min(1.0, total_spent / st.session_state.budget_goal)
st.write(f"**Budget Goal: ${st.session_state.budget_goal}**")
st.progress(progress)

st.divider()

# --- INPUT SECTION (FIXED WITH FORM) ---
# Using a form solves the "StreamlitAPIException" and clears inputs automatically
with st.form("expense_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        # Note: In forms, we use the values directly from the widgets on submission
        date_input = st.text_input("Date (DD/MM/YYYY)", placeholder="DD/MM/YYYY", key="date_input", on_change=validate_date)
        desc_input = st.text_input("Description", placeholder="Where did it go?")

    with c2:
        cat_options = ["Housing", "Groceries", "Dining", "Transport", "Gym", "Entertainment", "Shopping", "Medical", "Investment", "Misc"]
        cat_input = st.selectbox("Category", options=cat_options)
        amt_input = st.number_input("Amount ($)", min_value=0.0, step=1.0)

    with c3:
        st.write("**Quick Settings**")
        # Budget buttons live outside or inside; here we keep them inside for alignment
        submitted = st.form_submit_button("Save Expense", use_container_width=True, type="primary")
        
        if submitted:
            if len(date_input) == 10 and desc_input and amt_input > 0:
                st.session_state.expense_history.append({
                    "Date": date_input, "Description": desc_input, "Category": cat_input, "Amount": amt_input
                })
                st.toast("Expense Logged!", icon="💰")
                st.rerun()
            else:
                st.error("Please fill all fields correctly.")

# Budget Controls (Stay outside form to allow immediate rerun)
st.write("### Adjust Goal")
bc1, bc2, bc3 = st.columns([1, 1, 4])
with bc1: 
    if st.button("➖ $100"): 
        st.session_state.budget_goal -= 100
        st.rerun()
with bc2: 
    if st.button("➕ $100"): 
        st.session_state.budget_goal += 100
        st.rerun()

st.divider()

# --- ANALYTICS SECTION (STUNNING CHARTS) ---
if not df.empty:
    st.subheader("📊 Spending Insights")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # High-End Bar Chart
        # Convert date strings to datetime objects for proper sorting in the chart
        df_plot = df.copy()
        daily_total = df_plot.groupby("Date")["Amount"].sum().reset_index()
        
        fig_bar = px.bar(
            daily_total, x="Date", y="Amount",
            title="➤ Daily Spending Trend",
            color="Amount",
            color_continuous_scale="Blugrn", # Professional aesthetic
            text_auto='.2s'
        )
        fig_bar.update_layout(showlegend=False, coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        # Donut Chart
        fig_pie = px.pie(
            df, values='Amount', names='Category', 
            hole=0.6,
            title="➤ Category Distribution",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📋 Expense Log")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Log your first expense to unlock analytics!")

# --- WISDOM SECTION ---
st.divider()
tips = ["Save 20% of income.", "Avoid impulse buys.", "Track every cent.", "Build an emergency fund."]
st.subheader("💡 Wisdom")
if st.button("➤ Next Tip"):
    st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)
st.success(f"➤ {tips[st.session_state.tip_index]}")