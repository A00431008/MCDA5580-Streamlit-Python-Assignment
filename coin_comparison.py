import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define Base URL and currency
BASE_URL = 'https://api.coingecko.com/api/v3/coins'
currency = 'usd'

# Function to Fetch Data
@st.cache_data
def fetch_data(coin_name, days):
    url = f"{BASE_URL}/{coin_name}/market_chart"
    # Set Parameters
    params = {
            'vs_currency': currency,
            'days': days
        }
    
    try:
        # make a request and fetch data as response
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for any HTTP error
        data = response.json() # set data as json
        prices = data['prices'] # obtain prices from the data 
        timestamps = [entry[0] for entry in prices] #extract timestamps from prices
        prices = [entry[1] for entry in prices] #keep only prices in prices

        # Now form dataframe and return it
        df = pd.DataFrame({'Timestamp': timestamps, f'Price (USD) - {coin_name.capitalize()}': prices})
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        return df
    
    except requests.exceptions.RequestException as e:
        # Throw error if errors in fetching or processing data
        st.error(f"Error fetching data: {e}")
        return None

def plot_data(df1, df2, coin1_name, coin2_name):
    # Plot data for 2 coins in a single plot
    fig, ax = plt.subplots()
    ax.plot(df1['Timestamp'], df1[f'Price (USD) - {coin1_name.capitalize()}'], color='blue', label=coin1_name.capitalize())
    ax.plot(df2['Timestamp'], df2[f'Price (USD) - {coin2_name.capitalize()}'], color='red', label=coin2_name.capitalize())
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.set_title('Price Comparison')
    ax.legend()
    # display plot in streamlit app
    st.pyplot(fig)

# Main function
def main():

    st.title('Coin Comparison App')
    st.sidebar.title('Coin Comparison')
    
    # Get user Inputs
    coin1_name = st.sidebar.text_input('Enter first cryptocurrency name (e.g., bitcoin):').lower()
    coin2_name = st.sidebar.text_input('Enter second cryptocurrency name (e.g., ethereum):').lower()
    days = st.sidebar.selectbox('Select time frame:', ['1 Week', '1 Month', '3 Months', '6 Months', '1 Year'])

    # Set days according to user inputs
    if days == '1 Week':
        days = 7
    elif days == '1 Month':
        days = 30
    elif days == '3 Months':
        days = 90
    elif days == '6 Months':
        days = 180
    elif days == '1 Year':
        days = 365

    # fetch the 2 data for 2 coins and plot the data 
    if coin1_name and coin2_name:
        try:
            data1 = fetch_data(coin1_name, days)
            data2 = fetch_data(coin2_name, days)

            if data1 is not None and data2 is not None:
                st.subheader(f'Price Comparison of {coin1_name.capitalize()} and {coin2_name.capitalize()}')
                plot_data(data1, data2, coin1_name, coin2_name)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
