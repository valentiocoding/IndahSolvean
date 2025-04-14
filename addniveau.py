import streamlit as st
from database import get_data_supabase, insert_niveau

def init_session_state():
    """Initialize or refresh the niveau list"""
    st.session_state.niveau_list = get_data_supabase("niveau")

def main():
    # Initialize session state
    if "niveau_list" not in st.session_state:
        init_session_state()
    
    # Display table
    st.dataframe(st.session_state.niveau_list)
    
    # Input form with columns for better layout
    col1, col2 = st.columns([4, 1])
    with col1:
        new_niveau = st.text_input("New Niveau", key="new_niveau")
    with col2:
        st.write("")  # Vertical spacer
        add_clicked = st.button("Add New")
    
    # Handle add new logic
    if add_clicked and new_niveau:
        insert_niveau(new_niveau)
        init_session_state()  # Refresh the data
        st.rerun()  # Refresh the UI

if __name__ == "__main__":
    main()