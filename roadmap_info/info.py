import os
import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
from functions import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.colored_header import colored_header
from streamlit_extras.grid import grid
import pickle
from pathlib import Path


# -------- Header ----------------
text,img=st.columns((4,3),gap='medium')
with text:
    # -------- Header ----------------
    st.title('Roadmapping Digital')
    #st.subheader('Ajude a sua empresa a criar uma estratégia digital alinhada com os seus objetivos, expectativas e recursos.')
    st.subheader('''Ajude a sua empresa a criar uma estratégia digital alinhada com os seus objetivos, expectativas e recursos.''')
    st.write('''O objetivo deste serviço é permitir que a empresa reflita sobre o seu posicionamento no mercado,
                as suas prioridades e defina um **plano de transformação** para a sua implementação.
                O Roadmapping Digital segue a abordagem metodológica preconizada pela **iniciativa ADMA**,
                que tem o apoio da Comissão Europeia para auxiliar as PMEs europeias a adotar soluções de produção avançadas e estratégias de inovação social,
                levando-as em direção ao conceito de "indústria do futuro" com uma produção mais competitiva, moderna e sustentável.''')
    
    # # ---------- LOGIN FORM ------------------
    # # Create user_state
    # if 'user_state' not in st.session_state:
    #     st.session_state.user_state = {
    #         'username': '',
    #         'password': '',
    #         'logged_in': False
    #     }

    # if not st.session_state.user_state['logged_in']:
    #     with st.form('login'):
    #         # Create login form
    #         st.subheader('Login')
    #         username = st.text_input('Nome de utilizador',placeholder='Username')
    #         password = st.text_input('Palavra-passe', type='password',placeholder='Password')
    #         submit = st.form_submit_button('Login')

    #         # Check if user is logged in
    #         if submit and st.session_state.user_state['logged_in'] == False:
    #             if username == 'bea' and password == 'a22c15b13':
    #                 st.session_state.user_state['username'] = username
    #                 st.session_state.user_state['password'] = password
    #                 st.session_state.user_state['logged_in'] = True
    #                 st.write('You are logged in')
    #                 st.rerun()
    #             else:
    #                 st.write('Invalid username or password')

    # elif st.session_state.user_state['logged_in']:     

    # -------- Upload file --------------
    st.markdown('')
    with st.form('upload_form'):
        st.subheader('Analisar respostas')
        uploaded_file=st.file_uploader('Selecione o ficheiro com as respostas',type='xlsx',accept_multiple_files=False)

        submit_btn=st.form_submit_button(label='Analisar',icon=':material/search:')
        
        if submit_btn and uploaded_file is not None:
            # read uploaded file
            df=pd.read_excel(uploaded_file,engine='openpyxl')
            # format the uploaded file, creating two dataframes, one with participants data and other with theirs answers
            part_df,answers_df=format_file(df)

            st.session_state['dataframe']=part_df,answers_df
            st.rerun()
        elif submit_btn and uploaded_file is None:
            st.error('Por favor selecione um ficheiro!',icon=':material/warning:')

    

        # logout_btn=st.button(label='Logout')
        # if logout_btn:
        #     logout()
with img:
    st.title('')
    with st.container(height=700,border=False):
        st.image('images/cover.jpg',use_container_width=True)




# st.header('Processo',anchor='process')
# col1,col2,col3,col4=st.columns((4),gap='medium')
# with col1:
#     st.subheader('1 | Reunião de Arranque')
#     st.write('''Destina-se a garantir que os colaboradores da empresa a envolver ficam cientes dos objetivos, da
#                     metodologia e das motivações.''')
    
# with col2:
#     st.subheader('2 | Resposta ao questionário')
#     st.write('''É selecionado um grupo de 5 a 8 colaboradores responsáveis pelas atividades-chave da empresa
#                     para preencher um **questionário** em formato online.''')
# with col3:
#     st.subheader('3 | Reunião de Feedback')
#     st.write('''    Destina-se a devolver os resultados à equipa envolvida no processo,
#                     procurando esclarecer as dimensões onde se registam disparidade nas respostas,
#                     recolher informação mais detalhada cuja necessidade foi suscitada pelo trabalho de agregação
#                     a definir as dimensões de intervenção prioritárias.''')
# with col4:
#     st.subheader('4 | Plano de transformação')
#     st.write('''    O plano de transformação resultante reflete o resultado agregado e consensual do questionário e faz
#                     uma análise em cada uma das sete dimensões de transformação.
#                     No final, este plano será apresentado e entregue à empresa e basear-se-á na análise scan com as devidas recomendações.''')
    




