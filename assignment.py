import streamlit as st
from stock_details import main as stock_details_main
from coin_comparison import main as coin_comparison_main
from number_classifier import main as number_classifier_main

# Create a dictionary to store the app names and their corresponding functions
apps = {
    "Stock Details App": stock_details_main,
    "Coin Comparison App": coin_comparison_main,
    "Number Classifier App": number_classifier_main
}

# sidebar - app TITLE display
st.sidebar.title('Upload Image')

# Add a dropdown menu to select the app to run
app_selection = st.sidebar.selectbox("Select App", list(apps.keys()))

# Run the selected app
apps[app_selection]()