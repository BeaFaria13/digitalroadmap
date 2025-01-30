import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
from functions import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header

st.set_page_config(layout='wide',page_title='Roadmapping Análise')
st.logo('images/Picture1.png')


# -------- Define pages ------------------
dashboard_page=st.Page("results/dashboard.py",title="Dashboard",icon="📊")
info_page=st.Page("roadmap_info/info.py",title="Roadmapping Digital",icon="🛣️")
transformations_page=st.Page("roadmap_info/transformations.py",title="Transformações",icon="📚")


# Change navigation depending on the existence of a dataframe
if "dataframe" not in st.session_state:
    pg=st.navigation([info_page], position='hidden')

else:
    pg=st.navigation([dashboard_page], position='hidden')




pg.run()
