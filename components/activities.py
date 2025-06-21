import streamlit as st
import random

def render_activities(activities_col):
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
            <div class="tile">
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
