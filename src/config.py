"""Configuración global, rutas de acceso, constantes de auditoría y paleta editorial.

Proyecto: Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

# ==============================================================================
# 1. Rutas del Sistema de Archivos (Pathlib)
# ==============================================================================

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
CHARTS_DIR = PROCESSED_DIR / "charts"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
APP_DIR = PROJECT_ROOT / "app"
TESTS_DIR = PROJECT_ROOT / "tests"
DELIVERABLES_DIR = PROJECT_ROOT / "deliverables"

# Subdirectorios de datos crudos
SPENSIONES_CUOTAS_DIR = RAW_DIR / "spensiones_cuotas"
SPENSIONES_CARTERAS_DIR = RAW_DIR / "spensiones_carteras"
BCENTRAL_DIR = RAW_DIR / "bcentral"
MARKET_DIR = RAW_DIR / "market"
ACTUARIAL_DIR = RAW_DIR / "actuarial"

# Archivos de datos procesados
MASTER_DAILY_PANEL_PATH = PROCESSED_DIR / "master_daily_panel.parquet"
MONTHLY_CHECKPOINTS_PATH = PROCESSED_DIR / "monthly_audit_checkpoints.parquet"
AFP_DERIVATIVES_PANEL_PATH = PROCESSED_DIR / "afp_derivatives_panel.parquet"
RV2020_TABLE_PATH = ACTUARIAL_DIR / "tabla_rv2020.csv"

# ==============================================================================
# 2. URLs y Endpoints de Extracción
# ==============================================================================

SPENSIONES_VCF_BASE_URL = "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php"
SPENSIONES_STATS_BASE_URL = "https://www.spensiones.cl/portal/institucional/594/w3-propertyvalue-9921.html"
MINDICADOR_API_URL = "https://mindicador.cl/api"
BCENTRAL_SI3_BASE_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"

# ==============================================================================
# 3. Administradoras de Fondos de Pensiones (AFPs)
# ==============================================================================

AFPS: List[str] = [
    "CAPITAL",
    "CUPRUM",
    "HABITAT",
    "MODELO",
    "PLANVITAL",
    "PROVIDA",
    "UNO",
]

# Caída real acumulada oficial del Fondo E en 2026 (ene-sep) por administradora
AFP_REAL_RETURNS_2026: Dict[str, float] = {
    "MODELO": -0.109,     # -10,9%
    "CAPITAL": -0.108,    # -10,8%
    "CUPRUM": -0.106,     # -10,6%
    "HABITAT": -0.104,    # -10,4%
    "PROVIDA": -0.103,    # -10,3%
    "PLANVITAL": -0.101,  # -10,1%
    "UNO": -0.099,        # -9,9%
}

# ==============================================================================
# 4. Parámetros Auditados del Colapso 2026 (Ground Truth)
# ==============================================================================

# Fechas clave del periodo auditado
AUDIT_START_DATE = "2025-12-31"
AUDIT_SEP_DATE = "2026-09-30"
AUDIT_CURRENT_DATE = "2026-10-15"

# Retornos agregados del Fondo E
OFFICIAL_NOMINAL_RETURN_2026 = -0.0740   # -7,40% nominal
OFFICIAL_REAL_RETURN_2026 = -0.1039      # -10,39% real en UF
OFFICIAL_REAL_RETURN_SEP_2026 = -0.0492  # -4,92% real solo en septiembre

# Descomposición de Pérdidas Nominales (Return Attribution)
ATTRIBUTION_NOMINAL_PP = {
    "swaps_usd": -0.0450,          # -4,5 pp en swaps externos de tasa en USD (IRS 5Y/10Y)
    "swaps_local": -0.0140,        # -1,4 pp en swaps locales de tasa (SPC CLP/UF)
    "total_swaps": -0.0590,        # -5,9 pp (79,7% ~ 80% del daño nominal total)
    "forwards_usd": -0.0080,       # -0,8 pp por sobrecobertura corta de USD
    "physical_bonds": -0.0070,     # -0,7 pp en renta fija física nacional/internacional
    "total_nominal": -0.0740,      # -7,40%
}

# Parámetros de Duración y Sensibilidad a Tasas
HISTORICAL_DURATION_YEARS = 5.0
PHYSICAL_BONDS_DURATION_2026 = 10.2
SYNTHETIC_SWAPS_DURATION_2026 = 6.8
TOTAL_EFFECTIVE_DURATION_2026 = 17.0

# Evolución del Nocional en Swaps de Tasas Extranjeras (MM US$)
SWAPS_NOTIONAL_EVOLUTION_MM_USD: Dict[str, float] = {
    "2023-08": 5300.0,
    "2024-12": 107100.0,
    "2025-12": 206900.0,
    "2026-09": 185000.0,  # En proceso de desarme por límite regulatorio
}

# Ratio de Sobrecobertura Cambiaria (Forwards Vendidos USD / Activos en Moneda Extranjera)
FX_HEDGE_RATIOS: Dict[str, float] = {
    "2025-12": 0.47,  # 47%
    "2026-07": 1.21,  # 121%
    "2026-09": 1.50,  # 150% (posición corta neta en USD)
}

# Parámetros de Mercado Subyacentes
US10Y_START_2026 = 0.0418   # 4,18% a fin 2025
US10Y_SEP_2026 = 0.0529     # 5,29% a fin sep 2026 (+111 pb)
USDCLP_START_2026 = 911.0
USDCLP_SEP_2026 = 970.0

# Hito Regulatorio
REGULATORY_STRESS_LIMIT_PCT = 0.02   # Tope de 2% de pérdida esperada bajo estrés
REGULATORY_DEADLINE = "2026-11-05"   # Plazo perentorio para desarmar posiciones

# ==============================================================================
# 5. Parámetros del Modelo Actuarial y Monte Carlo
# ==============================================================================

DEFAULT_TECHNICAL_RATE = 0.032       # 3,2% real anual (tasa técnica de retiro programado)
RETIREMENT_AGE_MEN = 65
RETIREMENT_AGE_WOMEN = 60
LEGAL_CONTRIBUTION_RATE = 0.10       # 10% de cotización obligatoria
MONTE_CARLO_SIMULATIONS = 10000
MONTE_CARLO_MAX_MONTHS = 180         # 15 años de horizonte de simulación

# ==============================================================================
# 6. Paleta de Colores Editorial (Financial Times / Bloomberg Dark Mode)
# ==============================================================================

PALETTE = {
    "swaps_loss": "#D90429",       # Rojo Carmesí (Pérdidas por Derivados/Swaps)
    "swaps_dark": "#8D0801",       # Rojo Borgoña Profundo
    "forwards_loss": "#F77F00",    # Ámbar / Naranja (Pérdidas por Forwards FX)
    "bonds_physical": "#2B2D42",   # Azul Acero / Marino (Renta fija física)
    "fondo_e": "#E63946",          # Coral / Rojo Intenso (Fondo E)
    "fondo_a": "#2A9D8F",          # Verde Petróleo (Fondo A - Renta Variable)
    "deposit": "#457B9D",          # Azul Slate (Depósito a Plazo / Libre de Riesgo)
    "background_dark": "#0D1117",  # Fondo Principal Dark Mode
    "surface_dark": "#161B22",     # Superficie de Tarjetas / Paneles
    "border_dark": "#30363D",      # Bordes
    "text_primary": "#F0F6FC",     # Texto Principal Alto Contraste
    "text_muted": "#8B949E",       # Texto Secundario / Metadatos
    "grid_color": "#21262D",       # Cuadrículas de Gráficos
}
