"""Pruebas unitarias para el módulo de visualizaciones editoriales (src/viz/)."""

import pytest

from src.config import CHARTS_DIR
from src.viz.charts_interactive import (
    build_interactive_product_1,
    build_interactive_product_2,
    build_interactive_product_3,
    build_interactive_product_4,
    build_interactive_product_5,
)
from src.viz.charts_social import (
    export_product_1_underwater_chart,
    export_product_2_waterfall_chart,
    export_product_3_duration_thermometer,
    export_product_4_herding_matrix,
)


def test_interactive_figures_build_successfully():
    """Verifica que las figuras interactivas de Plotly se construyan con sus tipos esperados."""
    fig1 = build_interactive_product_1()
    assert len(fig1.data) >= 3

    fig2 = build_interactive_product_2()
    assert len(fig2.data) == 1
    assert fig2.data[0].type == "waterfall"

    fig3 = build_interactive_product_3()
    assert len(fig3.data) == 2

    fig4 = build_interactive_product_4()
    assert len(fig4.data) == 1
    assert fig4.data[0].type == "bar"

    fig5 = build_interactive_product_5()
    assert len(fig5.data) >= 10


def test_static_charts_exported_exist():
    """Verifica que los archivos PNG 300 DPI en 16:9 y 4:5 existan en data/processed/charts/."""
    expected_files = [
        "producto1_underwater_var_16x9.png",
        "producto1_underwater_var_4x5.png",
        "producto2_waterfall_atribucion_16x9.png",
        "producto2_waterfall_atribucion_4x5.png",
        "producto3_termometro_duracion_swaps_16x9.png",
        "producto3_termometro_duracion_swaps_4x5.png",
        "producto4_heatmap_herding_afp_16x9.png",
        "producto4_heatmap_herding_afp_4x5.png",
        "producto1_underwater_var.html",
        "producto2_waterfall_atribucion.html",
        "producto3_termometro_duracion_swaps.html",
        "producto4_heatmap_herding_afp.html",
        "producto5_montecarlo_recuperacion.html",
    ]

    for fname in expected_files:
        fpath = CHARTS_DIR / fname
        assert fpath.exists(), f"No se encontró el archivo exportado: {fname}"
        assert fpath.stat().st_size > 1000, f"Archivo vacío o corrupto: {fname}"
