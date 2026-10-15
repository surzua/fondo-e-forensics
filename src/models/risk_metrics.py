"""Motor de Métricas Cuantitativas de Riesgo y Análisis de Colas (Risk Metrics Engine).

Módulo especializado en el cálculo de Drawdowns, Volatilidad Móvil, VaR (Histórico,
Paramétrico y Cornish-Fisher), Conditional VaR (Expected Shortfall) y Beta Rolling.

Fórmulas matemáticas detalladas:

1. Drawdown y Maximum Drawdown (MDD):
   Peak_t = max_{s <= t} P_s
   Drawdown_t = (P_t - Peak_t) / Peak_t
   MDD = min_t Drawdown_t

2. Volatilidad Anualizada Móvil (Rolling Volatility):
   sigma_t = sqrt(252) * sqrt( 1/(W-1) * sum_{i=0}^{W-1} (R_{t-i} - R_bar_t)^2 )

3. Value at Risk (VaR):
   - VaR Histórico:
     VaR_alpha^{hist} = -Quantile_alpha(R)
   - VaR Paramétrico (Gaussiano):
     VaR_alpha^{param} = -(mu + z_alpha * sigma)
     donde z_{0.05} = -1.64485 y z_{0.01} = -2.32635
   - VaR Cornish-Fisher (Modificado para Asimetría y Curtosis):
     S = Skewness(R) = E[(R - mu)^3] / sigma^3
     K_ex = Kurtosis(R) - 3 = (E[(R - mu)^4] / sigma^4) - 3
     z_CF = z_alpha + (1/6)*(z_alpha^2 - 1)*S + (1/24)*(z_alpha^3 - 3*z_alpha)*K_ex - (1/36)*(2*z_alpha^3 - 5*z_alpha)*S^2
     VaR_alpha^{CF} = -(mu + z_CF * sigma)

4. Conditional Value at Risk (CVaR / Expected Shortfall):
   CVaR_alpha = -E[R | R <= -VaR_alpha]

5. Rolling Beta contra Tasas del Tesoro de EE.UU. (Delta US10Y):
   Beta_t = Cov_W(R_t, Delta y_t) / Var_W(Delta y_t)
   donde Delta y_t = US10Y_t - US10Y_{t-1}

6. Sharpe y Sortino Ratios:
   Sharpe = sqrt(252) * (mean(R) - R_f) / std(R)
   Downside_std = sqrt( mean( min(0, R - R_f)^2 ) )
   Sortino = sqrt(252) * (mean(R) - R_f) / Downside_std
"""

from __future__ import annotations

import logging
from typing import Dict, Optional, Tuple, Union

import numpy as np
import polars as pl
from scipy import stats

logger = logging.getLogger("RiskMetrics")


def calculate_drawdown_series(
    prices_or_values: Union[np.ndarray, pl.Series],
) -> Tuple[np.ndarray, np.ndarray, float]:
    """Calcula la serie de picos históricos acumulados, drawdowns y el máximo drawdown (MDD).

    Fórmulas:
        Peak_t = max_{s <= t} P_s
        Drawdown_t = (P_t - Peak_t) / Peak_t
        MDD = min_t Drawdown_t

    Retorna:
        Tuple[peaks, drawdowns, max_drawdown]
    """
    if isinstance(prices_or_values, pl.Series):
        values = prices_or_values.to_numpy()
    else:
        values = np.asarray(prices_or_values, dtype=np.float64)

    if len(values) == 0:
        return np.array([]), np.array([]), 0.0

    peaks = np.maximum.accumulate(values)
    drawdowns = (values - peaks) / peaks
    max_drawdown = float(np.min(drawdowns)) if len(drawdowns) > 0 else 0.0

    return peaks, drawdowns, max_drawdown


def calculate_rolling_volatility(
    returns: Union[np.ndarray, pl.Series],
    window: int = 30,
    annualization_factor: float = 252.0,
) -> np.ndarray:
    """Calcula la volatilidad anualizada móvil para una ventana de W días.

    Fórmula:
        sigma_t = sqrt(annualization_factor) * sqrt( 1/(W-1) sum_{i=0}^{W-1} (R_{t-i} - mu_t)^2 )
    """
    if isinstance(returns, pl.Series):
        r = returns.to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)

    n = len(r)
    vol = np.full(n, np.nan, dtype=np.float64)

    if n < window:
        return vol

    for i in range(window, n + 1):
        window_slice = r[i - window : i]
        # std con ddof=1 (muestral)
        vol[i - 1] = np.std(window_slice, ddof=1) * np.sqrt(annualization_factor)

    return vol


def calculate_var_historical(
    returns: Union[np.ndarray, pl.Series],
    confidence_level: float = 0.95,
) -> float:
    """Calcula el Value at Risk Histórico empírico.

    Fórmula:
        VaR_alpha = -Quantile_{1 - confidence_level}(R)
    """
    if isinstance(returns, pl.Series):
        r = returns.drop_nulls().to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)
        r = r[~np.isnan(r)]

    if len(r) == 0:
        return 0.0

    alpha = 1.0 - confidence_level
    quantile_val = float(np.percentile(r, alpha * 100.0))
    return -quantile_val


def calculate_var_parametric(
    returns: Union[np.ndarray, pl.Series],
    confidence_level: float = 0.95,
) -> float:
    """Calcula el Value at Risk Paramétrico (Gaussiano / Normal).

    Fórmula:
        VaR_alpha = -(mu + z_alpha * sigma)
    """
    if isinstance(returns, pl.Series):
        r = returns.drop_nulls().to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)
        r = r[~np.isnan(r)]

    if len(r) < 2:
        return 0.0

    mu = float(np.mean(r))
    sigma = float(np.std(r, ddof=1))
    alpha = 1.0 - confidence_level
    z_alpha = float(stats.norm.ppf(alpha))

    return -(mu + z_alpha * sigma)


def calculate_var_cornish_fisher(
    returns: Union[np.ndarray, pl.Series],
    confidence_level: float = 0.95,
) -> float:
    """Calcula el Value at Risk modificado de Cornish-Fisher.

    Ajusta el cuantil estándar por la asimetría (skewness) y el exceso de curtosis
    para modelar con precisión las colas pesadas generadas por el apalancamiento en swaps.

    Fórmulas:
        S = Skewness(R)
        K_ex = Kurtosis(R) - 3
        z_CF = z_alpha + (1/6)*(z_alpha^2 - 1)*S + (1/24)*(z_alpha^3 - 3*z_alpha)*K_ex - (1/36)*(2*z_alpha^3 - 5*z_alpha)*S^2
        VaR_alpha^{CF} = -(mu + z_CF * sigma)
    """
    if isinstance(returns, pl.Series):
        r = returns.drop_nulls().to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)
        r = r[~np.isnan(r)]

    if len(r) < 4:
        return calculate_var_parametric(returns, confidence_level=confidence_level)

    mu = float(np.mean(r))
    sigma = float(np.std(r, ddof=1))

    if sigma == 0.0:
        return 0.0

    # Sesgo y Curtosis
    skew = float(stats.skew(r))
    kurt_ex = float(stats.kurtosis(r, fisher=True))  # Fisher: normal = 0.0

    alpha = 1.0 - confidence_level
    z_a = float(stats.norm.ppf(alpha))

    # Expansión polinomial de Cornish-Fisher
    term1 = (1.0 / 6.0) * (z_a**2 - 1.0) * skew
    term2 = (1.0 / 24.0) * (z_a**3 - 3.0 * z_a) * kurt_ex
    term3 = (1.0 / 36.0) * (2.0 * z_a**3 - 5.0 * z_a) * (skew**2)

    z_cf = z_a + term1 + term2 - term3

    return -(mu + z_cf * sigma)


def calculate_cvar(
    returns: Union[np.ndarray, pl.Series],
    confidence_level: float = 0.95,
) -> float:
    """Calcula el Conditional Value at Risk (CVaR / Expected Shortfall).

    Fórmula:
        CVaR_alpha = -E[R | R <= -VaR_alpha^{hist}]
    """
    if isinstance(returns, pl.Series):
        r = returns.drop_nulls().to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)
        r = r[~np.isnan(r)]

    if len(r) == 0:
        return 0.0

    alpha = 1.0 - confidence_level
    cutoff = float(np.percentile(r, alpha * 100.0))
    tail_losses = r[r <= cutoff]

    if len(tail_losses) == 0:
        return -cutoff

    return float(-np.mean(tail_losses))


def calculate_rolling_beta(
    asset_returns: Union[np.ndarray, pl.Series],
    benchmark_deltas: Union[np.ndarray, pl.Series],
    window: int = 60,
) -> np.ndarray:
    """Calcula el Beta móvil (sensibilidad) de los retornos del activo frente a variaciones de tasa.

    Fórmula:
        Beta_t = Cov_W(R_t, Delta y_t) / Var_W(Delta y_t)
    """
    if isinstance(asset_returns, pl.Series):
        y = asset_returns.to_numpy()
    else:
        y = np.asarray(asset_returns, dtype=np.float64)

    if isinstance(benchmark_deltas, pl.Series):
        x = benchmark_deltas.to_numpy()
    else:
        x = np.asarray(benchmark_deltas, dtype=np.float64)

    n = len(y)
    betas = np.full(n, np.nan, dtype=np.float64)

    if n != len(x) or n < window:
        return betas

    for i in range(window, n + 1):
        x_win = x[i - window : i]
        y_win = y[i - window : i]

        valid_mask = ~np.isnan(x_win) & ~np.isnan(y_win)
        x_valid = x_win[valid_mask]
        y_valid = y_win[valid_mask]

        if len(x_valid) < 10:
            continue

        var_x = np.var(x_valid, ddof=1)
        if var_x > 1e-12:
            cov_xy = np.cov(y_valid, x_valid)[0, 1]
            betas[i - 1] = cov_xy / var_x

    return betas


def calculate_risk_profile_summary(
    returns: Union[np.ndarray, pl.Series],
    prices: Optional[Union[np.ndarray, pl.Series]] = None,
    rf_daily: float = 0.0,
) -> Dict[str, float]:
    """Genera un reporte consolidado con todos los indicadores de riesgo de cola y retornos."""
    if isinstance(returns, pl.Series):
        r = returns.drop_nulls().to_numpy()
    else:
        r = np.asarray(returns, dtype=np.float64)
        r = r[~np.isnan(r)]

    if len(r) == 0:
        return {}

    mu_daily = float(np.mean(r))
    vol_annual = float(np.std(r, ddof=1) * np.sqrt(252.0))
    skew = float(stats.skew(r)) if len(r) >= 3 else 0.0
    kurt = float(stats.kurtosis(r, fisher=True)) if len(r) >= 4 else 0.0

    var_hist_95 = calculate_var_historical(r, 0.95)
    var_hist_99 = calculate_var_historical(r, 0.99)
    var_param_95 = calculate_var_parametric(r, 0.95)
    var_param_99 = calculate_var_parametric(r, 0.99)
    var_cf_95 = calculate_var_cornish_fisher(r, 0.95)
    var_cf_99 = calculate_var_cornish_fisher(r, 0.99)
    cvar_95 = calculate_cvar(r, 0.95)
    cvar_99 = calculate_cvar(r, 0.99)

    # Sharpe y Sortino
    excess_return = mu_daily - rf_daily
    sharpe = float((excess_return * 252.0) / vol_annual) if vol_annual > 0 else 0.0

    downside_returns = r[r < rf_daily] - rf_daily
    downside_vol = float(np.sqrt(np.mean(downside_returns**2)) * np.sqrt(252.0)) if len(downside_returns) > 0 else 0.0
    sortino = float((excess_return * 252.0) / downside_vol) if downside_vol > 0 else 0.0

    # Max Drawdown si se entregan precios
    mdd = 0.0
    if prices is not None:
        _, _, mdd = calculate_drawdown_series(prices)

    return {
        "media_diaria": mu_daily,
        "media_anualizada": mu_daily * 252.0,
        "volatilidad_anualizada": vol_annual,
        "asimetria_skewness": skew,
        "curtosis_exceso": kurt,
        "var_historico_95": var_hist_95,
        "var_historico_99": var_hist_99,
        "var_parametrico_95": var_param_95,
        "var_parametrico_99": var_param_99,
        "var_cornish_fisher_95": var_cf_95,
        "var_cornish_fisher_99": var_cf_99,
        "cvar_expected_shortfall_95": cvar_95,
        "cvar_expected_shortfall_99": cvar_99,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "max_drawdown": mdd,
    }
