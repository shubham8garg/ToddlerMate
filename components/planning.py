import streamlit as st
import random

def render_planning(planning_col):
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
            <div class="tile">
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
