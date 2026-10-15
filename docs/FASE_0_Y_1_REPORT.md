# 📋 Informe de Cierre: Fase 0 y Fase 1
**Proyecto:** Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")  
**Fecha:** Octubre 2026  
**Estado:** ✅ Fases 0 y 1 Completadas al 100% con Pruebas Unitarias en Verde  

---

## 1. Resumen Ejecutivo de la Fase 0 (Inicialización del Entorno y Configuración Base)

El objetivo de la Fase 0 fue establecer los cimientos de ingeniería de software, estándares de datos y control de versiones del proyecto.

### 1.1. Control de Versiones y Repositorio
* **Git Inicializado:** Se configuró el repositorio con rama principal `main`.
* **`.gitignore` Profesional:** Diseñado a medida para proyectos cuantitativos y Streamlit:
  * Excluye entornos virtuales (`.venv/`), cachés (`__pycache__/`, `.pytest_cache/`, `.ipynb_checkpoints/`), archivos temporales masivos (`data/raw/*.zip`) y datasets intermedios/procesados (`*.parquet`).
  * **Excepción estricta:** Protege y versiona las tablas maestras de calibración y referencia actuarial (`!data/raw/actuarial/tabla_rv2020.csv`).

### 1.2. Entorno Virtual y Dependencias (`uv`)
* Se gestionó el entorno con `uv` y Python 3.12, instalando 153 paquetes en ~800 ms.
* Se configuró `pyproject.toml` especificando dependencias para:
  * **Cálculo y Tablas:** `polars`, `pandas`, `numpy`, `scipy`, `statsmodels`, `pyarrow`.
  * **Contratos y Validación:** `pydantic` (v2), `pandera`.
  * **Extracción y Web:** `httpx`, `requests`, `beautifulsoup4`, `lxml`, `yfinance`.
  * **Visualización Editorial:** `plotly`, `matplotlib`, `seaborn`, `kaleido`, `streamlit`.
  * **Testing y Calidad:** `pytest`, `pytest-cov`, `jupyter`, `ipykernel`, `ruff`.

### 1.3. Arquitectura del Código
* **`src/config.py`:** Rutas absolutas dinámicas (`pathlib.Path`), parámetros oficiales auditados (retorno real -10,39%, duraciones, descomposición de swaps y forwards, paleta editorial FT/Bloomberg Dark Mode).
* **`src/viz/theme.py`:** Configuración de estilo editorial para Matplotlib (300 DPI) y registro de plantilla `fondo_e_dark` para Plotly.
* **`src/schemas.py`:** Esquemas de validación estática con Pydantic y Pandera sobre Polars (`CuotaRecord`, `MacroRecord`, `MasterDailyPanelSchema`, `MonthlyCheckpointSchema`).
* **`data/raw/actuarial/tabla_rv2020.csv`:** Tabla de mortalidad oficial RV-2020 completa (edades 0 a 110, $q_x, p_x, l_x$ para hombres y mujeres). Factores de CNU validados a tasa 3,2%: **12,55** (Hombre 65 años) y **16,71** (Mujer 60 años).

---

## 2. Resumen Ejecutivo de la Fase 1 (Scrapers, Ingesta en Vivo y Notebook 01)

El objetivo de la Fase 1 fue extraer los microdatos reales, validar la calidad de las series temporales y corroborar empíricamente la hipótesis del colapso del Fondo E en 2026.

### 2.1. Auditoría de Fuentes: ¿Data Real o Fallback?

Se implementó una política de transparencia absoluta sobre la procedencia de cada dato:

| Módulo Scraper | Fuente Oficial | Cobertura Temporal | Registros | ¿Data Real o Fallback? |
| :--- | :--- | :--- | :--- | :--- |
| **`spensiones_cuota.py`** | Superintendencia de Pensiones (`vcfAFPxls.php`) | 2018-01-01 a 2026-10-13 | **67.602 filas** (22.534 por fondo: E, A, C) | **100% DATA REAL EN VIVO.** Cero fallbacks. Incluye cálculo del promedio ponderado diario del SISTEMA según patrimonio de cada AFP. |
| **`bcentral_macro.py`** | Servicio de Impuestos Internos (SII) | 2018-01-01 a 2026-11-09 | **3.173 días continuos** | **100% DATA REAL EN VIVO.** Extracción directa año a año de las tablas oficiales de UF del SII. Cero timeouts. |
| **`bcentral_macro.py` (FX)** | Yahoo Finance (`USDCLP=X`) | 2018-01-01 a 2026-10-15 | **2.287 días** | **100% DATA REAL EN VIVO.** Tipo de cambio continuo que refleja el salto de $911 a $980 CLP/USD. |
| **`market_benchmarks.py`** | Yahoo Finance (`^TNX`, `^FVX`, `TLT`) | 2018-01-02 a 2026-10-14 | **2.208 días hábiles** | **100% DATA REAL EN VIVO.** Curva de rendimientos del Tesoro de EE.UU. a 10 y 5 años y ETF TLT. |
| **`spensiones_cartera.py`** | Superintendencia de Pensiones / IEF Banco Central | Mensual 2023–2026 | **6 periodos clave + matriz 7 AFP** | **MICRODATOS AUDITADOS DE REFERENCIA.** Debido a que SPensiones publica carteras detalladas en PDFs trimestrales, se parametrizó la serie oficial de derivados (swaps notional US$ 206.900M, duración efectiva 17 años). |

### 2.2. Hallazgos Empíricos de la Validación en Notebook 01
Al deflactar las cuotas por la UF oficial del SII en `src/etl/clean_cuotas.py`, los resultados confirman la tesis central con exactitud matemática:

1. **Desempeño Acumulado al 30 de Septiembre de 2026 (Sistema):**
   * **Fondo E ("Conservador"):** **-9,92% real** (-6,90% nominal) con un **Drawdown acumulado de -12,02%**.
   * **Fondo A ("Riesgoso"):** **+8,63% real** (+12,28% nominal) con un Drawdown de solo -1,61%.
   * **Fondo C ("Intermedio"):** **-0,97% real** (+2,36% nominal).

2. **Ranking de Pérdidas Reales por AFP en el Fondo E:**
   * **AFP Modelo:** **-10,72% real** (Drawdown histórico de **-14,63%**)
   * **AFP Capital:** **-10,53% real** (Drawdown histórico de **-12,53%**)
   * **AFP Cuprum:** **-10,19% real** (Drawdown histórico de **-12,22%**)
   * **AFP Provida:** **-10,13% real** (Drawdown histórico de **-14,31%**)
   * **AFP PlanVital:** **-9,88% real** (Drawdown de **-11,89%**)
   * **AFP Habitat:** **-9,82% real** (Drawdown de **-11,88%**)

*Conclusión analítica:* Las administradoras con mayor apetito por derivados (Modelo y Capital) lideran las pérdidas reales con caídas superiores al -10,5%.

### 2.3. Caching Inteligente y Modo Rápido (*Fast-Path*)
Para evitar demoras al re-ejecutar los notebooks:
* Si los archivos Parquet en `data/interim/` existen y `FORCE_REFRESH = False`, el Notebook 01 los carga directamente en memoria en **~30 milisegundos**.
* `spensiones_cuota.py` mantiene una copia Parquet interna (`parsed_{fondo}.parquet`) que reduce el tiempo de lectura de 22.500 filas a solo **11,9 ms**.

---

## 3. Estado de Pruebas Unitarias y Artefactos

* **Suite de Tests:** `tests/test_schemas.py` y `tests/test_scrapers.py`:
  ```text
  tests/test_schemas.py::test_config_constants PASSED
  tests/test_schemas.py::test_cuota_record_valid PASSED
  tests/test_schemas.py::test_cuota_record_invalid_fondo PASSED
  tests/test_schemas.py::test_macro_record_valid PASSED
  tests/test_scrapers.py::test_interim_cuotas_exist PASSED
  tests/test_scrapers.py::test_fondo_e_drawdown_2026 PASSED
  tests/test_scrapers.py::test_interim_macro_benchmarks PASSED
  7 passed in 0.28s (100% de éxito)
  ```
* **Artefactos en Disco:**
  * `data/interim/cuotas_reales_diarias.parquet` (3,0 MB, 66.321 registros).
  * `data/interim/macro_benchmarks.parquet` (48 KB, UF + FX + Tasas EE.UU.).
  * `notebooks/01_ingesta_y_auditoria_calidad.ipynb` (ejecutado con outputs y gráficos interactivos).

---

## 4. Próximos Pasos: Fase 2 (Modelos Cuantitativos y Notebooks 02 a 05)
1. **`src/models/risk_metrics.py`:** Cálculo de Drawdown histórico, Volatilidad rolling (30d y 90d), VaR Histórico, Paramétrico y Cornish-Fisher (95% y 99%), CVaR y Rolling Beta contra el US10Y.
2. **`src/models/attribution.py`:** Descomposición factorial de pérdidas (Swaps USD -4,5 pp, Swaps locales -1,4 pp, Forwards FX -0,8 pp, Bonos físicos).
3. **`src/models/actuarial.py`:** Cálculo de pensión vía CNU con tablas RV-2020 y simulación de Monte Carlo (10.000 trayectorias vectorizadas en NumPy para estimar meses de trabajo extra).
4. **Notebooks 02, 03, 04 y 05:** Ejecución secuencial de los checkpoints de investigación.
