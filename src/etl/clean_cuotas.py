"""Módulo de limpieza, deflactación por UF y cálculo de retornos reales del Fondo E.

Calcula el valor cuota real en UF, retornos diarios nominales/reales,
retorno acumulado de 2026 y la serie de drawdowns.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Optional

import polars as pl

logger = logging.getLogger("CleanCuotasETL")


def clean_and_deflate_cuotas(
    df_cuotas: pl.DataFrame,
    df_macro: pl.DataFrame,
    base_date_2026: date = date(2025, 12, 31),
) -> pl.DataFrame:
    """Cruza los valores cuota diarios con la UF oficial para calcular el valor cuota real.

    Calcula retornos nominales, reales y drawdown histórico.
    """
    # 1. Asegurar tipos de fecha y ordenar
    cuotas_sorted = df_cuotas.sort(["fondo", "afp", "fecha"])
    macro_sorted = df_macro.select(["fecha", "uf", "dolar_observado"]).sort("fecha")

    # 2. Join con macro por fecha
    merged = cuotas_sorted.join(macro_sorted, on="fecha", how="inner")

    # 3. Deflactación por UF: VC_real = VC_nominal / UF
    merged = merged.with_columns([
        (pl.col("valor_cuota") / pl.col("uf")).alias("vc_real_uf"),
    ])

    # 4. Cálculo de retornos diarios nominales y reales por grupo (fondo, afp)
    merged = merged.with_columns([
        pl.col("valor_cuota").pct_change().over(["fondo", "afp"]).alias("ret_nominal_diario"),
        pl.col("vc_real_uf").pct_change().over(["fondo", "afp"]).alias("ret_real_diario"),
    ])

    # 5. Cálculo del retorno acumulado 2026 respecto a base_date_2026
    # Obtener el valor base al 31-12-2025 para cada (fondo, afp)
    base_vals = (
        merged.filter(pl.col("fecha") == base_date_2026)
        .select(["fondo", "afp", pl.col("vc_real_uf").alias("vc_real_base_2026"), pl.col("valor_cuota").alias("vc_nom_base_2026")])
    )

    if base_vals.height == 0:
        # Si la fecha exacta 31-12-2025 no está presente, tomar el último día hábil de 2025
        base_vals = (
            merged.filter(pl.col("fecha") <= base_date_2026)
            .group_by(["fondo", "afp"])
            .agg([
                pl.col("fecha").max().alias("fecha_max_2025"),
                pl.col("vc_real_uf").last().alias("vc_real_base_2026"),
                pl.col("valor_cuota").last().alias("vc_nom_base_2026"),
            ])
        )

    merged = merged.join(base_vals.select(["fondo", "afp", "vc_real_base_2026", "vc_nom_base_2026"]), on=["fondo", "afp"], how="left")

    merged = merged.with_columns([
        ((pl.col("vc_real_uf") / pl.col("vc_real_base_2026")) - 1.0).alias("ret_real_acum_2026"),
        ((pl.col("valor_cuota") / pl.col("vc_nom_base_2026")) - 1.0).alias("ret_nom_acum_2026"),
    ])

    # 6. Cálculo del Drawdown acumulado desde el máximo histórico previo (Peak-to-Trough)
    merged = merged.with_columns([
        pl.col("vc_real_uf").cum_max().over(["fondo", "afp"]).alias("peak_historico_real"),
    ]).with_columns([
        ((pl.col("vc_real_uf") / pl.col("peak_historico_real")) - 1.0).alias("drawdown_real"),
    ])

    logger.info("ETL de cuotas completado: %d registros procesados", len(merged))
    return merged
