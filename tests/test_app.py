from app.components.report import generate_audit_csv, generate_audit_report_html
from app.components.state import get_latest_uf_value
from app.components.ui import render_badge
from src.models.actuarial import ActuarialEngine
from src.schemas import ActuarialProfile


def test_state_and_uf_retrieval():
    """Valida que la UF se recupere adecuadamente y sea positiva."""
    uf = get_latest_uf_value()
    assert uf > 30000.0


def test_report_generation():
    """Valida la generación correcta del reporte ejecutivo en HTML y CSV."""
    profile = ActuarialProfile(
        saldo_actual_clp=89_610_000.0,
        afp="MODELO",
        edad_actual=63,
        sexo="hombre",
        edad_jubilacion=65,
        sueldo_imponible=1_800_000.0,
        tasa_tecnica=0.032,
    )
    engine = ActuarialEngine()
    impact = engine.evaluate_profile_impact(profile, shock_pct=-0.1090)

    html = generate_audit_report_html(
        profile=profile,
        impact=impact,
        afp_real_return_pct=-10.90,
        afp_swaps_damage_pp=-6.10,
    )

    assert "<!DOCTYPE html>" in html
    assert "AFP MODELO" in html
    assert f"-${impact.perdida_patrimonial_clp:,.0f}" in html
    assert "RV-2020" in html

    csv_data = generate_audit_csv(
        profile=profile,
        impact=impact,
        afp_real_return_pct=-10.90,
        afp_swaps_damage_pp=-6.10,
    )

    assert "variable,valor,unidad,descripcion" in csv_data
    assert "afp,MODELO,texto" in csv_data
    assert "recorte_pension_mensual" in csv_data


def test_ui_components():
    """Valida que los helpers de UI generen el HTML esperado."""
    badge = render_badge("Test Badge", "red")
    assert "badge-forensic badge-red" in badge
    assert "Test Badge" in badge
