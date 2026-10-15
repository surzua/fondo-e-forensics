"""Configuración de temas visuales y estilos editoriales (Financial Times / Bloomberg Dark Mode).

Provee configuración para Matplotlib, Seaborn y plantillas Plotly de alto contraste
para su uso en publicaciones de LinkedIn, blogs y la aplicación en Streamlit.
"""

from __future__ import annotations

from typing import Any, Dict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

from src.config import PALETTE


def setup_matplotlib_theme() -> None:
    """Configura los parámetros globales de Matplotlib (rcParam) para estética editorial."""
    plt.style.use("default")
    
    custom_params: Dict[str, Any] = {
        "figure.facecolor": PALETTE["background_dark"],
        "axes.facecolor": PALETTE["surface_dark"],
        "axes.edgecolor": PALETTE["border_dark"],
        "axes.labelcolor": PALETTE["text_primary"],
        "axes.labelsize": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.grid": True,
        "grid.color": PALETTE["grid_color"],
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "xtick.color": PALETTE["text_muted"],
        "ytick.color": PALETTE["text_muted"],
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "text.color": PALETTE["text_primary"],
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Roboto", "DejaVu Sans", "Helvetica", "Arial"],
        "legend.facecolor": PALETTE["surface_dark"],
        "legend.edgecolor": PALETTE["border_dark"],
        "legend.fontsize": 10,
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.facecolor": PALETTE["background_dark"],
        "savefig.edgecolor": PALETTE["background_dark"],
        "savefig.bbox": "tight",
    }
    
    plt.rcParams.update(custom_params)


def get_plotly_template() -> go.layout.Template:
    """Retorna una plantilla personalizada de Plotly optimizada para Dark Mode editorial."""
    template = go.layout.Template()
    
    template.layout = go.Layout(
        font=dict(
            family="Inter, Roboto, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
            color=PALETTE["text_primary"],
            size=12,
        ),
        paper_bgcolor=PALETTE["background_dark"],
        plot_bgcolor=PALETTE["surface_dark"],
        colorway=[
            PALETTE["swaps_loss"],
            PALETTE["forwards_loss"],
            PALETTE["bonds_physical"],
            PALETTE["fondo_a"],
            PALETTE["deposit"],
            PALETTE["fondo_e"],
        ],
        title=dict(
            font=dict(
                size=18,
                color=PALETTE["text_primary"],
            ),
            x=0.02,
            xanchor="left",
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=PALETTE["grid_color"],
            gridwidth=1,
            zeroline=True,
            zerolinecolor=PALETTE["border_dark"],
            linecolor=PALETTE["border_dark"],
            tickfont=dict(color=PALETTE["text_muted"], size=10),
            title=dict(font=dict(color=PALETTE["text_primary"], size=12)),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=PALETTE["grid_color"],
            gridwidth=1,
            zeroline=True,
            zerolinecolor=PALETTE["border_dark"],
            linecolor=PALETTE["border_dark"],
            tickfont=dict(color=PALETTE["text_muted"], size=10),
            title=dict(font=dict(color=PALETTE["text_primary"], size=12)),
        ),
        legend=dict(
            bgcolor="rgba(22, 27, 34, 0.8)",
            bordercolor=PALETTE["border_dark"],
            borderwidth=1,
            font=dict(color=PALETTE["text_primary"], size=11),
        ),
        hoverlabel=dict(
            bgcolor=PALETTE["surface_dark"],
            bordercolor=PALETTE["border_dark"],
            font=dict(color=PALETTE["text_primary"], size=12),
        ),
    )
    
    return template


def register_plotly_theme() -> None:
    """Registra la plantilla editorial 'fondo_e_dark' en Plotly."""
    custom_template = get_plotly_template()
    pio.templates["fondo_e_dark"] = custom_template
    pio.templates.default = "fondo_e_dark"


# Inicializar temas por defecto al importar el módulo
setup_matplotlib_theme()
register_plotly_theme()
