# Load the required modules
import streamlit as st
from utils import StockAPI

# Intitialize streamlit app
st.set_page_config(page_title="Stock Market Project", layout="wide")

# Intialize stock client
client = StockAPI()

# Show the title of project 
st.title("Stock Market Web application")
st.subheader("By Utkarsh Gaikwad")

# Get the company name as input from user
company = st.text_input("Please enter company name : ")

# If company name is provided
if company:
    # Search for symbols of given company
    search = client.symbol_search(company)
    symbols = search.keys()

    # Create a dropdown to show company symbol and information
    option = st.selectbox("Choose stock symbol", options=symbols)
    
    # Display information of the company
    st.success(f"Company name : {search[option][0]}")
    st.success(f"Region : {search[option][1]}")
    st.success(f"Currency : {search[option][2]}")

    # Create a submit button to display stock prices
    button = st.button("submit", type="primary")

    # After clicking submit button the app should show the plotly chart
    if button:
        with st.spinner():
            df = client.get_daily_data(option)
            fig = client.candlestick_chart(df)
            st.plotly_chart(fig)
