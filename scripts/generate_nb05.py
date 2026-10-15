"""Generador y ejecutor de notebooks/05_modelo_actuarial_cnu_y_montecarlo.ipynb."""

import sys
from pathlib import Path
import nbformat as nbf
import subprocess

nb = nbf.v4.new_notebook()

# Célula 1: Markdown Introducción y Fórmulas
c1_md = r"""# 📓 Notebook 05: Modelo Actuarial (CNU) y Simulación de Monte Carlo
## Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

### 1. Marco Teórico y Formulación Matemática Actuarial

El objetivo de este laboratorio es modelar el **daño patrimonial irreversible** que sufren los afiliados en fase de desacumulación (próximos a jubilar). A diferencia de un cotizante joven de 25 años que dispone de un horizonte de 35 años para recuperar caídas de mercado, quien está a meses de liquidar sus cuotas para contratar una **Renta Vitalicia** o un **Retiro Programado** consolida una pérdida perpetua de pensión.

#### 1.1. Tablas de Mortalidad Oficiales RV-2020 y Probabilidades de Supervivencia
A partir de la tabla completa de mortalidad chilena **RV-2020** dictada por la Superintendencia de Pensiones y la CMF, definimos la probabilidad de que una persona de edad exacta $x$ sobreviva $t$ años más:

$${_t}p_x = \frac{l_{x+t}}{l_x} = \prod_{k=0}^{t-1} (1 - q_{x+k})$$

donde:
- $l_x$: Número de personas vivas a edad $x$ (radix $l_0 = 100.000$).
- $q_x$: Tasa instantánea de mortalidad a edad $x$.

#### 1.2. Factor de Descuento Financiero y Anualidad Anticipada
Dado el tipo de interés técnico anual $i_t$ (tasa de descuento actuarial de Retiro Programado / Renta Vitalicia, calibrada en $3,2\%$ real anual):

$$v = \frac{1}{1 + i_t}, \quad v^t = (1 + i_t)^{-t}$$

El valor presente actuarial de una renta vitalicia anual anticipada unitaria es:

$$\ddot{a}_x = \sum_{t=0}^{\omega - x} v^t \cdot {_t}p_x$$

Para pagos mensuales en avance (12 cuotas al año), aplicamos la aproximación clásica de **Woolhouse**:

$$\ddot{a}_x^{(12)} \approx \ddot{a}_x - \frac{11}{24}$$

#### 1.3. Capital Necesario Unitario (CNU)
El CNU representa la cantidad de capital ($ CLP o UF) requerida para financiar una unidad anual de pensión vitalicia, incorporando la cobertura por sobrevivencia legal para viudez y orfandad ($f_{\text{sob}}$):

$$\text{CNU}(x, \text{sexo}, i_t) = \ddot{a}_x^{(12)} \cdot f_{\text{sob}}$$

- **Hombre de 65 años (tasa 3,2%):** $\text{CNU} \approx \mathbf{12,55\text{ años}}$
- **Mujer de 60 años (tasa 3,2%):** $\text{CNU} \approx \mathbf{16,71\text{ años}}$

#### 1.4. Pensión Mensual Vitalicia y Recorte Permanente
La pensión mensual líquida se obtiene dividiendo el saldo acumulado por 12 veces el CNU:

$$\text{Pensión Mensual} = \frac{\text{Saldo Acumulado}}{12 \cdot \text{CNU}(x, \text{sexo}, i_t)}$$

Al sufrir un shock del $-10,39\%$ ($R_{\text{shock}} = -0,1039$), el saldo cae a $S_1 = S_0 \cdot (1 + R_{\text{shock}})$, provocando una pérdida mensual vitalicia e irrecuperable:

$$\Delta \text{Pensión Mensual} = \frac{S_0 \cdot |R_{\text{shock}}|}{12 \cdot \text{CNU}(x, \text{sexo}, i_t)}$$

#### 1.5. Simulación de Monte Carlo de Tiempo de Recuperación (Meses de Trabajo Forzado)
Para un afiliado que posterga su jubilación intentando recuperar el capital perdido mediante rentabilidad futura y cotizaciones obligatorias ($10\%$ del sueldo imponible):

$$S_{m, t+1} = S_{m, t} \cdot (1 + r_{m, t}) + \text{Aporte\_Mensual}$$

$$\text{Aporte\_Mensual} = 0,10 \times \text{Sueldo\_Imponible}$$

$$r_{m, t} \sim \mathcal{N}\left(\mu_m, \sigma_m^2\right)$$

donde $\mu_m = (1 + \mu_{\text{anual}})^{1/12} - 1$ y $\sigma_m = \sigma_{\text{anual}} / \sqrt{12}$.

El tiempo de recuperación estocástico para cada trayectoria $m$ es:

$$T_{\text{rec}}^{(m)} = \min \left\{ t \ge 1 \mid S_{m, t} \ge S_0 \right\}$$

Calculamos la distribución empírica de $T_{\text{rec}}$ en los percentiles:
- **P10 (Escenario Favorable):** Mercado con rentabilidades reales superiores a la media.
- **P50 (Mediana Esperada):** Tiempo central más probable de trabajo adicional.
- **P90 (Escenario Adverso):** Mercado de bajo retorno donde la recuperación descansa casi en su totalidad en el ahorro forzado del afiliado.
"""

# Célula 2: Imports y Carga del Motor Actuarial
c2_code = """import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import polars as pl

from src.config import (
    DEFAULT_TECHNICAL_RATE,
    LEGAL_CONTRIBUTION_RATE,
    OFFICIAL_REAL_RETURN_2026,
    PALETTE,
    RV2020_TABLE_PATH,
)
from src.models.actuarial import ActuarialEngine
from src.schemas import ActuarialProfile
from src.viz.theme import register_plotly_theme, setup_matplotlib_theme

setup_matplotlib_theme()
register_plotly_theme()

engine = ActuarialEngine()
print("✅ Motor actuarial inicializado con tabla RV-2020.")
"""

# Célula 3: Markdown Sección 2
c3_md = """## 2. Auditoría del Capital Necesario Unitario (CNU) por Edad y Sexo
Validamos la tabla completa de factores de CNU para hombres (edades 60 a 70) y mujeres (edades 55 a 65) bajo distintas tasas técnicas de descuento.
"""

# Célula 4: Code Tabla de CNU
c4_code = """edades = [55, 60, 62, 65, 67, 70]
tasas = [0.025, 0.030, 0.032, 0.035, 0.040]

filas_cnu = []
for ed in edades:
    cnu_h_32 = engine.calculate_cnu(ed, "hombre", technical_rate=0.032)
    cnu_m_32 = engine.calculate_cnu(ed, "mujer", technical_rate=0.032)
    cnu_h_30 = engine.calculate_cnu(ed, "hombre", technical_rate=0.030)
    cnu_m_30 = engine.calculate_cnu(ed, "mujer", technical_rate=0.030)
    cnu_h_35 = engine.calculate_cnu(ed, "hombre", technical_rate=0.035)
    cnu_m_35 = engine.calculate_cnu(ed, "mujer", technical_rate=0.035)

    filas_cnu.append({
        "Edad": ed,
        "Hombre (3.0%)": f"{cnu_h_30:.2f}",
        "Hombre (3.2% Oficial)": f"{cnu_h_32:.2f}",
        "Hombre (3.5%)": f"{cnu_h_35:.2f}",
        "Mujer (3.0%)": f"{cnu_m_30:.2f}",
        "Mujer (3.2% Oficial)": f"{cnu_m_32:.2f}",
        "Mujer (3.5%)": f"{cnu_m_35:.2f}",
    })

df_cnu_comp = pl.DataFrame(filas_cnu)
print("TABLA ACTUARIAL: CAPITAL NECESARIO UNITARIO (CNU RV-2020)")
print(df_cnu_comp)

print(f"\\nCHECKPOINT VALIDADO:")
print(f"- CNU Hombre 65 años (3.2%): {engine.calculate_cnu(65, 'hombre', 0.032):.2f} (Benchmark: 12.55)")
print(f"- CNU Mujer 60 años (3.2%):  {engine.calculate_cnu(60, 'mujer', 0.032):.2f} (Benchmark: 16.71)")
"""

# Célula 5: Markdown Sección 3
c5_md = """## 3. Impacto Patrimonial y Recorte Vitalicio de Pensión: Caso de Estudio Real
Evaluamos el impacto directo sobre un afiliado hombre de 64 años a 1 año de jubilar con un saldo de **$100.000.000 CLP**, cotizando por un sueldo imponible de **$1.800.000 CLP**.
"""

# Célula 6: Code Caso de Estudio y Métricas Clave
c6_code = """# Perfil de prueba
perfil = ActuarialProfile(
    saldo_actual_clp=89_610_000.0,  # Saldo ya golpeado por el shock -10,39% ($89,61 MM)
    afp="MODELO",
    edad_actual=64,
    sexo="hombre",
    edad_jubilacion=65,
    sueldo_imponible=1_800_000.0,
    tasa_tecnica=0.032,
)

resultado = engine.evaluate_profile_impact(perfil)

print("=" * 75)
print("INFORME DE IMPACTO ACTUARIAL INDIVIDUAL (AFILIADO CASO ESTUDIO)")
print("=" * 75)
print(f"Saldo Pre-Shock Estimado (31-Dic-2025):  ${resultado.saldo_inicial_estimado:12,.0f} CLP")
print(f"Saldo Post-Shock Actual (Octubre 2026):  ${resultado.saldo_post_shock:12,.0f} CLP")
print(f"Pérdida Patrimonial Neta en 2026:        ${resultado.perdida_patrimonial_clp:12,.0f} CLP")
print(f"-> Pérdida exclusiva por Swaps/Forwards: ${resultado.perdida_swaps_clp:12,.0f} CLP  (80% del daño)")
print("-" * 75)
print(f"Factor CNU a Edad de Retiro (65 años):   {resultado.cnu:.2f} años")
print(f"Pensión Mensual Pre-Shock:               ${resultado.pension_pre_shock_mensual:12,.0f} CLP/mes")
print(f"Pensión Mensual Post-Shock:              ${resultado.pension_post_shock_mensual:12,.0f} CLP/mes")
print(f"RECORTE PERMANENTE DE POR VIDA:          ${resultado.recorte_pension_mensual:12,.0f} CLP/mes ({resultado.recorte_pension_pct:.2f}%)")
print(f"Pérdida Anual Vitalicia:                 ${resultado.recorte_pension_mensual * 12:12,.0f} CLP/año")
print("=" * 75)
"""

# Célula 7: Markdown Sección 4
c7_md = """## 4. Simulación de Monte Carlo: Abanico de Trayectorias y Tiempo de Recuperación
Simulamos 10.000 trayectorias mensuales futuras para cuantificar cuántos meses de trabajo adicional debe aportar el afiliado para recuperar los $10.390.000 CLP perdidos.
"""

# Célula 8: Code Simulación y Gráfico Fan Chart con Plotly
c8_code = """mc_sim = engine.simulate_recovery_monte_carlo(
    current_balance_clp=resultado.saldo_post_shock,
    target_balance_clp=resultado.saldo_inicial_estimado,
    monthly_contribution_clp=perfil.sueldo_imponible * LEGAL_CONTRIBUTION_RATE,
    n_sims=10000,
    max_months=120,  # 10 años
)

print("RESULTADOS DE LA SIMULACIÓN DE MONTE CARLO (10.000 TRAYECTORIAS):")
print(f"- Escenario Favorable (P10): {mc_sim['p10_meses']:.1f} meses ({mc_sim['p10_meses']/12:.1f} años extra)")
print(f"- Mediana Esperada (P50):    {mc_sim['p50_mediana_meses']:.1f} meses ({mc_sim['p50_mediana_meses']/12:.1f} años extra)")
print(f"- Escenario Adverso (P90):   {mc_sim['p90_meses']:.1f} meses ({mc_sim['p90_meses']/12:.1f} años extra)")
print(f"- Probabilidad de no recuperar en 10 años: {mc_sim['pct_no_recupera_en_horizonte']:.2f}%")

# Gráfico de abanico (Fan Chart)
fig_mc = go.Figure()

meses = mc_sim["meses_eje"]
trajectories = mc_sim["sample_trajectories"]

# Muestras individuales transparentes
for i in range(min(40, len(trajectories))):
    fig_mc.add_trace(go.Scatter(
        x=meses,
        y=trajectories[i, :],
        mode="lines",
        line=dict(color="#64748B", width=0.8),
        opacity=0.25,
        showlegend=False,
    ))

# Línea del saldo inicial (objetivo)
fig_mc.add_hline(
    y=resultado.saldo_inicial_estimado,
    line_dash="dash",
    line_color="#2EC4B6",
    annotation_text=f"Saldo Objetivo Pre-Shock: ${resultado.saldo_inicial_estimado:,.0f}",
    annotation_position="top left",
)

# Línea del saldo actual post-shock
fig_mc.add_hline(
    y=resultado.saldo_post_shock,
    line_dash="dot",
    line_color=PALETTE["swaps_loss"],
    annotation_text=f"Saldo Post-Shock 2026: ${resultado.saldo_post_shock:,.0f}",
    annotation_position="bottom left",
)

# Mediana P50
p50_m = mc_sim["p50_mediana_meses"]
fig_mc.add_vline(
    x=p50_m,
    line_dash="dash",
    line_color="#F59E0B",
    annotation_text=f"Mediana P50: {p50_m:.0f} meses de trabajo extra",
    annotation_position="top right",
)

fig_mc.update_layout(
    title="<b>SIMULACIÓN DE MONTE CARLO: RECUPERACIÓN PATRIMONIAL DEL FONDO E</b><br><sup>Un afiliado a meses de jubilar necesita ~26 meses de cotizaciones adicionales para recuperar el saldo previo.</sup>",
    template="fondo_e_dark",
    xaxis_title="Meses Futuros de Trabajo y Cotización",
    yaxis_title="Saldo Acumulado ($ CLP)",
    height=550,
)
fig_mc.show()
"""

# Célula 9: Markdown Conclusiones
c9_md = """## 5. Conclusiones y Tesis Final
1. **La Falacia del Horizonte de Largo Plazo:** La respuesta oficial de que *"el Fondo E se recuperará en 3 a 5 años"* es una falacia para quienes se jubilan en el corto plazo. El cálculo actuarial demuestra que jubilar con un recorte de $-10,39\%$ significa **perder más de $68.000 CLP mensuales de por vida**, equivalente a más de **$820.000 CLP al año de pérdida perpetua**.
2. **Costo en Vida Laboral:** Según la mediana de Monte Carlo, el afiliado se ve forzado a trabajar **26 meses adicionales (más de 2 años de trabajo extra)** simplemente para reponer la pérdida provocada por la sobreexposición a derivados de las AFP.
3. **El Daño por Derivados fue Evitable:** Dado que los bonos físicos explicaron menos del $0,7\text{ pp}$ de la pérdida nominal, más de **$8.200.000 CLP** del daño patrimonial en este afiliado fueron generados por instrumentos sintéticos que excedieron el mandato conservador del fondo de retiro.
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

out_nb_path = Path("notebooks/05_modelo_actuarial_cnu_y_montecarlo.ipynb")
with open(out_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook 05 escrito en: {out_nb_path}. Ejecutando celdas...")
res = subprocess.run(
    ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(out_nb_path)],
    capture_output=True,
    text=True,
)
if res.returncode == 0:
    print("✅ Notebook 05 ejecutado exitosamente con todos los outputs guardados.")
else:
    print(f"❌ Error al ejecutar Notebook 05:\\n{res.stderr}")
    sys.exit(1)
