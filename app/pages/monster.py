import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

marcas = pd.read_excel('Caso_Analista_Base_Datos_1.xlsx', 'Marca')
sabores = pd.read_excel('C:/Users/Rodrigo/Documents/Monster/Caso_Analista_Base_Datos_1.xlsx', 'Sabores Monster')
emb = pd.read_excel('C:/Users/Rodrigo/Documents/Monster/Caso_Analista_Base_Datos_1.xlsx', 'Embarques')

# amper25 = marcas[(marcas['Marca'] == 'Amper') & (marcas['Periodo'] <= '2025-09-01')]
# amper26 = marcas[(marcas['Marca'] == 'Amper') & (marcas['Periodo'] > '2025-09-01')]
# boost25 = marcas[(marcas['Marca'] == 'Boost') & (marcas['Periodo'] <= '2025-09-01')]
# boost26 = marcas[(marcas['Marca'] == 'Boost') & (marcas['Periodo'] > '2025-09-01')]
# monster25 = marcas[(marcas['Marca'] == 'Monster') & (marcas['Periodo'] <= '2025-09-01')]
# monster26 = marcas[(marcas['Marca'] == 'Monster') & (marcas['Periodo'] > '2025-09-01')]
# predator25 = marcas[(marcas['Marca'] == 'Predator') & (marcas['Periodo'] <= '2025-09-01')]
# predator26 = marcas[(marcas['Marca'] == 'Predator') & (marcas['Periodo'] > '2025-09-01')]
# redbull25 = marcas[(marcas['Marca'] == 'Red Bull') & (marcas['Periodo'] <= '2025-09-01')]
# redbull26 = marcas[(marcas['Marca'] == 'Red Bull') & (marcas['Periodo'] > '2025-09-01')]
# sting25 = marcas[(marcas['Marca'] == 'Sting') & (marcas['Periodo'] <= '2025-09-01')]
# sting26 = marcas[(marcas['Marca'] == 'Sting') & (marcas['Periodo'] > '2025-09-01')]
# vive25 = marcas[(marcas['Marca'] == 'Vive 100') & (marcas['Periodo'] <= '2025-09-01')]
# vive26 = marcas[(marcas['Marca'] == 'Vive 100') & (marcas['Periodo'] > '2025-09-01')]
# volt25 = marcas[(marcas['Marca'] == 'Volt') & (marcas['Periodo'] <= '2025-09-01')]
# volt26 = marcas[(marcas['Marca'] == 'Volt') & (marcas['Periodo'] > '2025-09-01')]
# other25 = marcas[(marcas['Marca'] == 'Otras marcas') & (marcas['Periodo'] <= '2025-09-01')]
# other26 = marcas[(marcas['Marca'] == 'Otras marcas') & (marcas['Periodo'] > '2025-09-01')]


marcas['Year'] = np.where(marcas['Periodo'] <= '2025-09-01', '2025', '2026') #Add column tagging accordingly 2025 or 2026
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
growth_filtered['Change'] = (growth_filtered['2026'] / growth_filtered['2025'] - 1)
#st.bar_chart(data= growth_filtered, y= 'Change')

#Plot YoY side by side
fig1 = px.bar(growth_filtered, y= ['2025', '2026'], barmode= 'group', text_auto= ',.2f', category_orders= {'Marca': ['MEC', 'Monster', 'Predator', 'Total']})
fig1.update_traces(textposition="outside")
st.subheader(f'Total de {metric_filter} de 2025 y 2026')
st.plotly_chart(fig1)

#Plot YoY change
fig = px.bar(growth_filtered, y= 'Change', text_auto= '.2%', category_orders= {'Marca': ['MEC', 'Monster', 'Predator', 'Total']})
fig.update_traces(textposition="outside")
st.subheader(f'Cambio en {metric_filter} de 2025 a 2026 (%)')
st.plotly_chart(fig)


#print(marcas[marcas['Periodo'] == '2025-10-01'])
#print(sabores)
#print(emb)