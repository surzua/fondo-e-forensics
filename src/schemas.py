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
