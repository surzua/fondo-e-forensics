"""Scraper y parser de series diarias de Valor Cuota y Patrimonio de la Superintendencia de Pensiones.

Descarga directa en vivo desde https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php
y cálculo del promedio ponderado por patrimonio del sistema.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx
import polars as pl

from src.config import AFPS, SPENSIONES_CUOTAS_DIR, SPENSIONES_VCF_BASE_URL
from src.scrapers.base import BaseScraper

logger = logging.getLogger("SpensionesCuotaScraper")


class SpensionesCuotaScraper(BaseScraper):
    """Descarga y procesa series diarias históricas de valor cuota y patrimonio por AFP."""

    def __init__(self, cache_dir: Optional[Path] = None):
        super().__init__(cache_dir=cache_dir or SPENSIONES_CUOTAS_DIR, timeout=45.0, max_retries=3)
        self.endpoint_xls = "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php"

    def download_fondo_raw(
        self,
        fondo: str = "E",
        start_year: int = 2018,
        end_year: int = 2026,
        force_refresh: bool = False,
    ) -> Tuple[Path, str]:
        """Descarga el archivo plano oficial de valores cuota para un fondo específico.

        Retorna:
            (ruta_archivo, procedencia) donde procedencia es 'LIVE_NETWORK' o 'LOCAL_CACHE'.
        """
        fondo = fondo.upper()
        if fondo not in ["A", "B", "C", "D", "E"]:
            raise ValueError(f"Fondo inválido: {fondo}. Debe ser A, B, C, D o E.")

        target_file = self.cache_dir / f"vcf_{fondo}_{start_year}_{end_year}.csv"
        if target_file.exists() and not force_refresh:
            logger.info("Archivo local ya existente: %s", target_file)
            return target_file, "LOCAL_CACHE"

        # SPensiones requiere establecer sesión en vcfAFP.php antes de solicitar vcfAFPxls.php
        init_url = f"{SPENSIONES_VCF_BASE_URL}?tf={fondo}"
        headers = {
            "Referer": init_url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        # 1. Petición inicial para cookies de sesión
        with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
            client.headers.update(self.get_headers(headers))
            r_init = client.get(init_url)
            if r_init.status_code != 200:
                raise RuntimeError(f"Error al inicializar sesión en SPensiones: HTTP {r_init.status_code}")

            # 2. Descarga del archivo con rango de años
            params = {
                "aaaaini": str(start_year),
                "aaaafin": str(end_year),
                "tf": fondo,
                "fecconf": datetime.now().strftime("%Y%m%d"),
            }
            logger.info("Descargando Fondo %s (%d-%d) desde SPensiones...", fondo, start_year, end_year)
            r_data = client.get(self.endpoint_xls, params=params)

            if r_data.status_code != 200:
                raise RuntimeError(f"Error descargando datos de SPensiones: HTTP {r_data.status_code}")

            content = r_data.content
            if len(content) < 500:
                raise RuntimeError(f"Respuesta inesperada de SPensiones (contenido muy corto): {content.decode('latin-1', errors='ignore')}")

            target_file.write_bytes(content)
            logger.info("Datos del Fondo %s guardados exitosamente en %s (%d bytes)", fondo, target_file, len(content))
            return target_file, "LIVE_NETWORK"

    def parse_csv(self, file_path: Path, fondo: str) -> pl.DataFrame:
        """Parsea el archivo crudo de SPensiones manejando la estructura de dos filas de encabezado,

        separador punto y coma, puntos de miles y comas decimales.
        """
        # Lectura con encoding latino típico de SPensiones
        text = file_path.read_text(encoding="latin-1")
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if len(lines) < 4:
            raise ValueError(f"Archivo {file_path} no contiene suficientes filas para parsear.")

        # Buscar la fila que contiene las AFPs
        header_idx = -1
        for idx, line in enumerate(lines[:10]):
            if "CAPITAL" in line.upper() and "HABITAT" in line.upper():
                header_idx = idx
                break

        if header_idx == -1:
            raise ValueError(f"No se encontró el encabezado de AFPs en {file_path}")

        # Identificar las AFPs presentes en las columnas
        afp_line = lines[header_idx].split(";")
        # La estructura típica es: Fecha; AFP1;; AFP2;; AFP3...
        afp_names: List[str] = []
        for col in afp_line[1:]:
            col_clean = col.strip().upper()
            if col_clean and col_clean in AFPS:
                afp_names.append(col_clean)

        logger.info("AFPs identificadas en archivo (%s): %s", fondo, afp_names)

        # Parsear las filas de datos
        data_rows = []
        for line in lines[header_idx + 2:]:
            parts = line.split(";")
            if len(parts) < 3:
                continue

            fecha_str = parts[0].strip()
            # Validar formato de fecha YYYY-MM-DD
            try:
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                continue

            # Para cada AFP hay 2 columnas: Valor Cuota y Patrimonio
            col_ptr = 1
            for afp in afp_names:
                if col_ptr >= len(parts):
                    break
                vc_raw = parts[col_ptr].strip()
                pat_raw = parts[col_ptr + 1].strip() if (col_ptr + 1) < len(parts) else "0"

                # Limpieza de formato chileno: miles con '.' y decimales con ','
                try:
                    vc_clean = float(vc_raw.replace(".", "").replace(",", ".")) if vc_raw else None
                except ValueError:
                    vc_clean = None

                try:
                    pat_clean = float(pat_raw.replace(".", "").replace(",", ".")) if pat_raw else 0.0
                except ValueError:
                    pat_clean = 0.0

                if vc_clean is not None and vc_clean > 0:
                    data_rows.append({
                        "fecha": fecha_obj,
                        "fondo": fondo.upper(),
                        "afp": afp,
                        "valor_cuota": vc_clean,
                        "patrimonio": pat_clean,
                    })

                col_ptr += 2

        df = pl.DataFrame(data_rows)
        logger.info("DataFrame parseado para Fondo %s: %d filas totales", fondo, len(df))
        return df

    def compute_system_weighted(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calcula el Valor Cuota Ponderado del Sistema día a día según el patrimonio de cada AFP:

        VC_sistema = sum(VC_i * Pat_i) / sum(Pat_i)
        Agrega estas filas con afp='SISTEMA'.
        """
        # Agrupar por fecha y fondo
        system_df = (
            df.filter(pl.col("patrimonio") > 0)
            .group_by(["fecha", "fondo"])
            .agg([
                (pl.col("valor_cuota") * pl.col("patrimonio")).sum().alias("numerador"),
                pl.col("patrimonio").sum().alias("patrimonio_total"),
            ])
            .with_columns([
                (pl.col("numerador") / pl.col("patrimonio_total")).alias("valor_cuota"),
                pl.lit("SISTEMA").alias("afp"),
                pl.col("patrimonio_total").alias("patrimonio"),
            ])
            .select(["fecha", "fondo", "afp", "valor_cuota", "patrimonio"])
        )

        # Concatenar filas del sistema
        combined = pl.concat([df, system_df]).sort(["fecha", "afp"])
        return combined

    def get_fondo_dataset(
        self,
        fondo: str = "E",
        start_year: int = 2018,
        end_year: int = 2026,
        force_refresh: bool = False,
    ) -> Tuple[pl.DataFrame, str]:
        """Orquestador completo: descarga en vivo, parseo y ponderación del sistema."""
        raw_path, origin = self.download_fondo_raw(
            fondo=fondo,
            start_year=start_year,
            end_year=end_year,
            force_refresh=force_refresh,
        )
        parsed_df = self.parse_csv(raw_path, fondo=fondo)
        weighted_df = self.compute_system_weighted(parsed_df)
        return weighted_df, origin
