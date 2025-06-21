import streamlit as st
import random

def render_songs_rhymes(songs_col):
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
            <div class="tile">
                <h3>{st.session_state['selected_rhyme']['title']}</h3>
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
        lyrics = st.text_area("Lyrics (Optional)") # Added lyrics input
        if st.form_submit_button("Add"):
            songs_col.insert_one({"title": title, "url": url, "lyrics": lyrics})
            st.success("Rhyme added!")
            st.rerun()
