# 💳 Spendly Pro
### **Personal Finance, Reimagined for Focus.**

[**Launch Live Application**](https://myspendly.streamlit.app/) • [View Repository](https://github.com/AryaBuwa/MySpendly)

Spendly Pro is a high-performance, minimalist expense tracker inspired by the design languages of **Apple** and **Notion**. Built on Streamlit, it combines the structural clarity of a digital ledger with the visual depth of modern financial dashboards.

---

## 🎨 Design Philosophy
Spendly Pro is built for users who value **aesthetics as much as utility**.
* **Minimalist UI:** A deep-charcoal interface utilizing the `Inter` typeface for maximum legibility.
* **Tactile Feedback:** Notion-style color-coded tags for instant category recognition.
* **Apple-Inspired Alerts:** Dynamic status badges that distinguish between "Today" and historical entries.

---

## ✨ Key Features

### 📊 **Intelligent Analytics**
* **The Doughnut Allocation:** A high-contrast visualization of your spending distribution.
* **Activity Heatmap:** A 30-day GitHub-style grid to track spending frequency.
* **Live Metrics:** High-level summary cards for **Capacity**, **Expenditure**, and **Savings**.

### ⚙️ **Envelope Budgeting**
Manage your finances using the digital envelope method. Customize limits for core categories including Food, Rent, Transport, Fun, and Bills.

### 📂 **Data Sovereignty**
* **Instant Ledger:** Fast, responsive logging with a UUID-backed transaction system.
* **CSV Export:** One-click download for auditing in Excel or Apple Numbers.
* **Deep Search:** A powerful filter to drill down through transactions instantly.

---

## 🛠️ Technical Stack & Installation

| Component | Technology |
| :--- | :--- |
| **Framework** | Streamlit |
| **Data Engine** | Pandas |
| **Visualization** | Plotly (Graph Objects) |
| **Styling** | Custom CSS3 & HTML Injection |

**Local Setup:**
```bash
git clone [https://github.com/AryaBuwa/MySpendly.git](https://github.com/AryaBuwa/MySpendly.git) && cd MySpendly
pip install -r requirements.txt
streamlit run app.py


---

## 📝 Changelog & Roadmap

### **v1.0.0** — *Current Release*
> **Initial Stable Build**
* **Design:** Implementation of the Apple/Notion Dark Mode UI using custom CSS injection.
* **Logic:** Core "Envelope" budgeting system for categorized financial tracking.
* **Data:** CSV export functionality and interactive 30-day expenditure heatmap.
* **ID System:** UUID-backed transaction logging for precise record management.

### **Planned Features (Roadmap)**
* [ ] **Multi-Currency Support:** Automatic conversion for international use.
* [ ] **Recurring Transactions:** Automation for monthly subscriptions and rent.
* [ ] **PDF Summaries:** Beautifully formatted monthly financial reports for offline storage.
* [ ] **Visual Alerts:** Notifications when an "Envelope" exceeds 80% of its capacity.

---