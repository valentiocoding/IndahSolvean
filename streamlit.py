import streamlit as st

default = st.Page(
    page='default.py',
    title='Alumni Master Data',
    icon='📦',
    default=True
)

addniveau = st.Page(
    page='addniveau.py',
    title='Add New Niveau',
    icon='📦',

)

adddomain = st.Page(
    page='adddomain.py',
    title='Add New Domain',
    icon='📦',

)

addbourse = st.Page(
    page='addbourse.py',
    title='Add New Bourse',
    icon='📦',

)

versiai_gsheet = st.Page(
    page='versiai_gsheet.py',
    title='Alumni Master Data versi AI G_Sheet',
    icon='📦',
)

versiai_supabase = st.Page(
    page='versiai_supabase.py',
    title='Alumni',
    icon='📦',
)

custom_report = st.Page(
    page='custom_report.py',
    title='by Sexe',
    icon='📦',
)

addreport = st.Page(
    page='addreport.py',
    title='Add Another . . .',
    icon='📦',
)




pg = st.navigation({
    'Master Data': [versiai_supabase],
    'Created Data': [addniveau, adddomain, addbourse],
    'Custom Report': [custom_report, addreport]
})


pg.run()