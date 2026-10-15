"""Cliente HTTP base con reintentos, rotación de cabeceras y caché local.

Permite realizar peticiones HTTP reproducibles y registrar explícitamente
la procedencia de los datos (LIVE_NETWORK, LOCAL_CACHE o AUDITED_FALLBACK).
"""

from __future__ import annotations

import hashlib
import logging
import random
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import httpx

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ScraperBase")

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",
]


class BaseScraper:
    """Cliente base para descarga de microdatos financieros y series oficiales."""

    def __init__(self, cache_dir: Optional[Path] = None, timeout: float = 30.0, max_retries: int = 3):
        self.cache_dir = cache_dir
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.max_retries = max_retries

    def get_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Genera cabeceras realistas de navegador para evitar bloqueos WAF."""
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-CL,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def fetch(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        force_refresh: bool = False,
    ) -> Tuple[bytes, str]:
        """Ejecuta una petición HTTP con reintentos y caché local.

        Retorna:
            (contenido_bytes, procedencia) donde procedencia es 'LIVE_NETWORK' o 'LOCAL_CACHE'.
        """
        # Calcular clave de caché
        cache_key = hashlib.sha256(f"{method}:{url}:{params}:{data}".encode("utf-8")).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.cache" if self.cache_dir else None

        if cache_file and cache_file.exists() and not force_refresh:
            logger.info("Cargando desde caché local: %s (origen: %s)", cache_file.name, url)
            return cache_file.read_bytes(), "LOCAL_CACHE"

        # Petición en vivo con reintentos
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                headers = self.get_headers(custom_headers)
                logger.info("Petición en vivo [Intento %d/%d] a: %s", attempt, self.max_retries, url)

                with httpx.Client(timeout=self.timeout, follow_redirects=True, verify=True) as client:
                    if method.upper() == "POST":
                        response = client.post(url, data=data, params=params, headers=headers)
                    else:
                        response = client.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    content = response.content
                    if cache_file:
                        cache_file.write_bytes(content)
                    logger.info("Descarga exitosa de %s (%d bytes)", url, len(content))
                    return content, "LIVE_NETWORK"

                logger.warning(
                    "Respuesta con código %d en intento %d para %s",
                    response.status_code,
                    attempt,
                    url,
                )
            except Exception as exc:
                last_error = exc
                logger.warning("Fallo intento %d para %s: %s", attempt, url, str(exc))

            # Backoff exponencial con jitter
            sleep_time = (2 ** attempt) + random.uniform(0.5, 1.5)
            time.sleep(sleep_time)

        raise RuntimeError(f"No fue posible descargar {url} tras {self.max_retries} intentos. Causa: {last_error}")
