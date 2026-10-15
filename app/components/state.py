"""Gestor de estado global y perfiles de afiliado en Streamlit (session_state)."""

import polars as pl
import streamlit as st

from src.config import (
    DEFAULT_TECHNICAL_RATE,
    MASTER_DAILY_PANEL_PATH,
)
from src.schemas import ActuarialProfile

DEFAULT_UF = 39536.53


def get_latest_uf_value() -> float:
    """Obtiene el último valor oficial de la UF desde el panel maestro o fallback."""
    try:
        if MASTER_DAILY_PANEL_PATH.exists():
            df = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
            return float(df["uf"].tail(1)[0])
    except (FileNotFoundError, pl.exceptions.PolarsError, KeyError, IndexError):
        return DEFAULT_UF
    return DEFAULT_UF


def init_session_state() -> None:
    """Inicializa las variables del perfil del afiliado en el session_state si no existen."""
    if "uf_value" not in st.session_state:
        st.session_state["uf_value"] = get_latest_uf_value()

    if "saldo_clp" not in st.session_state:
        st.session_state["saldo_clp"] = 100_000_000.0

    if "afp_selected" not in st.session_state:
        st.session_state["afp_selected"] = "MODELO"

    if "edad_actual" not in st.session_state:
        st.session_state["edad_actual"] = 63

    if "sexo" not in st.session_state:
        st.session_state["sexo"] = "hombre"

    if "edad_jubilacion" not in st.session_state:
        st.session_state["edad_jubilacion"] = 65

    if "sueldo_imponible" not in st.session_state:
        st.session_state["sueldo_imponible"] = 1_500_000.0

    if "tasa_tecnica" not in st.session_state:
        st.session_state["tasa_tecnica"] = DEFAULT_TECHNICAL_RATE


def get_actuarial_profile() -> ActuarialProfile:
    """Construye un objeto ActuarialProfile a partir de las variables actuales de session_state."""
    init_session_state()
    return ActuarialProfile(
        saldo_actual_clp=float(st.session_state["saldo_clp"]),
        afp=str(st.session_state["afp_selected"]),
        edad_actual=int(st.session_state["edad_actual"]),
        sexo=str(st.session_state["sexo"]),
        edad_jubilacion=int(st.session_state["edad_jubilacion"]),
        sueldo_imponible=float(st.session_state["sueldo_imponible"]),
        tasa_tecnica=float(st.session_state["tasa_tecnica"]),
    )
