"""
╔══════════════════════════════════════════════════════════════════╗
║                      हिसाब किताब                                  ║
║              Personal Finance Analytics Dashboard                ║
║                                                                  ║
║  A sleek, light-themed expense & investment tracker built        ║
║  with Streamlit, Pandas, and Plotly. Generates realistic        ║
║  mock data — no external APIs required.                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ─── Imports ────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import textwrap

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hisaab Kitaab — Personal Finance",
    page_icon="HK",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS: Light Fintech Theme ───────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global overrides ─────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Force light background everywhere */
    .stApp {
        background-color: #FFFFFF;
    }

    /* ── Sidebar styling ──────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
    }

    /* ── Metric card styling ──────────────────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 60%, #DBEAFE 100%);
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.10);
    }

    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-weight: 500;
        font-size: 0.8rem;
        letter-spacing: 0.025em;
        text-transform: uppercase;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700;
        font-size: 1.6rem;
    }

    /* ── Tab styling ──────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F8FAFC;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.9rem;
        color: #64748B;
    }

    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }

    /* ── Dataframe / table styling ────────────────────────────────────────── */
    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Divider ──────────────────────────────────────────────────────────── */
    hr {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 1.5rem 0;
    }

    /* ── Alert boxes ──────────────────────────────────────────────────────── */
    .stAlert {
        border-radius: 12px;
    }

    /* ── Headline badge ───────────────────────────────────────────────────── */
    .headline-card {
        background: #F8FAFC;
        border-left: 4px solid #2563EB;
        border-radius: 0 10px 10px 0;
        padding: 14px 20px;
        margin-bottom: 12px;
        color: #334155;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .headline-card strong {
        color: #0F172A;
    }

    /* ── Section headers ──────────────────────────────────────────────────── */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }

    .section-subtitle {
        font-size: 0.82rem;
        color: #94A3B8;
        font-weight: 400;
        margin-bottom: 18px;
    }

    /* ── Sidebar brand ────────────────────────────────────────────────────── */
    .brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }

    .brand-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 400;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    /* ── Portfolio card ────────────────────────────────────────────────────── */
    .portfolio-card {
        background: linear-gradient(135deg, #F8FAFC, #EFF6FF);
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .portfolio-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.08);
    }

    .portfolio-label {
        font-size: 0.72rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .portfolio-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
    }

    .portfolio-return-positive {
        color: #16A34A;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .portfolio-return-negative {
        color: #DC2626;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* ── Insight box ──────────────────────────────────────────────────────── */
    .insight-box {
        background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
        border: 1px solid #FCD34D;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        line-height: 1.6;
    }

    .insight-box-blue {
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        border: 1px solid #93C5FD;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        line-height: 1.6;
    }

    .insight-box-green {
        background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        line-height: 1.6;
    }

    .insight-icon {
        font-size: 1.3rem;
        margin-right: 8px;
    }

    /* ── Footer ───────────────────────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #CBD5E1;
        font-size: 0.72rem;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #F1F5F9;
        letter-spacing: 0.04em;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA GENERATION — deterministic seed for reproducibility within a session
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def generate_expense_data() -> pd.DataFrame:
    """
    Synthesise 30 days of realistic Indian expense data.
    Merchant ↔ Category mapping keeps the data believable.
    """
    np.random.seed(42)
    random.seed(42)

    merchant_category_map = {
        "Zomato": "Food & Dining",
        "Swiggy": "Food & Dining",
        "Amazon": "Shopping",
        "Flipkart": "Shopping",
        "Myntra": "Shopping",
        "PhonePe Transfer": "Transfers",
        "Google Pay Transfer": "Transfers",
        "Jio Recharge": "Bills & Utilities",
        "Airtel Recharge": "Bills & Utilities",
        "Electricity Board": "Bills & Utilities",
        "Uber": "Transport",
        "Ola": "Transport",
        "Netflix": "Entertainment",
        "Spotify": "Entertainment",
        "BookMyShow": "Entertainment",
        "Apollo Pharmacy": "Health",
        "BigBasket": "Groceries",
        "Blinkit": "Groceries",
        "Zepto": "Groceries",
        "DMart": "Groceries",
    }

    merchants = list(merchant_category_map.keys())
    today = datetime.now().date()
    records = []

    for day_offset in range(30):
        date = today - timedelta(days=day_offset)
        # 2-6 transactions per day
        n_txns = random.randint(2, 6)
        for _ in range(n_txns):
            merchant = random.choice(merchants)
            category = merchant_category_map[merchant]

            # Realistic amount ranges per category
            amount_ranges = {
                "Food & Dining": (80, 750),
                "Shopping": (250, 5000),
                "Transfers": (100, 3000),
                "Bills & Utilities": (100, 2500),
                "Transport": (60, 500),
                "Entertainment": (99, 999),
                "Health": (50, 1500),
                "Groceries": (120, 2000),
            }
            lo, hi = amount_ranges[category]
            amount = round(random.uniform(lo, hi), 2)

            records.append({
                "Date": date,
                "Merchant": merchant,
                "Category": category,
                "Amount (₹)": amount,
            })

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False).reset_index(drop=True)
    return df


@st.cache_data
def generate_portfolio_data() -> pd.DataFrame:
    """
    Build a realistic Indian retail-investor portfolio with mixed asset classes.
    """
    np.random.seed(42)
    portfolio = [
        {
            "Asset": "Reliance Industries",
            "Platform": "Upstox (Stocks)",
            "Invested (₹)": 75_000,
            "Current Value (₹)": 91_350,
        },
        {
            "Asset": "HDFC Bank",
            "Platform": "Upstox (Stocks)",
            "Invested (₹)": 50_000,
            "Current Value (₹)": 54_200,
        },
        {
            "Asset": "Tata Motors",
            "Platform": "Upstox (Stocks)",
            "Invested (₹)": 30_000,
            "Current Value (₹)": 38_700,
        },
        {
            "Asset": "Axis Bluechip Fund",
            "Platform": "Zerodha (Mutual Funds)",
            "Invested (₹)": 1_00_000,
            "Current Value (₹)": 1_18_400,
        },
        {
            "Asset": "SBI Small Cap Fund",
            "Platform": "Zerodha (Mutual Funds)",
            "Invested (₹)": 60_000,
            "Current Value (₹)": 73_800,
        },
        {
            "Asset": "Parag Parikh Flexi Cap",
            "Platform": "Zerodha (Mutual Funds)",
            "Invested (₹)": 80_000,
            "Current Value (₹)": 97_600,
        },
        {
            "Asset": "SBI 1-Year FD",
            "Platform": "Bank FD",
            "Invested (₹)": 2_00_000,
            "Current Value (₹)": 2_14_500,
        },
        {
            "Asset": "HDFC 3-Year FD",
            "Platform": "Bank FD",
            "Invested (₹)": 1_50_000,
            "Current Value (₹)": 1_72_350,
        },
    ]
    df = pd.DataFrame(portfolio)
    df["Returns (%)"] = round(
        (df["Current Value (₹)"] - df["Invested (₹)"]) / df["Invested (₹)"] * 100, 2
    )
    return df


# ─── Load data once ────────────────────────────────────────────────────────────
expenses_df = generate_expense_data()
portfolio_df = generate_portfolio_data()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Brand + Navigation
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="brand-title">Hisaab Kitaab</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Personal Finance Dashboard</div>', unsafe_allow_html=True)

    st.divider()

    # Navigation radio
    page = st.radio(
        "Navigate",
        ["The Pulse — Expenses", "The Vault — Investments", "The Guru — AI Analyst"],
        label_visibility="collapsed",
    )

    st.divider()

    # Contextual sidebar info
    total_invested = portfolio_df["Invested (₹)"].sum()
    total_current = portfolio_df["Current Value (₹)"].sum()
    net_gain = total_current - total_invested
    st.markdown("##### Quick Snapshot")
    st.caption(f"**Portfolio Value:** ₹{total_current:,.0f}")
    st.caption(f"**Net Gain:** ₹{net_gain:,.0f}")
    st.caption(f"**30-Day Spend:** ₹{expenses_df['Amount (₹)'].sum():,.0f}")

    st.divider()
    st.markdown(
        '<div class="footer">Built with Streamlit<br>© 2026 Hisaab Kitaab</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — THE PULSE  (Expense Tracker)
# ═══════════════════════════════════════════════════════════════════════════════

if page == "The Pulse — Expenses":

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">The Pulse</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-subtitle">Track every rupee. Own every decision.</p>',
        unsafe_allow_html=True,
    )

    # ── Date filter ───────────────────────────────────────────────────────────
    col_a, col_b, _ = st.columns([1, 1, 2])
    min_date = expenses_df["Date"].min().date()
    max_date = expenses_df["Date"].max().date()

    with col_a:
        start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    with col_b:
        end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

    # Filter data by selected range
    mask = (expenses_df["Date"].dt.date >= start_date) & (expenses_df["Date"].dt.date <= end_date)
    filtered_df = expenses_df.loc[mask].copy()

    st.divider()

    # ── Top-level metric cards ────────────────────────────────────────────────
    today_mask = filtered_df["Date"].dt.date == datetime.now().date()
    today_spend = filtered_df.loc[today_mask, "Amount (₹)"].sum()
    total_spend = filtered_df["Amount (₹)"].sum()

    if not filtered_df.empty:
        top_category = (
            filtered_df.groupby("Category")["Amount (₹)"]
            .sum()
            .idxmax()
        )
        top_category_amt = filtered_df.groupby("Category")["Amount (₹)"].sum().max()
    else:
        top_category = "—"
        top_category_amt = 0

    bank_balance = 45_000  # Simulated starting balance

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current Bank Balance", f"₹{bank_balance:,.0f}")
    m2.metric("Today's Expenses", f"₹{today_spend:,.0f}")
    m3.metric("Period Total", f"₹{total_spend:,.0f}")
    m4.metric("Highest Category", f"{top_category}", delta=f"₹{top_category_amt:,.0f}")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    chart_col, table_col = st.columns([1, 1])

    with chart_col:
        st.markdown("##### Spending by Category")
        if not filtered_df.empty:
            cat_spend = (
                filtered_df.groupby("Category")["Amount (₹)"]
                .sum()
                .reset_index()
                .sort_values("Amount (₹)", ascending=False)
            )
            fig_pie = px.pie(
                cat_spend,
                values="Amount (₹)",
                names="Category",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
            )
            fig_pie.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#334155"),
                showlegend=False,
                height=380,
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenses in this date range.")

    with table_col:
        st.markdown("##### Daily Spend Trend")
        if not filtered_df.empty:
            daily_spend = (
                filtered_df.groupby(filtered_df["Date"].dt.date)["Amount (₹)"]
                .sum()
                .reset_index()
            )
            daily_spend.columns = ["Date", "Amount (₹)"]
            daily_spend = daily_spend.sort_values("Date")

            fig_bar = px.bar(
                daily_spend,
                x="Date",
                y="Amount (₹)",
                color_discrete_sequence=["#2563EB"],
            )
            fig_bar.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="₹"),
                font=dict(family="Inter", color="#334155"),
                height=380,
            )
            fig_bar.update_traces(
                hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
                marker_cornerradius=6,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No expenses in this date range.")

    st.divider()

    # ── Transactions table ────────────────────────────────────────────────────
    st.markdown("##### Recent Transactions")
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
        display_df["Amount (₹)"] = display_df["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=420,
        )
    else:
        st.info("No transactions found for the selected dates.")


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — THE VAULT  (Portfolio & Investments)
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "The Vault — Investments":

    st.markdown('<p class="section-header">The Vault</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-subtitle">Your wealth, organised and transparent.</p>',
        unsafe_allow_html=True,
    )

    # ── Aggregate metrics ─────────────────────────────────────────────────────
    total_invested = portfolio_df["Invested (₹)"].sum()
    total_current = portfolio_df["Current Value (₹)"].sum()
    total_return_pct = round((total_current - total_invested) / total_invested * 100, 2)
    net_pnl = total_current - total_invested

    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Total Invested", f"₹{total_invested:,.0f}")
    v2.metric("Current Value", f"₹{total_current:,.0f}")
    v3.metric("Net P&L", f"₹{net_pnl:,.0f}", delta=f"{total_return_pct}%")
    v4.metric("Assets Held", f"{len(portfolio_df)}")

    st.divider()

    # ── Portfolio cards by platform ───────────────────────────────────────────
    platforms = portfolio_df["Platform"].unique()

    for platform in platforms:
        st.markdown(f"##### {platform}")
        plat_df = portfolio_df[portfolio_df["Platform"] == platform]
        cols = st.columns(len(plat_df))
        for i, (_, row) in enumerate(plat_df.iterrows()):
            ret_class = "portfolio-return-positive" if row["Returns (%)"] >= 0 else "portfolio-return-negative"
            ret_sign = "+" if row["Returns (%)"] >= 0 else ""
            with cols[i]:
                st.markdown(f"""
                <div class="portfolio-card">
                    <div class="portfolio-label">{row['Asset']}</div>
                    <div class="portfolio-value">₹{row['Current Value (₹)']:,.0f}</div>
                    <div style="font-size:0.78rem; color:#94A3B8; margin:4px 0;">
                        Invested ₹{row['Invested (₹)']:,.0f}
                    </div>
                    <div class="{ret_class}">{ret_sign}{row['Returns (%)']}%</div>
                </div>
                """, unsafe_allow_html=True)
        st.write("")  # spacer

    st.divider()

    # ── Allocation Chart ──────────────────────────────────────────────────────
    alloc_col, trend_col = st.columns([1, 1])

    with alloc_col:
        st.markdown("##### Asset Allocation")
        alloc_df = (
            portfolio_df.groupby("Platform")["Current Value (₹)"]
            .sum()
            .reset_index()
        )
        fig_alloc = px.pie(
            alloc_df,
            values="Current Value (₹)",
            names="Platform",
            hole=0.48,
            color_discrete_sequence=["#2563EB", "#7C3AED", "#0EA5E9"],
        )
        fig_alloc.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
        )
        fig_alloc.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#334155"),
            showlegend=False,
            height=340,
        )
        st.plotly_chart(fig_alloc, use_container_width=True)

    # ── Market Headlines ──────────────────────────────────────────────────────
    with trend_col:
        st.markdown("##### Market Updates — What's New")
        headlines = [
            {
                "icon": "",
                "text": "<strong>Nifty 50 closes at all-time high of 27,350</strong> — "
                        "Broad-based rally led by banking and IT heavyweights. "
                        "FII inflows surge ₹4,200 Cr in the last week.",
            },
            {
                "icon": "",
                "text": "<strong>SBI revises FD rates upward by 25 bps</strong> — "
                        "1-year deposits now earn 7.10% p.a. Senior citizen "
                        "rates revised to 7.60%. Effective from April 15, 2026.",
            },
            {
                "icon": "",
                "text": "<strong>Small-cap mutual funds see record SIP inflows</strong> — "
                        "₹3,800 Cr poured into small-cap funds in March 2026. "
                        "SEBI cautions investors to assess risk carefully.",
            },
            {
                "icon": "",
                "text": "<strong>RBI holds repo rate at 6.25%</strong> — "
                        "MPC unanimously decides to maintain rates amid "
                        "global uncertainty. Inflation stays within target band.",
            },
        ]
        for hl in headlines:
            st.markdown(
                f'<div class="headline-card">'
                f'{hl["text"]}</div>',
                unsafe_allow_html=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — THE GURU  (AI Financial Analyst)
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "The Guru — AI Analyst":

    st.markdown('<p class="section-header">The Guru</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-subtitle">Data-driven insights. No fluff, only actions.</p>',
        unsafe_allow_html=True,
    )

    # ── Insight generator ─────────────────────────────────────────────────────
    def generate_insights(exp_df: pd.DataFrame, port_df: pd.DataFrame) -> list[dict]:
        """
        Analyse expense + portfolio data and produce actionable financial insights.
        Returns a list of dicts with keys: icon, style, title, body.
        """
        insights: list[dict] = []

        # ─ Insight 1: Top merchant spend ──────────────────────────────────────
        merchant_spend = exp_df.groupby("Merchant")["Amount (₹)"].sum()
        top_merchant = merchant_spend.idxmax()
        top_merchant_amt = merchant_spend.max()

        # Estimate potential MF returns (12% CAGR over 5 years)
        redirect_pct = 0.20
        redirect_amt = top_merchant_amt * redirect_pct
        future_value = redirect_amt * ((1 + 0.12) ** 5)

        insights.append({
            "icon": "",
            "style": "insight-box",
            "title": "Shopping Pattern Detected",
            "body": (
                f"You've spent <strong>₹{top_merchant_amt:,.0f}</strong> on "
                f"<strong>{top_merchant}</strong> over the last 30 days. "
                f"Redirecting just 20% (₹{redirect_amt:,.0f}/month) into a "
                f"mutual fund with ~12% CAGR could grow to "
                f"<strong>₹{future_value:,.0f}</strong> in 5 years."
            ),
        })

        # ─ Insight 2: Food delivery overspend ────────────────────────────────
        food_spend = exp_df[exp_df["Category"] == "Food & Dining"]["Amount (₹)"].sum()
        daily_food_avg = food_spend / 30

        insights.append({
            "icon": "",
            "style": "insight-box-blue",
            "title": "Food Delivery Spend Alert",
            "body": (
                f"Your monthly food delivery spend is "
                f"<strong>₹{food_spend:,.0f}</strong> "
                f"(~₹{daily_food_avg:,.0f}/day). "
                f"Cooking at home 3 days a week could save you approximately "
                f"<strong>₹{daily_food_avg * 3 * 4:,.0f}</strong> per month — "
                f"that's enough to cover a Netflix + Spotify subscription and "
                f"still save."
            ),
        })

        # ─ Insight 3: Portfolio health ────────────────────────────────────────
        best_asset = port_df.loc[port_df["Returns (%)"].idxmax()]
        worst_asset = port_df.loc[port_df["Returns (%)"].idxmin()]

        insights.append({
            "icon": "",
            "style": "insight-box-green",
            "title": "Portfolio Health Check",
            "body": (
                f"Your best performer is <strong>{best_asset['Asset']}</strong> "
                f"at <strong>+{best_asset['Returns (%)']:.1f}%</strong>. "
                f"Your weakest holding — <strong>{worst_asset['Asset']}</strong> — "
                f"is at <strong>+{worst_asset['Returns (%)']:.1f}%</strong>. "
                f"Consider rebalancing: shift partial profits from the top "
                f"performer into a diversified index fund to lock gains and "
                f"reduce concentration risk."
            ),
        })

        # ─ Insight 4: Bill optimization ───────────────────────────────────────
        bills_spend = exp_df[exp_df["Category"] == "Bills & Utilities"]["Amount (₹)"].sum()
        transport_spend = exp_df[exp_df["Category"] == "Transport"]["Amount (₹)"].sum()

        insights.append({
            "icon": "",
            "style": "insight-box",
            "title": "Bills & Transport Optimisation",
            "body": (
                f"You've spent <strong>₹{bills_spend:,.0f}</strong> on bills and "
                f"<strong>₹{transport_spend:,.0f}</strong> on transport this month. "
                f"Switching to annual plans for OTT subscriptions and leveraging "
                f"UPI cashback offers on recharges could save 8—12% on recurring bills. "
                f"For transport, carpooling 2 days/week saves ~₹{transport_spend * 0.3:,.0f}."
            ),
        })

        # ─ Insight 5: Emergency fund check ────────────────────────────────────
        monthly_spend = exp_df["Amount (₹)"].sum()
        recommended_emergency = monthly_spend * 6

        insights.append({
            "icon": "",
            "style": "insight-box-blue",
            "title": "Emergency Fund Recommendation",
            "body": (
                f"With monthly expenses around <strong>₹{monthly_spend:,.0f}</strong>, "
                f"your ideal emergency fund should be at least "
                f"<strong>₹{recommended_emergency:,.0f}</strong> (6 months' cover). "
                f"Park this in a liquid fund or high-yield savings account for "
                f"instant access with better returns than a regular savings a/c."
            ),
        })

        return insights

    # ── Render insights ───────────────────────────────────────────────────────
    insights = generate_insights(expenses_df, portfolio_df)

    for insight in insights:
        st.markdown(
            f'<div class="{insight["style"]}">'
            f'<strong>{insight["title"]}</strong><br><br>'
            f'{insight["body"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Spending heatmap / category breakdown ─────────────────────────────────
    st.markdown("##### Expense Breakdown — Behind The Numbers")

    cat_summary = (
        expenses_df.groupby("Category")["Amount (₹)"]
        .agg(["sum", "count", "mean"])
        .reset_index()
    )
    cat_summary.columns = ["Category", "Total (₹)", "Transactions", "Avg per Txn (₹)"]
    cat_summary = cat_summary.sort_values("Total (₹)", ascending=False)
    cat_summary["Total (₹)"] = cat_summary["Total (₹)"].apply(lambda x: f"₹{x:,.0f}")
    cat_summary["Avg per Txn (₹)"] = cat_summary["Avg per Txn (₹)"].apply(lambda x: f"₹{x:,.0f}")

    st.dataframe(cat_summary, use_container_width=True, hide_index=True)

    # ── Merchant-level bar chart ──────────────────────────────────────────────
    st.markdown("##### Top 10 Merchants by Spend")
    merchant_agg = (
        expenses_df.groupby("Merchant")["Amount (₹)"]
        .sum()
        .reset_index()
        .sort_values("Amount (₹)", ascending=True)
        .tail(10)
    )
    fig_merchant = px.bar(
        merchant_agg,
        x="Amount (₹)",
        y="Merchant",
        orientation="h",
        color_discrete_sequence=["#2563EB"],
    )
    fig_merchant.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="₹"),
        yaxis=dict(showgrid=False, title=""),
        font=dict(family="Inter", color="#334155"),
        height=380,
    )
    fig_merchant.update_traces(
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        marker_cornerradius=6,
    )
    st.plotly_chart(fig_merchant, use_container_width=True)


# ─── Global footer ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    "Hisaab Kitaab v1.0 — A personal finance demo dashboard. "
    "Data shown is simulated and for demonstration purposes only."
    "</div>",
    unsafe_allow_html=True,
)
