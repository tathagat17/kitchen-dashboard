"""
Cloud Kitchen P&L Dashboard
Python: 3.14 | Streamlit | Pandas | Plotly
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cloud Kitchen PNL Dashboard",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .stMetric { border-radius: 10px; padding: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
    .block-container { padding-top: 1rem; }
    h1 { color: #1a1a2e; }
    h2, h3 { color: #16213e; }
    .stDataFrame { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING WITH CACHE (Performance Optimization)
# For real-time refresh: cache expires every 5 minutes (ttl=300)
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_excel("Untitled_spreadsheet.xlsx", header=1)

    # Computed columns
    df["GM%"]          = (df["GROSS MARGIN"]    / df["NET REVENUE"] * 100).round(2)
    df["CM%"]          = (df["KITCHEN EBITDA"]  / df["NET REVENUE"] * 100).round(2)
    df["EBITDA%"]      = (df["KITCHEN EBITDA"]  / df["NET REVENUE"] * 100).round(2)
    df["VARIANCE%"]    = (df["VARIANCE"]         / df["NET REVENUE"] * 100).round(4)

    # Variance buckets
    def variance_bucket(v):
        if v < 2:   return "(a) Var < 2%"
        elif v < 3: return "(b) Var 2% to 3%"
        elif v < 5: return "(c) Var 3% to 5%"
        else:       return "(d) Var > 5%"
    df["VARIANCE BUCKET"] = df["VARIANCE%"].apply(variance_bucket)

    # Revenue bands (in lakhs) for Dashboard 2b
    rev_lacs = df["NET REVENUE"] / 100000
    df["REVENUE BAND"] = pd.cut(
        rev_lacs,
        bins=[0, 15, 25, 35, 45, float("inf")],
        labels=["(a) Below INR 15 lacs", "(b) INR 15 to 25 lacs",
                "(c) INR 25 to 35 lacs", "(d) INR 35 to 45 lacs",
                "(e) Above INR 45 lacs"]
    )

    # Month sort order
    month_order = ["Oct-2023","Nov-2023","Dec-2023","Jan-2024","Feb-2024","Mar-2024"]
    df["MONTH"] = pd.Categorical(df["MONTH"], categories=month_order, ordered=True)
    df = df.sort_values("MONTH")

    return df

# Load data
df = load_data()

# Last refresh timestamp (shown in sidebar for real-time awareness)
last_refresh = datetime.now().strftime("%d %b %Y, %I:%M %p")

# ─────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/restaurant.png", width=60)
st.sidebar.title("🍳 Kitchen Dashboard")
st.sidebar.markdown(f"🕐 Last refreshed: `{last_refresh}`")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
dashboard = st.sidebar.radio(
    "Select Dashboard",
    ["📊 Dashboard 1 — Kitchen Level PNL",
     "📉 Dashboard 2 — Variance Level PNL"]
)

# ══════════════════════════════════════════════
# DASHBOARD 1 — KITCHEN LEVEL PNL
# ══════════════════════════════════════════════
if dashboard == "📊 Dashboard 1 — Kitchen Level PNL":

    st.title("📊 Kitchen Level P&L Snapshot")
    st.markdown("Filter and explore store-level Profit & Loss across months.")

    # ── KPI CARDS ──
    total_stores    = df["STORE"].nunique()
    total_cities    = df["CITY"].nunique()
    avg_revenue     = df["NET REVENUE"].mean() / 100000
    pct_profitable  = (df["EBITDA CATEGORY"] == "EBITDA +ve").mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    kpi_css = """
        background: linear-gradient({bg1}, {bg2});
        border-radius: 14px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border-left: 5px solid {border};
    """

    cards = [
        (col1, "🏪", "Total Stores",        f"{total_stores}",       "#1a1a2e", "#16213e", "#4ecca3"),
        (col2, "🏙️", "Total Cities",        f"{total_cities}",       "#1a1a2e", "#0f3460", "#f5a623"),
        (col3, "💰", "Avg Net Revenue",     f"₹{avg_revenue:.1f}L",  "#1a1a2e", "#162447", "#e94560"),
        (col4, "📈", "% Profitable Stores", f"{pct_profitable:.1f}%","#1a1a2e", "#1b1b2f", "#a8ff78"),
    ]

    for col, icon, label, value, bg1, bg2, border in cards:
        col.markdown(f"""
        <div style="{kpi_css.format(bg1=bg1, bg2=bg2, border=border)}">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="color: #aaaaaa; font-size: 0.85rem; margin-top: 6px; letter-spacing: 1px; text-transform: uppercase;">{label}</div>
            <div style="color: {border}; font-size: 2rem; font-weight: 800; margin-top: 6px;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # ── FILTERS ──
    st.subheader("🔽 Filters")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        city_opts = ["All"] + sorted(df["CITY"].dropna().unique().tolist())
        sel_city = st.selectbox("City", city_opts)

    with f2:
        zone_opts = ["All"] + sorted(df["ZONE MAPPING"].dropna().unique().tolist())
        sel_zone = st.selectbox("Zone", zone_opts)

    with f3:
        month_opts = ["All"] + df["MONTH"].cat.categories.tolist()
        sel_month = st.selectbox("Month", month_opts)

    with f4:
        store_opts = ["All"] + sorted(df["STORE"].dropna().unique().tolist())
        sel_store = st.selectbox("Store", store_opts)

    f5, f6, f7 = st.columns(3)

    with f5:
        rev_cohort_opts = ["All"] + sorted(df["REVENUE COHORT"].dropna().unique().tolist())
        sel_rev_cohort = st.selectbox("Revenue Cohort", rev_cohort_opts)

    with f6:
        ebitda_cat_opts = ["All"] + sorted(df["EBITDA CATEGORY"].dropna().unique().tolist())
        sel_ebitda_cat = st.selectbox("EBITDA Category", ebitda_cat_opts)

    with f7:
        cm_cohort_opts = ["All"] + sorted(df["CM COHORT"].dropna().unique().tolist())
        sel_cm_cohort = st.selectbox("CM Cohort", cm_cohort_opts)

    # Range sliders
    s1, s2, s3 = st.columns(3)

    with s1:
        ebitda_min = int(df["KITCHEN EBITDA"].min())
        ebitda_max = int(df["KITCHEN EBITDA"].max())
        sel_ebitda_range = st.slider(
            "EBITDA Range (₹)",
            ebitda_min, ebitda_max, (ebitda_min, ebitda_max), step=10000
        )

    with s2:
        cm_min = int(df["CM%"].min())
        cm_max = int(df["CM%"].max())
        sel_cm_range = st.slider("CM% Range", cm_min, cm_max, (cm_min, cm_max))

    with s3:
        rev_min = int(df["NET REVENUE"].min())
        rev_max = int(df["NET REVENUE"].max())
        sel_rev_range = st.slider(
            "Net Revenue Range (₹)",
            rev_min, rev_max, (rev_min, rev_max), step=50000
        )

    # ── APPLY FILTERS ──
    fdf = df.copy()
    if sel_city  != "All": fdf = fdf[fdf["CITY"]           == sel_city]
    if sel_zone  != "All": fdf = fdf[fdf["ZONE MAPPING"]   == sel_zone]
    if sel_month != "All": fdf = fdf[fdf["MONTH"]          == sel_month]
    if sel_store != "All": fdf = fdf[fdf["STORE"]          == sel_store]
    if sel_rev_cohort  != "All": fdf = fdf[fdf["REVENUE COHORT"]  == sel_rev_cohort]
    if sel_ebitda_cat  != "All": fdf = fdf[fdf["EBITDA CATEGORY"] == sel_ebitda_cat]
    if sel_cm_cohort   != "All": fdf = fdf[fdf["CM COHORT"]       == sel_cm_cohort]

    fdf = fdf[
        (fdf["KITCHEN EBITDA"] >= sel_ebitda_range[0]) &
        (fdf["KITCHEN EBITDA"] <= sel_ebitda_range[1]) &
        (fdf["CM%"]            >= sel_cm_range[0])     &
        (fdf["CM%"]            <= sel_cm_range[1])     &
        (fdf["NET REVENUE"]    >= sel_rev_range[0])    &
        (fdf["NET REVENUE"]    <= sel_rev_range[1])
    ]

    st.markdown(f"**Showing {fdf['STORE'].nunique()} stores | {len(fdf)} records**")

    # ── PIVOT TABLE ──
    st.subheader("🧾 Kitchen Snapshot Table")

    pivot = fdf.pivot_table(
        index=["STORE", "CITY", "ZONE MAPPING"],
        columns="MONTH",
        values=["NET REVENUE", "GM%", "CM%", "KITCHEN EBITDA", "EBITDA%"],
        aggfunc="mean"
    ).round(2)

    # Flatten column names
    pivot.columns = [f"{col[0]} | {col[1]}" for col in pivot.columns]
    pivot = pivot.reset_index()

    # Color EBITDA cells
    def color_ebitda(val):
        try:
            if "KITCHEN EBITDA" in str(val):
                return ""
            return ""
        except:
            return ""

    st.dataframe(
        pivot,
        use_container_width=True,
        height=450
    )

    # ── CHART ──
    st.subheader("📈 EBITDA Distribution by City")
    chart_df = fdf.groupby("CITY")["KITCHEN EBITDA"].mean().reset_index()
    chart_df.columns = ["City", "Avg EBITDA"]
    fig = px.bar(
        chart_df, x="City", y="Avg EBITDA",
        color="Avg EBITDA",
        color_continuous_scale="RdYlGn",
        title="Average EBITDA by City",
        text_auto=".2s"
    )
    fig.update_layout(showlegend=False, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    # ── EBITDA +ve vs -ve Pie ──
    st.subheader("🥧 Profitable vs Loss-Making Stores")
    pie_df = fdf["EBITDA CATEGORY"].value_counts().reset_index()
    pie_df.columns = ["Category", "Count"]
    fig2 = px.pie(
        pie_df, names="Category", values="Count",
        color="Category",
        color_discrete_map={"EBITDA +ve": "#2ecc71", "EBITDA -ve": "#e74c3c"},
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════
# DASHBOARD 2 — VARIANCE LEVEL PNL
# ══════════════════════════════════════════════
else:
    st.title("📉 Variance Level P&L Dashboard")
    st.markdown("Analyse food material wastage (Variance) across revenue categories and store counts.")

    # ── TOP FILTER ──
    st.subheader("🔽 Variance Category Filter")
    all_buckets = ["(a) Var < 2%", "(b) Var 2% to 3%", "(c) Var 3% to 5%", "(d) Var > 5%"]
    sel_buckets = st.multiselect(
        "Select Variance Category (select one or more)",
        options=all_buckets,
        default=all_buckets
    )

    if not sel_buckets:
        st.warning("Please select at least one variance category.")
        st.stop()

    vdf = df[df["VARIANCE BUCKET"].isin(sel_buckets)]

    months_sorted = df["MONTH"].cat.categories.tolist()

    # ══ SUB-DASHBOARD 2a — AVG VARIANCE % BY REVENUE COHORT ══
    st.markdown("---")
    st.subheader("📋 Sub-Dashboard 1 — Average Variance % by Revenue Category")
    st.caption("Shows average variance % of kitchens under each revenue cohort per month")

    rev_cohort_order = ["INR 20 to 30 lacs", "INR 30 to 40 lacs", "More than 40 lacs"]

    pivot2a = vdf.pivot_table(
        index="REVENUE COHORT",
        columns="MONTH",
        values="VARIANCE%",
        aggfunc="mean"
    ).round(4)

    # Reorder rows
    pivot2a = pivot2a.reindex([r for r in rev_cohort_order if r in pivot2a.index])

    # Grand total row
    grand_row = pd.DataFrame(
        vdf.groupby("MONTH")["VARIANCE%"].mean().round(4)
    ).T
    grand_row.index = ["Grand Total"]
    pivot2a = pd.concat([pivot2a, grand_row])

    # Format as percentage (values are already in %, e.g. 0.62 means 0.62%)
    pivot2a_display = pivot2a.apply(lambda col: col.map(lambda x: f"{x:.2f}%" if pd.notnull(x) else "-"))

    st.dataframe(
        pivot2a_display,
        use_container_width=True
    )

    # Chart for 2a
    chart2a = vdf.groupby(["MONTH", "REVENUE COHORT"])["VARIANCE%"].mean().reset_index()
    fig3 = px.line(
        chart2a, x="MONTH", y="VARIANCE%",
        color="REVENUE COHORT",
        markers=True,
        title="Avg Variance % Trend by Revenue Cohort",
        labels={"VARIANCE%": "Avg Variance %", "MONTH": "Month"}
    )
    fig3.update_layout(plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

    # ══ SUB-DASHBOARD 2b — STORE COUNT BY REVENUE BAND ══
    st.markdown("---")
    st.subheader("📋 Sub-Dashboard 2 — Store Count by Revenue Range")
    st.caption("Count of kitchen stores in each revenue band per month, filtered by variance category above")

    rev_band_order = [
        "(a) Below INR 15 lacs", "(b) INR 15 to 25 lacs",
        "(c) INR 25 to 35 lacs", "(d) INR 35 to 45 lacs",
        "(e) Above INR 45 lacs"
    ]

    pivot2b = vdf.pivot_table(
        index="REVENUE BAND",
        columns="MONTH",
        values="STORE",
        aggfunc="count"
    ).fillna(0).astype(int)

    # Reorder rows
    pivot2b = pivot2b.reindex([r for r in rev_band_order if r in pivot2b.index])

    # Grand total row
    grand_row_b = pd.DataFrame(pivot2b.sum()).T
    grand_row_b.index = ["Grand Total"]
    pivot2b = pd.concat([pivot2b, grand_row_b])

    st.dataframe(
        pivot2b,
        use_container_width=True
    )

    # Chart for 2b
    chart2b = vdf.groupby(["MONTH", "REVENUE BAND"])["STORE"].count().reset_index()
    chart2b.columns = ["Month", "Revenue Band", "Store Count"]
    fig4 = px.bar(
        chart2b, x="Month", y="Store Count",
        color="Revenue Band",
        barmode="stack",
        title="Store Count by Revenue Band per Month",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig4.update_layout(plot_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)

    # ── BONUS: Variance Heatmap ──
    st.markdown("---")
    st.subheader("🔥 Bonus — Variance% Heatmap by City & Month")
    heat_df = vdf.pivot_table(
        index="CITY", columns="MONTH", values="VARIANCE%", aggfunc="mean"
    ).round(4)
    fig5 = px.imshow(
        heat_df,
        color_continuous_scale="RdYlGn_r",
        text_auto=".2f",
        title="Average Variance % — City × Month Heatmap"
    )
    st.plotly_chart(fig5, use_container_width=True)
