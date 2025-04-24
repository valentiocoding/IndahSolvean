import streamlit as st
import pandas as pd
from database import get_data_supabase, input_data, edit_data
from datetime import datetime, timedelta
from io import BytesIO

# Initialize session state
def init_session_state():
    if "maindata" not in st.session_state:
        st.session_state.maindata = get_data_supabase("maindata")
    if "niveau_list" not in st.session_state:
        st.session_state.niveau_list = get_data_supabase("niveau")
    if "bourse_list" not in st.session_state:
        st.session_state.bourse_list = get_data_supabase("bourse")
    if "domain_list" not in st.session_state:
        st.session_state.domain_list = get_data_supabase("domain")
    if "section" not in st.session_state:
        st.session_state.section = "search"
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = ''

init_session_state()

df = st.session_state.maindata

# Dynamic column filters
filter_by = st.multiselect("Filter by column", options=df.columns)

for col in filter_by:
    unique_vals = df[col].dropna().unique().tolist()
    selected_vals = st.multiselect(f"Filter values for {col}", options=unique_vals, key=f"filter_{col}")
    if selected_vals:
        df = df[df[col].isin(selected_vals)]

# Display the filtered dataframe
st.dataframe(df)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

st.download_button(
    label="Download all data to Excel",
    data=to_excel(st.session_state.maindata),
    file_name="maindata.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)