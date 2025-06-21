import streamlit as st
from datetime import datetime
import random

def render_milestones(milestones_col):
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
            <div class="tile">
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
