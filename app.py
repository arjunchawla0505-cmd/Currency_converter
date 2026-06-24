import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="Global Currency Converter",
    page_icon="💱",
    layout="centered"
)

# 2. API Fetching Function
@st.cache_data(ttl=3600)  # Cache data for 1 hour to optimize performance
def get_exchange_rates(base_currency):
    # Using the free, no-auth-required ExchangeRate-API pair endpoint fallback
    # For a full list, we use their standard free API
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["result"] == "success":
            return data["rates"]
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# 3. App Header
st.title("💱 Global Currency Converter")
st.markdown("A real-time currency conversion tool powered by live exchange rates.")
st.write("---")

# 4. Sidebar / Controls
st.sidebar.header("Settings")
available_currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR"]

base_curr = st.sidebar.selectbox("From (Base Currency)", available_currencies, index=0)
target_curr = st.sidebar.selectbox("To (Target Currency)", available_currencies, index=1)

# Fetch rates based on selection
rates = get_exchange_rates(base_curr)

if rates:
    # 5. Main UI Layout
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount to Convert", min_value=0.0, value=1.0, step=1.0)
    
    with col2:
        # Calculate conversion
        conversion_rate = rates.get(target_curr, 1.0)
        converted_amount = amount * conversion_rate
        
        # Display read-only result
        st.number_input("Converted Amount", value=converted_amount, disabled=True)
    
    # 6. Metrics and Visual Display
    st.write("---")
    st.subheader("Exchange Rate Summary")
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label=f"1 {base_curr} to {target_curr}", value=f"{conversion_rate:.4f}")
    m_col2.metric(label="Last Updated (UTC)", value="Just now")

    # Quick comparison table for popular pairs
    st.subheader(f"Popular Conversions for 1 {base_curr}")
    quick_rates = {k: v for k, v in rates.items() if k in available_currencies and k != base_curr}
    st.dataframe(quick_rates, column_config={"value": "Rate"}, use_container_width=True)

else:
    st.error("Failed to load currency rates. Please try again later.")