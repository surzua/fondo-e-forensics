"""Extractor de benchmarks internacionales de tasas y renta fija (US10Y, US5Y, TLT).

Utiliza yfinance para descargar series diarias oficiales del Tesoro de EE.UU.
y del ETF de bonos de larga duración TLT.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import polars as pl
import yfinance as yf

from src.config import MARKET_DIR
from src.scrapers.base import BaseScraper

logger = logging.getLogger("MarketBenchmarksScraper")


class MarketBenchmarksScraper(BaseScraper):
    """Descarga series de mercado internacional: ^TNX (US10Y), ^FVX (US5Y), TLT y USDCLP=X."""

    def __init__(self, cache_dir: Optional[Path] = None):
        super().__init__(cache_dir=cache_dir or MARKET_DIR, timeout=30.0, max_retries=3)

    def download_ticker(
        self,
        ticker_symbol: str,
        start_date: str = "2018-01-01",
        end_date: str = "2026-10-15",
        force_refresh: bool = False,
    ) -> Tuple[pd.DataFrame, str]:
        """Descarga el historial diario de un ticker desde Yahoo Finance con caché local."""
        clean_symbol = ticker_symbol.replace("^", "").replace("=", "_")
        cache_file = self.cache_dir / f"{clean_symbol}_{start_date}_{end_date}.parquet"

        if cache_file.exists() and not force_refresh:
            logger.info("Cargando %s desde caché local: %s", ticker_symbol, cache_file.name)
            df_cached = pd.read_parquet(cache_file)
            return df_cached, "LOCAL_CACHE"

        logger.info("Descargando en vivo ticker %s (%s a %s)...", ticker_symbol, start_date, end_date)
        ticker = yf.Ticker(ticker_symbol)
        df_live = ticker.history(start=start_date, end=end_date)

        if df_live.empty:
            raise RuntimeError(f"No se obtuvieron datos para el ticker {ticker_symbol}")

        # Reset index para tener la columna Date
        df_live = df_live.reset_index()
        # Asegurar Date como tipo date
        df_live["Date"] = pd.to_datetime(df_live["Date"]).dt.date
        df_live.to_parquet(cache_file)
        logger.info("Guardado en caché: %s (%d filas)", cache_file.name, len(df_live))
        return df_live, "LIVE_NETWORK"

    def get_benchmarks_panel(
        self,
        start_date: str = "2018-01-01",
        end_date: str = "2026-10-15",
        force_refresh: bool = False,
    ) -> Tuple[pl.DataFrame, str]:
        """Descarga y unifica US10Y (^TNX), US5Y (^FVX) y TLT en un panel Polars diario."""
        origins = set()

        # 1. US 10Y Yield (^TNX)
        df_tnx, o1 = self.download_ticker("^TNX", start_date, end_date, force_refresh)
        origins.add(o1)

        # 2. US 5Y Yield (^FVX)
        try:
            df_fvx, o2 = self.download_ticker("^FVX", start_date, end_date, force_refresh)
            origins.add(o2)
        except Exception as e:
            logger.warning("No fue posible descargar ^FVX: %s", e)
            df_fvx = pd.DataFrame()

        # 3. TLT ETF
        try:
            df_tlt, o3 = self.download_ticker("TLT", start_date, end_date, force_refresh)
            origins.add(o3)
        except Exception as e:
            logger.warning("No fue posible descargar TLT: %s", e)
            df_tlt = pd.DataFrame()

        # Unificar mediante Pandas y convertir a Polars
        merged = df_tnx[["Date", "Close"]].rename(columns={"Close": "us10y"})
        
        if not df_fvx.empty:
            merged = merged.merge(
                df_fvx[["Date", "Close"]].rename(columns={"Close": "us5y"}),
                on="Date",
                how="left",
            )
        else:
            merged["us5y"] = None

        if not df_tlt.empty:
            merged = merged.merge(
                df_tlt[["Date", "Close"]].rename(columns={"Close": "tlt_close"}),
                on="Date",
                how="left",
            )
        else:
            merged["tlt_close"] = None

        merged = merged.rename(columns={"Date": "fecha"}).sort_values("fecha")
        pl_df = pl.from_pandas(merged)
        
        dominant_origin = "LIVE_NETWORK" if "LIVE_NETWORK" in origins else "LOCAL_CACHE"
        logger.info("Panel de benchmarks unificado: %d días [Origen: %s]", len(pl_df), dominant_origin)
        return pl_df, dominant_origin
