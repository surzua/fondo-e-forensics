"""Componente de panel de control lateral (Sidebar) para el perfil del afiliado."""

import streamlit as st

from app.components.state import init_session_state
from src.config import (
    AFPS,
    RETIREMENT_AGE_MEN,
    RETIREMENT_AGE_WOMEN,
)


def render_affiliate_sidebar() -> None:
    """Renderiza los controles de entrada del afiliado en la barra lateral de Streamlit."""
    init_session_state()

    st.sidebar.markdown("### 👤 Panel de Control del Afiliado")
    st.sidebar.markdown(
        "<small style='color: #8B949E;'>Modifica tus parámetros para simular tu impacto patrimonial y recorte de pensión en tiempo real.</small>",
        unsafe_allow_html=True,
    )

    # Selector de Moneda para el Saldo
    moneda = st.sidebar.radio(
        "Moneda de Ingreso de Saldo:",
        options=["$ CLP (Pesos)", "UF (Unidades de Fomento)"],
        index=0,
        horizontal=True,
    )

    uf_val = st.session_state["uf_value"]

    if moneda == "$ CLP (Pesos)":
        saldo_clp = st.sidebar.number_input(
            "Saldo Actual en Fondo E ($ CLP):",
            min_value=1_000_000.0,
            max_value=2_000_000_000.0,
            value=float(st.session_state["saldo_clp"]),
            step=5_000_000.0,
            format="%.0f",
            help="Saldo total acumulado en tu cuenta obligatoria en el Fondo E.",
        )
        st.session_state["saldo_clp"] = saldo_clp
        st.sidebar.caption(f"Equivalente a: **{saldo_clp / uf_val:,.1f} UF** (UF = \\${uf_val:,.2f})")
    else:
        saldo_uf = st.sidebar.number_input(
            "Saldo Actual en Fondo E (UF):",
            min_value=25.0,
            max_value=50_000.0,
            value=float(st.session_state["saldo_clp"]) / uf_val,
            step=100.0,
            format="%.1f",
            help="Saldo en UF en el Fondo E.",
        )
        saldo_clp = saldo_uf * uf_val
        st.session_state["saldo_clp"] = saldo_clp
        st.sidebar.caption(f"Equivalente a: **\\${saldo_clp:,.0f} CLP**")

    # Selector de AFP
    afp_list = ["SISTEMA"] + AFPS
    current_afp = st.session_state["afp_selected"]
    afp_index = afp_list.index(current_afp) if current_afp in afp_list else 1

    afp_selected = st.sidebar.selectbox(
        "Tu Administradora (AFP):",
        options=afp_list,
        index=afp_index,
        help="Permite aplicar la tasa de pérdida y daño por swaps específico de tu AFP.",
    )
    st.session_state["afp_selected"] = afp_selected

    # Sexo biológico y edad legal
    sexo_col1, sexo_col2 = st.sidebar.columns(2)
    with sexo_col1:
        sexo_str = st.selectbox(
            "Sexo (Tablas RV-2020):",
            options=["Hombre", "Mujer"],
            index=0 if st.session_state["sexo"] == "hombre" else 1,
        )
        st.session_state["sexo"] = "hombre" if sexo_str == "Hombre" else "mujer"

    with sexo_col2:
        edad_legal = RETIREMENT_AGE_MEN if st.session_state["sexo"] == "hombre" else RETIREMENT_AGE_WOMEN
        st.metric("Edad Legal", f"{edad_legal} años")

    # Edad actual y retiro
    edad_actual = st.sidebar.slider(
        "Edad Actual:",
        min_value=40,
        max_value=75,
        value=int(st.session_state["edad_actual"]),
        step=1,
    )
    st.session_state["edad_actual"] = edad_actual

    edad_jubilacion = st.sidebar.slider(
        "Edad Planificada de Jubilación:",
        min_value=max(edad_actual, 50),
        max_value=80,
        value=max(int(st.session_state["edad_jubilacion"]), edad_actual),
        step=1,
    )
    st.session_state["edad_jubilacion"] = edad_jubilacion

    # Sueldo Imponible Mensual
    sueldo = st.sidebar.number_input(
        "Sueldo Imponible Mensual ($ CLP):",
        min_value=0.0,
        max_value=10_000_000.0,
        value=float(st.session_state["sueldo_imponible"]),
        step=100_000.0,
        format="%.0f",
        help="Base para calcular el 10% de cotización legal obligatoria mensual.",
    )
    st.session_state["sueldo_imponible"] = sueldo
    st.sidebar.caption(f"Cotización obligatoria (10%): **\\${sueldo * 0.10:,.0f} CLP/mes**")

    # Tasa Técnica de Descuento
    tasa_tec = st.sidebar.slider(
        "Tasa Técnica de Descuento Actuarial:",
        min_value=1.5,
        max_value=5.0,
        value=float(st.session_state["tasa_tecnica"] * 100.0),
        step=0.1,
        format="%.1f%%",
        help="Tasa oficial de cálculo de retiros programados y rentas vitalicias (SPensiones/CMF).",
    )
    st.session_state["tasa_tecnica"] = tasa_tec / 100.0

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size: 0.75rem; color: #6E7681; line-height: 1.4;'>"
        "<b>Auditoría Forense Fondo E</b><br>"
        "Microdatos oficiales SPensiones, Banco Central y Federal Reserve.<br>"
        "Fase 4 — Octubre 2026."
        "</div>",
        unsafe_allow_html=True,
    )
