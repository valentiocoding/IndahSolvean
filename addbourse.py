import streamlit as st
from database import get_data_supabase, insert_bourse

def init_session_state():
    """Initialize or refresh the niveau list"""
    st.session_state.bourse_list = get_data_supabase("bourse")

def main():
    # Initialize session state
    if "bourse_list" not in st.session_state:
        init_session_state()
    
    # Display table
    st.dataframe(st.session_state.bourse_list)
    
    # Input form with columns for better layout
    col1, col2 = st.columns([4, 1])
    with col1:
        new_bourse = st.text_input("New Bourse", key="new_bourse")
    with col2:
        st.write("")  # Vertical spacer
        add_clicked = st.button("Add New")
    
    # Handle add new logic
    if add_clicked and new_bourse:
        insert_bourse(new_bourse)
        init_session_state()  # Refresh the data
        st.rerun()  # Refresh the UI

if __name__ == "__main__":
    main()