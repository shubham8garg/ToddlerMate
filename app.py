import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import random

# Set page styling for better visibility
st.set_page_config(
    page_title="ToddlerMate",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visibility
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #4527A0;
    }
    .stButton button {
        background-color: #7E57C2;
        color: white;
        font-weight: bold;
    }
    .tile {
        background-color: #FFE9F3;
        border-radius: 2px;
        padding: 3px;
        margin: 1px;
        border: 1px solid #B39DDB;
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

# Sidebar Navigation
tabs = ["Songs & Rhymes", "Activities", "Planning", "Milestones"]
choice = st.sidebar.radio("Go to", tabs)

# Tab 1: Songs & Rhymes
if choice == "Songs & Rhymes":
    st.header("🎵 Songs & Rhymes")
    
    # Random shuffler and select one button at the top
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Shuffle and Select Random Rhyme"):
            rhymes_list = list(songs_col.find())
            if rhymes_list:
                random_rhyme = random.choice(rhymes_list)
                st.session_state['selected_rhyme'] = random_rhyme
    
    # Display selected rhyme if exists
    if 'selected_rhyme' in st.session_state:
        st.markdown("### 🌟 Selected Rhyme")
        with st.container():
            st.markdown(f"""
            <div class="tile" style="background-color: #FFE9F3;">
                <h4>{st.session_state['selected_rhyme']['title']}</h4>
                <p>{st.session_state['selected_rhyme'].get('lyrics', '')}</p>
                {f'<a href="{st.session_state["selected_rhyme"]["url"]}" target="_blank">Watch Video</a>' if st.session_state['selected_rhyme'].get('url') else ''}
            </div>
            """, unsafe_allow_html=True)
    
    # Display all rhymes in tile format
    st.subheader("Your Rhymes")
    rhymes = list(songs_col.find())
    if not rhymes:
        st.info("No rhymes added yet. Add your first rhyme below!")
    else:
        # Create rows with 3 tiles each
        for i in range(0, len(rhymes), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(rhymes):
                    with cols[j]:
                        rhyme = rhymes[i + j]
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{rhyme['title']}</h3>
                            <p>{rhyme.get('lyrics', '')}</p>
                            {f'<a href="{rhyme["url"]}" target="_blank">Watch Video</a>' if rhyme.get('url') else ''}
                        </div>
                        """, unsafe_allow_html=True)
    
    # Form at the bottom
    st.markdown("---")
    st.subheader("Add a New Rhyme")
    with st.form("add_rhyme"):
        title = st.text_input("Title")
        url = st.text_input("YouTube Link (Optional)")
        if st.form_submit_button("Add"):
            songs_col.insert_one({"title": title, "url": url})
            st.success("Rhyme added!")
            st.rerun()

# Tab 2: Activities
elif choice == "Activities":
    st.header("🏃 Activities")
    
    # Random shuffler and select one button at the top
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Shuffle and Select Random Activity"):
            activities_list = list(activities_col.find())
            if activities_list:
                random_activity = random.choice(activities_list)
                st.session_state['selected_activity'] = random_activity
    
    # Display selected activity if exists
    if 'selected_activity' in st.session_state:
        st.markdown("### 🌟 Selected Activity")
        with st.container():
            st.markdown(f"""
            <div class="tile" style="background-color: #D1C4E9;">
                <h3>{st.session_state['selected_activity']['name']} ({st.session_state['selected_activity']['category']})</h3>
                <p>{st.session_state['selected_activity']['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display all activities in tile format
    st.subheader("Your Activities")
    activities = list(activities_col.find())
    if not activities:
        st.info("No activities added yet. Add your first activity below!")
    else:
        # Create rows with 3 tiles each
        for i in range(0, len(activities), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(activities):
                    with cols[j]:
                        activity = activities[i + j]
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{activity['name']} ({activity['category']})</h3>
                            <p>{activity['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Form at the bottom
    st.markdown("---")
    st.subheader("Add a New Activity")
    with st.form("add_activity"):
        name = st.text_input("Activity Name")
        description = st.text_area("Description")
        category = st.selectbox("Category", ["Indoor", "Outdoor", "Creative", "Other"])
        if st.form_submit_button("Add"):
            activities_col.insert_one({"name": name, "description": description, "category": category})
            st.success("Activity added!")
            st.rerun()

# Tab 3: Planning
elif choice == "Planning":
    st.header("📅 Planning")
    
    # Random shuffler and select one button at the top
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Shuffle and Select Random Plan"):
            plans_list = list(planning_col.find())
            if plans_list:
                random_plan = random.choice(plans_list)
                st.session_state['selected_plan'] = random_plan
    
    # Display selected plan if exists
    if 'selected_plan' in st.session_state:
        st.markdown("### 🌟 Selected Plan")
        with st.container():
            st.markdown(f"""
            <div class="tile" style="background-color: #D1C4E9;">
                <h3>{st.session_state['selected_plan']['task']} - {st.session_state['selected_plan']['date']}</h3>
                <p>{st.session_state['selected_plan']['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display all plans in tile format
    st.subheader("Upcoming Plans")
    plans = list(planning_col.find().sort("date"))
    if not plans:
        st.info("No plans added yet. Add your first plan below!")
    else:
        # Create rows with 3 tiles each
        for i in range(0, len(plans), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(plans):
                    with cols[j]:
                        plan = plans[i + j]
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{plan['task']} - {plan['date']}</h3>
                            <p>{plan['notes']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Form at the bottom
    st.markdown("---")
    st.subheader("Add a Plan")
    with st.form("add_plan"):
        task = st.text_input("Plan Name")
        date = st.date_input("Date")
        notes = st.text_area("Notes")
        if st.form_submit_button("Add"):
            planning_col.insert_one({"task": task, "date": str(date), "notes": notes})
            st.success("Plan added!")
            st.rerun()

# Tab 4: Milestones
elif choice == "Milestones":
    st.header("🎯 Milestones")
    
    # Random shuffler and select one button at the top
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Shuffle and Select Random Milestone"):
            milestones_list = list(milestones_col.find())
            if milestones_list:
                random_milestone = random.choice(milestones_list)
                st.session_state['selected_milestone'] = random_milestone
    
    # Display selected milestone if exists
    if 'selected_milestone' in st.session_state:
        st.markdown("### 🌟 Selected Milestone")
        with st.container():
            st.markdown(f"""
            <div class="tile" style="background-color: #D1C4E9;">
                <h3>{st.session_state['selected_milestone']['goal']} ({st.session_state['selected_milestone']['status']})</h3>
                <p>{st.session_state['selected_milestone']['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display all milestones in tile format
    st.subheader("All Milestones")
    milestones = list(milestones_col.find())
    if not milestones:
        st.info("No milestones added yet. Add your first milestone below!")
    else:
        # Create rows with 3 tiles each
        for i in range(0, len(milestones), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(milestones):
                    with cols[j]:
                        m = milestones[i + j]
                        status_color = "#4CAF50" if m['status'] == "Completed" else "#FFC107" if m['status'] == "In Progress" else "#9E9E9E"
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{m['goal']}</h3>
                            <p style="color: {status_color}; font-weight: bold;">{m['status']}</p>
                            <p>{m['notes']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Form at the bottom
    st.markdown("---")
    st.subheader("Track Development")
    with st.form("add_milestone"):
        goal = st.text_input("Milestone Description")
        status = st.selectbox("Status", ["To Do", "In Progress", "Completed"])
        notes = st.text_area("Notes")
        if st.form_submit_button("Add"):
            milestones_col.insert_one({
                "goal": goal, "status": status, "notes": notes, "added": datetime.now()
            })
            st.success("Milestone added!")
            st.rerun()
