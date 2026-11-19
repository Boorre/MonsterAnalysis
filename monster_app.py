import streamlit as st

st.set_page_config(page_title='Desempeño Monster Energy Corporation 2026', page_icon= '⚡', layout= 'wide')

pages = st.navigation([
    st.Page('pages/marcas.py', title= 'Competencia', icon= '🏷️'),
    st.Page('pages/sabores.py', title= 'Sabores', icon= '🍹'),
    st.Page('pages/distribuidores.py', title= 'Distribuidores', icon= '📦')
])

st.markdown(
    """
    <div style="background-color: #1E3A8A; padding: 14px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
        <span style="color: white; font-size: 18px; font-weight: 600;">
            All data used was fabricated for this exercise.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

pages.run()