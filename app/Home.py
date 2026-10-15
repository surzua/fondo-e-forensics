"""Página principal de la aplicación interactiva Streamlit.

Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")
"""

import streamlit as st

st.set_page_config(
    page_title="Auditoría Fondo E | La Falacia del Fondo Seguro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏛️ Auditoría Cuantitativa del Fondo E")
st.subheader("La Falacia del Fondo Seguro: Análisis Forense del Colapso 2026")

st.markdown(
    """
    Bienvenido al ecosistema de auditoría del Fondo E de las AFP en Chile.
    Esta plataforma permite auditar con microdatos oficiales cómo el fondo supuestamente
    más conservador sufrió un colapso de **-10,39% real a septiembre de 2026**.

    Utiliza el menú lateral para navegar por los diferentes módulos de análisis:
    - **1. Calculadora de Daño Actuarial:** Estima la pérdida patrimonial y recorte vitalicio de pensión.
    - **2. Auditoría de Derivados y Swaps:** Descomposición factorial de pérdidas y duración sintética.
    - **3. Ranking y Efecto Manada AFP:** Comparativa transversal entre las 7 administradoras.
    """
)

st.info("Plataforma en inicialización. Ejecute el pipeline de datos para cargar las cifras auditadas.")
