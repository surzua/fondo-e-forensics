"""Componentes de interfaz, estilos CSS editoriales y widgets visuales."""

import streamlit as st

EDITORIAL_CSS = """
<style>
    /* Estilos Generales y Tipografía */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Fondo principal y espaciado */
    .stApp {
        background-color: #0D1117;
        color: #F8FAFC;
    }

    /* Tarjetas ejecutivas KPI */
    .kpi-card {
        background: linear-gradient(145deg, #161B22 0%, #1A2230 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #D90429;
    }

    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #8B949E;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
        line-height: 1.1;
    }

    .kpi-delta {
        font-size: 0.88rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .delta-red {
        color: #FF4D6D;
    }

    .delta-green {
        color: #2EC4B6;
    }

    .delta-amber {
        color: #F59E0B;
    }

    .kpi-subtitle {
        font-size: 0.78rem;
        color: #6E7681;
        margin-top: 6px;
        line-height: 1.3;
    }

    /* Insignias de auditoría */
    .badge-forensic {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-right: 6px;
    }

    .badge-red {
        background: rgba(217, 4, 41, 0.18);
        color: #FF4D6D;
        border: 1px solid rgba(217, 4, 41, 0.4);
    }

    .badge-cyan {
        background: rgba(46, 196, 182, 0.15);
        color: #2EC4B6;
        border: 1px solid rgba(46, 196, 182, 0.35);
    }

    .badge-gold {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    /* Caja de llamada explicativa */
    .callout-box {
        background-color: #161B22;
        border-left: 4px solid #D90429;
        border-radius: 4px 8px 8px 4px;
        padding: 16px 20px;
        margin: 16px 0;
        font-size: 0.92rem;
        line-height: 1.55;
        color: #C9D1D9;
    }

    .callout-box strong {
        color: #F8FAFC;
    }

    /* Tablas estilizadas */
    .dataframe {
        border-collapse: collapse !important;
        width: 100% !important;
        background-color: #161B22 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* Botones de acción */
    .stDownloadButton button, .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
</style>
"""


def apply_editorial_theme() -> None:
    """Inyecta la hoja de estilos CSS editorial en la página actual."""
    st.html(EDITORIAL_CSS)


def render_kpi_card(
    title: str,
    value: str,
    delta: str,
    delta_type: str = "red",
    subtitle: str = "",
) -> None:
    """Renderiza una tarjeta KPI con diseño financiero de alta fidelidad."""
    delta_class = f"delta-{delta_type}"
    sub_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ""
    html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-delta {delta_class}"><span>{delta}</span></div>'
        f'{sub_html}'
        f'</div>'
    )
    st.html(html)


def render_badge(text: str, color: str = "red") -> str:
    """Genera el HTML para una insignia de categoría."""
    return f'<span class="badge-forensic badge-{color}">{text}</span>'


def render_callout(text: str, border_color: str = "#D90429") -> None:
    """Renderiza un bloque explicativo con borde izquierdo de acento usando HTML nativo."""
    clean_lines = [line.strip() for line in text.strip().splitlines()]
    clean_text = "".join(clean_lines)
    html = f'<div class="callout-box" style="border-left-color: {border_color};">{clean_text}</div>'
    st.html(html)
