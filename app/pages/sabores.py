import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def color_sign(v):
    if pd.isna(v):
        return ""
    if v > 0:
        return "color: #2a9d8f"   # green
    if v < 0:
        return "color: #d62839"   # red
    return ""

sabores = pd.read_excel('Caso_Analista_Base_Datos_1.xlsx', 'Sabores Monster')
sabores_y = sabores

sabores_y['Year'] = np.where(sabores['Periodo'] <= '2025-09-01', '2025', '2026') #Add column tagging accordingly 2025 or 2026
sabores['Zero Sugar'] = np.where(sabores['Periodo'] < '2026-03-01', 'Pre', 'Post') #Add column tagging accordingly Pre or Post

sabores_ventas = sabores.groupby(['Sabor', 'Zero Sugar']).agg({
    "Ventas Valor ($000)": "mean",
    "Ventas Unidades (000)": "mean",
    "DN": "mean",
    "DP": "mean"
}).reset_index() #Group all data by flavor and Pre/Post Zero Sugar launch tag

sabores_ventas['Sales Share (without Zero Sugar)'] = sabores_ventas[sabores_ventas['Sabor'] != 'Monster Zero Sugar']['Ventas Valor ($000)'] / sabores_ventas[sabores_ventas['Sabor'] != 'Monster Zero Sugar'].groupby('Zero Sugar')['Ventas Valor ($000)'].transform('sum')
sabores_ventas['Sales Share (with Zero Sugar)'] = sabores_ventas['Ventas Valor ($000)'] / sabores_ventas.groupby('Zero Sugar')['Ventas Valor ($000)'].transform('sum')

sabores_cambio = sabores_ventas.pivot(index= 'Sabor', columns= 'Zero Sugar')

metric_filter = st.sidebar.selectbox('Select a metric to evaluate:', options= ['Ventas Valor ($000)', 'Ventas Unidades (000)', 'Sales Share (without Zero Sugar)', 'Sales Share (with Zero Sugar)', 'DN', 'DP'])

fig = px.bar(sabores_cambio[metric_filter], y= ['Pre', 'Post'], barmode= 'group', labels={'variable': '', 'value': metric_filter})
fig.update_traces(textposition="outside")
if metric_filter in ['Ventas Valor ($000)', 'Ventas Unidades (000)']:
    fig.update_traces(texttemplate= '%{y:,.2f}')
else:
    fig.update_traces(texttemplate= '%{y:.2f}%')
st.subheader(f'{metric_filter} promedio mensual Pre y Post lanzamiento de Zero Sugar')
st.plotly_chart(fig)

canib = sabores_ventas[['Sabor', 'Zero Sugar', 'Sales Share (with Zero Sugar)']].pivot(index= 'Sabor', columns= 'Zero Sugar')
canib['Sales Share Change'] = (canib['Sales Share (with Zero Sugar)']['Post'] - canib['Sales Share (with Zero Sugar)']['Pre'])
canib = canib.iloc[:-1]
canib_chart = canib['Sales Share Change'].reset_index().style.format({'Sales Share Change': '{:+.2%}'}).map(color_sign, subset= ['Sales Share Change'])

st.subheader('Canibalización de Zero Sugar')
st.dataframe(canib_chart, use_container_width= False, hide_index= True)
