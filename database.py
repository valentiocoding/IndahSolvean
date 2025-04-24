import streamlit as st
import pandas as pd
from supabase import create_client, Client

secrets = st.secrets["secrets"]

SUPABASE_URL = secrets["SUPABASE_URL"]
SUPABASE_KEY = secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def input_data(nom_prenom, prenom, nom, sex, birth_date, personal_address, code_post, personal_ville, personal_province, personal_pays, personal_number, personal_portable, personal_courriel, start_year, end_year, duree, niveau, university_sector, university_sub_sector, education, university_ville, status_professional, fonction, employeur, university_sector2, university_sub_sector2, activity_address, activity_ville, activity_province, activity_pays, activity_number, activity_courriel, bourse, notes):
    # Collect all the form data into a dictionary
    data = {
        "nom_prenom": nom_prenom, 
        "prenom": prenom, 
        "nom": nom, 
        "sex": sex, 
        "birth_date": birth_date, 
        "personal_address": personal_address, 
        "code_post": code_post, 
        "personal_ville": personal_ville, 
        "personal_province": personal_province, 
        "personal_pays": personal_pays, 
        "personal_number": personal_number, 
        "personal_portable": personal_portable, 
        "personal_courriel": personal_courriel, 
        "start_year": start_year, 
        "end_year": end_year, 
        "duree": duree, 
        "niveau": niveau, 
        "university_sector": university_sector, 
        "university_sub_sector": university_sub_sector, 
        "education": education, 
        "university_ville": university_ville, 
        "status_professional": status_professional, 
        "fonction": fonction, 
        "employeur": employeur, 
        "university_sector2": university_sector2, 
        "university_sub_sector2": university_sub_sector2, 
        "activity_address": activity_address, 
        "activity_ville": activity_ville, 
        "activity_province": activity_province, 
        "activity_pays": activity_pays, 
        "activity_number": activity_number, 
        "activity_courriel": activity_courriel, 
        "bourse": bourse, 
        "notes_commantaine": notes
    }
    
    try:
        # Insert the data into Supabase
        response = supabase.table("maindata").insert(data).execute()
        if response:
            st.success("Data berhasil disimpan")
            return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def get_data_supabase(table_name):
    response = supabase.table(table_name).select("*").execute()
    response = pd.DataFrame(response.data)
    return response

def insert_niveau(value):
    try:
        response = supabase.table("niveau").insert({"niveau": value}).execute()
        st.success("Data berhasil disimpan")
    except Exception as e:
        st.error(e)

def insert_domain(value):
    try:
        response = supabase.table("domain").insert({"domain": value}).execute()
        st.success("Data berhasil disimpan")
    except Exception as e:
        st.error(e)

def insert_bourse(value):
    try:
        response = supabase.table("bourse").insert({"bourse": value}).execute()
        st.success("Data berhasil disimpan")
    except Exception as e:
        st.error(e)



def edit_data(record_id, nom_prenom, prenom, nom, sex, birth_date, personal_address, code_post, personal_ville, personal_province, personal_pays, personal_number, personal_portable, personal_courriel, start_year, end_year, duree, niveau, university_sector, university_sub_sector, education, university_ville, status_professional, fonction, employeur, university_sector2, university_sub_sector2, activity_address, activity_ville, activity_province, activity_pays, activity_number, activity_courriel, bourse, notes):
    data = {
        "nom_prenom": nom_prenom, 
        "prenom": prenom, 
        "nom": nom, 
        "sex": sex, 
        "birth_date": birth_date, 
        "personal_address": personal_address, 
        "code_post": code_post, 
        "personal_ville": personal_ville, 
        "personal_province": personal_province, 
        "personal_pays": personal_pays, 
        "personal_number": personal_number, 
        "personal_portable": personal_portable, 
        "personal_courriel": personal_courriel, 
        "start_year": start_year, 
        "end_year": end_year, 
        "duree": duree, 
        "niveau": niveau, 
        "university_sector": university_sector, 
        "university_sub_sector": university_sub_sector, 
        "education": education, 
        "university_ville": university_ville, 
        "status_professional": status_professional, 
        "fonction": fonction, 
        "employeur": employeur, 
        "university_sector2": university_sector2, 
        "university_sub_sector2": university_sub_sector2, 
        "activity_address": activity_address, 
        "activity_ville": activity_ville, 
        "activity_province": activity_province, 
        "activity_pays": activity_pays, 
        "activity_number": activity_number, 
        "activity_courriel": activity_courriel, 
        "bourse": bourse, 
        "notes_commantaine":notes
    }
    try:
        # Convert date fields to ISO format
        if 'birth_date' in data and data['birth_date']:
            data['birth_date'] = data['birth_date'].isoformat()
        
        # Update the record
        response = supabase.table("maindata").update(data).eq("id", record_id).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
    

