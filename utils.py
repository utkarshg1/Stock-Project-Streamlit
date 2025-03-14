# Load the libraries
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

class StockAPI:

    def __init__(self):
        self.api_key = st.secrets["API_KEY"]
        # Get the url
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        # Show the headers
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    def symbol_search(self, company: str) -> dict:
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["bestMatches"]
        symbols = {}
        for i in data:
            s = i["1. symbol"]
            symbols[s] = [i["2. name"], i["4. region"], i["8. currency"]]
        # Return the symbols dictionary
        return symbols

    def get_daily_data(self, symbol: str) -> pd.DataFrame:
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(self.url, headers= self.headers, params=querystring)
        data = response.json()["Time Series (Daily)"]
        # Convert into dataframe
        df = pd.DataFrame(data).T
        # Convert datatypes to float
        df = df.astype(float)
        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        # Provide a name to index
        df.index.name = "Date"
        return df
    
    def candlestick_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = go.Figure(data = [
            go.Candlestick(
                x = df.index,
                open= df["1. open"],
                high= df["2. high"],
                low = df["3. low"],
                close= df["4. close"]
            )
        ])
        fig.update_layout(width = 1200, height = 800)
        return fig