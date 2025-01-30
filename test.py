import streamlit as st
import plotly.graph_objects as go

# Dados de exemplo
x_labels = ["Rótulo muito longo 1", "Rótulo muito longo 2", "Outro rótulo muito longo"]
y_values = [10, 20, 30]

# Criar o gráfico
fig = go.Figure(data=[go.Bar(x=x_labels, y=y_values)])
fig.update_layout(
    xaxis=dict(
        automargin=True,  # Ativar margens automáticas
        tickmode='array', 
        ticktext=[label.replace(" ", "<br>") for label in x_labels],  # Quebra com HTML
        tickvals=x_labels
    )
)

# Mostrar no Streamlit
st.plotly_chart(fig)
