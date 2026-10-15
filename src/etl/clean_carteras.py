"""Módulo ETL para el procesamiento y estructuración de carteras, duración y derivados.

Fórmulas matemáticas aplicadas:
1. Duración Efectiva Total:
   D_total = D_fisica + D_sintetica
   donde D_sintetica proviene de contratos Swaps de Tasas de Interés (IRS USD/UF).

2. Ratio de Cobertura Cambiaria (FX Hedge Ratio):
   Ratio_FX = Nocional Forwards Vendidos USD / Activos en Moneda Extranjera
   Un ratio > 1.0 (ej. 1.50) indica sobrecobertura corta neta (short USD),
   lo que genera pérdidas patrimoniales cuando el tipo de cambio se deprecia (USD sube).

3. Desglose Factorial de Renta Fija Nacional:
   w_total_nacional = w_tesoreria + w_bancarios + w_empresas
"""

from __future__ import annotations

import logging
from typing import Dict, Tuple

import polars as pl

from src.scrapers.spensiones_cartera import SpensionesCarteraScraper

logger = logging.getLogger("CleanCarterasETL")


def process_carteras_and_derivatives(
    force_refresh: bool = False,
) -> Tuple[pl.DataFrame, pl.DataFrame]:
    """Procesa y limpia las series mensuales de derivados, duración y la matriz de las 7 AFP.

    Retorna:
        Tuple[pl.DataFrame, pl.DataFrame]:
            - df_monthly: Panel mensual con nocional de swaps, ratios FX y duraciones.
            - df_afp_matrix: Matriz comparativa transversal de las 7 administradoras.
    """
    scraper = SpensionesCarteraScraper()
    df_raw_monthly, meta_monthly = scraper.get_cartera_derivatives_panel(force_refresh=force_refresh)
    df_raw_afp, meta_afp = scraper.get_afp_comparative_matrix()

    # 1. Enriquecer el panel mensual con cálculos derivados
    df_monthly_clean = df_raw_monthly.with_columns([
        # Asegurar suma de duración total
        (pl.col("duracion_bonos_fisicos") + pl.col("duracion_sintetica_swaps")).alias("duracion_calculada_total"),
        # Porcentaje total nacional
        (pl.col("bonos_tesoreria_pct") + pl.col("bonos_bancarios_pct") + pl.col("bonos_empresas_pct")).alias("renta_fija_nacional_total_pct"),
        # Ratio de apalancamiento sintético: Duración Sintética / Duración Física
        (pl.col("duracion_sintetica_swaps") / pl.col("duracion_bonos_fisicos")).alias("ratio_apalancamiento_sintetico"),
    ])

    # 2. Formatear y ordenar matriz de AFPs
    df_afp_clean = df_raw_afp.with_columns([
        # Daño de swaps como proporción del retorno real total
        (pl.col("danio_swaps_pp") / pl.col("ret_real_2026_pct")).alias("pct_danio_explicado_por_swaps"),
    ]).sort("ret_real_2026_pct")

    logger.info(
        "ETL de carteras completado: %d periodos mensuales, %d administradoras procesadas.",
        len(df_monthly_clean),
        len(df_afp_clean),
    )

    return df_monthly_clean, df_afp_clean
