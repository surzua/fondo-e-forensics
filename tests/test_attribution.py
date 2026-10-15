"""Pruebas unitarias para el motor de atribución factorial y duración (src/models/attribution.py)."""

import pytest

from src.config import (
    OFFICIAL_NOMINAL_RETURN_2026,
    OFFICIAL_REAL_RETURN_2026,
    TOTAL_EFFECTIVE_DURATION_2026,
)
from src.models.attribution import (
    calculate_duration_sensitivity,
    get_afp_attribution_table,
    get_official_attribution_breakdown,
    get_waterfall_chart_data,
)


def test_official_attribution_sums_to_nominal_total():
    """Verifica que la suma de componentes factoriales sume exactamente el retorno nominal (-7,40%)."""
    attr = get_official_attribution_breakdown()

    sum_nominal_pp = (
        attr["swaps_tasas_usd_pp"]
        + attr["swaps_tasas_locales_pp"]
        + attr["forwards_fx_pp"]
        + attr["bonos_fisicos_pp"]
    )

    assert pytest.approx(sum_nominal_pp, rel=1e-5) == OFFICIAL_NOMINAL_RETURN_2026 * 100.0
    assert pytest.approx(attr["total_swaps_pp"], rel=1e-5) == -5.90
    # Los swaps representan cerca del 80% (79,7%) del daño nominal
    assert 79.0 <= attr["pct_daño_explicado_por_swaps"] <= 80.5


def test_inflation_links_nominal_to_real():
    """Verifica la relación matemática entre retorno nominal, inflación UF y retorno real:

    (1 + R_nom) / (1 + pi_uf) = 1 + R_real
    """
    attr = get_official_attribution_breakdown()
    r_nom = attr["retorno_nominal_total_pct"] / 100.0
    pi_uf = attr["inflacion_uf_periodo_pct"] / 100.0
    r_real_calc = ((1.0 + r_nom) / (1.0 + pi_uf)) - 1.0

    assert pytest.approx(r_real_calc, rel=1e-4) == OFFICIAL_REAL_RETURN_2026


def test_duration_sensitivity_model():
    """Verifica el cálculo de duración efectiva combinada (10,2 + 6,8 = 17 años)."""
    sens = calculate_duration_sensitivity()

    assert sens["duracion_total_efectiva_anios"] == TOTAL_EFFECTIVE_DURATION_2026
    # Para un alza de ~111 pb con 17 años de duración, el impacto de duración supera -18% en el tramo
    assert sens["impacto_teorico_lineal_pct"] < -18.0
    # La sobre-sensibilidad generada respecto a los 5 años históricos debe ser marcadamente negativa
    assert sens["sobre_sensibilidad_generada_pct"] < -10.0


def test_waterfall_data_structure():
    """Verifica que los datos del waterfall contengan categorías, valores y medidas válidas."""
    wf = get_waterfall_chart_data()

    assert len(wf["categories"]) == len(wf["values"]) == len(wf["measure"])
    assert "total" in wf["measure"]
    assert "relative" in wf["measure"]
    # El valor final acumulado debe ser el retorno real (-10,39%)
    assert pytest.approx(wf["values"][-1], rel=1e-4) == OFFICIAL_REAL_RETURN_2026 * 100.0


def test_afp_attribution_table():
    """Verifica que la tabla de AFPs contenga las 7 administradoras y sus pérdidas sean consistentes."""
    df_afp = get_afp_attribution_table()

    assert len(df_afp) == 7
    assert "MODELO" in df_afp["afp"].to_list()
    assert "UNO" in df_afp["afp"].to_list()

    # AFP Modelo debe liderar las pérdidas reales (menor retorno)
    assert df_afp.filter(df_afp["afp"] == "MODELO")["ret_real_total_pct"][0] <= -10.8
    # AFP Uno debe tener la menor caída (-9,9%)
    assert df_afp.filter(df_afp["afp"] == "UNO")["ret_real_total_pct"][0] >= -10.0
