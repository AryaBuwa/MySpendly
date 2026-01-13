import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# 1. PERSISTENT STORAGE
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "tip_index" not in st.session_state:
    st.session_state.tip_index = 0
if "budget_goal" not in st.session_state:
    st.session_state.budget_goal = 1000.0

# 2. PAGE CONFIG
st.set_page_config(page_title="Spendly Pro", page_icon="💰", layout="wide")

# Custom CSS for "Bordered" look
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #eef0f2; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); }
    [data-testid="stMetricValue"] { color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATE VALIDATION LOGIC
def validate_date():
    # FIX: We use a temporary variable to avoid modifying session_state directly 
    # during the widget's own callback to prevent the StreamlitAPIException.
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
st.title("💰 Spendly")
st.caption("Professional Expense Tracking & Financial Insights")

df = pd.DataFrame(st.session_state.expense_history)
total_spent = df["Amount"].sum() if not df.empty else 0.0
top_cat = df["Category"].mode()[0] if not df.empty else "None"
budget_left = max(0.0, st.session_state.budget_goal - total_spent)

m1, m2, m3 = st.columns(3)
m1.metric("Total Spending", f"${total_spent:,.2f}")
m2.metric("Top Category", top_cat)
m3.metric("Budget Remaining", f"${budget_left:,.2f}")

# Progress Bar
progress = min(1.0, total_spent / st.session_state.budget_goal)
st.write(f"**Monthly Budget Goal: ${st.session_state.budget_goal}**")
st.progress(progress)

st.divider()

# --- INPUT SECTION ---
with st.container():
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        # Removed "Verified" labels for cleaner UI
        date_val = st.text_input("Date (DD/MM/YYYY)", key="date_input", on_change=validate_date, placeholder="DD/MM/YYYY")
        desc_val = st.text_input("Description", key="desc_input", placeholder="Store name / Item")

    with c2:
        categories = ["Housing", "Groceries", "Dining", "Transport", "Gym", "Entertainment", "Shopping", "Medical", "Investment", "Misc"]
        cat_val = st.selectbox("Category", options=categories, key="cat_input")
        amt_val = st.number_input("Amount ($)", min_value=0.0, step=0.01, key="amt_input")

    with c3:
        st.write("**Budget Goal Controls**")
        # FIX: Quick +/- buttons with st.rerun() to ensure single-click updates
        bc1, bc2, bc3 = st.columns([1, 2, 1])
        with bc1:
            if st.button("➖"):
                st.session_state.budget_goal -= 100.0
                st.rerun()
        with bc2:
            st.markdown(f"<h3 style='text-align:center; margin:0;'>${st.session_state.budget_goal}</h3>", unsafe_allow_html=True)
        with bc3:
            if st.button("➕"):
                st.session_state.budget_goal += 100.0
                st.rerun()
        
        st.write(" ") # Spacer
        if st.button("Save Expense", use_container_width=True, type="primary"):
            if len(date_val) == 10 and desc_val and amt_val > 0:
                st.session_state.expense_history.append({
                    "Date": date_val, "Description": desc_val, "Category": cat_val, "Amount": amt_val
                })
                # Clear inputs via session state
                st.session_state.date_input = ""
                st.session_state.desc_input = ""
                st.session_state.amt_input = 0.0
                st.toast("Expense Logged!", icon="💰")
                st.rerun()
            else:
                st.error("Please fill all fields correctly.")

st.divider()

# --- ANALYTICS SECTION ---
col_left, col_right = st.columns([0.6, 0.4])

with col_left:
    st.subheader("📋 Expense Log")
    if not df.empty:
        st.dataframe(df, use_container_width=True, height=300)
        ec1, ec2 = st.columns(2)
        with ec1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Report (CSV)", data=csv, file_name="spendly_report.csv", mime="text/csv", use_container_width=True)
        with ec2:
            if st.button("🗑️ Delete Last Entry", use_container_width=True):
                if st.session_state.expense_history:
                    st.session_state.expense_history.pop()
                    st.rerun()
    else:
        st.info("Start adding expenses to see your log!")

with col_right:
    st.subheader("🥧 Spending Breakdown")
    if not df.empty:
        fig = px.pie(df, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data to chart yet.")

# --- WISDOM SECTION ---
st.divider()
tips = [
    "Save 20% of your income monthly.", "Avoid impulse purchases.", "Track every expense.",
    "Build a 3-month emergency fund.", "Invest in low-cost index funds.", "Minimize high-interest debt."
]

tw1, tw2 = st.columns([0.95, 0.05])
with tw1:
    st.subheader("💡 Financial Wisdom")
with tw2:
    # Changed ">" to "➤" as requested
    if st.button("➤"):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)

if total_spent > st.session_state.budget_goal:
    st.error(f"⚠️ High Spending Alert: You are ${total_spent - st.session_state.budget_goal:,.2f} over your goal!")
else:
    # Changed tip indicator to "➤"
    st.success(f"➤ {tips[st.session_state.tip_index]}")