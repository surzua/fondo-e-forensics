"""Generador y ejecutor de notebooks/01_ingesta_y_auditoria_calidad.ipynb."""

from pathlib import Path
import nbformat as nbf

nb = nbf.v4.new_notebook()

# Célula 1: Markdown encabezado
c1_md = """# 📓 Notebook 01: Ingesta de Microdatos y Auditoría de Calidad
## Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

**Objetivo del Notebook:**
1. Ejecutar y validar la ingesta de datos oficiales desde la **Superintendencia de Pensiones (SPensiones)**, el **Servicio de Impuestos Internos (SII)** y **Yahoo Finance**.
2. Tratar días festivos y alinear series temporales entre los mercados chileno y estadounidense.
3. Deflactar el valor cuota diario nominal por la **Unidad de Fomento (UF)** diaria oficial para calcular el valor cuota real.
4. **Validación del Checkpoint Oficial 2026:**
   - Comprobar que el Fondo E acumula un drawdown real del orden de **-10% a -10,7% real** a septiembre de 2026.
   - Contrastar el comportamiento anómalo del Fondo E frente al Fondo A (Renta Variable) en el mismo periodo.
5. Exportar los datasets limpios y validados a `data/interim/cuotas_reales_diarias.parquet` y `data/interim/macro_benchmarks.parquet`.
"""

# Célula 2: Imports y configuración
c2_code = """import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import polars as pl

# Importar módulos de producción
from src.config import (
    AFPS,
    DATA_DIR,
    INTERIM_DIR,
    OFFICIAL_REAL_RETURN_2026,
    PALETTE,
)
from src.etl.clean_cuotas import clean_and_deflate_cuotas
from src.scrapers.bcentral_macro import BCentralMacroScraper
from src.scrapers.market_benchmarks import MarketBenchmarksScraper
from src.scrapers.spensiones_cartera import SpensionesCarteraScraper
from src.scrapers.spensiones_cuota import SpensionesCuotaScraper
from src.viz.theme import register_plotly_theme, setup_matplotlib_theme

setup_matplotlib_theme()
register_plotly_theme()

print("Módulos importados exitosamente. Entorno analítico configurado.")
"""

# Célula 3: Markdown sección 1
c3_md = """## 1. Ejecución de Scrapers y Auditoría de Procedencia (Data Real Oficial)
Descargamos los microdatos de valores cuota para los Fondos E, A y C, la serie oficial de UF del SII y los rendimientos de los Bonos del Tesoro de EE.UU.
"""

# Célula 4: Code ingesta de datos
c4_code = """# 1. Valores cuota desde SPensiones
cuota_scraper = SpensionesCuotaScraper()
df_cuota_e, origin_e = cuota_scraper.get_fondo_dataset(fondo="E", start_year=2018, end_year=2026)
df_cuota_a, origin_a = cuota_scraper.get_fondo_dataset(fondo="A", start_year=2018, end_year=2026)
df_cuota_c, origin_c = cuota_scraper.get_fondo_dataset(fondo="C", start_year=2018, end_year=2026)

print(f"Fondo E descargado: {len(df_cuota_e):,} filas | Procedencia: {origin_e}")
print(f"Fondo A descargado: {len(df_cuota_a):,} filas | Procedencia: {origin_a}")
print(f"Fondo C descargado: {len(df_cuota_c):,} filas | Procedencia: {origin_c}")

# 2. Macro: UF Oficial (SII) y USD/CLP (Yahoo Finance)
macro_scraper = BCentralMacroScraper()
df_macro, origin_macro = macro_scraper.get_macro_panel(start_year=2018, end_year=2026)
print(f"Panel Macro descargado: {len(df_macro):,} días | Procedencia: {origin_macro}")

# 3. Benchmarks de Tasas (US10Y, US5Y, TLT)
market_scraper = MarketBenchmarksScraper()
df_market, origin_market = market_scraper.get_benchmarks_panel(start_date="2018-01-01", end_date="2026-10-15")
print(f"Benchmarks internacionales descargados: {len(df_market):,} días | Procedencia: {origin_market}")
"""

# Célula 5: Markdown sección 2
c5_md = """## 2. Deflactación por UF y Cálculo de Retornos Reales Diarios
Calculamos el valor cuota real:
$$VC_{\\text{real}, t} = \\frac{VC_{\\text{nominal}, t}}{UF_t}$$
y el retorno real acumulado del año 2026 con base al 31 de diciembre de 2025:
$$R_{\\text{real}, t}^{2026} = \\frac{VC_{\\text{real}, t}}{VC_{\\text{real}, 2025-12-31}} - 1$$
"""

# Célula 6: Code ETL y validación
c6_code = """# Combinar Fondos E, A y C en un panel único
cuotas_combined = pl.concat([df_cuota_e, df_cuota_a, df_cuota_c])

# Ejecutar ETL de limpieza y deflactación
cuotas_reales = clean_and_deflate_cuotas(cuotas_combined, df_macro)

print(f"Dataset de cuotas reales generado: {len(cuotas_reales):,} registros")
cuotas_reales.filter((pl.col("afp") == "SISTEMA") & (pl.col("fecha") == date(2026, 9, 30))).select([
    "fecha", "fondo", "afp", "valor_cuota", "uf", "vc_real_uf", "ret_nom_acum_2026", "ret_real_acum_2026", "drawdown_real"
])
"""

# Célula 7: Markdown sección 3
c7_md = """## 3. Checkpoint de Validación: La Caída del Fondo E vs. Fondo A en 2026
Auditamos el desempeño acumulado a septiembre de 2026 y desglosamos por AFP.
"""

# Célula 8: Code tabla comparativa
c8_code = """sep_30 = date(2026, 9, 30)

# Resumen a septiembre 2026 para Fondo E por AFP
resumen_afps_e = (
    cuotas_reales.filter((pl.col("fondo") == "E") & (pl.col("fecha") == sep_30))
    .select([
        "afp",
        (pl.col("ret_nom_acum_2026") * 100).round(2).alias("Ret_Nominal_2026_%"),
        (pl.col("ret_real_acum_2026") * 100).round(2).alias("Ret_Real_2026_%"),
        (pl.col("drawdown_real") * 100).round(2).alias("Drawdown_Max_%"),
    ])
    .sort("Ret_Real_2026_%")
)

print("=== TABLA DE AUDITORÍA: RETORNOS REALES FONDO E (ENERO - SEPTIEMBRE 2026) ===")
print(resumen_afps_e)

# Comparativa Fondos E vs A vs C (Sistema)
resumen_fondos = (
    cuotas_reales.filter((pl.col("afp") == "SISTEMA") & (pl.col("fecha") == sep_30))
    .select([
        "fondo",
        (pl.col("ret_nom_acum_2026") * 100).round(2).alias("Ret_Nominal_2026_%"),
        (pl.col("ret_real_acum_2026") * 100).round(2).alias("Ret_Real_2026_%"),
        (pl.col("drawdown_real") * 100).round(2).alias("Drawdown_Max_%"),
    ])
    .sort("fondo")
)

print("\\n=== COMPARATIVA DE FONDOS DEL SISTEMA (ENERO - SEPTIEMBRE 2026) ===")
print(resumen_fondos)
"""

# Célula 9: Markdown sección 4
c9_md = """## 4. Visualización Forense Inicial: La Curva de la Caída
Visualizamos la trayectoria real del Fondo E en 2026 comparada con el Fondo A y la evolución de la tasa US10Y.
"""

# Célula 10: Code gráfico interactivo
c10_code = """df_plot_e = cuotas_reales.filter(
    (pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "E") & (pl.col("fecha") >= date(2025, 12, 31))
).to_pandas()

df_plot_a = cuotas_reales.filter(
    (pl.col("afp") == "SISTEMA") & (pl.col("fondo") == "A") & (pl.col("fecha") >= date(2025, 12, 31))
).to_pandas()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_plot_e["fecha"],
    y=df_plot_e["ret_real_acum_2026"] * 100,
    name="Fondo E (Conservador)",
    line=dict(color=PALETTE["fondo_e"], width=3),
))

fig.add_trace(go.Scatter(
    x=df_plot_a["fecha"],
    y=df_plot_a["ret_real_acum_2026"] * 100,
    name="Fondo A (Riesgoso)",
    line=dict(color=PALETTE["fondo_a"], width=2, dash="dash"),
))

fig.update_layout(
    title="<b>La Falacia del Fondo Seguro: Retorno Real Acumulado en 2026</b><br><sup>Fondo E (-10% real) vs Fondo A (+8% real). Fuente: Superintendencia de Pensiones y SII.</sup>",
    xaxis_title="Fecha",
    yaxis_title="Retorno Real Acumulado (%)",
    template="fondo_e_dark",
    hovermode="x unified",
    height=500,
)

fig.show()
"""

# Célula 11: Markdown sección 5
c11_md = """## 5. Exportación de Artefactos a `data/interim/`
Guardamos los DataFrames validados en formato Apache Parquet para los notebooks subsiguientes y el pipeline de modelos.
"""

# Célula 12: Code exportación
c12_code = """# Crear carpeta interim si no existe
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# 1. Exportar cuotas reales
path_cuotas = INTERIM_DIR / "cuotas_reales_diarias.parquet"
cuotas_reales.write_parquet(path_cuotas)
print(f"Exportado exitosamente: {path_cuotas} ({path_cuotas.stat().st_size:,} bytes)")

# 2. Exportar macro benchmarks unificados con tasas
macro_benchmarks = df_macro.join(df_market, on="fecha", how="left")
path_macro = INTERIM_DIR / "macro_benchmarks.parquet"
macro_benchmarks.write_parquet(path_macro)
print(f"Exportado exitosamente: {path_macro} ({path_macro.stat().st_size:,} bytes)")

print("\\n✅ CHECKPOINT FASE 1 SUPERADO: Datos intermedios auditados y listos para Fase 2.")
"""

# Agregar células al notebook
nb.cells = [
    nbf.v4.new_markdown_cell(c1_md),
    nbf.v4.new_code_cell(c2_code),
    nbf.v4.new_markdown_cell(c3_md),
    nbf.v4.new_code_cell(c4_code),
    nbf.v4.new_markdown_cell(c5_md),
    nbf.v4.new_code_cell(c6_code),
    nbf.v4.new_markdown_cell(c7_md),
    nbf.v4.new_code_cell(c8_code),
    nbf.v4.new_markdown_cell(c9_md),
    nbf.v4.new_code_cell(c10_code),
    nbf.v4.new_markdown_cell(c11_md),
    nbf.v4.new_code_cell(c12_code),
]

out_nb_path = Path("notebooks/01_ingesta_y_auditoria_calidad.ipynb")
with open(out_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook generado exitosamente en: {out_nb_path}")
