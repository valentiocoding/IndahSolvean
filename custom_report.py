import streamlit as st
import pandas as pd
from database import get_data_supabase, input_data, edit_data
from datetime import datetime, timedelta


# Initialize session state
def init_session_state():
    if "maindata" not in st.session_state:
        st.session_state.maindata = get_data_supabase("maindata")
    if "niveau_list" not in st.session_state:
        st.session_state.niveau_list = get_data_supabase("niveau")
    if "bourse_list" not in st.session_state:
        st.session_state.bourse_list = get_data_supabase("bourse")
    if "domain_list" not in st.session_state:
        st.session_state.bourse_list = get_data_supabase("domain")
    if "section" not in st.session_state:
        st.session_state.section = "search"
    if "selected_id" not in st.session_state:
            st.session_state.selected_id = ''

init_session_state()

sex = st.selectbox("Sexe", options=['Homme', 'Femme'], index=None, placeholder="Select Sexe")
st.dataframe(st.session_state.maindata[st.session_state.maindata['sex'] == sex])