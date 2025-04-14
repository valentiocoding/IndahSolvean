import streamlit as st
from database import get_data_supabase, insert_domain

def init_session_state():
    """Initialize or refresh the niveau list"""
    st.session_state.domain_list = get_data_supabase("domain")

def main():
    # Initialize session state
    if "domain_list" not in st.session_state:
        init_session_state()
    
    # Display table
    st.dataframe(st.session_state.domain_list)
    
    # Input form with columns for better layout
    col1, col2 = st.columns([4, 1])
    with col1:
        new_domain = st.text_input("New Domain", key="new_domain")
    with col2:
        st.write("")  # Vertical spacer
        add_clicked = st.button("Add New")
    
    # Handle add new logic
    if add_clicked and new_domain:
        insert_domain(new_domain)
        init_session_state()  # Refresh the data
        st.rerun()  # Refresh the UI

if __name__ == "__main__":
    main()