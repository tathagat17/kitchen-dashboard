# 🍳 Cloud Kitchen P&L Dashboard

A full-stack interactive data analytics dashboard built with **Python**, **Streamlit** and **Plotly** for analysing Profit & Loss across cloud kitchen stores, cities and zones.

---

## 🚀 Live Dashboard

👉 **[https://kitchen-dashboard.streamlit.app](https://kitchen-dashboard.streamlit.app)**

---

## 📋 Project Overview

This project analyses the P&L data of a cloud kitchen company across:
- **344 stores** across **5 cities** (Ahmedabad, Bangalore, Hyderabad, Mumbai, Pune)
- **4 zones** (North, South, East, West)
- **6 months** (Oct 2023 – Mar 2024)

The dashboard is split into **2 main sections:**

### Dashboard 1 — Kitchen Level PNL
An interactive kitchen-level P&L snapshot with the following filters:
- **Dropdown filters:** Store, City, Zone, Month, Revenue Cohort, EBITDA Category, CM Cohort, EBITDA Cohort
- **Range sliders:** EBITDA Range (₹), CM% Range, Net Revenue Range (₹), GM% Range
- **Visuals:** Kitchen Snapshot Pivot Table, EBITDA Distribution by City (bar chart), Profitable vs Loss-Making Stores (donut chart)

### Dashboard 2 — Variance Level PNL
Food material wastage (Variance) analysis split into:
- **Sub-dashboard 1:** Average Variance % by Revenue Category per month
- **Sub-dashboard 2:** Store count by Revenue Band per month
- **Visuals:** Plotly tables with black headers, trend line chart, stacked bar chart, City × Month heatmap

---

## ⚙️ Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.14 |
| Streamlit | 1.45.1 |
| Pandas | 2.2.3 |
| Plotly | 5.24.1 |
| Openpyxl | 3.1.5 |

---

## 📁 Repository Structure

```
kitchen-dashboard/
├── app.py                      # Main Streamlit dashboard
├── analysis.ipynb              # Data analysis & insights notebook
├── requirements.txt            # Package dependencies
├── Untitled_spreadsheet.xlsx   # Source dataset
└── README.md                   # Project documentation
```

---

## 🛠️ How to Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/tathagat17/kitchen-dashboard.git
cd kitchen-dashboard
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the dashboard**
```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## ⚡ Performance Optimization

The dashboard uses `@st.cache_data(ttl=300)` to cache data for **5 minutes**, ensuring:
- Data is loaded from Excel only once per session
- All filters and charts operate on in-memory cached dataframe
- A **Refresh Data** button in the sidebar allows manual cache clear
- IST timezone used for accurate refresh timestamps

```python
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_excel("Untitled_spreadsheet.xlsx", header=1)
    return df
```

---

## 📊 Key Insights

| # | Insight | Status |
|---|---------|--------|
| 1 | 52.1% of stores are EBITDA negative — majority loss-making | 🔴 Critical |
| 2 | Ahmedabad is the best city — highest EBITDA (₹7.2L), lowest wastage | 🟢 Positive |
| 3 | Mumbai underperforms — lowest EBITDA (₹6.3L) despite similar revenue | 🔴 Action needed |
| 4 | January 2024 is the peak month — highest revenue (₹35.6L) and EBITDA (₹7.3L) | 🟢 Seasonal |
| 5 | North zone has lowest CM% (16.0%) vs East zone (17.2%) | 🟡 Investigate |
| 6 | Pune has highest food wastage (0.63%) — Jan-2024 peak at 0.69% | 🟡 Fix ops |
| 7 | Andrews, Reed & Silva — chronic loss-maker with avg EBITDA of -₹1.3L | 🔴 Immediate review |

---

## 👤 Author

**Tathagata Ghosh**  
📧 Data Analyst  
🔗 [GitHub](https://github.com/tathagat17)
