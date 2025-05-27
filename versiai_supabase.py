import streamlit as st
import pandas as pd
from database import get_data_supabase, input_data, edit_data
from datetime import datetime, timedelta, date

# Configuration
st.set_page_config(layout="wide")
st.header(":gray[France Alumni Indonesia]", divider="gray")


def calculate_age(birth_date):
    today = datetime.now()
    
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    # Adjust for negative months or days
    if days < 0:
        months -= 1
        # Get the last day of the previous month
        previous_month = today.replace(day=1) - timedelta(days=1)
        days += previous_month.day
    
    if months < 0:
        years -= 1
        months += 12
    
    return years, months, days

def format_age(birth_date):
    years, months, days = calculate_age(birth_date)
    return f"{years} Tahun {months} Bulan {days} Hari"

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

# Data preparation - FIXED: Proper string conversion and handling
def prepare_data():
    data = st.session_state.maindata.copy()
    data["id"] = data['id'].astype(str).str.strip()  # Fixed: using .str.strip() for Series
    data["name_filter"] = data["id"] + " - " + data["nom_prenom"]
    return data

data = prepare_data()
niveau_list = st.session_state.niveau_list
bourse_list = st.session_state.bourse_list
domain_list = st.session_state.domain_list

# Helper function to display disabled fields - IMPROVED: better NaN handling
def display_field(label, value, key=None, disabled=True):
    if pd.isna(value):
        value = ""
    return st.text_input(label, value=str(value), key=key, disabled=disabled)

# Search Section - FIXED: handling empty selections
def display_search_section():
    col1,col2,col3 = st.columns([1,1,10])
    if col1.button("Add New"):
        st.session_state.section = "addnew"
        st.rerun()
    if col2.button("Edit"):
        st.session_state.section = "edit"
        st.rerun()
    col1, col2 = st.columns(2)
    
    with col1:
        name_options = data["name_filter"].tolist()
        name = st.selectbox("Name", options=name_options)

        if name:
            st.session_state.selected_id = data[data['name_filter'] == name]['id'].iloc[0]

        
        if len(data[data["name_filter"] == name]) > 0:
            selected_data = data[data["name_filter"] == name].iloc[0]
        else:
            selected_data = data.iloc[0]  # Default to first record if none selected
            
        display_field("Etat Professionnel", selected_data["status_professional"], "status_professional")
        
        

    with col2:
        display_field("Niveau d'etudes vise", selected_data["niveau"])
        display_field("Année de debut des etudes en France", selected_data["start_year"])
        display_field("Année de fin des etudes en France", selected_data["end_year"])
        display_field("Durée (prevue du sejour (en mois))", selected_data["duree"])

    # Tabs
    personal, university, activity, notes = st.tabs(['Personal Information', "University Information", "Activity Information", "Notes/Commantaine"])

    # Personal Tab - FIXED: consistent field display
    with personal:
        col1, col2 = st.columns(2)
        with col1:
            display_field("Nom/Prenom", selected_data["nom_prenom"])
            display_field("Prenom", selected_data["prenom"])
            display_field("Nom", selected_data["nom"])
            display_field("Adresse courriel", selected_data["personal_courriel"])
            display_field("Sexe", selected_data["sex"])
            birth_date = st.date_input("Date de Naissance", 
                                     value=datetime.strptime(selected_data["birth_date"], "%Y-%m-%d").date() if selected_data["birth_date"] else None,
                                     key="edit_birth_date", format="DD/MM/YYYY", disabled=True, min_value=date(1899, 1, 1), max_value=date(2100, 12, 31))

        with col2:
            display_field("Pays", selected_data["personal_pays"])
            display_field("Province", selected_data["personal_province"])
            st.text_area("Ville", value=selected_data.get("personal_ville", ""), disabled=True, key="personal_ville")
            st.text_area("Adresse Personnelle", value=selected_data.get("personal_address", ""), disabled=True, key="personal_address")
            display_field("Code postale", selected_data["code_post"])
            display_field("Numéro de téléphone", selected_data["personal_number"])
            display_field("Numéro de portable", selected_data["personal_portable"])

    # University Tab - FIXED: using .get() for safer dict access
    with university:
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Etude établissement", value=selected_data.get("education", ""), disabled=True, key="education")
        with col2:
            st.text_area("Ville", value=selected_data.get("university_ville", ""), disabled=True, key="university_ville")
            display_field("Bourse", selected_data.get("bourse", ""))
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Domain Etudes 1")
                st.text_area("Secteur / Domaine", value=selected_data.get("university_sector", ""), disabled=True, key="university_sector")
                st.text_area("Sub Secteur / Specialite", value=selected_data.get("university_sub_sector", ""), disabled=True, key="university_sub_sector")
            with col2:
                st.subheader("Domain Etudes 2")
                st.text_area("Secteur / Domaine", value=selected_data.get("university_sector2", ""), disabled=True, key="university_sector2")
                st.text_area("Sub Secteur / Specialite", value=selected_data.get("university_sub_sector2", ""), disabled=True, key="university_sub_sector2")

    # Activity Tab - FIXED: consistent field access
    with activity:
        col1, col2 = st.columns(2)
        with col1:
            display_field("Employeur", selected_data.get("employeur", ""))
            display_field("Fonction", selected_data.get("fonction", ""))
            display_field("Pays", selected_data.get("activity_pays", ""), "activity_pays")
            display_field("Province", selected_data.get("activity_province", ""), "activity_province")
            st.text_area("Ville", value=selected_data.get("activity_ville", ""), disabled=True, key="activity_ville")
        with col2:
            display_field("Adresse professionel", selected_data.get("activity_address", ""))
            display_field("N° de téléphone professionnel", selected_data.get("activity_number", ""))
            display_field("Adresse courriel professionnel", selected_data.get("activity_courriel", ""))

    with notes:
        col1,col2 = st.columns(2)
        with col1:
            display_field("Notes/Commantaine", selected_data.get('notes_commantaine',""))

# Add New Section - IMPROVED: better form handling
def display_addnew_section():
    if st.button("Back to Search"):
            st.session_state.section = "search"
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_professional = st.text_input("Etat Professionnel", key="status_professional")
        

    with col2:
        niveau_options = niveau_list['niveau'].tolist() if 'niveau' in niveau_list else []
        niveau = st.selectbox("Niveau d'etudes vise", options=niveau_options, key="niveau")
        start_year = st.text_input("Année de debut des etudes en France", key="start_year")
        end_year = st.text_input("Année de fin des etudes en France", key="end_year")
        duree = st.text_input("Durée (prevue du sejour (en mois))", key="duree")

    personal, university, activity, notes = st.tabs(['Personal Information', "University Information", "Activity Information", "Notes/Commantaine"])

    with personal:
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prenom", key="prenom")
            nom = st.text_input("Nom", key="nom")
            nom_prenom = f"{prenom} {nom}"
            st.text_input("Nom/prenom", value=nom_prenom, disabled=True)
            personal_courriel = st.text_input("Adresse courriel", key="personal_courriel")
            sex = st.selectbox("Sexe", options=['Homme', 'Femme', 'Inconnu'], key="sex")
            birth_date = st.date_input("Date de Naissance", key="birth_date", value=None, format="DD/MM/YYYY", min_value=date(1899, 1, 1), max_value=date(2100, 12, 31))

        with col2:
            personal_pays = st.text_input("Pays", key="personal_pays")
            personal_province = st.text_input("Province", key="personal_province")
            personal_ville = st.text_area("Ville", key="personal_ville")
            personal_address = st.text_area("Adresse Personnelle", key="personal_address")
            code_post = st.text_input("Code postale", key="code_post")
            personal_number = st.text_input("Numéro de téléphone", key="personal_number")
            personal_portable = st.text_input("Numéro de portable", key="personal_portable")

    with university:
        col1, col2 = st.columns(2)
        with col1:
            education = st.text_area("Etude établissement", key="education")
        with col2:
            university_ville = st.text_area("Ville", key="university_ville")
            bourse_options = bourse_list['bourse'].tolist() if 'bourse' in bourse_list else []
            bourse = st.selectbox("Bourse",options=bourse_options ,key="bourse", placeholder="Choose Bourse", index=None)
            
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                domain_options = domain_list['domain'].tolist() if 'domain' in domain_list else []
                st.subheader("Domain Etudes 1")
                university_sector = st.selectbox("Secteur / Domaine",options=domain_options, key="university_sector", index=None)
                university_sub_sector = st.text_area("Sub Secteur / Specialite", key="university_sub_sector")
            with col2:
                st.subheader("Domain Etudes 2")
                university_sector2 = st.selectbox("Secteur / Domaine", options=domain_options, key="university_sector2", index=None)
                university_sub_sector2 = st.text_area("Sub Secteur / Specialite",  key="university_sub_sector2")
    with activity:
        col1, col2 = st.columns(2)
        with col1:
            employeur = st.text_input("Employeur", key="employeur")
            fonction = st.text_input("Fonction", key="fonction")
            activity_pays = st.text_input("Pays", key="activity_pays")
            activity_province = st.text_input("Province", key="activity_province")
            activity_ville = st.text_area("Ville", key="activity_ville")

        with col2:
            activity_address = st.text_input("Adresse professionel", key="activity_address")
            activity_number = st.text_input("N° de téléphone professionnel",key="activity_number")
            activity_courriel = st.text_input("Adresse courriel professioinnel", key="activity_courriel")
    with notes:
        col1,col2 = st.columns(2)
        with col1:
            notes = st.text_input("Notes/Commantaine", key="notes_commantaine")



    # Add submit button
    if st.button("Submit New Record"):
        age = format_age(birth_date)
        birth_date = birth_date.strftime("%Y-%m-%d")
        input_data(nom_prenom, prenom, nom, sex, birth_date, personal_address, code_post, personal_ville, personal_province, personal_pays, personal_number, personal_portable, personal_courriel, start_year, end_year, duree, niveau, university_sector, university_sub_sector, education, university_ville, status_professional, fonction, employeur, university_sector2, university_sub_sector2, activity_address, activity_ville, activity_province, activity_pays, activity_number, activity_courriel, bourse, notes)
        st.session_state.maindata = get_data_supabase("maindata")
        st.session_state.section = 'search'
        
        st.success("New record added successfully!")
        st.rerun()


def display_edit_section():
    if st.button("Back to Search"):
            st.session_state.section = "search"
            st.rerun()
    # Get the selected record
    selected_name = st.text_input("Name", value=data[data['id'] == st.session_state.selected_id]['nom_prenom'].iloc[0], disabled=True)
    selected_data = data[data['id'] == st.session_state.selected_id].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_professional = st.text_input("Etat Professionnel", 
                                         value=selected_data["status_professional"], 
                                         key="edit_status_professional")
        
        

    with col2:
        niveau_options = niveau_list['niveau'].tolist() if 'niveau' in niveau_list else []
        niveau = st.selectbox("Niveau d'etudes vise", 
                            options=niveau_options, 
                            index=niveau_options.index(selected_data["niveau"]) if selected_data["niveau"] in niveau_options else 0,
                            key="edit_niveau")
        
        start_year = st.text_input("Année de debut des etudes en France", 
                                 value=selected_data["start_year"],
                                 key="edit_start_year")
        
        end_year = st.text_input("Année de fin des etudes en France", 
                               value=selected_data["end_year"],
                               key="edit_end_year")
        
        duree = st.text_input("Durée (prevue du sejour (en mois))", 
                            value=selected_data["duree"],
                            key="edit_duree")

    personal, university, activity, notes = st.tabs(['Personal Information', "University Information", "Activity Information", "Notes/Commantaine"])

    with personal:
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prenom", 
                                 value=selected_data["prenom"],
                                 key="edit_prenom")
            
            nom = st.text_input("Nom", 
                              value=selected_data["nom"],
                              key="edit_nom")
            
            nom_prenom = f"{prenom} {nom}"
            st.text_input("Nom/prenom", value=nom_prenom, disabled=True)
            
            personal_courriel = st.text_input("Adresse courriel", 
                                           value=selected_data["personal_courriel"],
                                           key="edit_personal_courriel")
            
            sex = st.selectbox("Sexe", 
                             options=['Homme', 'Femme', 'Inconnu'], 
                             index=['Homme', 'Femme', 'Inconnu'].index(selected_data["sex"]) if selected_data["sex"] in ['Homme', 'Femme', 'Inconnu'] else 2,
                             key="edit_sex")
            
            birth_date = st.date_input("Date de Naissance", 
                                     value=datetime.strptime(selected_data["birth_date"], "%Y-%m-%d").date() if selected_data["birth_date"] else None,
                                     key="edit_birth_date", format="DD/MM/YYYY",min_value=date(1899, 1, 1), max_value=date(2100, 12, 31))

        with col2:
            personal_pays = st.text_input("Pays", 
                                       value=selected_data["personal_pays"],
                                       key="edit_personal_pays")
            
            personal_province = st.text_input("Province", 
                                            value=selected_data["personal_province"],
                                            key="edit_personal_province")
            
            personal_ville = st.text_area("Ville", 
                                        value=selected_data["personal_ville"],
                                        key="edit_personal_ville")
            
            personal_address = st.text_area("Adresse Personnelle", 
                                         value=selected_data.get("personal_address", ""),
                                         key="edit_personal_address")
            
            code_post = st.text_input("Code postale", 
                                    value=selected_data["code_post"],
                                    key="edit_code_post")
            
            personal_number = st.text_input("Numéro de téléphone", 
                                         value=selected_data["personal_number"],
                                         key="edit_personal_number")
            
            personal_portable = st.text_input("Numéro de portable", 
                                            value=selected_data["personal_portable"],
                                            key="edit_personal_portable")
    with university:
        col1, col2 = st.columns(2)
        with col1:
            education = st.text_area("Etude établissement", value=selected_data['education'], key="education")
        with col2:
            university_ville = st.text_area("Ville", value=selected_data["university_ville"], key="university_ville")
            bourse = st.text_input("Bourse", value=selected_data.get("bourse", ""))
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Domain Etudes 1")
                university_sector = st.text_area("Secteur / Domaine", value=selected_data.get("university_sector", ""), key="university_sector")
                university_sub_sector = st.text_area("Sub Secteur / Specialite", value=selected_data.get("university_sub_sector", ""),  key="university_sub_sector")
            with col2:
                st.subheader("Domain Etudes 2")
                university_sector2 = st.text_area("Secteur / Domaine", value=selected_data.get("university_sector2", ""),  key="university_sector2")
                university_sub_sector2 = st.text_area("Sub Secteur / Specialite", value=selected_data.get("university_sub_sector2", ""),  key="university_sub_sector2")

    # Activity Tab - FIXED: consistent field access
    with activity:
        col1, col2 = st.columns(2)
        with col1:
            employeur = st.text_input("Employeur", selected_data.get("employeur", ""), key = "employeur")
            fonction = st.text_input("Fonction", selected_data.get("fonction", ""), key="fonction")
            activity_pays = st.text_input("Pays", selected_data.get("activity_pays", ""), key= "activity_pays")
            activity_province = st.text_input("Province", selected_data.get("activity_province", ""), key="activity_province")
            activity_ville = st.text_area("Ville", value=selected_data.get("activity_ville", ""), key="activity_ville")
        with col2:
            activity_address = st.text_input("Adresse professionel", selected_data.get("activity_address", ""))
            activity_number = st.text_input("N° de téléphone professionnel", selected_data.get("activity_number", ""))
            activity_courriel = st.text_input("Adresse courriel professionnel", selected_data.get("activity_courriel", ""))  

    with notes:
        col1,col2 = st.columns(2)
        with col1:
            notes = st.text_input("Notes/Commantaine", selected_data.get("notes_commantaine",""))      
        
            
    if st.button("Updated"):
        edit_data(st.session_state.selected_id,nom_prenom, prenom, nom, sex, birth_date, personal_address, code_post, personal_ville, personal_province, personal_pays, personal_number, personal_portable, personal_courriel, start_year, end_year, duree, niveau, university_sector, university_sub_sector, education, university_ville, status_professional, fonction, employeur, university_sector2, university_sub_sector2, activity_address, activity_ville, activity_province, activity_pays, activity_number, activity_courriel, bourse, notes)
        st.session_state.maindata = get_data_supabase("maindata")
        st.success("Success Update!")


# Main App Logic
if st.session_state.section == "search":
    display_search_section()
elif st.session_state.section == "addnew":
    display_addnew_section()
elif st.session_state.section == "edit":
    display_edit_section()