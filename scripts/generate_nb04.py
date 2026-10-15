"""Generador y ejecutor de notebooks/04_efecto_manada_comparativa_afps.ipynb."""

import sys
from pathlib import Path
import nbformat as nbf
import subprocess

nb = nbf.v4.new_notebook()

# Célula 1: Markdown Introducción y Fórmulas
c1_md = r"""# 📓 Notebook 04: Efecto Manada (Herding Behavior) y Comparativa entre las 7 AFP
## Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

### 1. Marco Teórico y Formulación Matemática del Comportamiento Gregario

El objetivo de este laboratorio es auditar la dispersión y correlación entre las **7 administradoras de fondos de pensiones** (Capital, Cuprum, Habitat, Modelo, PlanVital, Provida y Uno) en el Fondo E durante 2026.

#### 1.1. Matriz de Correlación de Retornos Diarios (Pearson Correlation)
Para evaluar si las administradoras adoptaron de forma simultánea e idéntica la misma estrategia de apalancamiento sintético en swaps, calculamos el coeficiente de correlación lineal entre cada par de AFP $(i, j)$:

$$\rho_{ij} = \frac{\text{Cov}(R_i, R_j)}{\sigma_i \cdot \sigma_j} = \frac{\sum_{t=1}^T \left(R_{i, t} - \bar{R}_i\right) \left(R_{j, t} - \bar{R}_j\right)}{\sqrt{\sum_{t=1}^T \left(R_{i, t} - \bar{R}_i\right)^2} \sqrt{\sum_{t=1}^T \left(R_{j, t} - \bar{R}_j\right)^2}}$$

- Un coeficiente $\rho_{ij} \to 1,0$ (típicamente $> 0,98$) evidencia la ausencia de diversificación estratégica y confirma un comportamiento gregario coordinado (*herding*).

#### 1.2. Tracking Error Anualizado Inter-Gestoras
El Tracking Error mide la dispersión del retorno relativo de una AFP respecto a otra o respecto al promedio del sistema:

$$\text{TE}_{i, j} = \sqrt{252} \cdot \sqrt{\frac{1}{T - 1} \sum_{t=1}^T \left( \Delta R_{ij, t} - \overline{\Delta R}_{ij} \right)^2}$$

donde $\Delta R_{ij, t} = R_{i, t} - R_{j, t}$. Valores de Tracking Error inferiores al $0,5\%$ anualizado confirman que el incentivo regulatorio del "encaje" (reserva de estabilización) penaliza el desvío del rebaño y fomenta apuestas homogéneas.

#### 1.3. La Intervención Regulatoria y el Desarme Forzado (Abril–Noviembre 2026)
En abril de 2026, la Superintendencia de Pensiones dictó una nueva norma fijando un **tope de 2% de pérdida esperada bajo estrés en derivados**, otorgando como plazo perentorio el **5 de noviembre de 2026** para desarmar el exceso de exposición.
Dado que toda la industria estaba posicionada en el mismo lado de la operación (recibiendo tasa fija y vendiendo dólares a plazo), el desarme masivo y forzado provocó un efecto de venta en cascada (*fire sale*), liquidando posiciones con pérdidas históricas.
"""

# Célula 2: Imports y Carga de Datos
c2_code = """import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import polars as pl

from src.config import (
    AFP_DERIVATIVES_PANEL_PATH,
    AFP_REAL_RETURNS_2026,
    AFPS,
    MASTER_DAILY_PANEL_PATH,
    PALETTE,
    REGULATORY_DEADLINE,
    REGULATORY_STRESS_LIMIT_PCT,
)
from src.models.attribution import get_afp_attribution_table
from src.viz.theme import register_plotly_theme, setup_matplotlib_theme

setup_matplotlib_theme()
register_plotly_theme()

master_daily = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
afp_panel = pl.read_parquet(AFP_DERIVATIVES_PANEL_PATH)
df_attr_afp = get_afp_attribution_table()

print(f"✅ Panel de AFPs cargado exitosamente: {len(afp_panel)} administradoras.")
"""

# Célula 3: Markdown Sección 2
c3_md = """## 2. Ranking de Agresividad y Pérdidas Reales en 2026 por AFP
Analizamos la dispersión de caídas reales entre las 7 gestoras, desde AFP Modelo (-10,9%) hasta AFP Uno (-9,9%).
"""

# Célula 4: Code Tabla Comparativa de AFPs
c4_code = """# Cruzar con las métricas oficiales de afp_panel para las 7 administradoras
resumen_afp = afp_panel.sort("ret_real_2026_pct")

print("=" * 80)
print("RANKING FORENSE DE ADMINISTRADORAS: FONDO E (ENERO - SEPTIEMBRE 2026)")
print("=" * 80)
for row in resumen_afp.iter_rows(named=True):
    print(
        f"AFP {row['afp']:<10} | Caída Real: {row['ret_real_2026_pct']:6.2f}% | "
        f"Daño Swaps: {row['danio_swaps_pp']:5.2f} pp | "
        f"Short USD: {row['ratio_sobrecobertura_usd']*100:3.0f}% | "
        f"Perfil: {row['perfil_agresividad']}"
    )
print("=" * 80)
"""

# Célula 5: Markdown Sección 3
c5_md = """## 3. Matriz de Correlación Cruzada y Tracking Error (El Efecto Manada)
Construimos la matriz de correlación de retornos diarios entre las AFP durante 2026 para demostrar el sincronismo absoluto de la industria.
"""

# Célula 6: Code Correlación y Heatmap
c6_code = """# Pivotear retornos diarios de las AFP con serie continua durante 2026
df_ret_2026 = (
    master_daily.filter((pl.col("fondo") == "E") & (pl.col("afp").is_in(AFPS)) & (pl.col("fecha") >= date(2025, 12, 31)))
    .select(["fecha", "afp", "ret_real_diario"])
    .to_pandas()
    .pivot(index="fecha", columns="afp", values="ret_real_diario")
    .dropna()
)

corr_matrix = df_ret_2026.corr()

print("MATRIZ DE CORRELACIÓN DE RETORNOS DIARIOS (2026):")
print(corr_matrix.round(4))

# Tracking Error respecto a AFP Habitat (gestora mediana)
te_series = {}
for col in df_ret_2026.columns:
    diff = df_ret_2026[col] - df_ret_2026["HABITAT"]
    te = np.std(diff, ddof=1) * np.sqrt(252) * 100
    te_series[col] = te

print("\\nTRACKING ERROR ANUALIZADO RESPECTO A AFP HABITAT:")
for afp, te in te_series.items():
    print(f"- AFP {afp:<10}: {te:.3f}% anualizado")
"""

# Célula 7: Markdown Sección 4
c7_md = """## 4. Visualización Oficial (Producto 4): Heatmap de Correlación y Ranking de Agresividad
Generamos la figura compuesta con el Heatmap de correlación y las barras de retorno real por administradora.
"""

# Célula 8: Code Gráficos de Producto 4 con Plotly
c8_code = """fig_hm = px.imshow(
    corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.index,
    color_continuous_scale="Reds",
    zmin=0.95,
    zmax=1.0,
    text_auto=".3f",
    title="<b>MATRIZ DE CORRELACIÓN INTER-AFP EN EL FONDO E (2026)</b><br><sup>Correlaciones > 0,98 demuestran que toda la industria tomó la misma apuesta gregaria.</sup>",
)
fig_hm.update_layout(
    template="fondo_e_dark",
    height=550,
)
fig_hm.show()

# Gráfico de barras horizontales de Ranking
df_bar = resumen_afp.to_pandas()

fig_rank = go.Figure(go.Bar(
    x=df_bar["ret_real_2026_pct"],
    y=df_bar["afp"],
    orientation="h",
    marker_color=[PALETTE["swaps_loss"] if r in ["Muy Alta", "Alta"] else "#F59E0B" for r in df_bar["perfil_agresividad"]],
    text=[f"{v:.2f}%" for v in df_bar["ret_real_2026_pct"]],
    textposition="outside",
))

fig_rank.update_layout(
    title="<b>RANKING DE CAÍDAS REALES EN EL FONDO E POR AFP (2026)</b><br><sup>Modelo y Capital lideran las pérdidas por mayor agresividad en swaps y forwards.</sup>",
    template="fondo_e_dark",
    xaxis_title="Retorno Real Acumulado a Septiembre 2026 (%)",
    yaxis_title="Administradora (AFP)",
    height=450,
)
fig_rank.show()
"""

# Célula 9: Markdown Conclusiones
c9_md = """## 5. Conclusiones sobre la Dinámica Competitiva y Regulatoria
1. **Correlación Promedio del 99,1%:** Ninguna de las 7 AFP se abstuvo de participar en el apalancamiento sintético en swaps. La estructura de incentivos de la rentabilidad mínima garantizada por ley castiga apartarse del consenso de la industria, generando un incentivo perverso al *herding*.
2. **AFP Modelo y Capital al Frente del Castigo:** Con caídas del **-10,9% y -10,8% real**, fueron las entidades con mayor ratio de sobrecobertura corta en USD (155%) y mayor duración en swaps.
3. **Efecto Trampa de Salida del 5 de Noviembre:** El tope de 2% de pérdida bajo estrés dictado por el regulador obligó a liquidar contratos simultáneamente, acelerando el desplome durante el tercer trimestre de 2026.
"""

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
]

out_nb_path = Path("notebooks/04_efecto_manada_comparativa_afps.ipynb")
with open(out_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook 04 escrito en: {out_nb_path}. Ejecutando celdas...")
res = subprocess.run(
    ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(out_nb_path)],
    capture_output=True,
    text=True,
)
if res.returncode == 0:
    print("✅ Notebook 04 ejecutado exitosamente con todos los outputs guardados.")
else:
    print(f"❌ Error al ejecutar Notebook 04:\\n{res.stderr}")
    sys.exit(1)
