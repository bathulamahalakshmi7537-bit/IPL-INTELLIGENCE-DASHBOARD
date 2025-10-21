import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
import importlib.util

# Set page configuration
st.set_page_config(
    page_title="IPL Fantasy Intelligence Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data function
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("ipl_data.csv")
        if 'season' in data.columns:
            data['season'] = data['season'].astype(str)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Function to load a page module
def load_page_module(page_name):
    # Construct the path to the page file
    page_path = os.path.join("pages", f"{page_name}.py")
    
    # Check if the file exists
    if not os.path.exists(page_path):
        st.error(f"Page file not found: {page_path}")
        return None
    
    # Load the module
    spec = importlib.util.spec_from_file_location(page_name, page_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", [
    "Home", 
    "Executive Overview",
    "Match Analysis", 
    "Player Performance Hub",
    "Team Analytics", 
    "Fantasy Strategy Lab",
    "About Us"
])

# Load data
data = load_data()

# Display the selected page
if selection == "Home":
    page_module = load_page_module("1_Home")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "Executive Overview":
    page_module = load_page_module("2_Executive_Overview")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "Match Analysis":
    page_module = load_page_module("3_Match_Analysis")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "Player Performance Hub":
    page_module = load_page_module("4_Player_Performance_Hub")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "Team Analytics":
    page_module = load_page_module("5_Team_Analytics")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "Fantasy Strategy Lab":
    page_module = load_page_module("6_Fantasy_Strategy_Lab")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)
elif selection == "About Us":
    page_module = load_page_module("7_About_Us")
    if page_module and hasattr(page_module, 'show'):
        page_module.show(data)