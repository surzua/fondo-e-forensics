# 📋 Informe de Cierre: Fase 2
**Proyecto:** Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")  
**Fecha:** Octubre 2026  
**Estado:** ✅ Fase 2 Completada al 100% (ETL, Motores Cuantitativos, 23 Tests Unitarios y Notebooks 02 a 05 Ejecutados)

---

## 1. Resumen Ejecutivo de la Fase 2

La Fase 2 implementó la capa de procesamiento analítico y los motores matemáticos del proyecto:
1. **Contratos de Datos y Schemas:** Validación estricta con Pydantic y Pandera sobre Polars en `src/schemas.py`.
2. **Pipeline ETL y Analytical Marts:** Generación de `master_daily_panel.parquet`, `afp_derivatives_panel.parquet` y `monthly_audit_checkpoints.parquet` en `data/processed/`.
3. **Módulos Cuantitativos (`src/models/`):**
   - `risk_metrics.py`: Drawdown, Volatilidad Móvil, VaR (Histórico, Paramétrico, Cornish-Fisher), CVaR y Rolling Beta contra el US10Y.
   - `attribution.py`: Sensibilidad de Duración Efectiva (17 años), Taylor Expansion y Descomposición Factorial (Waterfall).
   - `actuarial.py`: Tablas de Mortalidad RV-2020, Capital Necesario Unitario (CNU) y Motor de Monte Carlo vectorizado (10.000 trayectorias).
4. **Validación Experimental en Notebooks:** Ejecución exitosa y generación de figuras interactivas para los Notebooks 02, 03, 04 y 05.
5. **Calidad de Software:** 23 tests unitarios en verde en `tests/` ejecutados en menos de 1 segundo.

---

## 2. Formulación Matemática Detallada por Módulo

### 2.1. Métricas de Riesgo y Colas (`src/models/risk_metrics.py`)

#### A. Drawdown y Peak Histórico
Dado el valor cuota real en UF $P_t = \frac{VC_t}{UF_t}$:
$$\text{Peak}_t = \max_{0 \le s \le t} P_s, \quad \text{Drawdown}_t = \frac{P_t - \text{Peak}_t}{\text{Peak}_t} \le 0$$
$$\text{Maximum Drawdown (MDD)} = \min_{0 \le t \le T} \text{Drawdown}_t$$

#### B. Volatilidad Anualizada Rodante (Ventana $W = 30$ o $90$ días)
$$\sigma_{\text{rolling}, t} = \sqrt{252} \cdot \sqrt{\frac{1}{W-1} \sum_{i=0}^{W-1} \left(R_{t-i} - \bar{R}_t\right)^2}$$

#### C. Value at Risk (VaR)
- **VaR Histórico:** $\text{VaR}_\alpha^{\text{hist}} = -\text{Quantile}_\alpha(R)$
- **VaR Paramétrico (Gaussiano):** $\text{VaR}_\alpha^{\text{param}} = -(\mu + z_\alpha \cdot \sigma)$
- **VaR Modificado de Cornish-Fisher (Colas Pesadas y Asimetría):**
  $$S = \frac{\mathbb{E}[(R - \mu)^3]}{\sigma^3}, \quad K_{\text{ex}} = \frac{\mathbb{E}[(R - \mu)^4]}{\sigma^4} - 3$$
  $$z_{\text{CF}} = z_\alpha + \frac{1}{6}(z_\alpha^2 - 1) S + \frac{1}{24}(z_\alpha^3 - 3 z_\alpha) K_{\text{ex}} - \frac{1}{36}(2 z_\alpha^3 - 5 z_\alpha) S^2$$
  $$\text{VaR}_\alpha^{\text{CF}} = -(\mu + z_{\text{CF}} \cdot \sigma)$$

#### D. Conditional Value at Risk (CVaR / Expected Shortfall)
$$\text{CVaR}_\alpha = -\mathbb{E}[R \mid R \le -\text{VaR}_\alpha]$$

#### E. Rolling Beta contra Rendimiento del Bono del Tesoro US10Y ($\Delta y_t$)
$$\beta_t = \frac{\text{Cov}_W(R_{E, t}, \Delta y_t)}{\text{Var}_W(\Delta y_t)}$$

---

### 2.2. Atribución Factorial y Duración (`src/models/attribution.py`)

#### A. Sensibilidad de Taylor por Duración Efectiva y Convexidad
$$\frac{\Delta P}{P} \approx -D_{\text{efectiva}} \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$$
$$D_{\text{efectiva}} = D_{\text{bonos\_físicos}} (10,2\text{ años}) + D_{\text{swaps\_sintética}} (6,8\text{ años}) = \mathbf{17,0\text{ años}}$$
Para $\Delta y = 5,29\% - 4,18\% = +111\text{ pb}$:
$$\frac{\Delta P}{P}_{\text{lineal}} \approx -17,0 \times 0,0111 = \mathbf{-18,87\%}$$

#### B. Descomposición Factorial Aditiva de Pérdidas Nominales
$$R_{\text{nominal, total}} = R_{\text{swaps\_usd}} + R_{\text{swaps\_local}} + R_{\text{forwards\_fx}} + R_{\text{bonos\_físicos}}$$
- **Swaps Tasas Extranjeras (USD):** $-4,50\text{ pp}$
- **Swaps Tasas Locales (UF/CLP):** $-1,40\text{ pp}$
  - **Subtotal Swaps:** $\mathbf{-5,90\text{ pp}}$ (representa el **$79,73\%$** del desplome nominal de $-7,40\%$).
- **Forwards Cambiarios (Short USD al 150%):** $-0,80\text{ pp}$
- **Bonos Físicos:** $-0,70\text{ pp}$
- **Suma Nominal Total:** $\mathbf{-7,40\%}$
- **Efecto Inflación (UF):** $\Delta_{\text{inflación}} = R_{\text{real}} - R_{\text{nominal}} = -10,39\% - (-7,40\%) = \mathbf{-2,99\text{ pp}}$
- **Retorno Real Total:** $\mathbf{-10,39\%}$

---

### 2.3. Motor Actuarial y Monte Carlo (`src/models/actuarial.py`)

#### A. Probabilidad de Supervivencia y Descuento Actuarial
$${_t}p_x = \frac{l_{x+t}}{l_x} = \prod_{k=0}^{t-1} (1 - q_{x+k}), \quad v^t = (1 + i_t)^{-t}$$

#### B. Capital Necesario Unitario (CNU) con Fórmula de Woolhouse
$$\ddot{a}_x = \sum_{t=0}^{\omega - x} v^t \cdot {_t}p_x, \quad \ddot{a}_x^{(12)} = \ddot{a}_x - \frac{11}{24}$$
$$\text{CNU}(x, \text{sexo}, i_t) = \ddot{a}_x^{(12)} \cdot f_{\text{sob}}$$
- **Hombre 65 años ($i_t = 3,2\%$):** $\text{CNU} \approx \mathbf{12,55\text{ años}}$
- **Mujer 60 años ($i_t = 3,2\%$):** $\text{CNU} \approx \mathbf{16,71\text{ años}}$

#### C. Recorte Mensual Vitalicio de Pensión
$$\text{Pensión Mensual} = \frac{\text{Saldo}}{12 \cdot \text{CNU}}, \quad \Delta \text{Pensión} = \frac{S_0 \cdot |R_{\text{shock}}|}{12 \cdot \text{CNU}}$$
- Ejemplo caso base ($S_0 = \$100.000.000$ CLP, $R_{\text{shock}} = -10,39\%$):
  $$\Delta \text{Pensión} = \frac{\$10.390.000}{12 \times 12,55} \approx \mathbf{\$68.990\text{ CLP/mes de por vida}} \quad (\mathbf{\$827.880\text{ CLP/año}})$$

#### D. Motor de Monte Carlo Vectorizado en NumPy ($M = 10.000$ simulaciones)
$$S_{m, t+1} = S_{m, t} \cdot (1 + r_{m, t}) + \text{Aporte\_Mensual}$$
$$T_{\text{rec}}^{(m)} = \min \{ t \ge 1 \mid S_{m, t} \ge S_0 \}$$
- **P10 (Escenario Favorable):** $14,0\text{ meses}$ ($1,2\text{ años}$)
- **P50 (Mediana Esperada):** $\mathbf{26,0\text{ meses}}$ ($\mathbf{2,2\text{ años de trabajo extra}}$)
- **P90 (Escenario Adverso):** $50,0\text{ meses}$ ($4,2\text{ años}$)

---

## 3. Estado de Notebooks de Validación

| Notebook | Propósito | Métricas / Hallazgo Principal | Estado |
| :--- | :--- | :--- | :--- |
| **`01_ingesta_y_auditoria_calidad.ipynb`** | Ingesta en vivo de SPensiones, SII y Yahoo Finance | Fondo E: -9,92% real acumulado; Fondo A: +8,63% real | ✅ Ejecutado (Outputs guardados) |
| **`02_anatomia_drawdown_y_var_fondo_e.ipynb`** | Drawdown, VaR Cornish-Fisher y CVaR 99% | MDD Fondo E: -12,02% vs Fondo A: -1,61%. Colapso de Sortino | ✅ Ejecutado (Outputs guardados) |
| **`03_descomposicion_derivados_swaps_forwards.ipynb`** | Waterfall de atribución y termómetro de duración | Swaps explican el 80% (-5,9 pp de -7,4%). Duración efectiva = 17 años | ✅ Ejecutado (Outputs guardados) |
| **`04_efecto_manada_comparativa_afps.ipynb`** | Matriz de correlación y herding entre 7 AFP | Correlación inter-AFP > 0,98. Tracking error < 0,5%. Modelo (-10,9%) lidera | ✅ Ejecutado (Outputs guardados) |
| **`05_modelo_actuarial_cnu_y_montecarlo.ipynb`** | Daño actuarial perpetuo y Monte Carlo | Recorte de $68k/mes de por vida. Mediana de trabajo forzado: 26 meses | ✅ Ejecutado (Outputs guardados) |

---

## 4. Estado de Pruebas Unitarias

```text
tests/test_actuarial.py .....                                            [ 21%]
tests/test_attribution.py .....                                          [ 43%]
tests/test_etl_marts.py .                                                [ 47%]
tests/test_risk_metrics.py .....                                         [ 69%]
tests/test_schemas.py ....                                               [ 86%]
tests/test_scrapers.py ...                                               [100%]

============================== 23 passed in 0.90s ==============================
```
