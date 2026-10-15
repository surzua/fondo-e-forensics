"""Pruebas unitarias para el pipeline ETL y datasets procesados (src/etl/build_analytical_mart.py)."""

import polars as pl
import pytest

from src.config import (
    AFP_DERIVATIVES_PANEL_PATH,
    MASTER_DAILY_PANEL_PATH,
    MONTHLY_CHECKPOINTS_PATH,
)
from src.etl.build_analytical_mart import build_analytical_mart


def test_processed_parquets_exist_and_validate():
    """Verifica que los datasets procesados existan, tengan filas y cumplan los esquemas."""
    master, afp_matrix, checkpoints = build_analytical_mart(force_refresh=False)

    assert len(master) > 20000
    assert len(afp_matrix) == 7
    assert len(checkpoints) >= 6

    # Verificar existencia en disco
    assert MASTER_DAILY_PANEL_PATH.exists()
    assert AFP_DERIVATIVES_PANEL_PATH.exists()
    assert MONTHLY_CHECKPOINTS_PATH.exists()

    # Verificar columnas clave
    assert "vc_real_uf" in master.columns
    assert "drawdown_real" in master.columns
    assert "us10y" in master.columns

    assert "danio_swaps_pp" in afp_matrix.columns
    assert "ratio_sobrecobertura_usd" in afp_matrix.columns

    assert "contrib_swaps_usd" in checkpoints.columns
    assert "hedge_ratio_fx" in checkpoints.columns
