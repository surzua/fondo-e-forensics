"""Pruebas unitarias para validación de datos descargados e ingesta (Fase 1)."""

from datetime import date
from pathlib import Path
import polars as pl
import pytest

from src.config import INTERIM_DIR, OFFICIAL_REAL_RETURN_2026


def test_interim_cuotas_exist():
    """Verifica que el dataset de cuotas reales intermedias exista y tenga datos válidos."""
    path = INTERIM_DIR / "cuotas_reales_diarias.parquet"
    assert path.exists(), f"No se encontró {path}"
    
    df = pl.read_parquet(path)
    assert len(df) > 50000
    assert set(df["fondo"].unique().to_list()) == {"A", "C", "E"}
    assert "SISTEMA" in df["afp"].unique().to_list()
    assert "vc_real_uf" in df.columns
    assert "ret_real_acum_2026" in df.columns


def test_fondo_e_drawdown_2026():
    """Valida que el colapso del Fondo E a septiembre de 2026 esté en el rango esperado."""
    path = INTERIM_DIR / "cuotas_reales_diarias.parquet"
    df = pl.read_parquet(path)
    
    # Filtrar Fondo E al 30 de septiembre de 2026
    sep_data = df.filter((pl.col("fecha") == date(2026, 9, 30)) & (pl.col("fondo") == "E"))
    assert len(sep_data) > 0
    
    # El retorno real del sistema debe ser negativo severo (~ -9.9% a -10.5%)
    sistema = sep_data.filter(pl.col("afp") == "SISTEMA")
    ret_real_sistema = sistema["ret_real_acum_2026"][0]
    assert -0.12 <= ret_real_sistema <= -0.09, f"Retorno inesperado del sistema: {ret_real_sistema}"
    
    # El fondo A debe tener retorno positivo (+7% a +10%)
    sep_a = df.filter((pl.col("fecha") == date(2026, 9, 30)) & (pl.col("fondo") == "A") & (pl.col("afp") == "SISTEMA"))
    ret_real_a = sep_a["ret_real_acum_2026"][0]
    assert 0.05 <= ret_real_a <= 0.12, f"Retorno inesperado del fondo A: {ret_real_a}"


def test_interim_macro_benchmarks():
    """Verifica la integridad del dataset de macro y benchmarks."""
    path = INTERIM_DIR / "macro_benchmarks.parquet"
    assert path.exists(), f"No se encontró {path}"
    
    df = pl.read_parquet(path)
    assert len(df) > 2000
    assert "uf" in df.columns
    assert "us10y" in df.columns
    assert "dolar_observado" in df.columns
    
    # Validar que no haya valores nulos en UF
    assert df["uf"].null_count() == 0
