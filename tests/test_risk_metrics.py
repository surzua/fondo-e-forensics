"""Pruebas unitarias para el motor de métricas de riesgo y colas (src/models/risk_metrics.py)."""

import numpy as np
import pytest

from src.models.risk_metrics import (
    calculate_cvar,
    calculate_drawdown_series,
    calculate_risk_profile_summary,
    calculate_rolling_beta,
    calculate_rolling_volatility,
    calculate_var_cornish_fisher,
    calculate_var_historical,
    calculate_var_parametric,
)


def test_drawdown_calculation():
    """Verifica que el cálculo de Drawdown y Peak sea exacto."""
    prices = np.array([100.0, 110.0, 105.0, 90.0, 95.0, 115.0])
    peaks, drawdowns, mdd = calculate_drawdown_series(prices)

    assert peaks[1] == 110.0
    assert peaks[3] == 110.0
    assert peaks[5] == 115.0

    # Drawdown en t=3: (90 - 110) / 110 = -20/110 = -0.181818...
    expected_dd_3 = (90.0 - 110.0) / 110.0
    assert pytest.approx(drawdowns[3], rel=1e-4) == expected_dd_3
    assert pytest.approx(mdd, rel=1e-4) == expected_dd_3
    assert drawdowns[5] == 0.0  # Nuevo pico


def test_var_and_cvar_ordering():
    """Verifica que CVaR sea siempre más severo o igual que VaR, y 99% más severo que 95%."""
    np.random.seed(42)
    # Generar distribución con asimetría negativa (típica de shocks de swaps)
    returns = np.random.normal(0.0001, 0.01, 1000)
    # Introducir caídas extremas
    returns[::50] = -0.04

    var_hist_95 = calculate_var_historical(returns, 0.95)
    var_hist_99 = calculate_var_historical(returns, 0.99)
    cvar_95 = calculate_cvar(returns, 0.95)
    cvar_99 = calculate_cvar(returns, 0.99)

    # VaR 99% > VaR 95%
    assert var_hist_99 > var_hist_95
    # CVaR 95% >= VaR 95%
    assert cvar_95 >= var_hist_95
    # CVaR 99% >= VaR 99%
    assert cvar_99 >= var_hist_99


def test_cornish_fisher_adjusts_for_negative_skewness():
    """Verifica que la expansión de Cornish-Fisher incremente el VaR ante sesgo negativo y colas pesadas."""
    np.random.seed(123)
    normal_returns = np.random.normal(0.0, 0.01, 5000)

    # Distorsionar con pérdidas asimétricas
    skewed_returns = normal_returns.copy()
    skewed_returns[::100] = -0.05

    var_param = calculate_var_parametric(skewed_returns, 0.99)
    var_cf = calculate_var_cornish_fisher(skewed_returns, 0.99)

    # Cornish-Fisher debe capturar el riesgo de cola adicional (VaR_CF > VaR_Paramétrico)
    assert var_cf > var_param


def test_rolling_volatility_and_beta():
    """Verifica que la volatilidad y el beta móvil converjan y tengan dimensiones correctas."""
    np.random.seed(42)
    n = 150
    returns = np.random.normal(0.0, 0.008, n)
    # Tasa con correlación negativa
    delta_yields = -0.5 * returns + np.random.normal(0.0, 0.002, n)

    vol = calculate_rolling_volatility(returns, window=30)
    assert len(vol) == n
    assert np.isnan(vol[:29]).all()
    assert not np.isnan(vol[29:]).any()

    beta = calculate_rolling_beta(returns, delta_yields, window=40)
    assert len(beta) == n
    # El beta debe ser marcadamente negativo debido a la relación inversa
    valid_betas = beta[~np.isnan(beta)]
    assert np.mean(valid_betas) < 0.0


def test_risk_profile_summary():
    """Verifica la generación del diccionario resumen de riesgo."""
    np.random.seed(42)
    returns = np.random.normal(0.0002, 0.005, 500)
    prices = 100.0 * np.cumprod(1.0 + returns)

    summary = calculate_risk_profile_summary(returns, prices=prices)
    assert "volatilidad_anualizada" in summary
    assert "var_cornish_fisher_95" in summary
    assert "cvar_expected_shortfall_99" in summary
    assert "max_drawdown" in summary
    assert summary["max_drawdown"] <= 0.0
