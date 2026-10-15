"""Generador de Visualizaciones Interactivas con Plotly.

Exporta los Productos Analíticos 1, 2, 3, 4 y 5 en formato HTML independiente
y provee funciones para incrustar figuras interactivas en Streamlit o sitios web.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import polars as pl

from src.config import (
    AFP_DERIVATIVES_PANEL_PATH,
    AFPS,
    CHARTS_DIR,
    MASTER_DAILY_PANEL_PATH,
    MONTHLY_CHECKPOINTS_PATH,
    PALETTE,
    SWAPS_NOTIONAL_EVOLUTION_MM_USD,
)
from src.models.actuarial import ActuarialEngine
from src.models.attribution import (
    get_afp_attribution_table,
    get_official_attribution_breakdown,
    get_waterfall_chart_data,
)
from src.schemas import ActuarialProfile
from src.viz.theme import register_plotly_theme

logger = logging.getLogger("ChartsInteractive")


def build_interactive_product_1(
    master_df: Optional[pl.DataFrame] = None,
) -> go.Figure:
    """Construye la figura interactiva de doble panel del Producto 1 (Underwater & VaR)."""
    register_plotly_theme()
    df = master_df if master_df is not None else pl.read_parquet(MASTER_DAILY_PANEL_PATH)

    df_e = df.filter((pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "E")).sort("fecha").to_pandas()
    df_a = df.filter((pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "A")).sort("fecha").to_pandas()

    saldo_base = 100_000_000.0
    saldo_e = saldo_base * (df_e["vc_real_uf"] / df_e["vc_real_uf"].iloc[0])
    saldo_a = saldo_base * (df_a["vc_real_uf"] / df_a["vc_real_uf"].iloc[0])

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.55, 0.45],
        subplot_titles=(
            "<b>Evolución de un Saldo Base de $100 MM (Ajustado por UF)</b>",
            "<b>Curva de Drawdown Histórico (Underwater) y Rupturas de VaR</b>",
        ),
    )

    # Panel 1: Saldo real
    fig.add_trace(
        go.Scatter(
            x=df_e["fecha"],
            y=saldo_e,
            name="Fondo E (Conservador)",
            line=dict(color=PALETTE["swaps_loss"], width=2.5),
            hovertemplate="<b>Fondo E</b><br>Fecha: %{x}<br>Saldo Real: $%{y:,.0f} CLP<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_a["fecha"],
            y=saldo_a,
            name="Fondo A (Renta Variable)",
            line=dict(color="#2EC4B6", width=1.5, dash="dot"),
            hovertemplate="<b>Fondo A</b><br>Fecha: %{x}<br>Saldo Real: $%{y:,.0f} CLP<extra></extra>",
        ),
        row=1,
        col=1,
    )

    # Panel 2: Drawdown
    fig.add_trace(
        go.Scatter(
            x=df_e["fecha"],
            y=df_e["drawdown_real"] * 100,
            name="Drawdown Fondo E",
            line=dict(color=PALETTE["swaps_loss"], width=2),
            fill="tozeroy",
            fillcolor="rgba(217, 4, 41, 0.2)",
            hovertemplate="<b>Drawdown E</b>: %{y:.2f}%<extra></extra>",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_a["fecha"],
            y=df_a["drawdown_real"] * 100,
            name="Drawdown Fondo A",
            line=dict(color="#2EC4B6", width=1.2, dash="dash"),
            hovertemplate="<b>Drawdown A</b>: %{y:.2f}%<extra></extra>",
        ),
        row=2,
        col=1,
    )

    fig.add_annotation(
        x="2026-09-30",
        y=-10.39,
        xref="x2",
        yref="y2",
        text="<b>Cierre Sep-2026: -10,39%</b><br>Shock por Swaps y Forwards USD",
        showarrow=True,
        arrowhead=2,
        arrowcolor=PALETTE["swaps_loss"],
        bgcolor="#1E293B",
        bordercolor=PALETTE["swaps_loss"],
        font=dict(color="#F8FAFC", size=10),
    )

    fig.update_layout(
        height=720,
        template="fondo_e_dark",
        title="<b>THE UNDERWATER & VaR SHOCK: AUDITORÍA DEL FONDO E (2018–2026)</b><br><sup>Fuente: Elaboración propia en base a SPensiones y SII. El Fondo E cayó 7x más que el Fondo A en 2026.</sup>",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(title_text="Patrimonio ($ CLP)", tickformat="$,.0f", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown (%)", ticksuffix="%", row=2, col=1)

    return fig


def build_interactive_product_2() -> go.Figure:
    """Construye el gráfico Waterfall interactivo del Producto 2 (Atribución Factorial)."""
    register_plotly_theme()
    wf_data = get_waterfall_chart_data()

    fig = go.Figure(
        go.Waterfall(
            name="Atribución Factorial",
            orientation="v",
            measure=wf_data["measure"],
            x=wf_data["categories"],
            textposition="outside",
            text=[f"{v:+.2f}%" if m == "relative" else f"{v:.2f}%" for v, m in zip(wf_data["values"], wf_data["measure"])],
            y=wf_data["values"],
            connector={"line": {"color": "#64748B", "width": 1.5, "dash": "dot"}},
            decreasing={"marker": {"color": PALETTE["swaps_loss"]}},
            increasing={"marker": {"color": "#2EC4B6"}},
            totals={"marker": {"color": "#3B82F6"}},
            hovertemplate="<b>%{x}</b><br>Impacto: %{y:+.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title="<b>DESCOMPOSICIÓN FACTORIAL DE PÉRDIDAS: FONDO E 2026</b><br><sup>El 80% del daño nominal (-5,9 pp de -7,4%) fue provocado por Swaps. Fuente: SPensiones e IEF Banco Central.</sup>",
        template="fondo_e_dark",
        yaxis_title="Contribución al Retorno (%)",
        height=550,
        showlegend=False,
    )
    return fig


def build_interactive_product_3() -> go.Figure:
    """Construye el Termómetro de Duración y Crecimiento de Swaps del Producto 3."""
    register_plotly_theme()
    periodos = list(SWAPS_NOTIONAL_EVOLUTION_MM_USD.keys())
    nocionales = [v / 1000.0 for v in SWAPS_NOTIONAL_EVOLUTION_MM_USD.values()]
    duraciones = [8.3, 12.6, 16.0, 17.0]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=periodos,
            y=nocionales,
            name="Nocional Swaps (US$ Billones)",
            marker_color=PALETTE["swaps_loss"],
            opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Nocional Swaps: US$ %{y:.1f} Billones<extra></extra>",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=periodos,
            y=duraciones,
            name="Duración Total Efectiva (Años)",
            line=dict(color="#F59E0B", width=3),
            mode="lines+markers+text",
            text=[f"{d:.1f}a" for d in duraciones],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>Duración Efectiva: %{y:.1f} años<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title="<b>EL SALTO DEL APALANCAMIENTO SINTÉTICO (2023–2026)</b><br><sup>El nocional en Swaps escaló 40x mientras la duración efectiva combinada alcanzó 17 años.</sup>",
        template="fondo_e_dark",
        height=520,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(title_text="Nocional Swaps (US$ Billones)", secondary_y=False)
    fig.update_yaxes(title_text="Duración Efectiva (Años)", secondary_y=True, range=[5, 20])

    return fig


def build_interactive_product_4() -> go.Figure:
    """Construye el ranking interactivo de las 7 AFP y su perfil de agresividad del Producto 4."""
    register_plotly_theme()
    afp_df = pl.read_parquet(AFP_DERIVATIVES_PANEL_PATH).sort("ret_real_2026_pct").to_pandas()

    fig = go.Figure(
        go.Bar(
            x=afp_df["ret_real_2026_pct"],
            y=afp_df["afp"],
            orientation="h",
            marker_color=[PALETTE["swaps_loss"] if r in ["Muy Alta", "Alta"] else "#F59E0B" for r in afp_df["perfil_agresividad"]],
            text=[f"{v:.2f}%" for v in afp_df["ret_real_2026_pct"]],
            textposition="outside",
            customdata=np.stack((afp_df["danio_swaps_pp"], afp_df["ratio_sobrecobertura_usd"] * 100, afp_df["perfil_agresividad"]), axis=-1),
            hovertemplate=(
                "<b>AFP %{y}</b><br>"
                "Retorno Real: %{x:.2f}%<br>"
                "Daño Swaps: %{customdata[0]:.2f} pp<br>"
                "Short USD: %{customdata[1]:.0f}%<br>"
                "Perfil: %{customdata[2]}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="<b>RANKING DE CAÍDAS REALES EN EL FONDO E POR AFP (2026)</b><br><sup>Modelo y Capital lideraron las pérdidas por mayor exposición a swaps y forwards USD.</sup>",
        template="fondo_e_dark",
        xaxis_title="Retorno Real Acumulado a Septiembre 2026 (%)",
        yaxis_title="Administradora (AFP)",
        height=480,
    )
    return fig


def build_interactive_product_5(
    current_balance: float = 89_610_000.0,
    target_balance: float = 100_000_000.0,
    salary: float = 1_800_000.0,
    annual_expected_return: float = 0.030,
    annual_volatility: float = 0.040,
) -> go.Figure:
    """Construye el Fan Chart interactivo de Monte Carlo del Producto 5."""
    register_plotly_theme()
    engine = ActuarialEngine()
    mc_sim = engine.simulate_recovery_monte_carlo(
        current_balance_clp=current_balance,
        target_balance_clp=target_balance,
        monthly_contribution_clp=salary * 0.10,
        n_sims=10000,
        max_months=120,
        annual_expected_return=annual_expected_return,
        annual_volatility=annual_volatility,
    )

    meses = mc_sim["meses_eje"]
    trajectories = mc_sim["sample_trajectories"]

    fig = go.Figure()

    for i in range(min(40, len(trajectories))):
        fig.add_trace(
            go.Scatter(
                x=meses,
                y=trajectories[i, :],
                mode="lines",
                line=dict(color="#64748B", width=0.8),
                opacity=0.20,
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.add_hline(
        y=target_balance,
        line_dash="dash",
        line_color="#2EC4B6",
        annotation_text=f"Saldo Objetivo Pre-Shock: ${target_balance:,.0f}",
        annotation_position="top left",
    )
    fig.add_hline(
        y=current_balance,
        line_dash="dot",
        line_color=PALETTE["swaps_loss"],
        annotation_text=f"Saldo Post-Shock: ${current_balance:,.0f}",
        annotation_position="bottom left",
    )

    p50_m = mc_sim["p50_mediana_meses"]
    fig.add_vline(
        x=p50_m,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Mediana P50: {p50_m:.0f} meses de trabajo extra",
        annotation_position="top right",
    )

    fig.update_layout(
        title="<b>SIMULACIÓN DE MONTE CARLO: RECUPERACIÓN PATRIMONIAL DEL FONDO E</b><br><sup>Un afiliado a meses de jubilar necesita ~26 meses de cotizaciones adicionales para recuperar el saldo previo.</sup>",
        template="fondo_e_dark",
        xaxis_title="Meses Futuros de Trabajo y Cotización",
        yaxis_title="Saldo Acumulado ($ CLP)",
        height=540,
    )
    return fig


def export_all_interactive_charts() -> Dict[str, Path]:
    """Genera y guarda en data/processed/charts/ los archivos HTML interactivos de los Productos 1 al 5."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    fig1 = build_interactive_product_1()
    p1 = CHARTS_DIR / "producto1_underwater_var.html"
    fig1.write_html(str(p1), include_plotlyjs="cdn")

    fig2 = build_interactive_product_2()
    p2 = CHARTS_DIR / "producto2_waterfall_atribucion.html"
    fig2.write_html(str(p2), include_plotlyjs="cdn")

    fig3 = build_interactive_product_3()
    p3 = CHARTS_DIR / "producto3_termometro_duracion_swaps.html"
    fig3.write_html(str(p3), include_plotlyjs="cdn")

    fig4 = build_interactive_product_4()
    p4 = CHARTS_DIR / "producto4_heatmap_herding_afp.html"
    fig4.write_html(str(p4), include_plotlyjs="cdn")

    fig5 = build_interactive_product_5()
    p5 = CHARTS_DIR / "producto5_montecarlo_recuperacion.html"
    fig5.write_html(str(p5), include_plotlyjs="cdn")

    logger.info("Todos los gráficos interactivos exportados a HTML en: %s", CHARTS_DIR)
    return {
        "producto_1": p1,
        "producto_2": p2,
        "producto_3": p3,
        "producto_4": p4,
        "producto_5": p5,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    export_all_interactive_charts()
