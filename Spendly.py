import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import uuid
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Spendly Pro", page_icon="💳", layout="wide")

# ---------------- SESSION STATE ----------------
if "expense_history" not in st.session_state:
    st.session_state.expense_history = []
if "budget_goal" not in st.session_state:
    st.session_state.budget_goal = 50000.0

COLUMNS = ["id", "Date", "Category", "Description", "Amount"]

# ---------------- STYLES & HAPTIC ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(-45deg, #050505, #0f172a, #0a2540, #050505);
    background-size: 400% 400%;
    animation: bgMove 20s ease infinite;
    color: white;
}

@keyframes bgMove {0% {background-position:0% 50%;} 50% {background-position:100% 50%;} 100% {background-position:0% 50%;}}

/* Global shimmer overlay */
#shimmer-layer {
    pointer-events: none;
    position: fixed;
    inset: -50%;
    z-index: 9999;
    background: linear-gradient(
        120deg,
        transparent 35%,
        rgba(255,255,255,0.06) 45%,
        rgba(255,255,255,0.12) 50%,
        rgba(255,255,255,0.06) 55%,
        transparent 65%
    );
    animation: shimmerMove 14s linear infinite;
}
@keyframes shimmerMove {from {transform: translateX(-50%) translateY(-50%);} to {transform: translateX(50%) translateY(50%);}}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(25px) saturate(180%);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    padding: 20px;
    transition: all 0.3s ease;
}
.glass:hover {transform: translateY(-3px); box-shadow: 0 12px 32px rgba(0,0,0,0.25);}

/* Inputs */
input, select, [data-baseweb="input"] {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
}

/* Glass button */
.glass-button {
    display: inline-block;
    padding: 10px 28px;
    border-radius: 16px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.2);
    color: #0A84FF;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
}
.glass-button:hover {
    background: rgba(255,255,255,0.15);
    box-shadow: 0 6px 20px rgba(10,132,255,0.2);
}

/* Delete button - iOS style minimal */
.delete-btn {
    display:inline-block;
    padding:6px 16px;
    border-radius:14px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.2);
    color: #FF3B30;
    font-weight:600;
    font-size:0.85rem;
    cursor:pointer;
    transition: all 0.25s ease;
}
.delete-btn:hover {
    background: rgba(255,255,255,0.15);
    box-shadow: 0 4px 12px rgba(255,59,48,0.15);
}

/* Haptic micro shake */
@keyframes haptic {
  0% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  50% { transform: translateX(2px); }
  75% { transform: translateX(-1px); }
  100% { transform: translateX(0); }
}
.haptic:active { animation: haptic 0.15s ease; }
</style>

<div id="shimmer-layer"></div>

<script>
function haptic() {
    if (navigator.vibrate) { navigator.vibrate(15); }
    const audio = new Audio("https://actions.google.com/sounds/v1/cartoon/pop.ogg");
    audio.volume = 0.15;
    audio.play();
}
</script>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ⚙️ Budget")
    st.session_state.budget_goal = st.number_input("Goal (₹)", value=float(st.session_state.budget_goal), step=1000.0)
    st.divider()
    st.caption("Spendly Pro v5.1 - iOS Theme")

# ---------------- HEADER ----------------
st.markdown("<h1>Spendly <span style='color:#0A84FF'>Pro</span></h1>", unsafe_allow_html=True)
st.caption(date.today().strftime("%A, %B %d"))

# ---------------- DATA ----------------
df = pd.DataFrame(st.session_state.expense_history, columns=COLUMNS)
total = df["Amount"].sum() if not df.empty else 0.0
rem = st.session_state.budget_goal - total

# ---------------- METRICS ----------------
c1, c2 = st.columns(2)
c1.metric("Total Expenses", f"₹{total:,.0f}")
c2.metric("Balance", f"₹{rem:,.0f}", "Over" if rem < 0 else "Under")

# ---------------- NEW ENTRY FORM ----------------
st.write("##")
with st.form("new_entry", clear_on_submit=False):
    col1, col2, col3, col4 = st.columns([1,1.5,2,1])
    d = col1.date_input("Date", value=date.today())
    cat = col2.selectbox("Category", ["Food","Rent","Transport","Fun","Bills","Other"])
    desc = col3.text_input("Description")
    amt = col4.number_input("Amount (₹)", min_value=0.0)

    submit_clicked = st.form_submit_button("Confirm Transaction")
    reset_clicked = st.form_submit_button("Reset Form")

    if submit_clicked:
        if desc and amt>0:
            st.session_state.expense_history.insert(0,{
                "id": str(uuid.uuid4()),
                "Date": d,
                "Category": cat,
                "Description": desc,
                "Amount": amt
            })
            st.markdown("<script>haptic();</script>", unsafe_allow_html=True)
            st.experimental_rerun()

    if reset_clicked:
        st.markdown("<script>haptic();</script>", unsafe_allow_html=True)
        st.experimental_rerun()

# ---------------- ANALYTICS ----------------
if not df.empty:
    st.write("##")
    l, r = st.columns([2,1])

    with l:
        plot_df = df.copy()
        plot_df["DateObj"] = pd.to_datetime(plot_df["Date"], errors="coerce")
        daily = plot_df.groupby("DateObj")["Amount"].sum().reset_index()
        fig1 = px.area(daily, x="DateObj", y="Amount")
        fig1.update_layout(height=350, transition={'duration':500})
        st.plotly_chart(fig1, use_container_width=True)

    with r:
        fig2 = px.pie(df, values="Amount", names="Category", hole=0.7)
        fig2.update_layout(height=350, transition={'duration':500})
        st.plotly_chart(fig2, use_container_width=True)

# ---------------- CSV EXPORT ----------------
if not df.empty:
    st.write("##")
    csv = df.to_csv(index=False).encode("utf-8")
    b64 = base64.b64encode(csv).decode()
    col1, col2, col3 = st.columns([3,2,3])
    with col2:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:15px;">
            <a download="spendly.csv" href="data:text/csv;base64,{b64}" class="glass-button" onclick="haptic()">
                📊 Download CSV
            </a>
        </div>
        """, unsafe_allow_html=True)

# ---------------- ACTIVITY & DELETE ----------------
if st.session_state.expense_history:
    st.write("##")
    st.markdown("### 🕒 Recent Activity")

    for item in st.session_state.expense_history:
        safe_date = pd.to_datetime(item["Date"]).strftime("%d %b %Y")

        # Flex container for entry + delete button
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
            <div class="glass" style="flex:1; padding:15px;">
                <b>{item['Description']}</b><br>
                {item['Category']} • {safe_date}<br>
                ₹{item['Amount']:,.0f}
            </div>
            <div style="margin-left:10px;">
                <form>
                    <button type="submit" name="del_{item['id']}" class="delete-btn" onclick="haptic()">
                        Delete
                    </button>
                </form>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("del_" + item["id"], key=item["id"]):
            st.session_state.expense_history = [x for x in st.session_state.expense_history if x["id"] != item["id"]]
            st.markdown("<script>haptic();</script>", unsafe_allow_html=True)
            st.experimental_rerun()
