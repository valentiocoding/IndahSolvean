import streamlit as st
import pandas as pd
from supabase import create_client, Client
from database import get_data_supabase, input_data, insert_niveau
from db_sheet import get_data_gsheet

st.set_page_config(layout="wide")

# Initialize session state
# st.session_state.setdefault("maindata", get_data_supabase("maindata"))
# st.session_state.setdefault("niveau_list", get_data_supabase("niveau"))
# st.session_state.setdefault("bourse_list", get_data_supabase("bourse"))

st.session_state.setdefault("maindata", get_data_gsheet("1OFjU_hko0oTF76kNyN1VGs9NpKzZ6qfCq2TJIuvTiBg","MainData"))


st.header(":gray[France Alumni Indonesia - Main Data]", divider="gray")

data = st.session_state.maindata

niveau_list = st.session_state.niveau_list

bourse_list = st.session_state.bourse_list

st.write(data.sample())


if "section" not in st.session_state:
    st.session_state.section = "search"


if st.session_state.section == "search":

    # Start Header

    col1,col2 = st.columns(2)
    data["id"] = data["id"].astype(str)
    data["name_filter"] = data["id"] + " - " + data["nom_prenom"]
    with col1:
        name = st.selectbox("Name", options=data["name_filter"])
        status_professional = st.text_input("Etat Professionnel", value=data[data["name_filter"] == name]["status_professional"].values[0], key="status_professional", disabled=True)
        addnew = st.button("Add New")
        if addnew:
            st.session_state.section = "addnew"
            st.rerun()

    with col2:
        niveau = st.text_input("Niveau d'etudes vise", value=data[data['name_filter'] == name]['niveau'].values[0], disabled=True)
        start_year = st.text_input("Année de debut des etudes en France",value=data[data['name_filter'] == name]['start_year'].values[0], disabled=True)
        end_year = st.text_input("Année de fin des etudes en France",value=data[data['name_filter'] == name]['end_year'].values[0], disabled=True)
        duree = st.text_input("Durée (prevue du sejour (en mois))",value=data[data['name_filter'] == name]['duree'].values[0], disabled=True)

    # End Header


    # Start Tab

    personal, university, activity,notes = st.tabs(['Personal Information', "University Information", "Activity Information", "Notes/Commantaine"])

    # Start Personal
    with personal:
        col1, col2 = st.columns(2)
        with col1:
            nom_prenom = st.text_input("Nom/Prenom", value=data[data['name_filter'] == name]['nom_prenom'].values[0], disabled=True)
            prenom = st.text_input("Prenom", value=data[data['name_filter'] == name]['prenom'].values[0], disabled=True)
            nom = st.text_input("Nom", value=data[data['name_filter'] == name]['nom'].values[0], disabled=True)
            personal_courriel = st.text_input("Adresse courriel", value=data[data['name_filter'] == name]['personal_courriel'].values[0], disabled=True)
            sex = st.text_input("Sexe", value = data[data['name_filter'] == name]['sex'].values[0], disabled=True)
            birth_date = st.text_input("Date de Naissance", value=data[data['name_filter'] == name]['birth_date'].values[0], disabled=True)

        with col2:
            personal_pays = st.text_input("Pays", value=data[data['name_filter'] == name]['personal_pays'].values[0], disabled=True)
            personal_province = st.text_input("Province", value=data[data['name_filter'] == name]['personal_province'].values[0], disabled=True)
            personal_ville = st.text_area("Ville", value=data[data['name_filter'] == name]['personal_ville'].values[0], disabled=True, key="personal_ville")
            code_post = st.text_input("Code postale", value=data[data['name_filter'] == name]['code_post'].values[0], disabled=True)
            
    # End Personal


    # Start University
    with university:
        col1, col2 = st.columns(2)
        with col1:
            education = st.text_area("Etude établissement", value=data[data['name_filter'] == name]['education'].values[0], disabled=True, key="education")
        with col2:
            university_ville = st.text_area("Ville", value=data[data['name_filter'] == name]['university_ville'].values[0], disabled=True, key="university_ville")
            bourse = st.text_input("Bourse", value=data[data['name_filter'] == name]['bourse'].values[0], disabled=True)
        with st.container(border=True):
            col1,col2 = st.columns(2)
            with col1:
                st.subheader("Domain Etudes 1")
                university_sector = st.text_area("Secteur / Domaine", value=data[data['name_filter'] == name]['university_sector'].values[0], disabled=True, key="university_sector")
                university_sub_sector = st.text_area("Sub Secteur / Specialite", value=data[data['name_filter'] == name]['university_sub_sector'].values[0], disabled=True, key="university_sub_sector")
            with col2:
                st.subheader("Domain Etudes 2")
                university_sector2 = st.text_area("Secteur / Domaine", value=data[data['name_filter'] == name]['university_sector2'].values[0], disabled=True, key="university_sector2")
                university_sub_sector2 = st.text_area("Sub Secteur / Specialite", value=data[data['name_filter'] == name]['university_sub_sector2'].values[0], disabled=True, key="university_sub_sector2")

    # End University


    # Start Activity
    with activity:
        
        col1, col2 = st.columns(2)
        with col1:
            employeur = st.text_input("Employeur", value=data[data['name_filter'] == name]['employeur'].values[0], disabled=True)
            fonction = st.text_input("Fonction", value=data[data['name_filter'] == name]['fonction'].values[0], disabled=True)
            activity_pays = st.text_input("Pays", value=data[data['name_filter'] == name]['activity_pays'].values[0], disabled=True, key="activity_pays")
            activity_province = st.text_input("Province", value=data[data['name_filter'] == name]['activity_province'].values[0], disabled=True, key="activity_province")
            activity_ville = st.text_area("Ville", value=data[data['name_filter'] == name]['activity_ville'].values[0], disabled=True, key="activity_ville")
        with col2:
            activity_address = st.text_input("Adresse professionel", value=data[data['name_filter'] == name]['activity_address'].values[0], disabled=True)
            activity_number = st.text_input("N° de téléphone professionnel", value=data[data['name_filter'] == name]['activity_number'].values[0], disabled=True)
            activity_courriel = st.text_input("Adresse courriel professionnel", value=data[data['name_filter'] == name]['activity_courriel'].values[0], disabled=True)

    # End Activity
    with notes:
        col1,col2 = st.columns(2)
        with col1:
            notes = st.text_input("Notes/Commantaine", value=data[data['name_filter'] == name]['notes_commantaine'].values[0],disabled=True)
    # End Tab














# Add New Section
elif st.session_state.section == 'addnew':
    st.dataframe(data[data['type'].isin(['Section', 'Header'])])
    # Start Header

    col1,col2 = st.columns(2)
    # data["id"] = data["id"].astype(str)
    # data["name_filter"] = data["id"] + " - " + data["nom_prenom"]
    with col1:
        # prenom = st.text_input("Prenom",key="prenom")
        # nom = st.text_input("Nom",key="nom")
        status_professional = st.text_input("Etat Professionnel", key="status_professional")
        addnew = st.button("Search")
        if addnew:
            st.session_state.section = "search"
            st.rerun()

    with col2:
        niveau = st.selectbox("Niveau d'etudes vise", options=niveau_list['niveau'], key="niveau")
        start_year = st.text_input("Année de debut des etudes en France", key="start_year")
        end_year = st.text_input("Année de fin des etudes en France", key="end_year")
        duree = st.text_input("Durée (prevue du sejour (en mois))", key="duree")


    # End Header


    # Start Tab

    personal, university, activity = st.tabs(['Personal Information', "University Information", "Activity Information"])

     # Start Personal
    with personal:
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prenom", key="prenom")
            nom = st.text_input("Nom", key = "nom")
            nom_prenom = prenom + nom
            st.text_input("Nom/prenom", value=nom_prenom, disabled=True)
            personal_courriel = st.text_input("Adresse courriel")
            sex = st.selectbox("Sex", option=['Homme', 'Femme', 'Inconnu'])

        with col2:
            personal_pays = st.text_input("Pays")
            personal_province = st.text_input("Province")
            personal_ville = st.text_area("Ville")
            code_post = st.text_input("Code postale")
            
    # End Personal


