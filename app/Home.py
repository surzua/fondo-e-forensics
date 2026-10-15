"""Página Principal / Landing Ejecutiva de la Plataforma de Auditoría Forense.

Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")
"""

import streamlit as st

from app.components.sidebar import render_affiliate_sidebar
from app.components.state import init_session_state
from app.components.ui import (
    apply_editorial_theme,
    render_callout,
    render_kpi_card,
)

st.set_page_config(
    page_title="Auditoría Fondo E | La Falacia del Fondo Seguro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_editorial_theme()
init_session_state()
render_affiliate_sidebar()

# Encabezado Principal
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="badge-forensic badge-red">AUDITORÍA FORENSE CUANTITATIVA</span>
        <span class="badge-forensic badge-cyan">DATOS CERTIFICADOS OCTUBRE 2026</span>
        <h1 style="font-size: 2.6rem; font-weight: 800; letter-spacing: -0.03em; margin: 12px 0 6px 0; color: #F8FAFC;">
            La Falacia del Fondo Seguro
        </h1>
        <p style="font-size: 1.25rem; color: #8B949E; margin: 0; line-height: 1.4;">
            Análisis Forense del Colapso Patrimonial del Fondo E y la Crisis de los Swaps de Tasas en las AFP
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4 KPIs Superiores de Nivel Sistema
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    render_kpi_card(
        title="Retorno Real Oficial 2026",
        value="-10,39%",
        delta="▼ Caída 7x mayor que Fondo A",
        delta_type="red",
        subtitle="Cierre oficial auditado SPensiones a sep-2026.",
    )

with kpi2:
    render_kpi_card(
        title="Daño Atribuible a Swaps",
        value="-5,90 pp",
        delta="▼ 79,7% de la pérdida nominal total",
        delta_type="red",
        subtitle="Swaps EE.UU. (-4,5 pp) + Locales (-1,4 pp).",
    )

with kpi3:
    render_kpi_card(
        title="Duración Total Efectiva",
        value="17,0 Años",
        delta="▲ 3,4x sobre duración histórica (5a)",
        delta_type="amber",
        subtitle="10,2a bonos locales + 6,8a swaps sintéticos.",
    )

with kpi4:
    render_kpi_card(
        title="Efecto Manada Inter-AFP",
        value="ρ > 0,98",
        delta="▲ 100% de la industria replicó la apuesta",
        delta_type="amber",
        subtitle="Correlación cruzada diaria perfecta entre las 7 AFP.",
    )

st.markdown("---")

# Resumen Ejecutivo y Bloque de Alerta Regulatoria
col_text, col_alert = st.columns([1.5, 1.0])

with col_text:
    st.markdown("### 📋 Síntesis de la Investigación")
    st.markdown(
        """
        El **Fondo E** fue diseñado por ley como el refugio de máxima seguridad del sistema previsional chileno,
        destinado a preservar el capital de los trabajadores a meses de pensionarse. Sin embargo, en 2026 sufrió un
        **desplome histórico de -10,39% en términos reales**, destruyendo los ahorros de miles de pensionados y superando
        con creces las pérdidas de los fondos más riesgosos.

        Nuestra auditoría cuantitativa en base a los microdatos diarios de carteras y valores cuota revela que esta catástrofe
        **no fue producto de la renta fija tradicional**, sino de una transformación silenciosa hacia el apalancamiento sintético:
        
        * **Crecimiento desmedido en Swaps:** Entre agosto de 2023 y diciembre de 2025, el valor nocional en derivados de tasas de interés externas se disparó **40 veces**, pasando de **US$ 5.300 millones a US$ 206.900 millones**.
        * **Sensibilidad de Tasa Extrema:** La duración combinada alcanzó **17,0 años**. Cuando el Bono del Tesoro de EE.UU. a 10 años (US10Y) subió de **4,18% a 5,29%**, la cartera sufrió una pérdida masiva.
        * **Trampa de Sobrecobertura Cambiaria:** Al vender dólares a futuro al **150%**, las AFP anularon el amortiguador cambiario natural del dólar cuando subió de $911 a $970 CLP, multiplicando el daño.
        """
    )

with col_alert:
    st.markdown("### ⚖️ Contexto Regulatorio")
    render_callout(
        """
        <strong>Oficio Reservado e Instrucción SPensiones:</strong><br><br>
        Ante el riesgo sistémico de liquidez y márgenes de garantía, la Superintendencia de Pensiones impuso un
        <strong>límite de estrés del 2% del valor del fondo</strong> para pérdidas proyectadas en derivados.<br><br>
        📅 <strong>Plazo Límite de Desarme: 5 de Noviembre de 2026.</strong><br>
        Todas las administradoras están obligadas a desmantelar aceleradamente sus posiciones sintéticas,
        cristalizando pérdidas multimillonarias en las cuentas individuales.
        """,
        border_color="#D90429",
    )

st.markdown("---")

# Guía Interactiva hacia los 3 Módulos
st.markdown("### 🧭 Explora los Módulos de Auditoría")
st.markdown("<small style='color:#8B949E;'>Selecciona un módulo en el menú lateral de páginas o haz clic a continuación:</small>", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 2rem; margin-bottom: 8px;">🧮</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                1. Calculadora Actuarial
            </div>
            <div style="font-size: 0.88rem; color: #8B949E; line-height: 1.45; margin-bottom: 14px;">
                Simula tu caso personal: calcula el recorte permanente en tu pensión mensual vitalicia (tablas RV-2020) y los meses de trabajo forzado adicional requeridos mediante Monte Carlo.
            </div>
            <a href="Calculadora_Actuarial" target="_self" style="text-decoration: none; color: #2EC4B6; font-weight: 600; font-size: 0.9rem;">
                Ir a la Calculadora →
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 2rem; margin-bottom: 8px;">🔍</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                2. Auditoría Swaps y Derivados
            </div>
            <div style="font-size: 0.88rem; color: #8B949E; line-height: 1.45; margin-bottom: 14px;">
                Descomposición factorial en cascada (Waterfall), escalada del apalancamiento sintético a US$ 206,9B, duración de 17 años y la trampa de los forwards cortos en dólares al 150%.
            </div>
            <a href="Auditoria_Derivados_y_Swaps" target="_self" style="text-decoration: none; color: #2EC4B6; font-weight: 600; font-size: 0.9rem;">
                Ver Auditoría Forense →
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav3:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 2rem; margin-bottom: 8px;">📊</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                3. Ranking y Efecto Manada
            </div>
            <div style="font-size: 0.88rem; color: #8B949E; line-height: 1.45; margin-bottom: 14px;">
                Gráfico Underwater & rupturas de VaR 99%, heatmap de correlación entre administradoras (ρ > 0,98) y ranking de pérdidas liderado por AFP Modelo y Capital.
            </div>
            <a href="Ranking_y_Efecto_Manada_AFP" target="_self" style="text-decoration: none; color: #2EC4B6; font-weight: 600; font-size: 0.9rem;">
                Ver Ranking de AFPs →
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    """
    <div style="font-size: 0.8rem; color: #6E7681; text-align: center; margin-top: 30px;">
        <b>Fuentes de Datos Certificadas:</b> Superintendencia de Pensiones de Chile (Carteras y Valores Cuota), Banco Central de Chile (Informes de Estabilidad Financiera), Federal Reserve Bank of St. Louis (FRED), Servicio de Impuestos Internos (UF diaria).<br>
        Investigación Cuantitativa y Forense Previsional — Todos los derechos reservados © 2026.
    </div>
    """,
    unsafe_allow_html=True,
)
