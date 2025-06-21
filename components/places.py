import streamlit as st
# from geopy.geocoders import Nominatim # Will be needed for actual distance calculation
# from geopy.distance import geodesic # Will be needed for actual distance calculation

def render_places(places_col):
    st.header("📍 Place to Go")

    # Display all places in tile format
    st.subheader("Your Places")
    places = list(places_col.find())
    if not places:
        st.info("No places added yet. Add your first place below!")
    else:
        # Create rows with 2 tiles each (can be adjusted)
        for i in range(0, len(places), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(places):
                    with cols[j]:
                        place = places[i + j]
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{place['name']} ({place['type']})</h3>
                            <p><a href="{place['map_link']}" target="_blank">View on Google Maps</a></p>
                            <p>Distance: {place.get('distance_km', 'N/A')} km from 02169</p>
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Add a New Place")
    with st.form("add_place"):
        name = st.text_input("Place Name")
        place_type = st.text_input("Type of Place (e.g., Park, Museum, Playground)")
        maps_link = st.text_input("Google Maps Link")

        # Placeholder for distance calculation for now
        # In a real scenario, this would involve geocoding the address/map_link
        # and then calculating distance to "02169"

        submitted = st.form_submit_button("Add Place")
        if submitted:
            if not name or not place_type or not maps_link:
                st.error("Please fill in all fields.")
            else:
                # Simulate distance calculation (placeholder)
                # In a real app, you'd use a geocoding service here
                simulated_distance = "N/A"
                try:
                    # Basic check if it's a valid maps link (very basic)
                    if "google.com/maps" in maps_link:
                        # A more robust solution would parse lat/lon from the link or use a geocoder
                        # For now, let's just add a random distance as a placeholder
                        import random
                        simulated_distance = round(random.uniform(1, 50), 1)
                    else:
                        st.warning("The Google Maps link might not be valid. Distance calculation might be affected.")
                except Exception as e:
                    st.warning(f"Could not determine distance: {e}")

                places_col.insert_one({
                    "name": name,
                    "type": place_type,
                    "map_link": maps_link,
                    "distance_km": simulated_distance
                })
                st.success(f"Place '{name}' added!")
                st.rerun()
