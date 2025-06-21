import streamlit as st
from datetime import datetime

def render_purchases(purchases_col):
    st.header("🛍️ To Purchase")

    # Display all purchase items in tile format
    st.subheader("Your Purchase List")
    items = list(purchases_col.find())
    if not items:
        st.info("No items added to your purchase list yet. Add your first item below!")
    else:
        # Create rows with 2 tiles each (can be adjusted)
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(items):
                    with cols[j]:
                        item = items[i + j]
                        status_color = "green" if item['status'] == "Purchased" else "orange" if item['status'] == "Wishlist" else "gray"
                        st.markdown(f"""
                        <div class="tile">
                            <h3>{item['name']}</h3>
                            <p>Category: {item.get('category', 'N/A')}</p>
                            <p>Estimated Price: ${item.get('price', 'N/A'):.2f}</p>
                            <p style="color: {status_color}; font-weight: bold;">Status: {item['status']}</p>
                            {f"<p>Purchased on: {item['purchase_date']}</p>" if item['status'] == "Purchased" and item.get('purchase_date') else ""}
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Add New Item to Purchase List")
    with st.form("add_purchase_item"):
        name = st.text_input("Item Name")
        category = st.text_input("Category (e.g., Toys, Clothes, Books)")
        price_str = st.text_input("Estimated Price (e.g., 29.99)")
        status = st.selectbox("Status", ["Wishlist", "To Buy Soon", "Purchased"])

        purchase_date = None
        if status == "Purchased":
            purchase_date = st.date_input("Purchase Date", value=datetime.today())

        submitted = st.form_submit_button("Add Item")
        if submitted:
            if not name:
                st.error("Item Name is required.")
            else:
                try:
                    price = float(price_str) if price_str else 0.0
                except ValueError:
                    st.error("Invalid price format. Please enter a number (e.g., 29.99).")
                    return

                item_data = {
                    "name": name,
                    "category": category,
                    "price": price,
                    "status": status,
                    "added_on": datetime.now()
                }
                if status == "Purchased" and purchase_date:
                    item_data["purchase_date"] = str(purchase_date)

                purchases_col.insert_one(item_data)
                st.success(f"Item '{name}' added to purchase list!")
                st.rerun()
