"""Módulo 1: Calculadora de Daño Patrimonial e Impacto Actuarial.

Permite simular el impacto personalizado del desplome del Fondo E en 2026:
- Pérdida en saldo ($ CLP) y atribución por swaps
- Recorte vitalicio permanente en pensión mensual (Tablas oficiales RV-2020)
- Simulación estocástica de Monte Carlo (10.000 trayectorias) para estimar meses de trabajo forzado adicional
"""

import streamlit as st

from app.components.report import generate_audit_csv, generate_audit_report_html
from app.components.sidebar import render_affiliate_sidebar
from app.components.state import get_actuarial_profile, init_session_state
from app.components.ui import (
    apply_editorial_theme,
    render_badge,
    render_callout,
    render_kpi_card,
)
from src.config import (
    AFP_REAL_RETURNS_2026,
    OFFICIAL_REAL_RETURN_2026,
)
from src.models.actuarial import ActuarialEngine
from src.models.attribution import get_afp_attribution_table
from src.viz.charts_interactive import build_interactive_product_5

st.set_page_config(
    page_title="Calculadora Actuarial | Auditoría Fondo E",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_editorial_theme()
init_session_state()
render_affiliate_sidebar()

profile = get_actuarial_profile()

# Encabezado
st.markdown(
    f"""
    <div style="margin-bottom: 20px;">
        {render_badge("Módulo 1: Gancho Ciudadano", "cyan")}
        {render_badge(f"AFP: {profile.afp}", "gold")}
        <h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; margin: 10px 0 4px 0; color: #F8FAFC;">
            Calculadora de Daño Patrimonial y Actuarial
        </h1>
        <p style="font-size: 1.1rem; color: #8B949E; margin: 0;">
            Cuantificación individualizada del recorte vitalicio de pensión y meses de postergación del retiro.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inicializar motor actuarial
engine = ActuarialEngine()

# Determinar shock específico según AFP
if profile.afp in AFP_REAL_RETURNS_2026:
    afp_real_ret = AFP_REAL_RETURNS_2026[profile.afp]
else:
    afp_real_ret = OFFICIAL_REAL_RETURN_2026

# Atribución por swaps de la AFP
try:
    df_afp_attr = get_afp_attribution_table().to_pandas()
    row_afp = df_afp_attr[df_afp_attr["afp"] == profile.afp]
    if not row_afp.empty:
        afp_swaps_pp = float(row_afp["total_swaps_pp"].iloc[0])
    else:
        afp_swaps_pp = -5.90
except (KeyError, ValueError, FileNotFoundError, IndexError):
    afp_swaps_pp = -5.90

# Evaluar impacto actuarial base
impact = engine.evaluate_profile_impact(profile, shock_pct=afp_real_ret)

# ==============================================================================
# 1. Cuatro KPIs Superiores con Deltas
# ==============================================================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    render_kpi_card(
        title="Pérdida Patrimonial Total",
        value=f"-${impact.perdida_patrimonial_clp:,.0f}",
        delta=f"▼ {afp_real_ret * 100:.2f}% retorno real 2026",
        delta_type="red",
        subtitle=f"Saldo cayó de ${impact.saldo_inicial_estimado:,.0f} a ${impact.saldo_post_shock:,.0f}.",
    )

with kpi2:
    render_kpi_card(
        title="Pérdida Atribuible a Swaps",
        value=f"-${impact.perdida_swaps_clp:,.0f}",
        delta=f"▼ {afp_swaps_pp:.2f} pp causados por derivados",
        delta_type="red",
        subtitle=f"Aproximadamente 80% de la caída nominal en AFP {profile.afp}.",
    )

with kpi3:
    render_kpi_card(
        title="Recorte Permanente de Pensión",
        value=f"-${impact.recorte_pension_mensual:,.0f}",
        delta=f"▼ {impact.recorte_pension_pct:.2f}% de por vida",
        delta_type="red",
        subtitle=f"Pensión cae de ${impact.pension_pre_shock_mensual:,.0f} a ${impact.pension_post_shock_mensual:,.0f}/mes.",
    )

with kpi4:
    meses_p50 = impact.monte_carlo_meses_recuperacion_p50
    anios_extra = meses_p50 / 12.0 if meses_p50 else 0.0
    render_kpi_card(
        title="Meses de Trabajo Adicional",
        value=f"{meses_p50:.0f} meses",
        delta=f"▲ {anios_extra:.1f} años de retraso",
        delta_type="amber",
        subtitle="Mediana P50 de Monte Carlo con cotización legal del 10%.",
    )

st.markdown("---")

# ==============================================================================
# 2. Simulación de Monte Carlo Interactiva (Fan Chart)
# ==============================================================================
st.markdown("### 🎲 Simulación Estocástica de Recuperación Patrimonial (Monte Carlo)")
st.markdown(
    "<small style='color: #8B949E;'>Modela 10.000 trayectorias aleatorias mensuales de evolución de saldo incorporando tu cotización legal obligatoria (10% de tu sueldo imponible). Ajusta las expectativas de retorno futuro:</small>",
    unsafe_allow_html=True,
)

ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 1])

with ctrl1:
    ret_futuro_pct = st.slider(
        "Retorno Real Anual Futuro Esperado del Fondo E:",
        min_value=1.0,
        max_value=6.0,
        value=3.0,
        step=0.25,
        format="%.2f%%",
        help="Supuesto de rentabilidad real anual promedio de la renta fija post-crisis.",
    )
    ret_futuro = ret_futuro_pct / 100.0

with ctrl2:
    vol_futura_pct = st.slider(
        "Volatilidad Anual Esperada (σ):",
        min_value=2.0,
        max_value=8.0,
        value=4.0,
        step=0.5,
        format="%.1f%%",
        help="Dispersión anualizada de retornos. La volatilidad histórica del Fondo E ronda el 3%-5%.",
    )
    vol_futura = vol_futura_pct / 100.0

with ctrl3:
    sueldo_aporte = profile.sueldo_imponible * 0.10
    st.metric(
        "Aporte Mensual de Ahorro",
        f"${sueldo_aporte:,.0f} CLP/mes",
        f"10% de ${profile.sueldo_imponible:,.0f}",
    )

# Ejecutar Monte Carlo dinámico con los parámetros del usuario
mc_custom = engine.simulate_recovery_monte_carlo(
    current_balance_clp=impact.saldo_post_shock,
    target_balance_clp=impact.saldo_inicial_estimado,
    monthly_contribution_clp=sueldo_aporte,
    n_sims=10000,
    max_months=120,
    annual_expected_return=ret_futuro,
    annual_volatility=vol_futura,
)

# Renderizar Fan Chart interactivo
fig_mc = build_interactive_product_5(
    current_balance=impact.saldo_post_shock,
    target_balance=impact.saldo_inicial_estimado,
    salary=profile.sueldo_imponible,
    annual_expected_return=ret_futuro,
    annual_volatility=vol_futura,
)

st.plotly_chart(fig_mc, use_container_width=True)

# Percentiles de Monte Carlo
mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)

with mc_col1:
    st.metric(
        "Escenario Optimista (P10)",
        f"{mc_custom['p10_meses']:.0f} meses",
        f"{mc_custom['p10_meses'] / 12:.1f} años",
    )

with mc_col2:
    st.metric(
        "Mediana Esperada (P50)",
        f"{mc_custom['p50_mediana_meses']:.0f} meses",
        f"{mc_custom['p50_mediana_meses'] / 12:.1f} años",
    )

with mc_col3:
    st.metric(
        "Escenario Conservador (P90)",
        f"{mc_custom['p90_meses']:.0f} meses",
        f"{mc_custom['p90_meses'] / 12:.1f} años",
    )

with mc_col4:
    st.metric(
        "No Recupera en 10 años",
        f"{mc_custom['pct_no_recupera_en_horizonte']:.1f}%",
        "Probabilidad empírica",
    )

st.markdown("---")

# ==============================================================================
# 3. Desglose Actuarial y Tablas de Mortalidad RV-2020
# ==============================================================================
st.markdown("### 📑 Desglose Actuarial y Parámetros del Cálculo")

tab_col1, tab_col2 = st.columns([1.2, 1.0])

with tab_col1:
    st.markdown(
        f"""
        | Parámetro Actuarial | Valor Aplicado | Descripción / Base Legal |
        | :--- | :--- | :--- |
        | **Tabla de Mortalidad** | `RV-2020` | Tabla oficial CMF / SPensiones para pensiones de vejez. |
        | **Capital Necesario Unitario (CNU)** | `{impact.cnu:.4f} años` | Anualidad anticipada mensual ajustada por Woolhouse y sobrevivencia. |
        | **Tasa Técnica de Descuento** | `{profile.tasa_tecnica * 100:.2f}% real anual` | Tasa oficial vigente para retiro programado y renta vitalicia. |
        | **Edad de Jubilación Evaluada** | `{profile.edad_jubilacion} años` | Sexo: {profile.sexo.capitalize()} (Edad legal: 65H / 60M). |
        | **Pensión Estimada Pre-Shock** | `${impact.pension_pre_shock_mensual:,.0f} CLP/mes` | Pensión vitalicia autofinanciada antes del desplome 2026. |
        | **Pensión Actual Post-Shock** | `${impact.pension_post_shock_mensual:,.0f} CLP/mes` | Pensión vitalicia calculada con el saldo auditado actual. |
        | **Recorte Mensual Definitivo** | `-${impact.recorte_pension_mensual:,.0f} CLP/mes` | **Pérdida vitalicia irreversible** si el afiliado se jubila hoy. |
        """
    )

with tab_col2:
    render_callout(
        f"""
        <strong>¿Por qué el recorte es permanente?</strong><br><br>
        En el sistema previsional chileno, el monto de la pensión (tanto en Retiro Programado como en Renta Vitalicia)
        se calcula dividiendo el saldo acumulado por el factor <code>12 × CNU</code>.<br><br>
        Al sufrir una pérdida de <strong>{afp_real_ret * 100:.2f}%</strong> a meses de jubilarse, el capital base disminuye en
        <strong>${impact.perdida_patrimonial_clp:,.0f} CLP</strong>. A diferencia de un afiliado joven que dispone de décadas
        para recuperarse, un trabajador en el tramo de 60 a 65 años <strong>consolida la pérdida de por vida</strong>
        a menos que postergue su retiro por <strong>{meses_p50:.0f} meses</strong>.
        """,
        border_color="#FF4D6D",
    )

st.markdown("---")

# ==============================================================================
# 4. Descarga de Informes Personalizados
# ==============================================================================
st.markdown("### 📥 Exportar Reporte de Auditoría Personalizado")
st.markdown(
    "<small style='color: #8B949E;'>Descarga tu informe forense con membrete ejecutivo, listo para presentar, archivar o imprimir como PDF, o exporta la planilla con todas las variables en CSV:</small>",
    unsafe_allow_html=True,
)

html_report = generate_audit_report_html(
    profile=profile,
    impact=impact,
    afp_real_return_pct=afp_real_ret * 100.0,
    afp_swaps_damage_pp=afp_swaps_pp,
)

csv_report = generate_audit_csv(
    profile=profile,
    impact=impact,
    afp_real_return_pct=afp_real_ret * 100.0,
    afp_swaps_damage_pp=afp_swaps_pp,
)

btn_col1, btn_col2, btn_spacer = st.columns([1.2, 1.2, 2.0])

with btn_col1:
    st.download_button(
        label="📄 Descargar Informe Ejecutivo (HTML / PDF)",
        data=html_report,
        file_name=f"informe_auditoria_fondo_e_afp_{profile.afp.lower()}_{profile.edad_actual}anios.html",
        mime="text/html",
        help="Abre el archivo descargado en cualquier navegador y presiona Ctrl+P (o Cmd+P) para guardar como PDF profesional.",
    )

with btn_col2:
    st.download_button(
        label="📊 Descargar Datos del Cálculo (CSV)",
        data=csv_report,
        file_name=f"datos_auditoria_fondo_e_{profile.afp.lower()}.csv",
        mime="text/csv",
        help="Descarga la planilla estructurada para abrir en Excel o Google Sheets.",
    )
