"""Módulo 2: Auditoría Forense de Derivados, Swaps y Sensibilidad de Duración.

Descompone la mecánica financiera que ocasionó el desplome del Fondo E en 2026:
- Descomposición factorial aditiva (Gráfico Waterfall)
- Escalada del nocional en swaps (US$ 5,3B a US$ 206,9B) y duración combinada de 17 años
- La trampa de la sobrecobertura cambiaria (Forwards USD al 150%)
- El límite regulatorio de estrés del 2% y el plazo de desarme al 5 de noviembre
"""

import streamlit as st

from app.components.sidebar import render_affiliate_sidebar
from app.components.state import init_session_state
from app.components.ui import (
    apply_editorial_theme,
    render_badge,
    render_callout,
    render_kpi_card,
)
from src.models.attribution import (
    calculate_duration_sensitivity,
    get_official_attribution_breakdown,
)
from src.viz.charts_interactive import (
    build_interactive_product_2,
    build_interactive_product_3,
)

st.set_page_config(
    page_title="Auditoría de Derivados | Fondo E",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_editorial_theme()
init_session_state()
render_affiliate_sidebar()

# Encabezado
st.markdown(
    f"""
    <div style="margin-bottom: 20px;">
        {render_badge("Módulo 2: Auditoría Forense", "red")}
        {render_badge("Derivados & Riesgo Financiero", "gold")}
        <h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; margin: 10px 0 4px 0; color: #F8FAFC;">
            ¿Por Qué Cayó el Fondo Seguro?
        </h1>
        <p style="font-size: 1.1rem; color: #8B949E; margin: 0;">
            Descomposición cuantitativa de pérdidas: Swaps de tasas en EE.UU., duración sintética de 17 años y sobrecobertura cambiaria corta.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Métricas Principales de Atribución
attr = get_official_attribution_breakdown()
sens = calculate_duration_sensitivity()

m1, m2, m3, m4 = st.columns(4)

with m1:
    render_kpi_card(
        title="Nocional Pico en Swaps",
        value="US$ 206,9 B",
        delta="▲ 40x desde ago-2023",
        delta_type="amber",
        subtitle="Monto nocional contratado en swaps de tasas.",
    )

with m2:
    render_kpi_card(
        title="Daño Total por Swaps",
        value=f"{attr['total_swaps_pp']:.2f} pp",
        delta="▼ 79,7% de la pérdida nominal",
        delta_type="red",
        subtitle="Swaps EE.UU. (-4,5 pp) + Swaps locales (-1,4 pp).",
    )

with m3:
    render_kpi_card(
        title="Salto Tasa US Treasury 10Y",
        value="+111 bps",
        delta="▲ De 4,18% a 5,29%",
        delta_type="amber",
        subtitle="Rendimiento del bono soberano estadounidense.",
    )

with m4:
    render_kpi_card(
        title="Ratio Cobertura USD",
        value="150%",
        delta="▼ Sobrecobertura corta neta",
        delta_type="red",
        subtitle="Venta de dólares a futuro que anuló el colchón cambiario.",
    )

st.markdown("---")

# ==============================================================================
# 1. Gráfico Waterfall de Atribución Factorial
# ==============================================================================
st.markdown("### 🌊 1. Descomposición Factorial Aditiva de Pérdidas")
st.markdown(
    "<small style='color: #8B949E;'>Cada barra representa la contribución exacta en puntos porcentuales al retorno acumulado de 2026. Los bonos físicos tradicionales solo explican -0,7 pp de la caída.</small>",
    unsafe_allow_html=True,
)

fig_waterfall = build_interactive_product_2()
st.plotly_chart(fig_waterfall, use_container_width=True)

wf_col1, wf_col2 = st.columns([1.3, 1.0])

with wf_col1:
    st.markdown(
        f"""
        | Factor / Instrumento Financiero | Contribución (pp) | % del Daño Nominal | Naturaleza del Riesgo |
        | :--- | :---: | :---: | :--- |
        | **Swaps Tasas Extranjeras (USD)** | `{attr['swaps_tasas_usd_pp']:+.2f} pp` | **60,8%** | Posición pagadora de tasa fija ante salto del US10Y. |
        | **Swaps Tasas Locales (CLP/UF)** | `{attr['swaps_tasas_locales_pp']:+.2f} pp` | **18,9%** | Contratos de tasas locales en Cámara y BCP. |
        | **Forwards Cambiarios USD (Short)** | `{attr['forwards_fx_pp']:+.2f} pp` | **10,8%** | Pérdida al subir el dólar de $911 a $970 con posición corta al 150%. |
        | **Bonos Físicos (RF Local/Ext)** | `{attr['bonos_fisicos_pp']:+.2f} pp` | **9,5%** | Deuda soberana chilena tradicional de bajo riesgo. |
        | **Subtotal Retorno Nominal** | `{attr['retorno_nominal_total_pct']:.2f}%` | **100,0%** | Retorno nominal antes del ajuste de inflación. |
        | **Arrastre de Inflación (Variación UF)** | `{attr['arrastre_inflacion_uf_pp']:+.2f} pp` | — | Pérdida de poder adquisitivo por inflación del período (+3,34%). |
        | **Retorno Real Total Auditado** | `{attr['retorno_real_total_pct']:.2f}%` | — | **Cierre oficial auditado por la Superintendencia de Pensiones.** |
        """
    )

with wf_col2:
    render_callout(
        """
        <strong>Hallazgo Clave de la Descomposición:</strong><br><br>
        Si las administradoras hubiesen mantenido el Fondo E invertido exclusivamente en
        <strong>bonos físicos tradicionales</strong> (como estipulaba su filosofía conservadora original),
        el fondo solo habría caído <strong>-0,70 pp nominales</strong>.<br><br>
        El <strong>90,5% restante de la pérdida nominal (-6,7 pp de -7,4%)</strong> fue provocado por la
        ingeniería financiera de <strong>derivados sintéticos (Swaps y Forwards)</strong>.
        """,
        border_color="#D90429",
    )

st.markdown("---")

# ==============================================================================
# 2. Termómetro de Duración y Escalada de Swaps
# ==============================================================================
st.markdown("### 🌡️ 2. La Escalada del Apalancamiento Sintético (2023–2026)")
st.markdown(
    "<small style='color: #8B949E;'>Evolución temporal del monto nocional contratado en swaps y la duración efectiva combinada de la cartera:</small>",
    unsafe_allow_html=True,
)

fig_thermometer = build_interactive_product_3()
st.plotly_chart(fig_thermometer, use_container_width=True)

dur_col1, dur_col2 = st.columns(2)

with dur_col1:
    st.markdown(
        f"""
        #### 📐 Sensibilidad Matemática de Duración y Convexidad
        La variación de precio ante cambios en la tasa de interés se modela mediante la expansión de Taylor:
        
        $$\\frac{{\\Delta P}}{{P}} \\approx -D_{{\\text{{total}}}} \\cdot \\Delta y + \\frac{{1}}{{2}} \\cdot C \\cdot (\\Delta y)^2$$
        
        * **Duración Física (Bonos Locales UF):** `10,2 años`
        * **Duración Sintética (Swaps USD):** `6,8 años`
        * **Duración Total Efectiva:** **`17,0 años`**
        * **Salto de Tasa Evaluado ($\\Delta y$):** `+111 puntos básicos` (+1,11%)
        
        Con una duración histórica de **5,0 años**, la pérdida estimada por tasas habría sido de solo **{sens['impacto_duracion_historica_pct']:.2f}%**.
        Sin embargo, al extender la duración a **17,0 años**, el impacto teórico se disparó a **{sens['impacto_teorico_con_convexidad_pct']:.2f}%**,
        generando una sobresensibilidad artificial de **{sens['sobre_sensibilidad_generada_pct']:.2f} pp**.
        """
    )

with dur_col2:
    render_callout(
        """
        <strong>¿Por qué tomaron una duración de 17 años en el Fondo más conservador?</strong><br><br>
        Las mesas de dinero de las AFP apostaron agresivamente a que la Reserva Federal (Fed) recortaría
        las tasas de interés de forma acelerada durante 2026. Al extender la duración a 17 años con swaps sintéticos,
        buscaban amplificar las ganancias de capital cuando las tasas bajaran.<br><br>
        <strong>El desenlace opuesto:</strong> La inflación persistente en EE.UU. forzó a la Fed a mantener una postura restrictiva
        y la tasa del bono del tesoro escaló hasta <strong>5,29%</strong>, convirtiendo la apuesta en una trampa de pérdidas masivas.
        """,
        border_color="#F59E0B",
    )

st.markdown("---")

# ==============================================================================
# 3. La Trampa de la Sobrecobertura Cambiaria (Forwards USD al 150%)
# ==============================================================================
st.markdown("### 💱 3. La Trampa de la Sobrecobertura Cambiaria (Forwards USD al 150%)")

fx_col1, fx_col2 = st.columns([1.2, 1.0])

with fx_col1:
    st.markdown(
        """
        En condiciones normales, la inversión en el extranjero cuenta con un **amortiguador cambiario natural**:
        cuando los mercados financieros internacionales caen, el dólar tiende a apreciarse en Chile (efecto "vuelo a la calidad").
        Al subir el tipo de cambio USD/CLP, la ganancia por conversión de moneda compensa parte de la caída en el precio del activo externo.

        **¿Qué hicieron las AFP?**
        1. Tomaron posiciones cortas en derivados de tipo de cambio (*Forwards USD/CLP*) con un ratio de cobertura del **150% del valor de los activos externos**.
        2. Al vender futuros de dólares por un monto 1,5 veces superior a sus tenencias reales, **anularon por completo el amortiguador cambiario** y asumieron una posición neta apostando a la apreciación del peso chileno.
        3. Cuando el dólar en Chile escaló de **$911 a $970 CLP** (+6,5%), las posiciones en forwards sufrieron liquidaciones forzosas, **restando -0,80 pp adicionales** al retorno del fondo.
        """
    )

with fx_col2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Mecánica del Desastre Cambiario</div>
            <div style="font-size: 1.05rem; line-height: 1.6; color: #C9D1D9; margin-top: 10px;">
                <span style="color:#2EC4B6;">● Activo Externo Cae</span> → Pérdida en Bonos/Swaps.<br>
                <span style="color:#F59E0B;">● Dólar Sube ($911 → $970)</span> → Debería haber mitigado la pérdida.<br>
                <span style="color:#FF4D6D;">● Posición Corta al 150%</span> → El alza del dólar <b>multiplica las pérdidas</b> en lugar de frenarlas.<br>
                <hr style="border-color: #30363D; margin: 12px 0;">
                <b>Resultado Neto:</b> Daño directo de <b>-0,80 pp</b> en el Fondo E.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==============================================================================
# 4. El Límite Regulatorio de Estrés y el Desarme al 5 de Noviembre
# ==============================================================================
st.markdown("### ⚖️ 4. El Oficio de la SPensiones y el Plazo Fatal al 5 de Noviembre")

st.markdown(
    """
    Hacia septiembre de 2026, la acumulación desmedida de derivados encendió las alertas en el Banco Central y la Superintendencia de Pensiones.
    El volumen de garantías líquidas (*collateral calls*) exigido por las contrapartes internacionales en Wall Street amenazaba con forzar
    la liquidación desordenada de bonos locales.

    * **La Regla del 2% de Estrés:** La Superintendencia dictaminó que ninguna administradora podía mantener una exposición en derivados cuya pérdida proyectada bajo escenarios de estrés severo superara el **2% del valor total del fondo**.
    * **Desapalancamiento Forzado:** Para cumplir la normativa, las AFP iniciaron un desarme masivo de swaps, vendiendo contratos a precios deprimidos.
    * **Plazo Fatal (5 de Noviembre de 2026):** Todas las posiciones deben estar plenamente normalizadas en esa fecha. Esta venta obligada en bloque cristalizó las pérdidas en las cuentas individuales de los afiliados justo antes de su jubilación.
    """
)
