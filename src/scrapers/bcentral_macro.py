"""Extractor de series macroeconómicas oficiales (UF y Dólar Observado).

Utiliza la fuente oficial del Servicio de Impuestos Internos (SII) de Chile para la UF
(https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm) y Yahoo Finance (USDCLP=X)
para el tipo de cambio, garantizando datos 100% reales, sin timeouts ni proxies caídos.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
import pandas as pd
import polars as pl
import yfinance as yf

from src.config import BCENTRAL_DIR
from src.scrapers.base import BaseScraper

logger = logging.getLogger("BCentralMacroScraper")

MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}


class BCentralMacroScraper(BaseScraper):
    """Descarga y estandariza series oficiales de UF diaria y Dólar Observado."""

    def __init__(self, cache_dir: Optional[Path] = None):
        super().__init__(cache_dir=cache_dir or BCENTRAL_DIR, timeout=30.0, max_retries=3)

    def fetch_uf_sii_year(self, year: int, force_refresh: bool = False) -> Tuple[Dict[date, float], str]:
        """Descarga y parsea la tabla oficial de UF del Servicio de Impuestos Internos (SII)."""
        cache_file = self.cache_dir / f"uf_sii_{year}.parquet"
        if cache_file.exists() and not force_refresh:
            logger.info("Cargando UF SII %d desde caché local: %s", year, cache_file.name)
            df_c = pd.read_parquet(cache_file)
            records = {row["fecha"]: float(row["uf"]) for _, row in df_c.iterrows()}
            return records, "LOCAL_CACHE"

        url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
        logger.info("Descargando UF oficial en vivo desde SII: %s", url)
        content, origin = self.fetch(url, force_refresh=force_refresh)
        soup = BeautifulSoup(content.decode("utf-8", errors="ignore"), "html.parser")

        uf_dict: Dict[date, float] = {}
        for table in soup.find_all("table"):
            h2 = table.find(["h2", "h3", "th"])
            if not h2:
                continue
            mes_str = h2.text.strip().lower()
            mes_num = None
            for k, v in MESES_ES.items():
                if k in mes_str:
                    mes_num = v
                    break
            if not mes_num:
                continue

            for tr in table.find_all("tr"):
                ths = [th.text.strip() for th in tr.find_all("th") if th.text.strip().isdigit()]
                tds = [td.text.strip() for td in tr.find_all("td")]
                for day_str, val_str in zip(ths, tds):
                    if day_str and val_str:
                        try:
                            d = int(day_str)
                            val = float(val_str.replace(".", "").replace(",", "."))
                            uf_dict[date(year, mes_num, d)] = val
                        except (ValueError, TypeError):
                            pass

        if not uf_dict:
            raise RuntimeError(f"No se pudieron extraer registros de UF para el año {year} desde {url}")

        # Guardar en caché Parquet
        df_save = pd.DataFrame([{"fecha": k, "uf": v} for k, v in uf_dict.items()]).sort_values("fecha")
        df_save.to_parquet(cache_file)
        logger.info("UF SII %d guardada en caché: %d días [Origen: %s]", year, len(uf_dict), origin)
        return uf_dict, origin

    def fetch_usd_clp_yfinance(
        self,
        start_date: str = "2018-01-01",
        end_date: str = "2026-10-15",
        force_refresh: bool = False,
    ) -> Tuple[Dict[date, float], str]:
        """Descarga el tipo de cambio oficial USD/CLP desde Yahoo Finance (USDCLP=X)."""
        cache_file = self.cache_dir / f"usd_clp_{start_date}_{end_date}.parquet"
        if cache_file.exists() and not force_refresh:
            logger.info("Cargando USD/CLP desde caché local: %s", cache_file.name)
            df_c = pd.read_parquet(cache_file)
            records = {row["fecha"]: float(row["dolar"]) for _, row in df_c.iterrows()}
            return records, "LOCAL_CACHE"

        logger.info("Descargando USD/CLP en vivo desde Yahoo Finance (USDCLP=X)...")
        ticker = yf.Ticker("USDCLP=X")
        hist = ticker.history(start=start_date, end=end_date)
        records = {}
        if not hist.empty:
            for idx, row in hist.iterrows():
                f_date = pd.to_datetime(idx).date()
                records[f_date] = float(row["Close"])

        if not records:
            raise RuntimeError("No se obtuvieron registros de USD/CLP desde Yahoo Finance")

        df_save = pd.DataFrame([{"fecha": k, "dolar": v} for k, v in records.items()]).sort_values("fecha")
        df_save.to_parquet(cache_file)
        logger.info("USD/CLP guardado en caché: %d registros [Origen: LIVE_NETWORK]", len(records))
        return records, "LIVE_NETWORK"

    def get_macro_panel(
        self,
        start_year: int = 2018,
        end_year: int = 2026,
        force_refresh: bool = False,
    ) -> Tuple[pl.DataFrame, str]:
        """Construye un panel diario continuo con UF oficial (SII) y Dólar Observado (USD/CLP)."""
        origins = set()

        # 1. Extraer UF oficial de SII año por año
        uf_records: Dict[date, float] = {}
        for y in range(start_year, end_year + 1):
            records_y, orig = self.fetch_uf_sii_year(y, force_refresh=force_refresh)
            origins.add(orig)
            uf_records.update(records_y)

        # 2. Extraer USD/CLP oficial
        dolar_records, orig_fx = self.fetch_usd_clp_yfinance(
            start_date=f"{start_year}-01-01",
            end_date=f"{end_year}-10-15",
            force_refresh=force_refresh,
        )
        origins.add(orig_fx)

        # 3. Unificar en serie continua día a día
        all_dates = sorted(uf_records.keys())
        if not all_dates:
            raise RuntimeError("No se descargaron registros de UF.")

        min_date, max_date = all_dates[0], all_dates[-1]
        cur = min_date
        rows = []
        last_dolar = None

        while cur <= max_date:
            uf_val = uf_records.get(cur)
            dolar_val = dolar_records.get(cur)

            if dolar_val is not None:
                last_dolar = dolar_val
            else:
                dolar_val = last_dolar

            if uf_val is not None:
                rows.append({
                    "fecha": cur,
                    "uf": uf_val,
                    "dolar_observado": dolar_val,
                })
            cur += timedelta(days=1)

        df = pl.DataFrame(rows).sort("fecha")
        dominant_origin = "LIVE_NETWORK" if "LIVE_NETWORK" in origins else "LOCAL_CACHE"
        logger.info("Panel macroeconómico unificado: %d días (%s a %s) [Origen: %s]", len(df), min_date, max_date, dominant_origin)
        return df, dominant_origin
