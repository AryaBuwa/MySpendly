# 1. Create the project directory
mkdir spendly-pro
cd spendly-pro

# 2. Create the README.md file
cat << 'EOF' > README.md
# 💳 Spendly Pro v5.1 - iOS Themed

Spendly Pro is a sleek, iOS-inspired personal finance tracker built with **Streamlit**, **Pandas**, and **Plotly**. Track your expenses, visualize spending trends, and stay on top of your budget—all with a buttery smooth iOS-style interface.  

---

## 🚀 Features

- **Add, track, and manage expenses** with categories like Food, Rent, Transport, Fun, Bills, and Other.  
- **iOS-inspired UI**:
  - Glass-style cards & buttons  
  - Rounded corners & subtle shadows  
  - Smooth hover transitions  
  - Minimalistic delete button  
- **Analytics**:
  - Daily expense area chart  
  - Category-wise pie chart with smooth transitions  
- **Budget tracking**: Set monthly goal and see total expenses & balance.  
- **Recent activity log** with aligned delete buttons  
- **CSV Export** of expense history  
- **Haptic feedback** and audio cues on actions (add, delete, reset, download)  
- **Fully responsive** layout suitable for desktop browsers.  

---

## ⚙️ Installation

1. **Clone the repo:**
   \`\`\`bash
   git clone https://github.com/yourusername/spendly-pro.git
   cd spendly-pro
   \`\`\`

2. **Create a virtual environment (optional but recommended):**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   .\venv\Scripts\activate     # Windows
   \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install streamlit pandas plotly
   \`\`\`

4. **Run the app:**
   \`\`\`bash
   streamlit run SpendlyPro.py
   \`\`\`

---

## 📷 Screenshots
*Add screenshots here showing the dashboard, charts, and iOS-themed cards.*

---

## 💡 Usage

* **Enter new expenses** in the form to start tracking.
* **View metrics and charts** to visualize your spending habits.
* **Delete entries** smoothly using the iOS-style buttons.
* **Export history** as a CSV file for external record-keeping.
* **Adjust your budget** goal in the sidebar to update your balance in real-time.
EOF

# 3. Setup Python Environment (Optional)
python -m venv venv
# Note: Activate based on your OS (source venv/bin/activate or venv\Scripts\activate)

# 4. Install Dependencies
pip install streamlit pandas plotly

echo "Project folder created and README.md generated successfully!"