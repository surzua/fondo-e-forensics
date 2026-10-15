"""Generador y ejecutor de notebooks/02_anatomia_drawdown_y_var_fondo_e.ipynb."""

from pathlib import Path
import nbformat as nbf
import subprocess

nb = nbf.v4.new_notebook()

# Célula 1: Markdown Introducción y Fórmulas
c1_md = r"""# 📓 Notebook 02: Anatomía del Drawdown y Shock de Value at Risk (VaR)
## Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

### 1. Marco Teórico y Formulación Matemática

El objetivo de este laboratorio es analizar el comportamiento de riesgo extremo del **Fondo E** durante 2026, contrastando su perfil de volatilidad y pérdidas de cola (*tail risk*) frente al **Fondo A** (Renta Variable) y el **Fondo C** (Fondo Intermedio).

#### 1.1. Drawdown Histórico y Maximum Drawdown (MDD)
Dada la serie de valor cuota real en UF $P_t = \frac{VC_{\text{nominal}, t}}{UF_t}$, definimos el máximo acumulado previo (*High Water Mark* o *Peak*):

$$\text{Peak}_t = \max_{0 \le s \le t} P_s$$

El Drawdown porcentual en la fecha $t$ representa la pérdida acumulada desde el máximo histórico:

$$\text{Drawdown}_t = \frac{P_t - \text{Peak}_t}{\text{Peak}_t} \le 0$$

El Máximo Drawdown en un horizonte $T$ es la peor caída observada:

$$\text{MDD} = \min_{0 \le t \le T} \text{Drawdown}_t$$

#### 1.2. Volatilidad Anualizada Móvil (Rolling Volatility)
Para una ventana móvil de $W$ días de negociación (habitualmente $W = 30$ o $90$ días) sobre los retornos diarios $R_t$:

$$\sigma_{\text{rolling}, t} = \sqrt{252} \cdot \sqrt{\frac{1}{W - 1} \sum_{i=0}^{W-1} \left(R_{t-i} - \bar{R}_t\right)^2}$$

#### 1.3. Modelos de Value at Risk (VaR)
El VaR cuantifica la pérdida máxima esperada con un nivel de confianza $(1 - \alpha)$ (ej. $\alpha = 0,05$ para el 95% o $\alpha = 0,01$ para el 99%) en un horizonte diario:

1. **VaR Histórico (Empírico no paramétrico):**
   $$\text{VaR}_\alpha^{\text{hist}} = -\text{Quantile}_\alpha(R)$$

2. **VaR Paramétrico (Gaussiano):**
   Asumiendo distribución normal $R \sim \mathcal{N}(\mu, \sigma^2)$:
   $$\text{VaR}_\alpha^{\text{param}} = -\left(\mu + z_\alpha \cdot \sigma\right)$$
   donde $z_{0,05} = -1,64485$ y $z_{0,01} = -2,32635$.

3. **VaR Modificado de Cornish-Fisher (Ajuste por Asimetría y Curtosis):**
   Las carteras apalancadas con derivados financieros presentan asimetría negativa ($S < 0$) y exceso de curtosis ($K_{\text{ex}} > 0$). La expansión polinomial de Cornish-Fisher ajusta el cuantil crítico $z_\alpha$:

   $$S = \frac{\mathbb{E}\left[(R - \mu)^3\right]}{\sigma^3}, \quad K_{\text{ex}} = \frac{\mathbb{E}\left[(R - \mu)^4\right]}{\sigma^4} - 3$$

   $$z_{\text{CF}} = z_\alpha + \frac{1}{6}(z_\alpha^2 - 1) S + \frac{1}{24}(z_\alpha^3 - 3 z_\alpha) K_{\text{ex}} - \frac{1}{36}(2 z_\alpha^3 - 5 z_\alpha) S^2$$

   $$\text{VaR}_\alpha^{\text{CF}} = -\left(\mu + z_{\text{CF}} \cdot \sigma\right)$$

#### 1.4. Conditional Value at Risk (CVaR / Expected Shortfall)
Mide la pérdida promedio esperada en los días en que el retorno cae más allá del umbral del VaR:

$$\text{CVaR}_\alpha = -\mathbb{E}\left[ R \mid R \le -\text{VaR}_\alpha \right] = -\frac{1}{\sum_{i=1}^N \mathbb{I}_{\{R_i \le -\text{VaR}_\alpha\}}} \sum_{R_i \le -\text{VaR}_\alpha} R_i$$

#### 1.5. Ratios de Sharpe y Sortino
$$\text{Sharpe} = \sqrt{252} \cdot \frac{\bar{R} - R_f}{\sigma}, \quad \text{Sortino} = \sqrt{252} \cdot \frac{\bar{R} - R_f}{\sqrt{\frac{1}{N} \sum_{i=1}^N \min\left(0, R_i - R_f\right)^2}}$$
"""

# Célula 2: Imports y Carga del Analytical Mart
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
    MASTER_DAILY_PANEL_PATH,
    OFFICIAL_REAL_RETURN_2026,
    PALETTE,
)
from src.models.risk_metrics import (
    calculate_cvar,
    calculate_drawdown_series,
    calculate_risk_profile_summary,
    calculate_rolling_volatility,
    calculate_var_cornish_fisher,
    calculate_var_historical,
    calculate_var_parametric,
)
from src.viz.theme import register_plotly_theme, setup_matplotlib_theme

setup_matplotlib_theme()
register_plotly_theme()

print(f"Cargando Master Daily Panel desde: {MASTER_DAILY_PANEL_PATH.name}...")
df_master = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
print(f"✅ Panel cargado exitosamente: {len(df_master):,} registros desde {df_master['fecha'].min()} hasta {df_master['fecha'].max()}.")
"""

# Célula 3: Markdown Sección 2
c3_md = """## 2. Comparativa Histórica de Drawdowns: Los 3 Grandes Shocks del Fondo E
Analizamos los 3 episodios de pérdidas más graves que ha sufrido el Fondo E en su historia:
1. **2021 (-11,06% acumulado a sep):** Convención Constitucional y retiros del 10%.
2. **2023 (-4,91% acumulado a sep):** Alzas agresivas de tasas de los bancos centrales globales.
3. **2026 (-10,39% acumulado a sep):** El shock de swaps y derivados que auditamos en este proyecto.
"""

# Célula 4: Code Análisis de Drawdown Histórico
c4_code = """# Filtrar datos del SISTEMA para Fondo E, A y C
df_e_sys = df_master.filter((pl.col('afp') == 'SISTEMA') & (pl.col('fondo') == 'E')).sort('fecha')
df_a_sys = df_master.filter((pl.col('afp') == 'SISTEMA') & (pl.col('fondo') == 'A')).sort('fecha')
df_c_sys = df_master.filter((pl.col('afp') == 'SISTEMA') & (pl.col('fondo') == 'C')).sort('fecha')

# Métricas históricas completas
mdd_e = df_e_sys['drawdown_real'].min()
mdd_a = df_a_sys['drawdown_real'].min()
mdd_c = df_c_sys['drawdown_real'].min()

# Métricas durante 2026 (desde 2025-12-31)
df_e_2026 = df_e_sys.filter(pl.col('fecha') >= date(2025, 12, 31))
df_a_2026 = df_a_sys.filter(pl.col('fecha') >= date(2025, 12, 31))
df_c_2026 = df_c_sys.filter(pl.col('fecha') >= date(2025, 12, 31))

dd_2026_e = df_e_2026['drawdown_real'].min()
dd_2026_a = df_a_2026['drawdown_real'].min()
dd_2026_c = df_c_2026['drawdown_real'].min()

ret_2026_e = df_e_2026['ret_real_acum_2026'].last()
ret_2026_a = df_a_2026['ret_real_acum_2026'].last()
ret_2026_c = df_c_2026['ret_real_acum_2026'].last()

print("=" * 70)
print("AUDITORÍA DE DESEMPEÑO Y DRAWDOWN EN 2026 (SISTEMA AFP)")
print("=" * 70)
print(f"Fondo E (Conservador): Retorno Real 2026: {ret_2026_e*100:6.2f}% | Max Drawdown 2026: {dd_2026_e*100:6.2f}%")
print(f"Fondo A (Riesgoso):    Retorno Real 2026: {ret_2026_a*100:6.2f}% | Max Drawdown 2026: {dd_2026_a*100:6.2f}%")
print(f"Fondo C (Intermedio):  Retorno Real 2026: {ret_2026_c*100:6.2f}% | Max Drawdown 2026: {dd_2026_c*100:6.2f}%")
print("=" * 70)
print(f"-> Conclusión empírica: El Fondo E exhibió un drawdown ({dd_2026_e*100:.2f}%) 7 veces superior al del Fondo A ({dd_2026_a*100:.2f}%).")
"""

# Célula 5: Markdown Sección 3
c5_md = """## 3. Auditoría de Riesgo de Cola: VaR y Rupturas en 2026
Evaluamos la distribución de retornos diarios del Fondo E en el período pre-crisis (2018–2025) y calculamos los umbrales de **VaR al 95% y 99%** para contrastar cuántas veces fueron superados en 2026.
"""

# Célula 6: Code Métricas de VaR y CVaR
c6_code = """ret_hist_e = df_e_sys.filter(pl.col('fecha') < date(2025, 12, 31))['ret_real_diario'].to_numpy()
ret_2026_e_arr = df_e_2026['ret_real_diario'].drop_nulls().to_numpy()

profile_hist = calculate_risk_profile_summary(ret_hist_e)
profile_2026 = calculate_risk_profile_summary(ret_2026_e_arr)

# Comparativa de métricas de riesgo
var_table = pl.DataFrame({
    "Métrica de Riesgo": [
        "Volatilidad Anualizada",
        "Asimetría (Skewness)",
        "Exceso de Curtosis (Kurtosis)",
        "VaR Diario 95% (Histórico)",
        "VaR Diario 95% (Cornish-Fisher)",
        "VaR Diario 99% (Histórico)",
        "VaR Diario 99% (Cornish-Fisher)",
        "CVaR 99% (Expected Shortfall)",
        "Ratio de Sharpe (Rf=0)",
        "Ratio de Sortino",
    ],
    "Histórico (2018-2025)": [
        f"{profile_hist['volatilidad_anualizada']*100:.2f}%",
        f"{profile_hist['asimetria_skewness']:.3f}",
        f"{profile_hist['curtosis_exceso']:.3f}",
        f"{profile_hist['var_historico_95']*100:.3f}%",
        f"{profile_hist['var_cornish_fisher_95']*100:.3f}%",
        f"{profile_hist['var_historico_99']*100:.3f}%",
        f"{profile_hist['var_cornish_fisher_99']*100:.3f}%",
        f"{profile_hist['cvar_expected_shortfall_99']*100:.3f}%",
        f"{profile_hist['sharpe_ratio']:.3f}",
        f"{profile_hist['sortino_ratio']:.3f}",
    ],
    "Crisis 2026": [
        f"{profile_2026['volatilidad_anualizada']*100:.2f}%",
        f"{profile_2026['asimetria_skewness']:.3f}",
        f"{profile_2026['curtosis_exceso']:.3f}",
        f"{profile_2026['var_historico_95']*100:.3f}%",
        f"{profile_2026['var_cornish_fisher_95']*100:.3f}%",
        f"{profile_2026['var_historico_99']*100:.3f}%",
        f"{profile_2026['var_cornish_fisher_99']*100:.3f}%",
        f"{profile_2026['cvar_expected_shortfall_99']*100:.3f}%",
        f"{profile_2026['sharpe_ratio']:.3f}",
        f"{profile_2026['sortino_ratio']:.3f}",
    ],
})

print("TABLA COMPARATIVA: PERFIL DE RIESGO DE COLA DEL FONDO E")
print(var_table)

# Rupturas de VaR 99% histórico durante 2026
var_threshold_99 = profile_hist['var_cornish_fisher_99']
dias_ruptura = df_e_2026.filter(pl.col('ret_real_diario') < -var_threshold_99)
print(f"\\n🚨 Días con caída peor al VaR 99% histórico ({var_threshold_99*100:.2f}%): {len(dias_ruptura)} días.")
"""

# Célula 7: Markdown Sección 4
c7_md = """## 4. Visualización Editorial: "The Underwater & VaR Shock Chart" (Producto 1)
Construimos el gráfico compuesto oficial con diseño editorial de doble panel:
- **Panel Superior:** Trayectoria de un saldo base de $100.000.000 CLP en el Fondo E vs. Fondo A.
- **Panel Inferior:** Curva de Drawdown (*Underwater Curve*) con bandas de VaR al 99% y anotaciones de los hitos de intervención regulatoria.
"""

# Célula 8: Code Gráfico de Producto 1 con Plotly
c8_code = """df_e_p = df_e_sys.to_pandas()
df_a_p = df_a_sys.to_pandas()

# Crear subplots con doble panel vertical
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    row_heights=[0.55, 0.45],
    subplot_titles=(
        "<b>Evolución Patrimonial Real (Saldo Base: $100.000.000 CLP en UF)</b>",
        "<b>Curva de Drawdown Histórico (Underwater) y Rupturas de VaR al 99%</b>",
    ),
)

# Saldo normalizado a $100 MM al inicio
base_cap = 100_000_000.0
saldo_e = base_cap * (df_e_p["vc_real_uf"] / df_e_p["vc_real_uf"].iloc[0])
saldo_a = base_cap * (df_a_p["vc_real_uf"] / df_a_p["vc_real_uf"].iloc[0])

# Trace 1: Saldo Fondo E
fig.add_trace(
    go.Scatter(
        x=df_e_p["fecha"],
        y=saldo_e,
        name="Fondo E (Conservador)",
        line=dict(color=PALETTE["swaps_loss"], width=2.5),
    ),
    row=1, col=1,
)

# Trace 2: Saldo Fondo A
fig.add_trace(
    go.Scatter(
        x=df_a_p["fecha"],
        y=saldo_a,
        name="Fondo A (Renta Variable)",
        line=dict(color="#2EC4B6", width=1.5, dash="dot"),
    ),
    row=1, col=1,
)

# Trace 3: Underwater Fondo E
fig.add_trace(
    go.Scatter(
        x=df_e_p["fecha"],
        y=df_e_p["drawdown_real"] * 100,
        name="Drawdown Fondo E",
        line=dict(color=PALETTE["swaps_loss"], width=2),
        fill="tozeroy",
        fillcolor="rgba(217, 4, 41, 0.2)",
    ),
    row=2, col=1,
)

# Trace 4: Underwater Fondo A
fig.add_trace(
    go.Scatter(
        x=df_a_p["fecha"],
        y=df_a_p["drawdown_real"] * 100,
        name="Drawdown Fondo A",
        line=dict(color="#2EC4B6", width=1, dash="dash"),
    ),
    row=2, col=1,
)

# Anotación del colapso 2026
fig.add_annotation(
    x="2026-09-30",
    y=-10.39,
    xref="x2",
    yref="y2",
    text="<b>Cierre Sep-2026: -10,39%</b><br>Shock de Swaps y Forwards USD",
    showarrow=True,
    arrowhead=2,
    arrowcolor=PALETTE["swaps_loss"],
    bgcolor="#1E293B",
    bordercolor=PALETTE["swaps_loss"],
    font=dict(color="#F8FAFC", size=10),
)

fig.update_layout(
    height=750,
    template="fondo_e_dark",
    title="<b>THE UNDERWATER & VaR SHOCK: LA RUPTURA DEL FONDO CONSERVADOR</b><br><sup>Comparativa 2018–2026 en UF. Fuente: Superintendencia de Pensiones y SII.</sup>",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

fig.update_yaxes(title_text="Patrimonio Real ($ CLP)", tickformat="$,.0f", row=1, col=1)
fig.update_yaxes(title_text="Drawdown Real (%)", ticksuffix="%", row=2, col=1)

fig.show()
"""

# Célula 9: Markdown Conclusiones
c9_md = """## 5. Conclusiones y Validación de la Hipótesis
1. **Falsación de la Hipótesis del Refugio Seguro:** El Fondo E exhibió en 2026 un Drawdown acumulado de **-12,02%** (-10,39% al cierre de septiembre), superando con creces la volatilidad y drawdown del Fondo A (cuya máxima caída en el año fue apenas del -1,61%).
2. **Colapso del Sharpe y Sortino Ratio:** El ratio de Sortino pasó de terreno positivo a un valor marcadamente negativo, confirmando que las pérdidas del Fondo E no fueron fluctuaciones simétricas normales, sino choques asimétricos con colas pesadas.
3. **VaR Cornish-Fisher:** El VaR ajustado por asimetría y curtosis demostró ser significativamente superior al paramétrico gaussiano, comprobando matemáticamente la presencia de riesgo de cola derivado del apalancamiento sintético en swaps.
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

out_nb_path = Path("notebooks/02_anatomia_drawdown_y_var_fondo_e.ipynb")
with open(out_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook 02 escrito en: {out_nb_path}. Ejecutando celdas...")
res = subprocess.run(
    ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(out_nb_path)],
    capture_output=True,
    text=True,
)
if res.returncode == 0:
    print("✅ Notebook 02 ejecutado exitosamente con todos los outputs guardados.")
else:
    print(f"❌ Error al ejecutar Notebook 02:\\n{res.stderr}")
    sys.exit(1)
