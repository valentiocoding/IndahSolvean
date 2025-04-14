import streamlit as st
import pandas as pd
from database import get_data_supabase
from db_sheet import get_data_gsheet

# Configuration
st.set_page_config(layout="wide")
st.header(":gray[Alumni Master Data]", divider="gray")

# Initialize session state
def init_session_state():
    sheet_id = "1OFjU_hko0oTF76kNyN1VGs9NpKzZ6qfCq2TJIuvTiBg"
    if "maindata" not in st.session_state:
        st.session_state.maindata = get_data_gsheet(sheet_id, "MainData")
    # if "niveau_list" not in st.session_state:
    #     st.session_state.niveau_list = get_data_gsheet(sheet_id,"niveau")
    # if "bourse_list" not in st.session_state:
    #     st.session_state.bourse_list = get_data_gsheet(sheet_id,"bourse")
    if "section" not in st.session_state:
        st.session_state.section = "search"

init_session_state()

# Data preparation
def prepare_data():
    data = st.session_state.maindata.copy()
    data["id"] = data["id"].astype(str)
    data["name_filter"] = data["id"] + " - " + data["nom_prenom"]
    return data

data = prepare_data()
# niveau_list = st.session_state.niveau_list
# bourse_list = st.session_state.bourse_list

# Helper function to display disabled fields
def display_field(label, value, key=None, disabled=True):
    if pd.isna(value):
        value = ""
    return st.text_input(label, value=str(value), key=key, disabled=disabled)

# Search Section
def display_search_section():
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.selectbox("Name", options=data["name_filter"])
        selected_data = data[data["name_filter"] == name].iloc[0]
        
        display_field("Etat Professionnel", selected_data["status_professional"], "status_professional")
        
        if st.button("Add New"):
            st.session_state.section = "addnew"
            st.rerun()

    with col2:
        display_field("Niveau d'etudes vise", selected_data["niveau"])
        display_field("Année de debut des etudes en France", selected_data["start_year"])
        display_field("Année de fin des etudes en France", selected_data["end_year"])
        display_field("Durée (prevue du sejour (en mois))", selected_data["duree"])

    # Tabs
    personal, university, activity = st.tabs(['Personal Information', "University Information", "Activity Information"])

    # Personal Tab
    with personal:
        col1, col2 = st.columns(2)
        with col1:
            display_field("Nom/Prenom", selected_data["nom_prenom"])
            display_field("Prenom", selected_data["prenom"])
            display_field("Nom", selected_data["nom"])
            display_field("Adresse courriel", selected_data["personal_courriel"])
            display_field("Sexe", selected_data["sex"])
            display_field("Date de Naissance", selected_data["birth_date"])

        with col2:
            display_field("Pays", selected_data["personal_pays"])
            display_field("Province", selected_data["personal_province"])
            st.text_area("Ville", value=selected_data["personal_ville"], disabled=True, key="personal_ville")
            display_field("Code postale", selected_data["code_post"])

    # University Tab
    with university:
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Etude établissement", value=selected_data["education"], disabled=True, key="education")
        with col2:
            st.text_area("Ville", value=selected_data["university_ville"], disabled=True, key="university_ville")
            display_field("Bourse", selected_data["bourse"])
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Domain Etudes 1")
                st.text_area("Secteur / Domaine", value=selected_data["university_sector"], disabled=True, key="university_sector")
                st.text_area("Sub Secteur / Specialite", value=selected_data["university_sub_sector"], disabled=True, key="university_sub_sector")
            with col2:
                st.subheader("Domain Etudes 2")
                st.text_area("Secteur / Domaine", value=selected_data["university_sector2"], disabled=True, key="university_sector2")
                st.text_area("Sub Secteur / Specialite", value=selected_data["university_sub_sector2"], disabled=True, key="university_sub_sector2")

    # Activity Tab
    with activity:
        col1, col2 = st.columns(2)
        with col1:
            display_field("Employeur", selected_data["employeur"])
            display_field("Fonction", selected_data["fonction"])
            display_field("Pays", selected_data["activity_pays"], "activity_pays")
            display_field("Province", selected_data["activity_province"], "activity_province")
            st.text_area("Ville", value=selected_data["activity_ville"], disabled=True, key="activity_ville")
        with col2:
            display_field("Adresse professionel", selected_data["activity_address"])
            display_field("N° de téléphone professionnel", selected_data["activity_number"])
            display_field("Adresse courriel professionnel", selected_data["activity_courriel"])

# Add New Section
def display_addnew_section():
    st.dataframe(data[data['type'].isin(['Section', 'Header'])])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Etat Professionnel", key="status_professional")
        if st.button("Search"):
            st.session_state.section = "search"
            st.rerun()

    with col2:
        st.selectbox("Niveau d'etudes vise", options=niveau_list['niveau'], key="niveau")
        st.text_input("Année de debut des etudes en France", key="start_year")
        st.text_input("Année de fin des etudes en France", key="end_year")
        st.text_input("Durée (prevue du sejour (en mois))", key="duree")

    personal, university, activity = st.tabs(['Personal Information', "University Information", "Activity Information"])

    with personal:
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prenom", key="prenom")
            nom = st.text_input("Nom", key="nom")
            nom_prenom = f"{prenom} {nom}"
            st.text_input("Nom/prenom", value=nom_prenom, disabled=True)
            personal_courriel = st.text_input("Adresse courriel", key="personal_courriel")
            sex = st.selectbox("Sexe", options=['Homme', 'Femme', 'Inconnu'], key="sex")

        with col2:
            personal_pays = st.text_input("Pays", key="personal_pays")
            personal_province = st.text_input("Province", key="personal_province")
            personal_ville = st.text_area("Ville", key="personal_ville")
            code_post = st.text_input("Code postale", key="code_post")

# Main App Logic
if st.session_state.section == "search":
    display_search_section()
elif st.session_state.section == "addnew":
    display_addnew_section()