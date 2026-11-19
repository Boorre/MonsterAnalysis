import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots

emb = pd.read_excel('Caso_Analista_Base_Datos_1.xlsx', 'Embarques')
ventas = pd.read_excel('Caso_Analista_Base_Datos_1.xlsx', 'Marca')

emb_fil = emb
emb_fil['Embarques Unidades (000)'] = emb_fil['Embarques (cajas 000)'] * 24
ventas_fil = ventas[(ventas['Marca'] == 'Monster') | (ventas['Marca'] == 'Predator')][['Embotellador', 'Periodo', 'Marca', 'Ventas Unidades (000)']]
ventas_fil = ventas_fil.groupby(['Embotellador', 'Periodo', 'Marca']).agg({'Ventas Unidades (000)': 'sum'}).reset_index()

final = pd.merge(emb_fil, ventas_fil, on= ['Embotellador', 'Periodo', 'Marca'], how= 'inner')
final.rename(columns= {'Embarques Unidades (000)': 'Sell-in', 'Ventas Unidades (000)': 'Sell-out'}, inplace= True)

final['New Stock-in-trade'] = final['Sell-in'] - final['Sell-out']

for dist, marca in zip(final['Embotellador'], final['Marca']):
    final.loc[(final['Embotellador'] == dist) & (final['Marca'] == marca), 'Avg WSO'] = final[(final['Embotellador'] == dist) & (final['Marca'] == marca)]['Sell-out'].mean() / 4
    final.loc[(final['Embotellador'] == dist) & (final['Marca'] == marca), 'Stock-in-trade'] = final[(final['Embotellador'] == dist) & (final['Marca'] == marca)]['New Stock-in-trade'].cumsum()

final = final[['Embotellador', 'Periodo', 'Marca', 'Embarques (cajas 000)', 'Sell-in', 'Sell-out', 'Avg WSO', 'New Stock-in-trade', 'Stock-in-trade']]

dist_filter = st.sidebar.selectbox('Select a distributor:', options= np.append('All', final['Embotellador'].unique()))
marca_filter = st.sidebar.selectbox('Select a brand:', options= ['All', 'Monster', 'Predator'])

final_to_plot = final[(final['Embotellador'] == dist_filter) & (final['Marca'] == marca_filter)]

if dist_filter == 'All' and marca_filter == 'All':
    final_to_plot = final.groupby(['Periodo']).sum().reset_index()
elif dist_filter == 'All':
    final_to_plot = final.groupby(['Periodo', 'Marca']).sum().reset_index()
    final_to_plot = final_to_plot[final_to_plot['Marca'] == marca_filter]
elif marca_filter == 'All':
    final_to_plot = final.groupby(['Periodo', 'Embotellador']).sum().reset_index()
    final_to_plot = final_to_plot[final_to_plot['Embotellador'] == dist_filter]
else:
    final_to_plot = final[(final['Embotellador'] == dist_filter) & (final['Marca'] == marca_filter)]

# fig1 = px.line(
#     final_to_plot,
#     x= 'Periodo',
#     y= ['Sell-in', 'Sell-out'],
#     markers= True
# )

# fig2 = px.area(
#     final_to_plot,
#     x= 'Periodo',
#     y= ['Stock-in-trade']
# )

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                    subplot_titles=("Sell-in vs Sell-out", "Stock-in-trade"))

fig.add_scatter(x=final_to_plot["Periodo"], y=final_to_plot["Sell-in"], name="Sell-in", mode="lines+markers", row=1, col=1)
fig.add_scatter(x=final_to_plot["Periodo"], y=final_to_plot["Sell-out"], name="Sell-out", mode="lines+markers", row=1, col=1)
fig.add_scatter(x=final_to_plot["Periodo"], y=final_to_plot["Stock-in-trade"], name="Stock-in-trade",
                fill="tozeroy", row=2, col=1)

fig.update_layout(height=600)
st.plotly_chart(fig)

fig0 = px.scatter(
    final_to_plot,
    x= 'Periodo',
    y= 'Sell-out',
    title= 'Ventas (miles de unidades)',
    trendline= 'ols'
)
st.plotly_chart(fig0)
final_to_df = final[['Embotellador', 'Marca', 'Avg WSO']].drop_duplicates()
#st.dataframe(final_to_df, use_container_width= False, hide_index= True)

col3, col4 = st.columns(2)
with col3:
    st.subheader('Weekly Sell-out promedio para Monster 2025 y 2026 (miles de unidades)')
    st.dataframe(final_to_df[final_to_df['Marca'] == 'Monster'].drop(columns=['Marca']), use_container_width= False, hide_index= True)

with col4:
    st.subheader('Weekly Sell-out promedio para Predator 2025 y 2026 (miles de unidades)')
    st.dataframe(final_to_df[final_to_df['Marca'] == 'Predator'].drop(columns=['Marca']), use_container_width= False, hide_index= True)

best_price = ventas[['Embotellador', 'Canal', 'Periodo', 'Marca', 'Ventas Valor ($000)', 'Ventas Unidades (000)']]
best_price = best_price[(best_price['Embotellador'] != 'México Total') & ((best_price['Marca'] == 'Monster') | (best_price['Marca'] == 'Predator'))]
best_price['Precio Promedio'] = best_price['Ventas Valor ($000)'] / best_price['Ventas Unidades (000)']
best_price_26 = best_price[best_price['Periodo'] >= '2025-10-01']
bp26_to_df = best_price_26.groupby(['Embotellador', 'Marca']).agg({'Precio Promedio': 'mean'}).reset_index()
bp26_to_df_monster = bp26_to_df[bp26_to_df['Marca'] == 'Monster'].sort_values(by= 'Precio Promedio', ascending= False)
bp26_to_df_predator = bp26_to_df[bp26_to_df['Marca'] == 'Predator'].sort_values(by= 'Precio Promedio', ascending= False)
bp26_to_df_monster['Precio Promedio'] = bp26_to_df_monster['Precio Promedio'].apply(lambda x: f"${x:,.2f}")
bp26_to_df_predator['Precio Promedio'] = bp26_to_df_predator['Precio Promedio'].apply(lambda x: f"${x:,.2f}")

col1, col2 = st.columns(2)
with col1:
    st.subheader('Precio promedio para Monster 2026')
    st.dataframe(bp26_to_df_monster.drop(columns=['Marca']), use_container_width= False, hide_index= True)

with col2:
    st.subheader('Precio promedio para Predator 2026')
    st.dataframe(bp26_to_df_predator.drop(columns=['Marca']), use_container_width= False, hide_index= True)
