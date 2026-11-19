import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

#st.set_page_config(layout="wide")

marcas = pd.read_excel('Caso_Analista_Base_Datos_1.xlsx', 'Marca')

marcas['Year'] = np.where(marcas['Periodo'] <= '2025-09-01', 2025, 2026) #Add column tagging accordingly 2025 or 2026
marcas_ventas = marcas.groupby(['Marca', 'Year']).agg({
    "Ventas Valor ($000)": "sum",
    "Ventas Unidades (000)": "sum",
    "DN": "mean",
    "DP": "mean",
    "SOV": "mean",
    "SOCI": "mean",
    "SOVI": "mean",
    "DN Cold": "mean"
}).reset_index() #Group all data by brand and year tag

#Adding together Monster and Predator to create MEC (Monster Energy Corp.)
mec = marcas_ventas[(marcas_ventas['Marca'] == 'Monster') | (marcas_ventas['Marca'] == 'Predator')].groupby('Year').agg({
    "Ventas Valor ($000)": "sum",
    "Ventas Unidades (000)": "sum",
    "DN": "mean",
    "DP": "mean",
    "SOV": "mean",
    "SOCI": "mean",
    "SOVI": "mean",
    "DN Cold": "mean"
}).reset_index()
mec['Marca'] = 'MEC'

#Adding together all brands to get a sense of the complete energy drink market development
marcas_global = marcas.groupby('Year').agg({
    "Ventas Valor ($000)": "sum",
    "Ventas Unidades (000)": "sum",
    "DN": "mean",
    "DP": "mean",
    "SOV": "mean",
    "SOCI": "mean",
    "SOVI": "mean",
    "DN Cold": "mean"
}).reset_index()
marcas_global['Marca'] = 'Total'

marcas_ventas = pd.concat([marcas_ventas, mec, marcas_global], ignore_index= True) #Merging new data with original

growth = marcas_ventas.pivot(index= 'Marca', columns= 'Year') #Reorder per brand
metric_filter = 'Ventas Valor ($000)' #Set default filter selection
metric_filter = st.sidebar.selectbox('Select a metric to evaluate:', options= marcas.columns[4:12])

growth_filtered = growth[metric_filter]
growth_filtered['Change'] = (growth_filtered[2026] / growth_filtered[2025] - 1)
#st.bar_chart(data= growth_filtered, y= 'Change')

#Plot YoY side by side
fig1 = px.bar(growth_filtered, y= [2025, 2026], labels={'variable': 'Año', 'value': metric_filter}, barmode= 'group', text_auto= ',.2f', category_orders= {'Marca': ['Total', 'MEC', 'Monster', 'Red Bull', 'Boost', 'Predator', 'Amper', 'Sting', 'Vive 100', 'Volt', 'Otras marcas']})
fig1.update_traces(textposition="outside")
st.subheader(f'Total de {metric_filter} de 2025 y 2026')
st.plotly_chart(fig1)

#Plot YoY change
fig = px.bar(growth_filtered, y= 'Change', text_auto= '.2%', category_orders= {'Marca': ['Total', 'MEC', 'Monster', 'Red Bull', 'Boost', 'Predator', 'Amper', 'Sting', 'Vive 100', 'Volt', 'Otras marcas']})
fig.update_traces(textposition="outside")
st.subheader(f'Cambio en {metric_filter} de 2025 a 2026 (%)')
st.plotly_chart(fig)

to_pie = marcas_ventas[(marcas_ventas['Year'] == 2026) & ~(marcas_ventas['Marca'].isin(['MEC', 'Total']))]

colors = {
    "Monster": "#2E9E44",
    "Predator": "#7A1F1F",
    "Red Bull": "#1F3A93",
    "Volt": "#F2A900",
    "Amper": "#E4572E",
    "Vive 100": "#8E44AD",
    "Boost": "#17A2B8",
    "Sting": "#C0392B",
    "Otras marcas": "#9AA5B1",
}

fig2 = px.pie(
    to_pie,
    names= to_pie['Marca'],
    values= to_pie['SOV']
)

fig2.update_traces(
    textinfo="label+percent",           # name and percentage on each slice
    textposition="inside",
    insidetextorientation="horizontal", # keeps the text from rotating
    textfont=dict(size=14, color="white"),
)
fig2.update_layout(showlegend=False)

st.subheader('Share of Voice 2026', text_alignment= 'center')
st.plotly_chart(fig2)
