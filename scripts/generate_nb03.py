"""Generador y ejecutor de notebooks/03_descomposicion_derivados_swaps_forwards.ipynb."""

from pathlib import Path
import nbformat as nbf
import subprocess

nb = nbf.v4.new_notebook()

# Célula 1: Markdown Introducción y Fórmulas
c1_md = r"""# 📓 Notebook 03: Descomposición de Derivados (Swaps & Forwards)
## Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

### 1. Marco Teórico y Formulación Matemática de Derivados

El objetivo central de este laboratorio es contrastar la narrativa oficial (*"cayeron los bonos chilenos"*) con los microdatos de derivados, demostrando que el **80% del desplome nominal** del Fondo E en 2026 provino exclusivamente de apuestas apalancadas en **Swaps de Tasas de Interés** y **Forwards Cambiarios**.

#### 1.1. Sensibilidad de Precio por Duración Efectiva y Convexidad (Taylor Expansion)
El cambio porcentual en el valor de una cartera de renta fija ante variaciones en la tasa de rendimiento $\Delta y = y_t - y_{t-1}$ se aproxima mediante la expansión de Taylor de segundo orden:

$$\frac{\Delta P}{P} \approx -D_{\text{efectiva}} \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$$

donde la **Duración Efectiva Total ($D_{\text{efectiva}}$)** es la suma de la duración de los bonos físicos más la duración sintética incorporada mediante derivados:

$$D_{\text{efectiva}} = D_{\text{bonos\_físicos}} + D_{\text{swaps\_sintética}}$$

- **Cartera de Bonos Físicos:** $D_{\text{bonos}} \approx 10,2$ años (alargada mediante deuda soberana BTP/BTU 2035–2050).
- **Swaps de Tasas de Interés (IRS USD):** Al recibir tasa fija de largo plazo en USD y pagar tasa flotante (SOFR), las AFP agregaron $D_{\text{swaps}} \approx 6,8$ años de duración sintética a costo cero de caja.
- **Duración Combinada:** $D_{\text{efectiva}} \approx 10,2 + 6,8 = \mathbf{17,0\text{ años}}$.

Frente a un shock de tasas del Tesoro de EE.UU. a 10 años ($\text{US10Y}$) de $+111\text{ pb}$ (pasando de $4,18\%$ a $5,29\%$):

$$\frac{\Delta P}{P}_{\text{lineal}} \approx -17,0 \times 0,0111 = \mathbf{-18,87\%}$$

#### 1.2. Descomposición Factorial Aditiva de Pérdidas (Return Attribution Waterfall)
El retorno nominal total del Fondo E en 2026 ($-7,40\%$) se descompone aditivamente en cuatro bloques de instrumentos:

$$R_{\text{nominal, total}} = R_{\text{swaps\_usd}} + R_{\text{swaps\_local}} + R_{\text{forwards\_fx}} + R_{\text{bonos\_físicos}}$$

1. **Swaps de Tasas Extranjeras (USD):** $-4,50\text{ pp}$ (IRS en USD a 5 y 10 años).
2. **Swaps de Tasas Locales:** $-1,40\text{ pp}$ (SPC en CLP y UF).
   - **Total Pérdida por Swaps:** $-4,50 - 1,40 = \mathbf{-5,90\text{ pp}}$ (representa el **$79,73\%$** de toda la caída nominal).
3. **Forwards de Tipo de Cambio (Short FX al 150%):** $-0,80\text{ pp}$. Las AFP vendieron dólares a plazo por el $150\%$ de su cartera extranjera. Al depreciarse el peso (USD/CLP subió de $\$911$ a $\$970$), la sobrecobertura corta destruyó valor en lugar de actuar como amortiguador.
4. **Bonos Físicos (Renta Fija Local e Internacional):** $-0,70\text{ pp}$.

#### 1.3. Efecto Inflación (Deflactación por UF)
La conversión entre el retorno nominal y el retorno real auditado ($-10,39\%$) responde a la identidad de Fisher:

$$1 + R_{\text{real}} = \frac{1 + R_{\text{nominal}}}{1 + \pi_{\text{UF}}} \implies R_{\text{real}} = \frac{1 - 0,0740}{1 + 0,0334} - 1 = \mathbf{-10,39\%}$$

$$\Delta_{\text{inflación}} = R_{\text{real}} - R_{\text{nominal}} = -10,39\% - (-7,40\%) = \mathbf{-2,99\text{ pp}}$$

#### 1.4. Regresión Móvil de Sensibilidad (Rolling Beta contra US10Y)
Para cuantificar empíricamente cómo el Fondo E pasó a depender de la política monetaria de la Reserva Federal:

$$R_{E, t} = \alpha_t + \beta_t \cdot \Delta y_{\text{US10Y}, t} + \epsilon_t, \quad \beta_t = \frac{\text{Cov}_W\left(R_{E, t}, \Delta y_{\text{US10Y}, t}\right)}{\text{Var}_W\left(\Delta y_{\text{US10Y}, t}\right)}$$
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
    MASTER_DAILY_PANEL_PATH,
    MONTHLY_CHECKPOINTS_PATH,
    PALETTE,
    SWAPS_NOTIONAL_EVOLUTION_MM_USD,
)
from src.models.attribution import (
    calculate_duration_sensitivity,
    get_afp_attribution_table,
    get_official_attribution_breakdown,
    get_waterfall_chart_data,
)
from src.models.risk_metrics import calculate_rolling_beta
from src.viz.theme import register_plotly_theme, setup_matplotlib_theme

setup_matplotlib_theme()
register_plotly_theme()

# Cargar datasets analíticos
master_daily = pl.read_parquet(MASTER_DAILY_PANEL_PATH)
checkpoints = pl.read_parquet(MONTHLY_CHECKPOINTS_PATH)
afp_panel = pl.read_parquet(AFP_DERIVATIVES_PANEL_PATH)

print("✅ Datasets de derivados y checkpoints cargados exitosamente.")
"""

# Célula 3: Markdown Sección 2
c3_md = """## 2. Auditoría Factorial de Pérdidas: ¿Dónde se Destruyó el Capital?
Examinamos la descomposición cuantitativa oficial y verificamos que el 80% del daño nominal provino exclusivamente de swaps.
"""

# Célula 4: Code Tabla de Atribución y Sensibilidad
c4_code = """attr = get_official_attribution_breakdown()
sens = calculate_duration_sensitivity()

print("=" * 75)
print("AUDITORÍA DE DESCOMPOSICIÓN FACTORIAL DEL FONDO E (ENERO - SEPTIEMBRE 2026)")
print("=" * 75)
print(f"1. Swaps Tasas Extranjeras (IRS USD 5Y/10Y):     {attr['swaps_tasas_usd_pp']:6.2f} pp")
print(f"2. Swaps Tasas Locales (SPC UF/CLP):              {attr['swaps_tasas_locales_pp']:6.2f} pp")
print(f"   -> SUB-TOTAL PÉRDIDA POR SWAPS:               {attr['total_swaps_pp']:6.2f} pp  ({attr['pct_daño_explicado_por_swaps']:.1f}% del daño nominal)")
print(f"3. Forwards USD (Sobrecobertura Corta al 150%):  {attr['forwards_fx_pp']:6.2f} pp")
print(f"   -> TOTAL DERIVADOS FINANCIEROS:               {attr['total_derivados_pp']:6.2f} pp  ({attr['pct_daño_explicado_por_derivados']:.1f}% del daño nominal)")
print(f"4. Renta Fija Física (Bonos Soberanos/Bancarios): {attr['bonos_fisicos_pp']:6.2f} pp")
print("-" * 75)
print(f"RETORNO NOMINAL TOTAL FONDO E:                    {attr['retorno_nominal_total_pct']:6.2f}%")
print(f"5. Arrastre por Variación de UF (Inflación):     {attr['arrastre_inflacion_uf_pp']:6.2f} pp")
print("=" * 75)
print(f"RETORNO REAL TOTAL FONDO E (EN UF):               {attr['retorno_real_total_pct']:6.2f}%")
print("=" * 75)

print(f"\\nSENSIBILIDAD POR DURACIÓN:")
print(f"- Duración Bonos Físicos:    {sens['duracion_fisica_anios']} años")
print(f"- Duración Sintética Swaps:   {sens['duracion_sintetica_swaps_anios']} años")
print(f"- Duración Total Efectiva:   {sens['duracion_total_efectiva_anios']} años")
print(f"- Impacto Teórico alza US10Y ({sens['delta_yield_bps']:.0f} pb): {sens['impacto_teorico_lineal_pct']:.2f}%")
"""

# Célula 5: Markdown Sección 3
c5_md = """## 3. Visualización Oficial (Producto 2): Waterfall de Atribución Factorial
Construimos el gráfico en cascada (*Waterfall Chart*) de alta precisión que ilustra visualmente el colapso del Fondo E tramo por tramo.
"""

# Célula 6: Code Gráfico Waterfall en Plotly
c6_code = """wf_data = get_waterfall_chart_data()

fig_wf = go.Figure(go.Waterfall(
    name="Atribución",
    orientation="v",
    measure=wf_data["measure"],
    x=wf_data["categories"],
    textposition="outside",
    text=[f"{v:+.2f}%" if m == "relative" else f"{v:.2f}%" for v, m in zip(wf_data["values"], wf_data["measure"])],
    y=wf_data["values"],
    connector={"line": {"color": "#64748B", "width": 1.5, "dash": "dot"}},
    decreasing={"marker": {"color": PALETTE["swaps_loss"]}},
    increasing={"marker": {"color": "#2EC4B6"}},
    totals={"marker": {"color": "#3B82F6"}},
))

fig_wf.update_layout(
    title="<b>DESCOMPOSICIÓN FACTORIAL DE PÉRDIDAS: FONDO E 2026</b><br><sup>El 80% de la caída nominal (-5,9 pp de -7,4%) fue provocado por Swaps de Tasas. Fuente: SPensiones e IEF Banco Central.</sup>",
    template="fondo_e_dark",
    yaxis_title="Contribución al Retorno (%)",
    height=550,
    showlegend=False,
)

fig_wf.show()
"""

# Célula 7: Markdown Sección 4
c7_md = """## 4. Visualización Oficial (Producto 3): Termómetro de Duración y Crecimiento en Swaps
Analizamos la escalada exponencial en la exposición nocional a Swaps extranjeros (pasando de US$ 5.300 millones en agosto de 2023 a US$ 206.900 millones a fines de 2025) y su correlación con la tasa del Tesoro de EE.UU. a 10 años (US10Y).
"""

# Célula 8: Code Gráfico de Nocional en Swaps y Tasa US10Y
c8_code = """periodos = list(SWAPS_NOTIONAL_EVOLUTION_MM_USD.keys())
nocionales = list(SWAPS_NOTIONAL_EVOLUTION_MM_USD.values())

fig_swaps = make_subplots(specs=[[{"secondary_y": True}]])

# Barra: Nocional de Swaps
fig_swaps.add_trace(
    go.Bar(
        x=periodos,
        y=[n / 1000.0 for n in nocionales],  # En Miles de Millones de USD (Billions)
        name="Nocional Swaps Tasas Externas (US$ Billones)",
        marker_color=PALETTE["swaps_loss"],
        opacity=0.85,
    ),
    secondary_y=False,
)

# Línea: Salto de Duración
duraciones = [8.3, 12.6, 16.0, 17.0]
fig_swaps.add_trace(
    go.Scatter(
        x=periodos,
        y=duraciones,
        name="Duración Total Efectiva (Años)",
        line=dict(color="#F59E0B", width=3, dash="solid"),
        mode="lines+markers+text",
        text=[f"{d:.1f} años" for d in duraciones],
        textposition="top center",
    ),
    secondary_y=True,
)

fig_swaps.update_layout(
    title="<b>EL SALTO DEL APALANCAMIENTO SINTÉTICO (2023–2026)</b><br><sup>Nocional en Swaps escaló 40x mientras la duración efectiva alcanzó 17 años. Fuente: IEF Banco Central.</sup>",
    template="fondo_e_dark",
    height=500,
    hovermode="x unified",
)

fig_swaps.update_yaxes(title_text="Nocional en Swaps (Miles de Millones USD)", secondary_y=False)
fig_swaps.update_yaxes(title_text="Duración Efectiva (Años)", secondary_y=True, range=[5, 20])

fig_swaps.show()
"""

# Célula 9: Markdown Sección 5
c9_md = """## 5. Regresión Móvil: El Beta del Fondo E contra las Tasas de EE.UU.
Calculamos el Beta rodante a 60 días entre el retorno diario del Fondo E y los cambios en el rendimiento del bono del Tesoro de EE.UU. a 10 años ($\Delta \text{US10Y}$).
"""

# Célula 10: Code Regresión y Gráfico de Beta
c10_code = """df_e_sys = master_daily.filter((pl.col('afp') == 'SISTEMA') & (pl.col('fondo') == 'E')).sort('fecha')

# Calcular delta de US10Y diario
df_beta = df_e_sys.with_columns([
    pl.col('us10y').diff().alias('delta_us10y'),
]).drop_nulls(subset=['ret_real_diario', 'delta_us10y'])

ret_e = df_beta['ret_real_diario'].to_numpy()
delta_y = df_beta['delta_us10y'].to_numpy()
fechas = df_beta['fecha'].to_list()

rolling_beta = calculate_rolling_beta(ret_e, delta_y, window=60)

fig_beta = go.Figure()

fig_beta.add_trace(go.Scatter(
    x=fechas,
    y=rolling_beta,
    name="Rolling Beta (60d)",
    line=dict(color=PALETTE["swaps_loss"], width=2),
))

fig_beta.add_hline(y=0.0, line_dash="dash", line_color="#94A3B8")

fig_beta.update_layout(
    title="<b>SENSIBILIDAD DIRECTA A LA RESERVA FEDERAL (ROLLING BETA CONTRA US10Y)</b><br><sup>Un alza de tasas en EE.UU. castigó al Fondo E con una correlación negativa extrema entre 2024 y 2026.</sup>",
    template="fondo_e_dark",
    yaxis_title="Beta Sensibilidad (Retorno E / Delta US10Y)",
    height=450,
)

fig_beta.show()
"""

# Célula 11: Markdown Conclusiones
c11_md = """## 6. Conclusiones Forenses
1. **Los Derivados Causaron el 80% de la Caída:** Los swaps de tasas en USD restaron **-4,5 pp** y los swaps locales **-1,4 pp** (total **-5,9 pp** de la caída nominal de **-7,4%**).
2. **Duración Oculta Propia de Hedge Fund:** La cartera combinó 10,2 años de bonos físicos con 6,8 años sintéticos en swaps para alcanzar **17 años de duración efectiva**, duplicando la sensibilidad del fondo conservador.
3. **Short USD Destructivo:** La sobrecobertura corta al 150% en forwards restó **0,8 pp**, transformando la apreciación del dólar en un factor de pérdida adicional en lugar de un refugio cambiario.
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
    nbf.v4.new_code_cell(c10_code),
    nbf.v4.new_markdown_cell(c11_md),
]

out_nb_path = Path("notebooks/03_descomposicion_derivados_swaps_forwards.ipynb")
with open(out_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook 03 escrito en: {out_nb_path}. Ejecutando celdas...")
res = subprocess.run(
    ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(out_nb_path)],
    capture_output=True,
    text=True,
)
if res.returncode == 0:
    print("✅ Notebook 03 ejecutado exitosamente con todos los outputs guardados.")
else:
    print(f"❌ Error al ejecutar Notebook 03:\\n{res.stderr}")
    sys.exit(1)
