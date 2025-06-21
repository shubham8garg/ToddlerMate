import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Import components
from components.songs_rhymes import render_songs_rhymes
from components.activities import render_activities
from components.planning import render_planning
from components.milestones import render_milestones
from components.places import render_places
from components.purchases import render_purchases # Import the new component

# Set page styling for better visibility
st.set_page_config(
    page_title="ToddlerMate",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visibility (will be updated in a later step)
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem; /* Slightly reduced top padding */
        padding-bottom: 1.5rem;
    }
    h1 {
        color: #333333; /* Darker color for main page title */
        text-align: center; /* Center main title */
    }
    h2 {
        color: #4A4A4A; /* Slightly lighter for section headers */
    }
    h3 {
        color: #FFFFFF; /* White text for tile headers */
    }
    /* General button styling - can be overridden by specific classes if needed */
    .stButton button {
        background-color: #6A5ACD; /* Dull purple */
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    .stButton button:hover {
        background-color: #5A4BAD; /* Darker purple on hover */
    }
    .tile {
        background-color: #6A5ACD; /* Dull purple background */
        color: #FFFFFF; /* White text */
        border-radius: 8px; /* More rounded corners */
        padding: 10px; /* Reduced padding for smaller tiles */
        margin: 5px;   /* Margin between tiles */
        border: 1px solid #5A4BAD; /* Slightly darker border */
        word-wrap: break-word; /* Ensure long words break */
        height: 50px; /* Fixed height for tiles - adjust as needed */
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Pushes content and links apart */
    }
    .tile h3 {
        font-size: 1.1em; /* Smaller heading for tiles */
        margin-top: 0;
        margin-bottom: 5px;
    }
    .tile p {
        font-size: 0.9em; /* Smaller paragraph text */
        margin-bottom: 5px;
    }
    .tile a {
        color: #E0E0E0; /* Lighter link color for contrast on purple */
        text-decoration: underline;
    }
    .tile a:hover {
        color: #FFFFFF; /* White link on hover */
    }

    /* Styling for form submit buttons specifically if needed to differentiate */
    div[data-testid="stForm"] .stButton button {
        background-color: #4CAF50; /* Green for submit buttons in forms */
        color: white;
    }
    div[data-testid="stForm"] .stButton button:hover {
        background-color: #45A049; /* Darker green on hover */
    }

</style>
""", unsafe_allow_html=True)

# MongoDB setup (replace with your actual connection string)
MONGO_URI = "mongodb+srv://shubham8garg:05TxCvTyeXKAnkX1@cluster0.hajrzms.mongodb.net/toddlermate?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["toddlermate"]

# Collections
songs_col = db["songs"]
activities_col = db["activities"]
planning_col = db["planning"]
milestones_col = db["milestones"]
places_col = db["places"]
purchases_col = db["purchases"] # Add new collection


# Sidebar Navigation
tabs = ["Songs & Rhymes", "Activities", "Planning", "Milestones", "Place to Go", "To Purchase"] # Add new tab
choice = st.sidebar.radio("Go to", tabs)

# Main content rendering based on choice
if choice == "Songs & Rhymes":
    render_songs_rhymes(songs_col)
elif choice == "Activities":
    render_activities(activities_col)
elif choice == "Planning":
    render_planning(planning_col)
elif choice == "Milestones":
    render_milestones(milestones_col)
elif choice == "Place to Go":
    render_places(places_col)
elif choice == "To Purchase": # Add new tab rendering
    render_purchases(purchases_col)
