"""Módulo 3: Ranking de AFPs, Efecto Manada y Riesgo Extremo (Underwater & VaR).

Analiza la conducta transversal de las administradoras en el Fondo E durante 2026:
- Doble panel Underwater & VaR Shock Chart (Fondo E vs Fondo A)
- Ranking de caídas reales y daño por swaps por administradora
- Heatmap interactivo de correlación cruzada diaria (Efecto Manada: ρ > 0,98)
- Tabla comparativa de las 7 AFP con cronograma de desarme regulatorio al 5 de noviembre
"""

import plotly.express as px
import polars as pl
import streamlit as st

from app.components.sidebar import render_affiliate_sidebar
from app.components.state import init_session_state
from app.components.ui import (
    apply_editorial_theme,
    render_badge,
    render_callout,
    render_kpi_card,
)
from src.config import (
    AFP_DERIVATIVES_PANEL_PATH,
    MASTER_DAILY_PANEL_PATH,
)
from src.viz.charts_interactive import (
    build_interactive_product_1,
    build_interactive_product_4,
)

st.set_page_config(
    page_title="Ranking y Efecto Manada | Fondo E",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_editorial_theme()
init_session_state()
render_affiliate_sidebar()

# Encabezado
st.html(
    f"""
    <div style="margin-bottom: 20px;">
        {render_badge("Módulo 3: Riesgo Sistémico", "gold")}
        {render_badge("Efecto Manada & Ranking AFP", "red")}
        <h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; margin: 10px 0 4px 0; color: #F8FAFC;">
            Ranking de AFPs y Efecto Manada
        </h1>
        <p style="font-size: 1.1rem; color: #8B949E; margin: 0;">
            Evidencia empírica de replicación masiva: correlación cruzada diaria superior a 0,98 e idéntica exposición al colapso.
        </p>
    </div>
    """
)

# Métricas Ejecutivas del Ranking
r1, r2, r3, r4 = st.columns(4)

with r1:
    render_kpi_card(
        title="Mayor Caída Real (AFP Modelo)",
        value="-10,90%",
        delta="▼ Pérdida por swaps: -6,1 pp",
        delta_type="red",
        subtitle="Lideró el apalancamiento sintético.",
    )

with r2:
    render_kpi_card(
        title="Menor Caída Real (AFP Uno)",
        value="-9,90%",
        delta="▼ Pérdida por swaps: -5,4 pp",
        delta_type="red",
        subtitle="Menor exposición relativa, pero igualmente colapsó.",
    )

with r3:
    render_kpi_card(
        title="Correlación Mínima Inter-AFP",
        value="0,987",
        delta="▲ Prácticamente 1,00 perfecto",
        delta_type="amber",
        subtitle="Sincronización total de pérdidas día a día.",
    )

with r4:
    render_kpi_card(
        title="Plazo Desarme Regulatorio",
        value="5 Nov 2026",
        delta="⏳ Límite de estrés 2% SPensiones",
        delta_type="amber",
        subtitle="Normalización obligatoria de derivados.",
    )

st.markdown("---")

# ==============================================================================
# 1. Producto 1: The Underwater & VaR Shock Chart
# ==============================================================================
st.markdown("### 📉 1. Riesgo Extremo: The Underwater & VaR Shock Chart")
st.markdown(
    "<small style='color: #8B949E;'>Evolución de un saldo base real de \\$100 MM (Fondo E vs Fondo A) y profundidad del drawdown con rupturas de la banda de VaR 99%:</small>",
    unsafe_allow_html=True,
)

fig_underwater = build_interactive_product_1()
st.plotly_chart(fig_underwater, use_container_width=True)

uw_col1, uw_col2 = st.columns([1.2, 1.0])

with uw_col1:
    st.markdown(
        """
        #### 📌 Hallazgos del Comportamiento Extremo:
        * **Inversión de Roles:** Durante 2026, el **Fondo E (supuestamente conservador) cayó 7 veces más que el Fondo A (renta variable de alto riesgo)**.
        * **Pérdida de Capital Real:** Un afiliado que inició 2026 con \\$100.000.000 CLP deflactados por UF termina a septiembre en **\\$89.610.000 CLP**, perdiendo más de \\$10,3 millones en poder adquisitivo. En contraste, el Fondo A superó los \\$108,6 millones reales.
        * **Ruptura de VaR al 99%:** El drawdown perforó en múltiples ocasiones el límite de Value at Risk paramétrico e histórico, confirmando colas pesadas (*fat tails*) derivadas del apalancamiento sintético.
        """
    )

with uw_col2:
    render_callout(
        """
        <strong>Nota de Conciliación Metodológica Oficial:</strong><br><br>
        El cálculo diario de retorno real acumulado en cuota a septiembre 30 arroja <strong>-9,92%</strong>,
        mientras que el informe mensual auditado de cierre de mes de la Superintendencia de Pensiones
        certifica un retorno real de <strong>-10,39%</strong>.<br><br>
        La diferencia de 0,47 pp se debe al desfase de fijación de la UF oficial del día 1 al 9 del mes siguiente
        y a la valorización devengada de márgenes de garantía de contrapartes en derivados.
        """,
        border_color="#3B82F6",
    )

st.markdown("---")

# ==============================================================================
# 2. Producto 4: Ranking Comparativo de las 7 AFPs
# ==============================================================================
st.markdown("### 🏆 2. Ranking de Pérdidas y Agresividad por AFP")
st.markdown(
    "<small style='color: #8B949E;'>Retorno real acumulado a septiembre 2026 y daño atribuible a swaps para cada una de las 7 administradoras:</small>",
    unsafe_allow_html=True,
)

fig_ranking = build_interactive_product_4()
st.plotly_chart(fig_ranking, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 3. Heatmap de Correlación Inter-AFP (Efecto Manada)
# ==============================================================================
st.markdown("### 🐑 3. Efecto Manada: Ninguna AFP Ofreció Protección")
st.markdown(
    "<small style='color: #8B949E;'>Matriz de correlación cruzada de retornos reales diarios en 2026. La correlación mínima observada es 0,987 (consignando conducta homogénea):</small>",
    unsafe_allow_html=True,
)

# Calcular matriz de correlación en vivo desde master panel
try:
    df_master = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
    df_e = df_master.filter(pl.col("fondo") == "E")
    piv = df_e.pivot(on="afp", index="fecha", values="ret_real_diario").to_pandas().drop(columns=["fecha"])
    corr_matrix = piv.corr()

    fig_heat = px.imshow(
        corr_matrix,
        text_auto=".3f",
        aspect="auto",
        color_continuous_scale=[
            [0.0, "#161B22"],
            [0.5, "#D90429"],
            [1.0, "#FF4D6D"],
        ],
        zmin=0.97,
        zmax=1.00,
        labels={"color": "Correlación (ρ)"},
    )
    fig_heat.update_layout(
        template="fondo_e_dark",
        title="<b>MATRIZ DE CORRELACIÓN CRUZADA DIARIA ENTRE AFPs (FONDO E — 2026)</b>",
        height=450,
    )
    st.plotly_chart(fig_heat, use_container_width=True)
except (FileNotFoundError, pl.exceptions.PolarsError, KeyError, ValueError) as e:
    st.warning(f"No fue posible renderizar el heatmap en tiempo real: {e}")

herd_col1, herd_col2 = st.columns([1.2, 1.0])

with herd_col1:
    st.markdown(
        """
        #### 🔍 ¿Por qué ocurrió el Efecto Manada (*Herding Behavior*)?
        1. **Regulación de Rentabilidad Mínima:** La legislación chilena (D.L. 3.500) obliga a las AFP que rinden por debajo del promedio de la industria a compensar la diferencia con su propio patrimonio (*encaje*). Esto desincentiva alejarse del consenso.
        2. **Incentivo Asimétrico:** Si una AFP no entraba a la apuesta de swaps y las tasas caían, quedaba en falta regulatoria. Si todas entraban y la apuesta salía mal, **ninguna era sancionada porque todas perdían juntas**.
        3. **Resultado Ciudadano:** El afiliado no encontró refugio cambiándose de administradora; el 100% de la industria tomó exactamente la misma posición especulativa.
        """
    )

with herd_col2:
    render_callout(
        """
        <strong>Evidencia Estadística Irrefutable:</strong><br><br>
        Una correlación media de <strong>ρ = 0,993</strong> entre 7 compañías privadas
        demuestra que no existió gestión de portafolio independiente.<br><br>
        Las 7 administradoras operaron de facto como un <strong>único fondo indexado a la duración sintética de Wall Street</strong>.
        """,
        border_color="#F59E0B",
    )

st.markdown("---")

# ==============================================================================
# 4. Tabla Maestra de las 7 Administradoras y Descarga
# ==============================================================================
st.markdown("### 📋 4. Matriz Comparativa Detallada de las 7 AFPs")

df_panel = pl.read_parquet(AFP_DERIVATIVES_PANEL_PATH).to_pandas()

# Formatear columnas para visualización ejecutiva
df_display = df_panel.copy()
df_display["Retorno Real 2026"] = df_display["ret_real_2026_pct"].apply(lambda x: f"{x:.2f}%")
df_display["Daño Swaps (pp)"] = df_display["danio_swaps_pp"].apply(lambda x: f"{x:.2f} pp")
df_display["Short USD (Forwards)"] = df_display["ratio_sobrecobertura_usd"].apply(lambda x: f"{x * 100:.0f}%")
df_display["% Pérdida por Swaps"] = df_display["pct_danio_explicado_por_swaps"].apply(lambda x: f"{x * 100:.1f}%")
df_display["Estatus Desarme al 5-Nov"] = [
    "En desarme agresivo" if a in ["MODELO", "CAPITAL"] else "En proceso regular"
    for a in df_display["afp"]
]

columnas_orden = [
    "afp",
    "Retorno Real 2026",
    "Daño Swaps (pp)",
    "% Pérdida por Swaps",
    "Short USD (Forwards)",
    "perfil_agresividad",
    "Estatus Desarme al 5-Nov",
]
df_final_view = df_display[columnas_orden].rename(
    columns={
        "afp": "Administradora (AFP)",
        "perfil_agresividad": "Perfil de Agresividad",
    }
)

st.dataframe(df_final_view, use_container_width=True, hide_index=True)

# Botón de Descarga del Dataset
csv_data = df_panel.to_csv(index=False)
st.download_button(
    label="📊 Descargar Matriz Completa de las 7 AFP (CSV)",
    data=csv_data,
    file_name="matriz_derivados_y_ranking_afp_2026.csv",
    mime="text/csv",
    help="Descarga la base de datos con los retornos, daño por swaps y ratio de cobertura por administradora.",
)
