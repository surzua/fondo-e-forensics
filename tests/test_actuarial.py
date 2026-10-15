"""Pruebas unitarias para el motor actuarial y de Monte Carlo (src/models/actuarial.py)."""

import time
import pytest

from src.models.actuarial import ActuarialEngine
from src.schemas import ActuarialProfile


@pytest.fixture
def engine():
    return ActuarialEngine()


def test_cnu_official_benchmarks(engine):
    """Verifica que el CNU a tasa técnica de 3,2% coincida con los valores oficiales de referencia:

    - Hombre 65 años: ~12,55
    - Mujer 60 años: ~16,71
    """
    cnu_hombre_65 = engine.calculate_cnu(age=65, sex="hombre", technical_rate=0.032)
    cnu_mujer_60 = engine.calculate_cnu(age=60, sex="mujer", technical_rate=0.032)

    assert pytest.approx(cnu_hombre_65, abs=0.20) == 12.55
    assert pytest.approx(cnu_mujer_60, abs=0.25) == 16.71


def test_cnu_monotonicity_and_rate_sensitivity(engine):
    """Verifica las propiedades fundamentales del CNU:

    1. A mayor edad, menor es la expectativa de vida remanente y por ende menor es el CNU.
    2. A mayor tasa de descuento, menor es el valor presente actuarial del CNU.
    """
    cnu_h60 = engine.calculate_cnu(60, "hombre", 0.032)
    cnu_h65 = engine.calculate_cnu(65, "hombre", 0.032)
    cnu_h70 = engine.calculate_cnu(70, "hombre", 0.032)

    assert cnu_h60 > cnu_h65 > cnu_h70

    # Sensibilidad a la tasa técnica
    cnu_low_rate = engine.calculate_cnu(65, "hombre", 0.025)
    cnu_high_rate = engine.calculate_cnu(65, "hombre", 0.040)
    assert cnu_low_rate > cnu_high_rate


def test_monthly_pension_calculation(engine):
    """Verifica que la pensión mensual cumpla la fórmula: Pension = Saldo / (12 * CNU)."""
    saldo = 100_000_000.0  # $100 MM CLP
    pension, cnu = engine.calculate_monthly_pension(saldo, age=65, sex="hombre", technical_rate=0.032)

    expected_pension = saldo / (12.0 * cnu)
    assert pytest.approx(pension, rel=1e-5) == expected_pension
    # La pensión para $100 MM en un hombre de 65 años debe rondar los $640.000 a $680.000 CLP
    assert 600_000.0 <= pension <= 750_000.0


def test_monte_carlo_speed_and_convergence(engine):
    """Verifica que la simulación de Monte Carlo con 10.000 trayectorias converja en < 1,5 segundos

    y que los percentiles cumplan P10 <= P50 <= P90.
    """
    t0 = time.time()
    res = engine.simulate_recovery_monte_carlo(
        current_balance_clp=89_610_000.0,  # Saldo con shock -10,39% de 100M
        target_balance_clp=100_000_000.0,
        monthly_contribution_clp=150_000.0,  # 10% de sueldo de 1.5M
        n_sims=10000,
        max_months=180,
    )
    elapsed = time.time() - t0

    assert elapsed < 1.5, f"La simulación tardó {elapsed:.3f}s, superando el límite de 1.5s"
    assert res["p10_meses"] <= res["p50_mediana_meses"] <= res["p90_meses"]
    assert 6.0 <= res["p50_mediana_meses"] <= 48.0


def test_evaluate_profile_impact(engine):
    """Verifica la evaluación del perfil integral de un afiliado próximo a jubilar."""
    profile = ActuarialProfile(
        saldo_actual_clp=89_610_000.0,
        afp="MODELO",
        edad_actual=64,
        sexo="hombre",
        edad_jubilacion=65,
        sueldo_imponible=1_800_000.0,
        tasa_tecnica=0.032,
    )

    impact = engine.evaluate_profile_impact(profile)

    assert impact.perdida_patrimonial_clp > 10_000_000.0
    assert impact.perdida_swaps_clp > 8_000_000.0
    assert impact.recorte_pension_mensual > 60_000.0
    assert impact.recorte_pension_pct > 9.5
    assert impact.monte_carlo_meses_recuperacion_p50 is not None
    assert impact.monte_carlo_meses_recuperacion_p50 > 0
