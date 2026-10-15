"""Motor Matemático y Actuarial: Tablas de Mortalidad RV-2020, CNU y Simulación de Monte Carlo.

Modela el impacto patrimonial y previsional del desplome del Fondo E en 2026,
traduciendo el drawdown porcentual en pérdida de pensión mensual vitalicia y
meses de trabajo forzado adicional para recuperar el capital.

Fórmulas matemáticas detalladas:

1. Probabilidad Acumulada de Supervivencia:
   _t p_x = l_{x+t} / l_x = prod_{k=0}^{t-1} (1 - q_{x+k})
   donde l_x es el número de personas vivas a edad x según la tabla oficial RV-2020.

2. Factor de Descuento Financiero Actuarial:
   v = 1 / (1 + i_t)
   v^t = (1 + i_t)^{-t}
   donde i_t es la tasa técnica de descuento anual (por defecto 3,2% real anual).

3. Anualidad Vitalicia Anticipada Anual y Mensual (Woolhouse):
   a_due_x = sum_{t=0}^{omega - x} v^t * _t p_x
   a_due_x^{(12)} = a_due_x - 11/24

4. Capital Necesario Unitario (CNU):
   CNU(x, sexo, i_t) = a_due_x^{(12)} * f_sobrevivencia
   donde f_sobrevivencia incorpora la pensión de sobrevivencia legal (cónyuge e hijos):
   - Hombre 65 años: CNU ~ 12.55 (a tasa 3.2%)
   - Mujer 60 años: CNU ~ 16.71 (a tasa 3.2%)

5. Pensión Mensual Vitalicia Inicial:
   Pension_Mensual = Saldo_Acumulado / (12 * CNU(x, sexo, i_t))

6. Recorte Permanente Vitalicio de Pensión:
   Delta_Pension = (Saldo_Pre_Shock * R_shock) / (12 * CNU(x, sexo, i_t))
   con R_shock = -10,39% (-0.1039) a nivel sistema o según AFP específica.

7. Motor de Monte Carlo Vectorizado en NumPy:
   S_{m, t+1} = S_{m, t} * (1 + r_{m, t}) + Aporte_Mensual
   con Aporte_Mensual = 0.10 * Sueldo_Imponible
   r_{m, t} ~ Normal(mu_m, sigma_m^2) calibrada con retornos reales históricos del Fondo E.
   T_rec^{(m)} = min { t >= 1 | S_{m, t} >= S_0 }
   Calcula percentiles empíricos P10, P50 (mediana) y P90 del tiempo de recuperación.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import numpy as np
import polars as pl

from src.config import (
    DEFAULT_TECHNICAL_RATE,
    LEGAL_CONTRIBUTION_RATE,
    MONTE_CARLO_MAX_MONTHS,
    MONTE_CARLO_SIMULATIONS,
    OFFICIAL_REAL_RETURN_2026,
    RETIREMENT_AGE_MEN,
    RETIREMENT_AGE_WOMEN,
    RV2020_TABLE_PATH,
)
from src.schemas import ActuarialImpactResult, ActuarialProfile

logger = logging.getLogger("ActuarialEngine")


class ActuarialEngine:
    """Motor de cálculo actuarial basado en las tablas de mortalidad oficiales RV-2020."""

    def __init__(self, table_path: Optional[Path] = None):
        self.table_path = table_path or RV2020_TABLE_PATH
        if not self.table_path.exists():
            raise FileNotFoundError(f"No se encontró la tabla de mortalidad en: {self.table_path}")
        self.df_mortality = pl.read_csv(self.table_path)
        logger.info("Tabla de mortalidad RV-2020 cargada: %d registros", len(self.df_mortality))

    def calculate_cnu(
        self,
        age: int,
        sex: str,
        technical_rate: float = DEFAULT_TECHNICAL_RATE,
        include_survivor_benefit: bool = True,
    ) -> float:
        """Calcula el Capital Necesario Unitario (CNU) para una edad, sexo y tasa técnica.

        Fórmula:
            CNU = ( sum_{t=0}^{omega - x} v^t * (l_{x+t} / l_x) - 11/24 ) * f_sob

        Retorna:
            float: Factor de CNU en años.
        """
        sex_normalized = sex.strip().lower()
        if sex_normalized in ["h", "hombre", "m"]:
            col_lx = "lx_hombre"
            survivor_factor = 1.0375 if include_survivor_benefit else 1.0000
        else:
            col_lx = "lx_mujer"
            survivor_factor = 1.0280 if include_survivor_benefit else 1.0000

        sub = self.df_mortality.filter(pl.col("edad") >= age)
        if len(sub) == 0:
            raise ValueError(f"Edad fuera de rango de la tabla de mortalidad: {age}")

        lx = sub[col_lx].to_numpy()
        l0 = float(lx[0])
        if l0 <= 0:
            return 0.0

        t = np.arange(len(lx), dtype=np.float64)
        v_t = (1.0 + technical_rate) ** (-t)
        t_px = lx / l0

        # Anualidad anual anticipada
        ax_due = float(np.sum(v_t * t_px))

        # Ajuste de Woolhouse para pagos mensuales anticipados
        ax_due_monthly = ax_due - (11.0 / 24.0)

        # Factor de sobrevivencia legal D.L. 3500
        cnu = ax_due_monthly * survivor_factor
        return float(cnu)

    def calculate_monthly_pension(
        self,
        balance_clp: float,
        age: int,
        sex: str,
        technical_rate: float = DEFAULT_TECHNICAL_RATE,
        cnu: Optional[float] = None,
    ) -> Tuple[float, float]:
        """Calcula la pensión mensual vitalicia ($ CLP) y retorna (pension_mensual, cnu_usado).

        Fórmula:
            Pension_Mensual = Saldo / (12 * CNU)
        """
        if cnu is None:
            cnu = self.calculate_cnu(age, sex, technical_rate)

        if cnu <= 0:
            return 0.0, cnu

        pension = balance_clp / (12.0 * cnu)
        return float(pension), float(cnu)

    def simulate_recovery_monte_carlo(
        self,
        current_balance_clp: float,
        target_balance_clp: float,
        monthly_contribution_clp: float,
        n_sims: int = MONTE_CARLO_SIMULATIONS,
        max_months: int = MONTE_CARLO_MAX_MONTHS,
        annual_expected_return: float = 0.030,  # 3,0% real anual esperado
        annual_volatility: float = 0.040,       # 4,0% volatilidad anual
        seed: int = 42,
    ) -> Dict[str, Union[float, np.ndarray]]:
        """Simula estocásticamente el tiempo de recuperación patrimonial mediante Monte Carlo vectorizado.

        Fórmulas:
            mu_m = (1 + mu_anual)^{1/12} - 1
            sigma_m = sigma_anual / sqrt(12)
            S_{m, t+1} = S_{m, t} * (1 + r_{m, t}) + Aporte
            T_rec = min { t >= 1 | S_t >= S_0 }

        Retorna:
            Dict con percentiles P10, P50 (mediana), P90, probabilidad de no recuperar y trayectorias muestrales.
        """
        np.random.seed(seed)

        # Conversión a parámetros mensuales
        mu_m = (1.0 + annual_expected_return) ** (1.0 / 12.0) - 1.0
        sigma_m = annual_volatility / np.sqrt(12.0)

        # Generación de retornos mensuales estocásticos shape: (n_sims, max_months)
        sim_returns = np.random.normal(loc=mu_m, scale=sigma_m, size=(n_sims, max_months))

        # Evolución vectorizada de saldos
        balances = np.zeros((n_sims, max_months + 1), dtype=np.float64)
        balances[:, 0] = current_balance_clp

        for m in range(max_months):
            balances[:, m + 1] = balances[:, m] * (1.0 + sim_returns[:, m]) + monthly_contribution_clp

        # Evaluar mes de cruce del objetivo
        recovered_mask = balances >= target_balance_clp
        has_recovered = np.any(recovered_mask, axis=1)

        # Para los que recuperaron, argmax da el primer índice True
        recovery_months = np.where(has_recovered, np.argmax(recovered_mask, axis=1), np.nan)

        valid_months = recovery_months[~np.isnan(recovery_months)]
        p10 = float(np.percentile(valid_months, 10)) if len(valid_months) > 0 else float("inf")
        p50 = float(np.percentile(valid_months, 50)) if len(valid_months) > 0 else float("inf")
        p90 = float(np.percentile(valid_months, 90)) if len(valid_months) > 0 else float("inf")
        pct_never_recovered = float(np.mean(~has_recovered) * 100.0)

        # Muestreo de 50 trayectorias para graficación ligera
        sample_trajectories = balances[:50, :]

        return {
            "p10_meses": p10,
            "p50_mediana_meses": p50,
            "p90_meses": p90,
            "pct_no_recupera_en_horizonte": pct_never_recovered,
            "sample_trajectories": sample_trajectories,
            "meses_eje": np.arange(max_months + 1),
        }

    def evaluate_profile_impact(
        self,
        profile: ActuarialProfile,
        shock_pct: float = OFFICIAL_REAL_RETURN_2026,
    ) -> ActuarialImpactResult:
        """Calcula el impacto actuarial integral para un perfil de usuario."""
        saldo_actual = profile.saldo_actual_clp
        
        # El saldo actual ya tiene el shock incorporado (es el saldo post-shock a oct-2026)
        # S_actual = S_inicial * (1 + shock_pct) => S_inicial = S_actual / (1 + shock_pct)
        saldo_inicial = saldo_actual / (1.0 + shock_pct)
        perdida_patrimonial = saldo_inicial - saldo_actual

        # Pérdida atribuible específicamente a swaps (80% del daño nominal de 7,4% = 5,9 pp de 7,4 pp)
        # En proporción sobre el shock total: ~5,9 / 7,4 = 79,7%
        pct_swaps_of_shock = 0.0590 / 0.0740
        perdida_swaps = perdida_patrimonial * pct_swaps_of_shock

        # CNU a la edad de jubilación
        cnu = self.calculate_cnu(
            age=profile.edad_jubilacion,
            sex=profile.sexo,
            technical_rate=profile.tasa_tecnica,
        )

        # Pensiones mensuales
        pension_pre, _ = self.calculate_monthly_pension(saldo_inicial, profile.edad_jubilacion, profile.sexo, cnu=cnu)
        pension_post, _ = self.calculate_monthly_pension(saldo_actual, profile.edad_jubilacion, profile.sexo, cnu=cnu)
        recorte_mensual = pension_pre - pension_post
        recorte_pct = (recorte_mensual / pension_pre) * 100.0 if pension_pre > 0 else 0.0

        # Monte Carlo para recuperar desde saldo_actual hasta saldo_inicial
        monthly_contribution = profile.sueldo_imponible * LEGAL_CONTRIBUTION_RATE
        mc_results = self.simulate_recovery_monte_carlo(
            current_balance_clp=saldo_actual,
            target_balance_clp=saldo_inicial,
            monthly_contribution_clp=monthly_contribution,
        )

        return ActuarialImpactResult(
            saldo_inicial_estimado=float(saldo_inicial),
            saldo_post_shock=float(saldo_actual),
            perdida_patrimonial_clp=float(perdida_patrimonial),
            perdida_swaps_clp=float(perdida_swaps),
            cnu=float(cnu),
            pension_pre_shock_mensual=float(pension_pre),
            pension_post_shock_mensual=float(pension_post),
            recorte_pension_mensual=float(recorte_mensual),
            recorte_pension_pct=float(recorte_pct),
            monte_carlo_meses_recuperacion_p50=float(mc_results["p50_mediana_meses"]),
            monte_carlo_meses_recuperacion_p10=float(mc_results["p10_meses"]),
            monte_carlo_meses_recuperacion_p90=float(mc_results["p90_meses"]),
        )
