import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st

# Autentikasi
google_cloud_secrets = st.secrets["google_cloud"]
creds = service_account.Credentials.from_service_account_info(
    google_cloud_secrets,
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)

# Fungsi yang lebih efisien
def get_data_gsheet(spreadsheet_id,sheetname):
    data = client.open_by_key(spreadsheet_id).worksheet(sheetname).get_all_records()
    return data


def init_session_state():
    if "maindata" not in st.session_state:
        st.session_state.maindata = get_data_gsheet("1obMxpHxza2KxEx5JA_6kGBp-YflZJWRZMQlr0I_oW7w", "MainData")
        
    if "section" not in st.session_state:
        st.session_state.section = "search"