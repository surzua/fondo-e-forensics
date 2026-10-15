"""Contratos de datos y esquemas de validación con Pydantic y Pandera.

Garantiza la tipificación estática, integridad de fechas, ausencia de nulos críticos
y rangos válidos para los datasets de cuotas, macro y atribución factorial.
"""

from __future__ import annotations

from datetime import date
from typing import Optional
import pandera.polars as pa
import polars as pl
from pydantic import BaseModel, Field, field_validator


# ==============================================================================
# 1. Modelos Pydantic (Validación por Registro / API)
# ==============================================================================

class CuotaRecord(BaseModel):
    """Representa un registro individual de valor cuota y patrimonio para una AFP y fondo."""
    fecha: date
    fondo: str = Field(pattern=r"^[A-E]$")
    afp: str
    valor_cuota: float = Field(gt=0)
    patrimonio: float = Field(ge=0)

    @field_validator("afp")
    @classmethod
    def validate_afp_name(cls, v: str) -> str:
        return v.strip().upper()


class MacroRecord(BaseModel):
    """Representa un registro diario de variables macroeconómicas."""
    fecha: date
    uf: float = Field(gt=0, description="Valor oficial de la Unidad de Fomento")
    dolar_observado: Optional[float] = Field(default=None, gt=0)
    us10y: Optional[float] = Field(default=None, description="Rendimiento US Treasury 10Y en %")
    us5y: Optional[float] = Field(default=None, description="Rendimiento US Treasury 5Y en %")
    tlt_close: Optional[float] = Field(default=None, description="Precio de cierre ETF TLT")


# ==============================================================================
# 2. Esquemas Pandera para Polars DataFrames (Validación en Bloque / ETL)
# ==============================================================================

class CuotaDiariaDataFrameSchema(pa.DataFrameModel):
    """Esquema de validación para el panel estandarizado de valores cuota en Polars."""
    fecha: pl.Date = pa.Field()
    fondo: pl.String = pa.Field(isin=["A", "B", "C", "D", "E"])
    afp: pl.String = pa.Field()
    valor_cuota: pl.Float64 = pa.Field(gt=0.0)
    patrimonio: pl.Float64 = pa.Field(ge=0.0)

    class Config:
        strict = True
        coerce = True


class MasterDailyPanelSchema(pa.DataFrameModel):
    """Esquema de validación para el panel diario maestro analítico."""
    fecha: pl.Date = pa.Field()
    vc_nominal: pl.Float64 = pa.Field(gt=0.0)
    uf: pl.Float64 = pa.Field(gt=0.0)
    vc_real_uf: pl.Float64 = pa.Field(gt=0.0)
    ret_nominal_diario: pl.Float64 = pa.Field()
    ret_real_diario: pl.Float64 = pa.Field()
    ret_real_acum_2026: pl.Float64 = pa.Field()
    drawdown_real: pl.Float64 = pa.Field(le=0.0)
    dolar_observado: pl.Float64 = pa.Field(gt=0.0, nullable=True)
    us10y: pl.Float64 = pa.Field(nullable=True)

    class Config:
        strict = False
        coerce = True


class MonthlyCheckpointSchema(pa.DataFrameModel):
    """Esquema de validación para los cierres mensuales auditados."""
    periodo: pl.String = pa.Field(str_matches=r"^\d{4}-\d{2}$")
    ret_nominal_mensual: pl.Float64 = pa.Field()
    ret_real_mensual: pl.Float64 = pa.Field()
    ret_real_acum_2026: pl.Float64 = pa.Field()
    contrib_swaps_usd: pl.Float64 = pa.Field()
    contrib_swaps_local: pl.Float64 = pa.Field()
    contrib_forwards_fx: pl.Float64 = pa.Field()
    contrib_bonds_phys: pl.Float64 = pa.Field()
    hedge_ratio_fx: pl.Float64 = pa.Field(ge=0.0)
    swaps_notional_mm_usd: pl.Float64 = pa.Field(ge=0.0)

    class Config:
        strict = False
        coerce = True


class AfpDerivativesPanelSchema(pa.DataFrameModel):
    """Esquema de validación para la matriz comparativa de las 7 AFP."""
    afp: pl.String = pa.Field()
    ret_real_2026_pct: pl.Float64 = pa.Field()
    danio_swaps_pp: pl.Float64 = pa.Field()
    ratio_sobrecobertura_usd: pl.Float64 = pa.Field(ge=0.0)
    perfil_agresividad: pl.String = pa.Field()

    class Config:
        strict = False
        coerce = True


# ==============================================================================
# 3. Modelos Pydantic para el Motor Actuarial
# ==============================================================================

class ActuarialProfile(BaseModel):
    """Parámetros de entrada para el cálculo actuarial y simulación de Monte Carlo."""
    saldo_actual_clp: float = Field(gt=0, description="Saldo actual en Fondo E ($ CLP)")
    afp: str = Field(default="SISTEMA", description="AFP del afiliado")
    edad_actual: int = Field(ge=40, le=80, description="Edad cronológica actual")
    sexo: str = Field(pattern=r"^(H|M|hombre|mujer)$", description="Sexo biológico para tablas de mortalidad")
    edad_jubilacion: int = Field(ge=50, le=80, description="Edad legal o planificada de retiro")
    sueldo_imponible: float = Field(default=0.0, ge=0.0, description="Sueldo imponible mensual para cotizaciones")
    tasa_tecnica: float = Field(default=0.032, gt=0.0, le=0.10, description="Tasa técnica de descuento anual")

    @field_validator("sexo")
    @classmethod
    def normalize_sexo(cls, v: str) -> str:
        v = v.strip().lower()
        return "hombre" if v in ["h", "hombre"] else "mujer"


class ActuarialImpactResult(BaseModel):
    """Resultado del impacto patrimonial y recorte vitalicio de pensión."""
    saldo_inicial_estimado: float
    saldo_post_shock: float
    perdida_patrimonial_clp: float
    perdida_swaps_clp: float
    cnu: float
    pension_pre_shock_mensual: float
    pension_post_shock_mensual: float
    recorte_pension_mensual: float
    recorte_pension_pct: float
    monte_carlo_meses_recuperacion_p50: Optional[float]
    monte_carlo_meses_recuperacion_p10: Optional[float]
    monte_carlo_meses_recuperacion_p90: Optional[float]

