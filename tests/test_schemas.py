"""Pruebas unitarias para esquemas de datos y configuración del proyecto."""

from datetime import date
import pytest
from pydantic import ValidationError

from src.config import (
    AFPS,
    OFFICIAL_NOMINAL_RETURN_2026,
    OFFICIAL_REAL_RETURN_2026,
    TOTAL_EFFECTIVE_DURATION_2026,
    ATTRIBUTION_NOMINAL_PP,
)
from src.schemas import CuotaRecord, MacroRecord


def test_config_constants():
    """Valida la consistencia de las constantes maestras de auditoría."""
    assert len(AFPS) == 7
    assert "MODELO" in AFPS
    assert "CAPITAL" in AFPS
    assert OFFICIAL_REAL_RETURN_2026 == -0.1039
    assert OFFICIAL_NOMINAL_RETURN_2026 == -0.0740
    assert TOTAL_EFFECTIVE_DURATION_2026 == 17.0
    
    # La suma de atribución factorial debe cuadrar con el retorno nominal total
    total_attrib = (
        ATTRIBUTION_NOMINAL_PP["swaps_usd"]
        + ATTRIBUTION_NOMINAL_PP["swaps_local"]
        + ATTRIBUTION_NOMINAL_PP["forwards_usd"]
        + ATTRIBUTION_NOMINAL_PP["physical_bonds"]
    )
    assert pytest.approx(total_attrib, abs=1e-4) == OFFICIAL_NOMINAL_RETURN_2026


def test_cuota_record_valid():
    """Valida que un registro válido de valor cuota sea aceptado."""
    record = CuotaRecord(
        fecha=date(2026, 9, 30),
        fondo="E",
        afp="habitat",
        valor_cuota=45230.12,
        patrimonio=1250000.5,
    )
    assert record.afp == "HABITAT"
    assert record.fondo == "E"
    assert record.valor_cuota > 0


def test_cuota_record_invalid_fondo():
    """Valida que un fondo inexistente falle la validación."""
    with pytest.raises(ValidationError):
        CuotaRecord(
            fecha=date(2026, 9, 30),
            fondo="Z",  # Inválido
            afp="HABITAT",
            valor_cuota=45230.12,
            patrimonio=1250000.5,
        )


def test_macro_record_valid():
    """Valida la creación de un registro macroeconómico."""
    record = MacroRecord(
        fecha=date(2026, 9, 30),
        uf=37980.50,
        dolar_observado=965.40,
        us10y=5.25,
    )
    assert record.uf == 37980.50
    assert record.dolar_observado == 965.40
