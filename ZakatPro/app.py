import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# --- Configuration ---
st.set_page_config(
    page_title="🌙 Smart Zakat Pro",
    page_icon="🕌",
    layout="wide",
    
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding and menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Custom CSS with professional color scheme
st.markdown("""
<style>
    :root {
        --primary-color:rgba(255, 255, 255, 0.76)
        --secondary-color: #D4AF37;
        --background-color: #F8F5E4;
        --sidebar-color:rgb(240, 240, 240);
        --card-color:rgb(255, 255, 255);
    }
    
    body {
        background-color: var(--background-color);
    }
    
    .stApp {

        background-size: cover;
        background-blend-mode: multiply;
        background-color: rgba(230, 236, 203, 0.97);
    }
    
    .stSidebar {
        background-color: var(--sidebar-color) !important;
        box-shadow: 2px 0 8px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        color: var(--primary-color);
        font-family: 'Arial', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        color: #555555;
    }
    
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        font-weight: 600;
        border-bottom: 3px solid var(--primary-color);
    }
    
    .article-card {
        border-radius: 12px;
        padding: 1.5rem;
        background: var(--card-color);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
        border: 1px solid #eeeeee;
    }
    
    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    .rate-card {
        padding: 2rem;
        background: var(--card-color);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #eeeeee;
    }
    
    .st-expander {
        background: var(--card-color) !important;
        border-radius: 12px !important;
        border: 1px solid #eeeeee !important;
    }
    
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
    }
    
    .stNumberInput input {
        border-radius: 8px !important;
    }
    
    h1 {
        color: var(--primary-color) !important;
        font-size: 2.8rem !important;
        margin-bottom: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #FFD700;
        --accent-color: #6A1B9A;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        font-weight: bold;
    }
    
    .article-card {
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        background: white;
        margin-bottom: 1rem;
    }
    
    .article-card:hover {
        transform: translateY(-3px);
    }
    
    .rate-card {
        padding: 1.5rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Data Fetching ---
def fetch_rates():
    """Get current gold/silver rates with fallback"""
    try:
        gold_api = "https://www.goldapi.io/api/XAU/PKR"
        headers = {"x-access-token": "goldapi-6kta7ju6t1r1u32-io"}
        gold_tola = requests.get(gold_api, headers=headers).json()['price'] / 31.1 * 11.664
        silver_tola = gold_tola * 0.0085
        return {
            'gold_tola': int(gold_tola),
            'gold_gram': int(gold_tola / 11.664),
            'silver_tola': int(silver_tola),
            'silver_gram': int(silver_tola / 11.664)
        }
    except:
        return {
            'gold_tola': 321500,
            'gold_gram': 27575,
            'silver_tola': 2700,
            'silver_gram': 231
        }

def get_historical_data():
    """Generate historical data"""
    dates = pd.date_range(end=datetime.today(), periods=30)
    return pd.DataFrame({
        'Date': dates,
        'Gold': [321500 + np.random.randint(-2000, 2000) for _ in range(30)],
        'Silver': [2700 + np.random.randint(-100, 100) for _ in range(30)]
    })

# --- Calculations ---
def calculate_zakat(assets, nisab_basis, gold_rate, silver_rate):
    """Calculate zakat obligations"""
    nisab = (7.5 * gold_rate) if nisab_basis == "Gold" else (52.5 * silver_rate)
    total_wealth = sum(assets.values())
    zakat = total_wealth * 0.025 if total_wealth >= nisab else 0
    return zakat, total_wealth, nisab

# --- UI Components ---
def wealth_inputs():
    """Asset input form"""
    with st.expander("➕ Add Assets", expanded=True):
        c1, c2 = st.columns(2)
        return {
            'Gold (Tola)': c1.number_input("Gold (Tola)", 0.0, 100.0, 5.0),
            'Silver (Tola)': c1.number_input("Silver (Tola)", 0.0, 1000.0, 50.0),
            'Cash (PKR)': c2.number_input("Cash Savings", 0, 10000000, 50000),
            'Investments (PKR)': c2.number_input("Investments", 0, 10000000, 100000)
        }

def display_rates(rates):
    """Styled rate display"""
    st.markdown(f"""
    <div class="rate-card">
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div>
                <h4 style="color: #2E7D32; margin: 0 0 1rem 0;">🪙 Gold Rates</h4>
                <p style="margin: 0;">
                    {rates['gold_tola']:,} PKR/tola<br>
                    <small>({rates['gold_gram']:,} PKR/g)</small>
                </p>
            </div>
            <div>
                <h4 style="color: #2E7D32; margin: 0 0 1rem 0;">🥈 Silver Rates</h4>
                <p style="margin: 0;">
                    {rates['silver_tola']:,} PKR/tola<br>
                    <small>({rates['silver_gram']:,} PKR/g)</small>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def islamic_finance_section():
    """Educational content with articles"""
    st.subheader("📚 Islamic Finance Resources")
    
    with st.expander("📜 Essential Zakat Guidelines", expanded=True):
        st.markdown("""
        ### Core Principles
        - **Nisab Threshold**: Minimum wealth requiring Zakat
        - **Gold Standard**: 7.5 Tola (87.48 grams)
        - **Silver Standard**: 52.5 Tola (612.36 grams)
        - **Payment Rate**: 2.5% of total eligible wealth
        """)
    
    with st.expander("📖 Educational Articles", expanded=True):
        articles = [
            {
                "title": "Modern Zakat Management",
                "image": "https://images.pexels.com/photos/31330436/pexels-photo-31330436/free-photo-of-euro-coins-spilled-from-rustic-mug.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "link": "https://modernzakat.com/"
            },
            {
                "title": "Islamic Wealth Principles",
                "image": "https://images.pexels.com/photos/15979752/pexels-photo-15979752/free-photo-of-the-spiritual-journey-of-a-young-boy-during-ramadan.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "link": "https://www.pakistangulfeconomist.com/2025/03/24/wealth-in-islam-a-trust-not-just-a-treasure/"
            },
            {
                "title": "Dignity, Duty, and Respect",
                "image": "https://images.pexels.com/photos/20475945/pexels-photo-20475945/free-photo-of-people-on-dinner-during-ramadan.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "link": "https://www.dawn.com/news/1899367"
            }
        ]
        
        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                article = articles[i]
                st.markdown(f"""
                <div class="article-card">
                    <img src="{article['image']}" style="width:100%; height:150px; object-fit:cover; border-radius:8px;">
                    <h4 style="color:#2E7D32; margin:1rem 0 0.5rem 0;">{article['title']}</h4>
                    <a href="{article['link']}" target="_blank">
                        <button style="background:#2E7D32; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; width:100%;">
                            Read Article →
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
    
    with st.expander("🕌 Verified Charity Partners", expanded=True):
        st.markdown("""
        - **Edhi Foundation**: [https://edhi.org](https://edhi.org)
        - **Saylani Welfare**: [https://saylaniwelfare.com](https://saylaniwelfare.com)
        - **Al-Khidmat**: [https://al-khidmatfoundation.org](https://al-khidmatfoundation.org)
        - **Islamic Relief**: [https://islamic-relief.org](https://islamic-relief.org)
        """)

# --- Main App ---
def main():
    st.title("🕌 ZakatFlow: Smart Islamic Wealth Manager")
    st.markdown("---")
    
    rates = fetch_rates()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("🔄 Refresh Market Data"):
            st.cache_data.clear()
        
        st.markdown("---")
        st.header("💰 Asset Inputs")
        assets = wealth_inputs()
        nisab_basis = st.radio("Nisab Basis", ["Gold", "Silver"])
        display_rates(rates)
    
    # Calculations
    calculated_assets = {
        k: (v * rates['gold_tola'] if "Gold" in k else 
            v * rates['silver_tola'] if "Silver" in k else v)
        for k, v in assets.items()
    }
    zakat, total_wealth, nisab = calculate_zakat(
        calculated_assets,
        nisab_basis,
        rates['gold_tola'],
        rates['silver_tola']
    )
    
    # Main Interface
    tab1, tab2, tab3 = st.tabs(["💰 Zakat Calculator", "📈 Wealth Analysis", "📚 Islamic Finance"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Wealth", f"PKR {total_wealth:,.0f}")
        with col2:
            st.metric("Nisab Threshold", f"PKR {nisab:,.0f} ({nisab_basis})")
        with col3:
            st.metric("Zakat Payable", f"PKR {zakat:,.0f}" if zakat > 0 else "Not Applicable")
        
        st.markdown("---")
        
        # Wealth Composition
        wealth_values = [
            assets["Gold (Tola)"] * rates['gold_tola'],
            assets["Silver (Tola)"] * rates['silver_tola'],
            assets["Cash (PKR)"],
            assets["Investments (PKR)"]
        ]
        fig = px.pie(names=list(assets.keys()), values=wealth_values, 
                    title="Wealth Composition",
                    color_discrete_sequence=['#2E7D32', '#FFD700', '#6A1B9A', '#C0C0C0'],
                    hole=0.4)
        fig.update_layout(plot_bgcolor='rgba(182, 179, 179, 0.93)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#2E7D32'))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market Trends
        hist_data = get_historical_data()
        fig = px.line(hist_data, x='Date', y=['Gold', 'Silver'], 
                     title="30-Day Market Trends",
                     labels={'value': 'PKR per Tola'},
                     color_discrete_sequence=['#FFD700', '#C0C0C0'])
        st.plotly_chart(fig, use_container_width=True)
        fig.update_layout( plot_bgcolor='#FFFBE6',paper_bgcolor='#FFFBE6', xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    
    with tab2:
        main_col1, main_col2 = st.columns([3, 2])
        
        with main_col1:
            st.subheader("💹 Investment Growth")
            years = st.slider("Investment Years", 1, 10, 1, key="invest_years")
            principal = st.number_input("Principal Amount (PKR)", 10000, 100000000, 10000, key="principal")
            rate = st.slider("Annual Return (%)", 1, 20, 2, key="rate")
            future_value = principal * (1 + rate/100) ** years
            st.metric("Future Value", f"PKR {future_value:,.0f}")

            # Generate growth data
            years_range = list(range(1, years + 1))
            growth_values = [principal * (1 + rate/100)**y for y in years_range]
            growth_data = pd.DataFrame({'Year': years_range, 'Value': growth_values})

            # First row of charts
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                fig = px.line(growth_data, x='Year', y='Value',
                            title='📈 Growth Trajectory',
                            labels={'Value': 'Amount (PKR)'},
                            height=350,
                            color_discrete_sequence=['#2E7D32'])
                fig.update_layout(showlegend=False, margin=dict(t=30))
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#2E7D32'),xaxis=dict(showgrid=False),yaxis=dict(showgrid=False)
)

            with row1_col2:
                growth_data['Growth'] = growth_data['Value'].diff().fillna(growth_data['Value'].iloc[0] - principal)
                fig = px.bar(growth_data, x='Year', y='Growth',
                            title='📊 Annual Growth Breakdown',
                            labels={'Growth': 'Yearly Gain (PKR)'},
                            color='Growth',
                            height=350, width=600,
                            color_continuous_scale='Greens')
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)


            # Second row of charts
            row2_col1, row2_col2 = st.columns(2)
            with row2_col1:
     
                interest = max(future_value - principal, 0)
                fig = px.pie(names=['Principal', 'Interest'],
                            values=[principal, interest],
                            title='🧮 Investment Composition',
                            color_discrete_sequence=['#2E7D32', '#FFD700'],
                            height=350, width=600)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

        with main_col2:
            st.subheader("📅 Savings Planner")
            monthly = st.number_input("Monthly Savings (PKR)", 0, 100000, 5000, key="monthly")
            savings_years = st.slider("Savings Period", 1, 30, 5, key="savings_years")
            total = monthly * 12 * savings_years
            st.metric("Total Savings", f"PKR {total:,.0f}")

            # Savings visualization
            savings_data = pd.DataFrame({
                'Year': list(range(1, savings_years + 1)),
                'Savings': [monthly * 12 * y for y in range(1, savings_years + 1)]
            })
            fig = px.area(savings_data, x='Year', y='Savings',
                        title='💹 Cumulative Savings Progress',
                        labels={'Savings': 'Total Saved (PKR)'},
                        height=500, width=600,
                        color_discrete_sequence=['#6A1B9A'])
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        islamic_finance_section()

if __name__ == "__main__":
    main()