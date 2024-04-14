import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = 'https://api.coingecko.com/api/v3/coins'
currency = 'usd'

def fetch_data(coin_name):
    url = f"{BASE_URL}/{coin_name}/market_chart"
    params = {
            'vs_currency': currency,
            'days': 365
        }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for any HTTP error
        data = response.json()
        prices = data['prices']
        timestamps = [entry[0] for entry in prices]
        prices = [entry[1] for entry in prices]
        df = pd.DataFrame({'Timestamp': timestamps, 'Price (USD)': prices})
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def plot_data(df):
    fig, ax = plt.subplots()
    ax.plot(df['Timestamp'], df['Price (USD)'], color='blue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.set_title('Price Over Last Year')
    st.pyplot(fig)

# Main function
def main():
    st.title('Cryptocurrency Price Visualizer')
    st.sidebar.title('Stock Details App')
    coin_name = st.sidebar.text_input('Enter cryptocurrency name (e.g., bitcoin):').lower()
    
    if coin_name:
        data = fetch_data(coin_name)
        if data is not None:
            st.subheader(f'Price Trend of {coin_name.capitalize()} Over Last Year')
            plot_data(data)

            max_price = data['Price (USD)'].max()
            min_price = data['Price (USD)'].min()
            st.write(f"Maximum Price: ${max_price:.2f}")
            st.write(f"Minimum Price: ${min_price:.2f}")

            max_day = data.loc[data['Price (USD)'].idxmax(), 'Timestamp']
            min_day = data.loc[data['Price (USD)'].idxmin(), 'Timestamp']
            st.write(f"Day with Maximum Price: {max_day.strftime('%Y-%m-%d')}")
            st.write(f"Day with Minimum Price: {min_day.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
