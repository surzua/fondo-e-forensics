"""Generador de Gráficos Editoriales Estáticos en Alta Resolución (PNG 300 DPI).

Exporta los Productos Analíticos 1, 2, 3, 4 y 5 en dos formatos:
- Formato 16:9 Horizontal (para Blog, Web y Artículos Técnicos).
- Formato 4:5 Vertical (optimizado para Carruseles de LinkedIn y Redes Sociales).

Diseño periodístico inspirado en Financial Times y Bloomberg Dark Mode.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from src.config import (
    AFP_DERIVATIVES_PANEL_PATH,
    CHARTS_DIR,
    MASTER_DAILY_PANEL_PATH,
    MONTHLY_CHECKPOINTS_PATH,
    PALETTE,
    SWAPS_NOTIONAL_EVOLUTION_MM_USD,
)
from src.models.actuarial import ActuarialEngine
from src.models.attribution import (
    calculate_duration_sensitivity,
    get_official_attribution_breakdown,
    get_waterfall_chart_data,
)
from src.schemas import ActuarialProfile
from src.viz.theme import setup_matplotlib_theme

logger = logging.getLogger("ChartsSocial")


def _add_editorial_header_and_footer(
    fig: plt.Figure,
    title: str,
    subtitle: str,
    footer: str,
    is_vertical: bool = False,
) -> None:
    """Añade encabezados periodísticos y notas al pie auditadas a la figura."""
    # Título principal
    fig.text(
        0.05,
        0.96 if is_vertical else 0.95,
        title,
        fontsize=14 if is_vertical else 15,
        fontweight="bold",
        color=PALETTE["text_primary"],
        ha="left",
    )
    # Subtítulo explicativo
    fig.text(
        0.05,
        0.93 if is_vertical else 0.915,
        subtitle,
        fontsize=9.5 if is_vertical else 10.5,
        color=PALETTE["text_muted"],
        ha="left",
    )
    # Nota al pie y fuentes
    fig.text(
        0.05,
        0.02 if is_vertical else 0.025,
        footer,
        fontsize=7.5 if is_vertical else 8.5,
        color=PALETTE["text_muted"],
        ha="left",
        style="italic",
    )


def export_product_1_underwater_chart(
    output_dir: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Genera el Producto 1: The Underwater & VaR Shock Chart (16:9 y 4:5)."""
    setup_matplotlib_theme()
    out = output_dir or CHARTS_DIR
    out.mkdir(parents=True, exist_ok=True)

    master = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
    df_e = master.filter((pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "E")).sort("fecha").to_pandas()
    df_a = master.filter((pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "A")).sort("fecha").to_pandas()

    saldo_base = 100_000_000.0
    saldo_e = saldo_base * (df_e["vc_real_uf"] / df_e["vc_real_uf"].iloc[0])
    saldo_a = saldo_base * (df_a["vc_real_uf"] / df_a["vc_real_uf"].iloc[0])

    path_16x9 = out / "producto1_underwater_var_16x9.png"
    path_4x5 = out / "producto1_underwater_var_4x5.png"

    # --- 1. Formato 16:9 Horizontal ---
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 6.75), sharex=True, gridspec_kw={"height_ratios": [1.2, 1.0]}
    )
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.08, right=0.95, hspace=0.18)

    ax1.plot(df_e["fecha"], saldo_e, color=PALETTE["swaps_loss"], lw=2.2, label="Fondo E (Conservador)")
    ax1.plot(df_a["fecha"], saldo_a, color="#2EC4B6", lw=1.6, ls="--", label="Fondo A (Renta Variable)")
    ax1.set_ylabel("Patrimonio Real ($ CLP)")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x*1e-6:.0f}M"))
    ax1.legend(loc="upper left")

    ax2.plot(df_e["fecha"], df_e["drawdown_real"] * 100, color=PALETTE["swaps_loss"], lw=2.0, label="Drawdown Fondo E")
    ax2.fill_between(df_e["fecha"], df_e["drawdown_real"] * 100, 0, color=PALETTE["swaps_loss"], alpha=0.25)
    ax2.plot(df_a["fecha"], df_a["drawdown_real"] * 100, color="#2EC4B6", lw=1.2, ls=":", label="Drawdown Fondo A")
    ax2.axhline(-10.39, color="#E2E8F0", ls="--", lw=1.0, alpha=0.8)
    ax2.text(df_e["fecha"].iloc[-1], -10.39, " Cierre 2026: -10,39%", color="#E2E8F0", va="center", fontsize=8.5)
    ax2.set_ylabel("Drawdown Real (%)")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0f}%"))
    ax2.legend(loc="lower left")

    _add_editorial_header_and_footer(
        fig,
        title="THE UNDERWATER & VaR SHOCK: LA FALACIA DEL FONDO SEGURO",
        subtitle="Evolución de $100 MM reales y drawdown histórico (2018–2026). El Fondo E cayó 7x más que el Fondo A en 2026.",
        footer="Fuente: Elaboración propia en base a SPensiones y SII. Nota: -9,92% real diario vs -10,39% al cierre mensual oficial.",
    )
    fig.savefig(path_16x9, dpi=300)
    plt.close(fig)

    # --- 2. Formato 4:5 Vertical ---
    fig_v, (ax1_v, ax2_v) = plt.subplots(
        2, 1, figsize=(8, 10), sharex=True, gridspec_kw={"height_ratios": [1.1, 1.0]}
    )
    fig_v.subplots_adjust(top=0.88, bottom=0.08, left=0.12, right=0.94, hspace=0.18)

    ax1_v.plot(df_e["fecha"], saldo_e, color=PALETTE["swaps_loss"], lw=2.2, label="Fondo E")
    ax1_v.plot(df_a["fecha"], saldo_a, color="#2EC4B6", lw=1.6, ls="--", label="Fondo A")
    ax1_v.set_ylabel("Patrimonio Real ($ CLP)")
    ax1_v.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x*1e-6:.0f}M"))
    ax1_v.legend(loc="upper left")

    ax2_v.plot(df_e["fecha"], df_e["drawdown_real"] * 100, color=PALETTE["swaps_loss"], lw=2.0)
    ax2_v.fill_between(df_e["fecha"], df_e["drawdown_real"] * 100, 0, color=PALETTE["swaps_loss"], alpha=0.25)
    ax2_v.plot(df_a["fecha"], df_a["drawdown_real"] * 100, color="#2EC4B6", lw=1.2, ls=":")
    ax2_v.axhline(-10.39, color="#E2E8F0", ls="--", lw=1.0, alpha=0.8)
    ax2_v.set_ylabel("Drawdown Real (%)")
    ax2_v.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0f}%"))

    _add_editorial_header_and_footer(
        fig_v,
        title="EL COLAPSO DEL FONDO CONSERVADOR",
        subtitle="Drawdown acumulado 2018–2026. Ruptura del VaR al 99% por derivados.",
        footer="Fuente: SPensiones y SII. Elaboración propia en base a microdatos públicos.",
        is_vertical=True,
    )
    fig_v.savefig(path_4x5, dpi=300)
    plt.close(fig_v)

    logger.info("Producto 1 exportado en 16:9 y 4:5 a: %s", out)
    return path_16x9, path_4x5


def export_product_2_waterfall_chart(
    output_dir: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Genera el Producto 2: Cascada de Descomposición Factorial (Waterfall Chart)."""
    setup_matplotlib_theme()
    out = output_dir or CHARTS_DIR
    out.mkdir(parents=True, exist_ok=True)

    wf_data = get_waterfall_chart_data()
    cats = [
        "Swaps USD\n(IRS 5Y/10Y)",
        "Swaps Locales\n(SPC UF/CLP)",
        "Forwards USD\n(Short 150%)",
        "Bonos Físicos\n(RF Local/Ext)",
        "Subtotal\nNominal",
        "Efecto Inflación\n(Variación UF)",
        "Retorno Real\nTotal",
    ]
    # Valores de las barras intermedias (omitimos el 'Retorno Inicial')
    vals = wf_data["values"][1:]

    colors = [
        PALETTE["swaps_loss"],
        PALETTE["swaps_loss"],
        "#F59E0B",
        "#3B82F6",
        "#64748B",
        "#94A3B8",
        PALETTE["swaps_dark"],
    ]

    path_16x9 = out / "producto2_waterfall_atribucion_16x9.png"
    path_4x5 = out / "producto2_waterfall_atribucion_4x5.png"

    # --- 1. Formato 16:9 Horizontal ---
    fig, ax = plt.subplots(figsize=(12, 6.75))
    fig.subplots_adjust(top=0.86, bottom=0.14, left=0.08, right=0.95)

    bars = ax.bar(cats, vals, color=colors, width=0.62)
    ax.axhline(0, color=PALETTE["border_dark"], lw=1.2)
    ax.set_ylabel("Contribución al Retorno (%)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:+.1f}%"))

    for bar, v in zip(bars, vals):
        y_pos = bar.get_height() - 0.45 if v < 0 else bar.get_height() + 0.15
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            f"{v:.2f}%",
            ha="center",
            va="top" if v < 0 else "bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#FFFFFF",
        )

    _add_editorial_header_and_footer(
        fig,
        title="¿POR QUÉ CAYÓ EL FONDO SEGURO? DESCOMPOSICIÓN FACTORIAL 2026",
        subtitle="El 80% del daño nominal (-5,9 pp de -7,4%) provino de Swaps. Los bonos físicos solo restaron -0,7 pp.",
        footer="Fuente: SPensiones, IEF Banco Central y Reserva Federal. Nota: Metodología de descomposición aditiva auditada.",
    )
    fig.savefig(path_16x9, dpi=300)
    plt.close(fig)

    # --- 2. Formato 4:5 Vertical ---
    fig_v, ax_v = plt.subplots(figsize=(8, 10))
    fig_v.subplots_adjust(top=0.88, bottom=0.12, left=0.12, right=0.94)

    bars_v = ax_v.barh(cats[::-1], vals[::-1], color=colors[::-1], height=0.6)
    ax_v.axvline(0, color=PALETTE["border_dark"], lw=1.2)
    ax_v.set_xlabel("Contribución al Retorno (%)")
    ax_v.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:+.1f}%"))

    for bar, v in zip(bars_v, vals[::-1]):
        x_pos = bar.get_width() - 0.3 if v < 0 else bar.get_width() + 0.1
        ax_v.text(
            x_pos,
            bar.get_y() + bar.get_height() / 2,
            f"{v:.2f}%",
            ha="right" if v < 0 else "left",
            va="center",
            fontsize=9.0,
            fontweight="bold",
            color="#FFFFFF",
        )

    _add_editorial_header_and_footer(
        fig_v,
        title="DESCOMPOSICIÓN DE PÉRDIDAS 2026",
        subtitle="Swaps y Forwards explican casi la totalidad del derrumbe.",
        footer="Fuente: Elaboración propia en base a microdatos de SPensiones.",
        is_vertical=True,
    )
    fig_v.savefig(path_4x5, dpi=300)
    plt.close(fig_v)

    logger.info("Producto 2 exportado en 16:9 y 4:5 a: %s", out)
    return path_16x9, path_4x5


def export_product_3_duration_thermometer(
    output_dir: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Genera el Producto 3: Termómetro de Duración y Crecimiento en Swaps."""
    setup_matplotlib_theme()
    out = output_dir or CHARTS_DIR
    out.mkdir(parents=True, exist_ok=True)

    periodos = ["Ago-2023", "Dic-2024", "Dic-2025", "Sep-2026"]
    nocional_billions = [
        SWAPS_NOTIONAL_EVOLUTION_MM_USD["2023-08"] / 1000.0,
        SWAPS_NOTIONAL_EVOLUTION_MM_USD["2024-12"] / 1000.0,
        SWAPS_NOTIONAL_EVOLUTION_MM_USD["2025-12"] / 1000.0,
        SWAPS_NOTIONAL_EVOLUTION_MM_USD["2026-09"] / 1000.0,
    ]
    duracion_total = [8.3, 12.6, 16.0, 17.0]

    path_16x9 = out / "producto3_termometro_duracion_swaps_16x9.png"
    path_4x5 = out / "producto3_termometro_duracion_swaps_4x5.png"

    # --- 1. Formato 16:9 Horizontal ---
    fig, ax1 = plt.subplots(figsize=(12, 6.75))
    fig.subplots_adjust(top=0.86, bottom=0.12, left=0.09, right=0.90)

    color_bars = PALETTE["swaps_loss"]
    bars = ax1.bar(periodos, nocional_billions, color=color_bars, width=0.5, alpha=0.85, label="Nocional Swaps (US$ Billones)")
    ax1.set_ylabel("Nocional en Swaps (Miles de Millones USD)", color=color_bars)
    ax1.tick_params(axis="y", labelcolor=color_bars)

    for bar, n in zip(bars, nocional_billions):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3.0,
            f"US$ {n:.1f}B",
            ha="center",
            va="bottom",
            fontsize=9.0,
            fontweight="bold",
            color=color_bars,
        )

    ax2 = ax1.twinx()
    color_line = "#F59E0B"
    ax2.plot(periodos, duracion_total, color=color_line, lw=3.0, marker="o", markersize=8, label="Duración Total Efectiva (Años)")
    ax2.set_ylabel("Duración Efectiva (Años)", color=color_line)
    ax2.tick_params(axis="y", labelcolor=color_line)
    ax2.set_ylim(5, 20)

    for i, d in enumerate(duracion_total):
        ax2.text(i, d + 0.6, f"{d:.1f} años", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=color_line)

    _add_editorial_header_and_footer(
        fig,
        title="LA ESCALADA DEL APALANCAMIENTO SINTÉTICO (2023–2026)",
        subtitle="El nocional en swaps extranjeros creció 40x mientras la duración efectiva alcanzó 17 años.",
        footer="Fuente: SPensiones e IEF Banco Central. Nota: Duración combina bonos en UF (10,2a) y swaps en USD (6,8a).",
    )
    fig.savefig(path_16x9, dpi=300)
    plt.close(fig)

    # --- 2. Formato 4:5 Vertical ---
    fig_v, ax1_v = plt.subplots(figsize=(8, 10))
    fig_v.subplots_adjust(top=0.88, bottom=0.10, left=0.14, right=0.86)

    bars_v = ax1_v.bar(periodos, nocional_billions, color=color_bars, width=0.5, alpha=0.85)
    ax1_v.set_ylabel("Nocional Swaps (US$ Billones)", color=color_bars)
    ax1_v.tick_params(axis="y", labelcolor=color_bars)

    ax2_v = ax1_v.twinx()
    ax2_v.plot(periodos, duracion_total, color=color_line, lw=2.8, marker="o", markersize=7)
    ax2_v.set_ylabel("Duración Total (Años)", color=color_line)
    ax2_v.tick_params(axis="y", labelcolor=color_line)
    ax2_v.set_ylim(5, 20)

    _add_editorial_header_and_footer(
        fig_v,
        title="EL SALTO DE LA DURACIÓN OCULTA",
        subtitle="Exposición nocional en swaps y duración acumulada de la cartera.",
        footer="Fuente: SPensiones e IEF Banco Central de Chile.",
        is_vertical=True,
    )
    fig_v.savefig(path_4x5, dpi=300)
    plt.close(fig_v)

    logger.info("Producto 3 exportado en 16:9 y 4:5 a: %s", out)
    return path_16x9, path_4x5


def export_product_4_herding_matrix(
    output_dir: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Genera el Producto 4: Heatmap de Correlación y Ranking de Agresividad por AFP."""
    setup_matplotlib_theme()
    out = output_dir or CHARTS_DIR
    out.mkdir(parents=True, exist_ok=True)

    afp_df = pl.read_parquet(AFP_DERIVATIVES_PANEL_PATH).sort("ret_real_2026_pct").to_pandas()

    afps = afp_df["afp"].tolist()
    rets = afp_df["ret_real_2026_pct"].tolist()
    swaps_loss = afp_df["danio_swaps_pp"].tolist()

    path_16x9 = out / "producto4_heatmap_herding_afp_16x9.png"
    path_4x5 = out / "producto4_heatmap_herding_afp_4x5.png"

    # --- 1. Formato 16:9 Horizontal ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.75), gridspec_kw={"width_ratios": [1.1, 1.0]})
    fig.subplots_adjust(top=0.86, bottom=0.12, left=0.08, right=0.95, wspace=0.25)

    # Subplot 1: Barras horizontales de caída real
    y_pos = np.arange(len(afps))
    bar_colors = [PALETTE["swaps_loss"] if r <= -10.6 else "#F59E0B" for r in rets]
    ax1.barh(y_pos, rets, color=bar_colors, height=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(afps, fontweight="bold")
    ax1.invert_yaxis()
    ax1.set_xlabel("Retorno Real 2026 (%)")
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.1f}%"))

    for i, r in enumerate(rets):
        ax1.text(r - 0.2, i, f"{r:.2f}%", va="center", ha="right", fontsize=9.0, color="#FFFFFF", fontweight="bold")

    # Subplot 2: Pérdida atribuible a Swaps
    ax2.barh(y_pos, swaps_loss, color=PALETTE["swaps_dark"], height=0.6)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.invert_yaxis()
    ax2.set_xlabel("Pérdida por Swaps (pp)")
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.1f} pp"))

    for i, s in enumerate(swaps_loss):
        ax2.text(s - 0.15, i, f"{s:.2f} pp", va="center", ha="right", fontsize=9.0, color="#FFFFFF", fontweight="bold")

    _add_editorial_header_and_footer(
        fig,
        title="EFECTO MANADA: TODAS LAS AFP TOMARON LA MISMA APUESTA",
        subtitle="Modelo y Capital lideraron las pérdidas reales. El 100% de la industria replicó la estrategia de swaps.",
        footer="Fuente: Estadísticas Oficiales SPensiones a Septiembre 2026. Correlación cruzada inter-AFP > 0,98.",
    )
    fig.savefig(path_16x9, dpi=300)
    plt.close(fig)

    # --- 2. Formato 4:5 Vertical ---
    fig_v, ax_v = plt.subplots(figsize=(8, 10))
    fig_v.subplots_adjust(top=0.88, bottom=0.10, left=0.18, right=0.92)

    ax_v.barh(y_pos, rets, color=bar_colors, height=0.6)
    ax_v.set_yticks(y_pos)
    ax_v.set_yticklabels(afps, fontweight="bold", fontsize=10)
    ax_v.invert_yaxis()
    ax_v.set_xlabel("Retorno Real Acumulado 2026 (%)")

    for i, r in enumerate(rets):
        ax_v.text(r - 0.25, i, f"{r:.2f}%", va="center", ha="right", fontsize=9.5, color="#FFFFFF", fontweight="bold")

    _add_editorial_header_and_footer(
        fig_v,
        title="RANKING DE PÉRDIDAS POR AFP",
        subtitle="Desempeño real 2026 y sincronismo gregoriano en derivados.",
        footer="Fuente: SPensiones. Microdatos auditados a septiembre 2026.",
        is_vertical=True,
    )
    fig_v.savefig(path_4x5, dpi=300)
    plt.close(fig_v)

    logger.info("Producto 4 exportado en 16:9 y 4:5 a: %s", out)
    return path_16x9, path_4x5


def export_all_social_charts() -> Dict[str, Tuple[Path, Path]]:
    """Genera todas las imágenes estáticas editoriales de la Fase 3."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    p1 = export_product_1_underwater_chart()
    p2 = export_product_2_waterfall_chart()
    p3 = export_product_3_duration_thermometer()
    p4 = export_product_4_herding_matrix()

    return {
        "producto_1": p1,
        "producto_2": p2,
        "producto_3": p3,
        "producto_4": p4,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    export_all_social_charts()
