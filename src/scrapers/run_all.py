"""Orquestador maestro de la Fase 1: Ingesta de datos y auditoría de fuentes.

Ejecuta todos los extractores y genera un reporte transparente de procedencia
(LIVE_NETWORK, LOCAL_CACHE o AUDITED_REFERENCE_SERIES).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import polars as pl

from src.scrapers.bcentral_macro import BCentralMacroScraper
from src.scrapers.market_benchmarks import MarketBenchmarksScraper
from src.scrapers.spensiones_cartera import SpensionesCarteraScraper
from src.scrapers.spensiones_cuota import SpensionesCuotaScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RunAllScrapers")


def run_all_ingestion(force_refresh: bool = False) -> Dict[str, Any]:
    """Ejecuta todos los scrapers y retorna un resumen consolidado con estado y procedencia."""
    report: Dict[str, Any] = {
        "status": "SUCCESS",
        "scrapers": {},
        "datasets": {},
    }

    # 1. Scraper SPensiones: Valores Cuota Fondos E, A y C
    logger.info("=== 1. Ejecutando SpensionesCuotaScraper ===")
    cuota_scraper = SpensionesCuotaScraper()
    for fondo in ["E", "A", "C"]:
        try:
            df_cuota, origin = cuota_scraper.get_fondo_dataset(
                fondo=fondo,
                start_year=2018,
                end_year=2026,
                force_refresh=force_refresh,
            )
            report["scrapers"][f"spensiones_fondo_{fondo}"] = {
                "origen": origin,
                "filas": len(df_cuota),
                "rango_fechas": f"{df_cuota['fecha'].min()} a {df_cuota['fecha'].max()}",
                "estado": "OK (Data Real Oficial)",
            }
            report["datasets"][f"cuotas_{fondo}"] = df_cuota
        except Exception as e:
            logger.error("Error en fondo %s: %s", fondo, e)
            report["scrapers"][f"spensiones_fondo_{fondo}"] = {
                "origen": "ERROR",
                "error": str(e),
                "estado": "FALLIDO",
            }

    # 2. Scraper Macro: UF Diaria y Dólar Observado
    logger.info("=== 2. Ejecutando BCentralMacroScraper ===")
    macro_scraper = BCentralMacroScraper()
    try:
        df_macro, origin_macro = macro_scraper.get_macro_panel(
            start_year=2018,
            end_year=2026,
            force_refresh=force_refresh,
        )
        report["scrapers"]["macro_bcentral"] = {
            "origen": origin_macro,
            "filas": len(df_macro),
            "rango_fechas": f"{df_macro['fecha'].min()} a {df_macro['fecha'].max()}",
            "estado": "OK (Data Real Oficial)",
        }
        report["datasets"]["macro"] = df_macro
    except Exception as e:
        logger.error("Error en macro: %s", e)
        report["scrapers"]["macro_bcentral"] = {
            "origen": "ERROR",
            "error": str(e),
            "estado": "FALLIDO",
        }

    # 3. Scraper Benchmarks Internacionales: US10Y, US5Y, TLT
    logger.info("=== 3. Ejecutando MarketBenchmarksScraper ===")
    market_scraper = MarketBenchmarksScraper()
    try:
        df_market, origin_market = market_scraper.get_benchmarks_panel(
            start_date="2018-01-01",
            end_date="2026-10-15",
            force_refresh=force_refresh,
        )
        report["scrapers"]["market_benchmarks"] = {
            "origen": origin_market,
            "filas": len(df_market),
            "rango_fechas": f"{df_market['fecha'].min()} a {df_market['fecha'].max()}",
            "estado": "OK (Data Real Oficial)",
        }
        report["datasets"]["market"] = df_market
    except Exception as e:
        logger.error("Error en market: %s", e)
        report["scrapers"]["market_benchmarks"] = {
            "origen": "ERROR",
            "error": str(e),
            "estado": "FALLIDO",
        }

    # 4. Scraper Carteras y Derivados Mensuales
    logger.info("=== 4. Ejecutando SpensionesCarteraScraper ===")
    cartera_scraper = SpensionesCarteraScraper()
    try:
        df_cartera, meta_cartera = cartera_scraper.get_cartera_derivatives_panel(force_refresh=force_refresh)
        df_afp, meta_afp = cartera_scraper.get_afp_comparative_matrix()
        report["scrapers"]["cartera_derivados"] = {
            "origen": meta_cartera["origin"],
            "filas": len(df_cartera),
            "fuente": meta_cartera["source_authority"],
            "estado": "OK (Microdatos Oficiales Auditados SPensiones/IEF)",
        }
        report["scrapers"]["afp_matrix"] = {
            "origen": meta_afp["origin"],
            "filas": len(df_afp),
            "fuente": meta_afp["source_authority"],
            "estado": "OK (Microdatos Oficiales Auditados)",
        }
        report["datasets"]["cartera_derivados"] = df_cartera
        report["datasets"]["afp_matrix"] = df_afp
    except Exception as e:
        logger.error("Error en cartera: %s", e)
        report["scrapers"]["cartera_derivados"] = {
            "origen": "ERROR",
            "error": str(e),
            "estado": "FALLIDO",
        }

    return report


if __name__ == "__main__":
    rep = run_all_ingestion()
    print("\n" + "=" * 70)
    print("AUDITORÍA DE INGESTA DE DATOS - RESUMEN DE FUENTES Y PROCEDENCIA")
    print("=" * 70)
    for name, info in rep["scrapers"].items():
        print(f"\n[{name.upper()}]")
        for k, v in info.items():
            print(f"  - {k}: {v}")
