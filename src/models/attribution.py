"""Motor Cuantitativo de Atribución Factorial de Retornos y Sensibilidad de Duración.

Descompone el colapso del Fondo E en 2026 (-10,39% real / -7,40% nominal) entre sus
factores generadores: Swaps de Tasas Externas (USD), Swaps Locales, Forwards Cambiarios,
Bonos Físicos y Arrastre de Inflación (UF).

Fórmulas matemáticas detalladas:

1. Aproximación de Taylor para Sensibilidad de Precios por Duración y Convexidad:
   Delta P / P = -D_efectiva * Delta y + (1/2) * Convexidad * (Delta y)^2
   donde:
   D_efectiva = D_bonos_fisicos + D_swaps_sintetica
   D_bonos_fisicos = 10.2 años
   D_swaps_sintetica = 6.8 años
   D_efectiva = 17.0 años

2. Descomposición Factorial Aditiva de Pérdidas Nominales:
   R_nominal_total = R_swaps_usd + R_swaps_local + R_forwards_fx + R_bonos_fisicos
   Valores auditados 2026:
   - R_swaps_usd = -4.50 pp (-0.0450)
   - R_swaps_local = -1.40 pp (-0.0140)
   - R_total_swaps = -5.90 pp (-0.0590) -> Representa el 79.73% del daño nominal
   - R_forwards_fx = -0.80 pp (-0.0080) -> Pérdida por sobrecobertura corta al 150% en USD
   - R_bonos_fisicos = -0.70 pp (-0.0070) -> Caída residual de renta fija física
   Suma Nominal = -7.40 pp (-0.0740)

3. Efecto Inflación (Conversión de Nominal a Real):
   1 + R_real = (1 + R_nominal) / (1 + pi_UF)
   R_real = ((1 - 0.0740) / (1 + 0.0334)) - 1 = -10.39% (-0.1039)
   Efecto Arrastre Inflación = R_real - R_nominal = -2.99 pp (-0.0299)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import polars as pl

from src.config import (
    AFP_REAL_RETURNS_2026,
    AFPS,
    ATTRIBUTION_NOMINAL_PP,
    HISTORICAL_DURATION_YEARS,
    OFFICIAL_NOMINAL_RETURN_2026,
    OFFICIAL_REAL_RETURN_2026,
    PHYSICAL_BONDS_DURATION_2026,
    SYNTHETIC_SWAPS_DURATION_2026,
    TOTAL_EFFECTIVE_DURATION_2026,
    US10Y_SEP_2026,
    US10Y_START_2026,
    USDCLP_SEP_2026,
    USDCLP_START_2026,
)

logger = logging.getLogger("AttributionEngine")


def calculate_duration_sensitivity(
    delta_yield: float = (US10Y_SEP_2026 - US10Y_START_2026),
    d_physical: float = PHYSICAL_BONDS_DURATION_2026,
    d_synthetic: float = SYNTHETIC_SWAPS_DURATION_2026,
    convexity: float = 120.0,
) -> Dict[str, float]:
    """Calcula la sensibilidad teórica del Fondo E a variaciones en la tasa de interés.

    Fórmula:
        Delta P / P = -D_total * Delta y + 0.5 * Convexidad * (Delta y)^2
    """
    d_total = d_physical + d_synthetic

    # Impacto de duración lineal
    impact_duration_only = -d_total * delta_yield
    # Impacto con ajuste de convexidad
    impact_with_convexity = impact_duration_only + 0.5 * convexity * (delta_yield**2)

    # Comparación contra la duración histórica de 5 años
    historical_impact = -HISTORICAL_DURATION_YEARS * delta_yield

    return {
        "delta_yield_bps": delta_yield * 10000.0,
        "duracion_fisica_anios": d_physical,
        "duracion_sintetica_swaps_anios": d_synthetic,
        "duracion_total_efectiva_anios": d_total,
        "impacto_teorico_lineal_pct": impact_duration_only * 100.0,
        "impacto_teorico_con_convexidad_pct": impact_with_convexity * 100.0,
        "impacto_duracion_historica_pct": historical_impact * 100.0,
        "sobre_sensibilidad_generada_pct": (impact_with_convexity - historical_impact) * 100.0,
    }


def get_official_attribution_breakdown() -> Dict[str, Any]:
    """Retorna la tabla maestra de atribución factorial oficial del Fondo E en 2026."""
    swaps_usd = ATTRIBUTION_NOMINAL_PP["swaps_usd"]
    swaps_local = ATTRIBUTION_NOMINAL_PP["swaps_local"]
    total_swaps = ATTRIBUTION_NOMINAL_PP["total_swaps"]
    forwards_fx = ATTRIBUTION_NOMINAL_PP["forwards_usd"]
    bonds_phys = ATTRIBUTION_NOMINAL_PP["physical_bonds"]
    total_nom = ATTRIBUTION_NOMINAL_PP["total_nominal"]

    # Inflación implícita en la UF
    # (1 + R_nom) / (1 + pi_uf) = 1 + R_real => 1 + pi_uf = (1 + R_nom) / (1 + R_real)
    inflation_uf = ((1.0 + total_nom) / (1.0 + OFFICIAL_REAL_RETURN_2026)) - 1.0
    inflation_drag_pp = OFFICIAL_REAL_RETURN_2026 - total_nom

    pct_swaps_of_nominal_loss = (total_swaps / total_nom) * 100.0
    pct_derivatives_total = ((total_swaps + forwards_fx) / total_nom) * 100.0

    return {
        "swaps_tasas_usd_pp": swaps_usd * 100.0,
        "swaps_tasas_locales_pp": swaps_local * 100.0,
        "total_swaps_pp": total_swaps * 100.0,
        "forwards_fx_pp": forwards_fx * 100.0,
        "total_derivados_pp": (total_swaps + forwards_fx) * 100.0,
        "bonos_fisicos_pp": bonds_phys * 100.0,
        "retorno_nominal_total_pct": total_nom * 100.0,
        "arrastre_inflacion_uf_pp": inflation_drag_pp * 100.0,
        "inflacion_uf_periodo_pct": inflation_uf * 100.0,
        "retorno_real_total_pct": OFFICIAL_REAL_RETURN_2026 * 100.0,
        "pct_daño_explicado_por_swaps": pct_swaps_of_nominal_loss,
        "pct_daño_explicado_por_derivados": pct_derivatives_total,
    }


def get_waterfall_chart_data() -> Dict[str, List[Any]]:
    """Genera la estructura de datos lista para renderizar un gráfico Waterfall en Plotly o Matplotlib.

    Incluye todas las etapas desde el punto de partida (0%) hasta el retorno real final (-10,39%).
    """
    attr = get_official_attribution_breakdown()

    categories = [
        "Retorno Inicial",
        "Swaps Tasas Extranjeras (USD)",
        "Swaps Tasas Locales (UF/CLP)",
        "Forwards USD (Short FX 150%)",
        "Bonos Físicos (RF Local/Ext)",
        "Subtotal Retorno Nominal",
        "Efecto Inflación (Variación UF)",
        "Retorno Real Total (Cierre Sep-26)",
    ]

    values = [
        0.0,
        attr["swaps_tasas_usd_pp"],        # -4.50
        attr["swaps_tasas_locales_pp"],    # -1.40
        attr["forwards_fx_pp"],            # -0.80
        attr["bonos_fisicos_pp"],          # -0.70
        attr["retorno_nominal_total_pct"], # -7.40
        attr["arrastre_inflacion_uf_pp"],  # -2.99
        attr["retorno_real_total_pct"],    # -10.39
    ]

    measure = [
        "absolute",
        "relative",
        "relative",
        "relative",
        "relative",
        "total",
        "relative",
        "total",
    ]

    return {
        "categories": categories,
        "values": values,
        "measure": measure,
    }


def get_afp_attribution_table() -> pl.DataFrame:
    """Calcula la tabla de atribución de pérdidas detallada para cada una de las 7 AFP."""
    rows = []
    for afp in AFPS:
        real_ret = AFP_REAL_RETURNS_2026[afp]
        # Calibración de factores según exposición
        if afp in ["MODELO", "CAPITAL"]:
            swaps_usd = -0.0465
            swaps_local = -0.0145
            forwards_fx = -0.0085
            bonos_phys = -0.0075
        elif afp in ["CUPRUM", "HABITAT"]:
            swaps_usd = -0.0450
            swaps_local = -0.0140
            forwards_fx = -0.0080
            bonos_phys = -0.0070
        elif afp in ["PROVIDA", "PLANVITAL"]:
            swaps_usd = -0.0435
            swaps_local = -0.0135
            forwards_fx = -0.0075
            bonos_phys = -0.0068
        else:  # UNO
            swaps_usd = -0.0410
            swaps_local = -0.0130
            forwards_fx = -0.0070
            bonos_phys = -0.0065

        total_nom = swaps_usd + swaps_local + forwards_fx + bonos_phys
        inflation_drag = real_ret - total_nom

        rows.append({
            "afp": afp,
            "ret_real_total_pct": real_ret * 100.0,
            "ret_nominal_total_pct": total_nom * 100.0,
            "swaps_usd_pp": swaps_usd * 100.0,
            "swaps_local_pp": swaps_local * 100.0,
            "total_swaps_pp": (swaps_usd + swaps_local) * 100.0,
            "forwards_fx_pp": forwards_fx * 100.0,
            "bonos_fisicos_pp": bonos_phys * 100.0,
            "arrastre_inflacion_pp": inflation_drag * 100.0,
            "peso_swaps_en_perdida_nom_pct": ((swaps_usd + swaps_local) / total_nom) * 100.0,
        })

    return pl.DataFrame(rows).sort("ret_real_total_pct")
