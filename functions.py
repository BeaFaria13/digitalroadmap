import streamlit as st
import pandas as pd
from itertools import repeat
import plotly_express as px
from statistics import mean,variance,pstdev
import math
import random
import string
import datetime
import numpy as np
import io
import base64
import os
from io import BytesIO
import plotly.io as pio
import matplotlib.pyplot as plt

from PIL import Image



#scores=pd.read_excel("Excel files/Transformações.xlsx",sheet_name='pontuacao')
scores=pd.read_excel("Excel files/Transformações.xlsx",sheet_name='trans_campo_perg_pont')
scores['Pergunta']=scores['Pergunta'].str.strip()
trans_name=pd.read_excel("Excel files/Transformações.xlsx",sheet_name='transf_names')
participants=pd.read_excel("Excel files/Transformações.xlsx",sheet_name='participantes')


def reset():
    del st.session_state['dataframe']



# --------------------------------------------
#                 Filters
# ---------------------------------------------

def companies_unique(df):
    # Return list with companies
    email_list=df["Email"]
    email_list=[x.lower() for x in email_list]
    email_list=[x.split('@') for x in email_list]
    email_list=[x[1].split('.') for x in email_list]

    unique_names=list()
    for name in email_list:
        if name[0] not in unique_names:
            unique_names.append(name[0])
    unique_names=[x.capitalize() for x in unique_names]

    return unique_names

def collect_compay(df):
    x=st.selectbox(label='Selecione a **empresa** a analisar',
                options=df['Empresa'].unique(),key='company')
    return x

def collect_participants(df,company):
    participants_by_company=df.query('Empresa==@company')['Colaborador']

    st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=select] span{
            max-width: 190px;
            font-size:0.88rem;
            background-color:#e9ecef;
            color:black;
        }
    </style>
    """, unsafe_allow_html=True)
    
    selected_options = st.multiselect("Selecione os **participantes** a considerar:",
        options=participants_by_company.unique(),
        default=participants_by_company.unique())
    # else:
    #     selected_options = container.multiselect("Selecione 1 ou mais participantes:",
    #         options=participants_by_company.unique())
        
    return selected_options
        



# generate random keys for data editor
def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
# --------------------------------------------
#             Cleaning DataFrames
# ---------------------------------------------

def format_file(df):

    #-------------------------------------------------
    #  FORMAT FILE
    #-------------------------------------------------

    # Return list with companies
    email_list=df["Email"]
    email_list=[x.lower() for x in email_list]
    email_list=[x.split('@') for x in email_list]
    email_list=[x[1].split('.') for x in email_list]
    df['Nome da Empresa']=[x[0].capitalize() for x in email_list]


    # Format employees names and e-mails
    df['Nome do colaborador']=[x.title() for x in df["Nome do colaborador"]]
    df['Email']=[x.lower() for x in df["Email"]]

    #Rename columns eliminating white spaces
    df.rename(columns={"Nome da Empresa":"Empresa","Nome do colaborador":"Colaborador"}, inplace=True)

    df['Hora de início']=pd.to_datetime(df['Hora de início'])
    df['Hora de conclusão']=pd.to_datetime(df['Hora de conclusão'])


    #-------------------------------------------------
    #  MERGE FILES
    #-------------------------------------------------

    # read complementary files
    transformations=pd.read_excel("Excel files/Transformações.xlsx",engine='openpyxl',sheet_name='tbl_transf_campo_perg')
    scores=pd.read_excel("Excel files/Transformações.xlsx",engine="openpyxl",sheet_name='pontuacao')


    # Build list of questions from answers file
    questions=list()
    for i in range(10,len(df.columns)):
        questions.append(df.columns[i])

    # replace double spaces with a single blank space in all the answers
    for q in questions:
        for i in range(0,len(df[q])):
            df.loc[i,q]=" ".join(df[q][i].split())
    

    # I want to create a new file (analysis_df) that will combine the answers 
    # given to each question(answers file) and the corresponding pontuation (scores file)

    # extrair colunas com respostas do ficheiro carregado e transpôr de forma a ser melhor interpretável
    answers_df=df.iloc[:,10:(len(df.columns)+1)]
    answers_transpose=answers_df.transpose() 

    answers_per_employee={} #dicionário que guarda uma lista das respostas dadas (value) para cada colaborador(key)
    for i in range(0,len(answers_transpose.columns)):
        respostas=[]
        respostas.extend(answers_transpose.iloc[:,i])
        answers_per_employee[df["Colaborador"][i]]=respostas
        
    # Define new columns
    names_column=[]
    empresa_column=[]
    answers_column=[]
    transf_column=[]
    campo_column=[]
    pergunta_column=[]
    question_category=[]

    #Create new columns 
    for k,v in answers_per_employee.items():
        names_column.extend(repeat(k,51))
        answers_column.extend(v)

    for i in df['Empresa']:
        empresa_column.extend(repeat(i,51))
    

    transf_column=list(transformations['Transformação'])*len(df['Colaborador'])
    campo_column=list(transformations['Campo'])*len(df['Colaborador'])
    pergunta_column=list(transformations['Pergunta'])*len(df['Colaborador'])
    question_category=list(transformations['Categoria'])*len(df['Colaborador'])

    df['Tempo de resposta']=(df['Hora de conclusão']-df['Hora de início'])


    #-------------------------------------------------
    #  CREATE TWO DATAFRAMES
    #-------------------------------------------------

    # PARTICIPANTS DATAFRAME
    participants_df=pd.DataFrame({
        'Colaborador':df['Colaborador'],
        'Email':df['Email'],
        'Empresa':df['Empresa'],
        'Hora de início':df['Hora de início'],
        'Hora de conclusão':df['Hora de conclusão'],
        'Tempo de resposta':df['Tempo de resposta']
    })


    # ANSWERS DATAFRAME
    new_df=pd.DataFrame({
        'Colaborador':names_column,
        'Empresa':empresa_column,
        'Transformação':transf_column,
        'Campo':campo_column,
        'Pergunta':pergunta_column,
        'Categoria':question_category,
        'Resposta':answers_column}
    )


    answers_dataframe=new_df.merge(scores,
                        left_on='Resposta',
                        right_on='Resposta',
                        how='left')
    
    answers_dataframe['Simulação']=answers_dataframe['Pontuação']

    # replace double spaces with a single blank space in all the questions
    answers_dataframe['Pergunta']=answers_dataframe['Pergunta'].str.strip()

    
    return participants_df,answers_dataframe


# --------------------------------------------
#                 RESULTADOS
# ---------------------------------------------
def calculate_mean(dataframe,company,participants):
    selection=dataframe.query("Empresa == @company and Colaborador== @participants")
    mean=round(selection['Pontuação'].mean(),2)

    return mean

def maturity_level(mean):
    if 1<=mean<=1.8:
        x='Baixo'
    elif mean<=2.6:
        x='Médio-Baixo'
    elif mean<=3.4:
        x='Médio'
    elif mean<4.2:
        x='Médio-Alto'
    else:
        x='Alto'
    return x

def average_per_transformation(df,company,participants):
    # create new dataframe
    transf=list(df['Transformação'].unique())
    transf_name=list(trans_name['Transformação_numero_nome'])

    mean_per_transf=[]
    for t in transf:
        selection=df.query("Empresa==@company and Transformação==@t and Colaborador==@participants")
        mean=round(selection['Pontuação'].mean(),2)
        mean_per_transf.append(mean)

    difference=[]
    for m in mean_per_transf:
        dif=4-m
        difference.append(dif)

    av_per_transf=pd.DataFrame(
        {'Nome Transformação':transf_name,
        'Transformação':transf,
         'Média':mean_per_transf,
         'Diferença para indústria do futuro':difference})

    return av_per_transf

def average_per_field(df):
    field=[]
    average=[]
    for campo in df['Campo'].unique(): # para cada campo
        df_select=df.where(df['Campo']==campo)['Pontuação'].dropna().tolist(),
        df_select=[item for sublist in df_select for item in sublist ]
        avg=round(mean(df_select),2) 
        sd=round(pstdev(df_select),2)

        field.append(campo)
        average.append(avg)

    new_df=pd.DataFrame({
        'Campo':field,
        'Média pontuação':average})

    return new_df


# --------------------------------------------
#                 SIMULAÇÃO
# ---------------------------------------------

# 1º criar função que origina uma nova dataframe com as colunas Empresa | Pergunta | Média pontuação | Pontuação Simulada
def average_per_question(df,participants):
    transf=[]
    campo=[]
    company=[]
    questions=[]
    average=[]
    var=[]
    standar_deviation=[]

    for e in df['Empresa'].unique():
        selection=df.query('Empresa==@e and Colaborador==@participants')

        for question in selection['Pergunta'].unique(): # para cada campo
            t=selection[selection['Pergunta']==question]['Transformação'].values[0]
            c=selection[selection['Pergunta']==question]['Campo'].values[0]
            df_select=selection.where(selection['Pergunta']==question)['Pontuação'].dropna().tolist(),
            df_select=[item for sublist in df_select for item in sublist ]

            avg=round(mean(df_select),2)
            v=round(variance(df_select),2) 
            sd=round(math.sqrt(v),2)

            questions.append(question)
            average.append(avg)
            company.append(e)
            transf.append(t)
            campo.append(c)
            var.append(v)
            standar_deviation.append(sd)


    new_df=pd.DataFrame({
        'Empresa':company,
        'Transformação':transf,
        'Campo':campo,
        'Pergunta':questions,
        'Variância':var,
        'Desvio Padrão':standar_deviation,
        'Média pontuação':average,
        'Simulação':average})

    return new_df

# 2º criar função que calcula a média total obtida a partir das médias por questão
def calculate_mean_using_question_avg(df,company):
    df=df.query("Empresa==@company")
    
    total_mean=round(mean(df['Média pontuação']),2)

    return  total_mean

def calculate_mean_simulation(df,company):
    df=df.query("Empresa==@company")
    
    total_mean=round(mean(df['Simulação']),2)

    return  total_mean








def best_transformations(df,company,participants):
    avg_per_transf=average_per_transformation(df,company,participants)

    biggest_two=avg_per_transf.nlargest(2,'Média')['Transformação'].tolist() # ['Transformação X','Transformação Y']
    transf_name=[]
    for i in biggest_two:
        transformation_name=trans_name.loc[trans_name['Transformação']==i,'Transformação_numero_nome']
        transf_name.append(transformation_name.item())

    return transf_name

def worst_transformations(df,company,participants):
    avg_per_transf=average_per_transformation(df,company,participants)


    lowest_two=avg_per_transf.nsmallest(2,'Média')['Transformação'].tolist() # ['Transformação X','Transformação Y']
    transf_name=[]
    for i in lowest_two:
        transformation_name=trans_name.loc[trans_name['Transformação']==i,'Transformação_numero_nome']
        transf_name.append(transformation_name.item())

    return transf_name

def calculate_variation(df):
    question=[]
    var=[]
    sd=[]
    questions=df['Pergunta'].unique()
    for q in questions:
        df_score_questions=df.where(df['Pergunta']==q)['Pontuação'].dropna().tolist(),
        df_score_questions=[item for sublist in df_score_questions for item in sublist ]

        v=round(variance(df_score_questions),2) 
        standard_dev=round(pstdev(df_score_questions),2)

        question.append(q)
        var.append(v)
        sd.append(standard_dev)
    
    new_df=pd.DataFrame({
        'Pergunta':question,
        'Variancia':var,
        'Desvio Padrão':sd
    })

    return new_df


def reset_sliders():
    st.session_state['slider_version']= +random.randint(1,100)


def pop_up(question_category):
    answers=scores.loc[scores['Categoria']==question_category,['Pontuação','Resposta']]
    return answers

def suggest_answer(question_category,simulated_score):
    answers=scores.loc[scores['Categoria']==question_category,['Pontuação','Resposta']]
    suggestion=answers.loc[scores['Pontuação']==round(simulated_score,0),['Resposta']].values[0][0]

    return suggestion

def highlight(val):
    if (val<datetime.timedelta(minutes=19)):
        return 'color: red'

    else:
        return ''



