# 📊 Informe de Cierre: Fase 3 — Fábrica de Visualizaciones Editoriales
**Proyecto:** Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")  
**Fecha:** Octubre 2026  
**Estado:** ✅ **Fase 3 Completada al 100% (Imágenes 300 DPI 16:9 y 4:5 + HTMLs Interactivos + 25 Tests en Verde)**

---

## 1. Resumen Ejecutivo de la Fase 3

El objetivo de la Fase 3 fue transformar los modelos cuantitativos y microdatos validados en las Fases 1 y 2 en un **catálogo de productos visuales de nivel periodístico financiero** (*Financial Times* / *Bloomberg Dark Mode*), listo para su difusión en LinkedIn, artículos web de investigación y la aplicación interactiva en Streamlit.

Se generaron e integraron exitosamente:
1. **Estilo Editorial Unificado ([`src/viz/theme.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/src/viz/theme.py)):** Paleta cromática semántica, tipografía sans-serif de alto contraste, modo oscuro (`#0D1117` / `#161B22`) y plantillas registradas para Matplotlib y Plotly (`fondo_e_dark`).
2. **Generador Estático en Alta Resolución ([`src/viz/charts_social.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/src/viz/charts_social.py)):** Exportación automática en **PNG 300 DPI** en dos formatos por producto:
   * **16:9 Horizontal:** Para el blog, artículo técnico y presentaciones ejecutivas.
   * **4:5 Vertical:** Para carruseles de LinkedIn e Instagram.
3. **Generador Interactivo Plotly ([`src/viz/charts_interactive.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/src/viz/charts_interactive.py)):** Exportación de archivos HTML autónomos y funciones de retorno de objetos `go.Figure` listos para ser consumidos por la aplicación Streamlit en la Fase 4.
4. **Incorporación Explícita de las Aclaraciones de la Auditoría Retroactiva:**
   * Nota de conciliación metodológica entre el drawdown diario ($-9,92\%$ a sep-30) y el cierre oficial mensual auditado ($-10,39\%$).
   * Aclaración de la naturaleza combinada multi-moneda de la duración efectiva de $17,0$ años (bonos locales en UF más swaps en USD).
   * Delimitación estricta de la pensión calculada como pensión contributiva autofinanciada (sin PGU) y cálculo con beneficiarios legales.

---

## 2. Catálogo de Productos Visuales Exportados (`data/processed/charts/`)

| Producto Analítico | Concepto Central | Formato 16:9 (Blog/Web) | Formato 4:5 (LinkedIn) | Interactivo (HTML) |
| :--- | :--- | :---: | :---: | :---: |
| **Producto 1: The Underwater & VaR Shock** | Saldo base $100 MM real (Fondo E vs Fondo A) y Drawdown histórico con rupturas de VaR 99%. | `producto1_underwater_var_16x9.png` (661 KB) | `producto1_underwater_var_4x5.png` (603 KB) | `producto1_underwater_var.html` (477 KB) |
| **Producto 2: Waterfall de Atribución** | Cascada aditiva: Swaps USD (-4,5 pp), Swaps locales (-1,4 pp), Forwards USD (-0,8 pp), Bonos (-0,7 pp). | `producto2_waterfall_atribucion_16x9.png` (264 KB) | `producto2_waterfall_atribucion_4x5.png` (231 KB) | `producto2_waterfall_atribucion.html` (3,3 KB) |
| **Producto 3: Termómetro de Duración y Swaps** | Nocional en Swaps (US$ 5.300M -> US$ 206.900M) vs Duración total efectiva ($17,0$ años). | `producto3_termometro_duracion_swaps_16x9.png` (265 KB) | `producto3_termometro_duracion_swaps_4x5.png` (194 KB) | `producto3_termometro_duracion_swaps.html` (3,4 KB) |
| **Producto 4: Efecto Manada y Ranking AFP** | Heatmap ($\rho > 0,98$) y ranking de caídas reales (Modelo -10,9% y Capital -10,8% al frente). | `producto4_heatmap_herding_afp_16x9.png` (259 KB) | `producto4_heatmap_herding_afp_4x5.png` (173 KB) | `producto4_heatmap_herding_afp.html` (3,2 KB) |
| **Producto 5: Monte Carlo Fan Chart** | 10.000 trayectorias de recuperación patrimonial (Mediana P50 = 26 meses de trabajo forzado extra). | *Generado en notebook / Streamlit* | *Generado en notebook / Streamlit* | `producto5_montecarlo_recuperacion.html` (71 KB) |

---

## 3. Detalle Visual y Periodístico por Producto

### 3.1. Producto 1: "The Underwater & VaR Shock Chart"
* **Encabezado Editorial:**
  * **Título:** *THE UNDERWATER & VaR SHOCK: LA FALACIA DEL FONDO SEGURO*
  * **Subtítulo:** *Evolución de $100 MM reales y drawdown histórico (2018–2026). El Fondo E cayó 7x más que el Fondo A en 2026.*
* **Estructura Gráfica:**
  * **Panel Superior:** Trayectoria de $100.000.000 CLP deflactados por UF. El Fondo E termina en $\approx \$89,6$ MM mientras el Fondo A supera los $\$108,6$ MM.
  * **Panel Inferior:** Área sombreada en rojo carmesí (`#D90429`, alpha 0.25) mostrando la profundidad del drawdown ($-12,02\%$).
* **Nota al Pie Incorporada:**  
  *"Fuente: Elaboración propia en base a SPensiones y SII. Nota metodológica: Retorno real diario acumulado de -9,92% a sep-30 vs -10,39% al cierre oficial mensual auditado."*

---

### 3.2. Producto 2: "Waterfall de Atribución Factorial de Pérdidas"
* **Encabezado Editorial:**
  * **Título:** *¿POR QUÉ CAYÓ EL FONDO SEGURO? DESCOMPOSICIÓN FACTORIAL 2026*
  * **Subtítulo:** *El 80% del daño nominal (-5,9 pp de -7,4%) provino de Swaps de Tasas. Los bonos físicos solo restaron -0,7 pp.*
* **Estructura Gráfica:**
  * Barras semánticas flotantes:
    * Rojo Carmesí (`#D90429`): Swaps USD ($-4,50\text{ pp}$) y Swaps Locales ($-1,40\text{ pp}$).
    * Ámbar (`#F59E0B`): Forwards USD Short al 150% ($-0,80\text{ pp}$).
    * Azul Acero (`#3B82F6`): Bonos Físicos ($-0,70\text{ pp}$).
    * Gris Neutro (`#64748B`): Subtotal Nominal ($-7,40\%$) y Arrastre Inflación UF ($-2,99\text{ pp}$).
    * Rojo Oscuro Totalizador (`#8D0801`): Retorno Real Final ($-10,39\%$).
* **Nota al Pie Incorporada:**  
  *"Fuente: SPensiones, IEF Banco Central y Reserva Federal. Descomposición aditiva auditada."*

---

### 3.3. Producto 3: "Termómetro de Duración y Crecimiento en Swaps"
* **Encabezado Editorial:**
  * **Título:** *LA ESCALADA DEL APALANCAMIENTO SINTÉTICO (2023–2026)*
  * **Subtítulo:** *El nocional en swaps extranjeros creció 40x mientras la duración efectiva combinada alcanzó 17 años.*
* **Estructura Gráfica:**
  * Eje izquierdo: Barras en rojo carmesí con el nocional en Swaps de Tasas Externas:
    * Ago-2023: $\text{US\$} 5,3\text{ Billones}$
    * Dic-2024: $\text{US\$} 107,1\text{ Billones}$
    * Dic-2025: $\text{US\$} 206,9\text{ Billones}$
    * Sep-2026: $\text{US\$} 185,0\text{ Billones}$ (en proceso de desarme por límite regulatorio).
  * Eje derecho: Línea dorada conectando los puntos de duración efectiva: $8,3\text{a} \to 12,6\text{a} \to 16,0\text{a} \to 17,0\text{a}$.
* **Nota al Pie Incorporada:**  
  *"Fuente: SPensiones e IEF Banco Central. Nota: La duración combina deuda soberana local en UF (10,2a) y swaps sintéticos en USD (6,8a)."*

---

### 3.4. Producto 4: "Efecto Manada y Ranking de AFPs"
* **Encabezado Editorial:**
  * **Título:** *EFECTO MANADA: TODAS LAS AFP TOMARON LA MISMA APUESTA*
  * **Subtítulo:** *Modelo y Capital lideraron las pérdidas reales. El 100% de la industria replicó la estrategia de swaps.*
* **Estructura Gráfica:**
  * **Subplot Izquierdo:** Barras horizontales del retorno real acumulado 2026 por administradora:
    * AFP Modelo: **$-10,90\%$**
    * AFP Capital: **$-10,80\%$**
    * AFP Cuprum: **$-10,60\%$**
    * AFP Habitat: **$-10,40\%$**
    * AFP Provida: **$-10,30\%$**
    * AFP PlanVital: **$-10,10\%$**
    * AFP Uno: **$-9,90\%$**
  * **Subplot Derecho:** Pérdida atribuible exclusivamente a Swaps por gestora (desde $-6,1\text{ pp}$ en Modelo/Capital hasta $-5,4\text{ pp}$ en Uno).
* **Nota al Pie Incorporada:**  
  *"Fuente: Estadísticas Oficiales SPensiones a Septiembre 2026. Correlación cruzada diaria inter-AFP > 0,98."*

---

### 3.5. Producto 5: "Calculadora Actuarial / Fan Chart de Monte Carlo"
* **Encabezado Editorial:**
  * **Título:** *SIMULACIÓN DE MONTE CARLO: RECUPERACIÓN PATRIMONIAL DEL FONDO E*
  * **Subtítulo:** *Un afiliado a meses de jubilar necesita ~26 meses de cotizaciones adicionales para recuperar el saldo previo.*
* **Estructura Gráfica:**
  * 40 trayectorias semi-transparentes en gris azulado (`#64748B`, alpha 0.20).
  * Línea horizontal turquesa discontinua en el saldo objetivo pre-shock ($\$100.000.000$ CLP).
  * Línea horizontal roja en el saldo post-shock ($\$89.610.000$ CLP).
  * Línea vertical ámbar discontinua marcando la mediana P50 ($26\text{ meses}$).
* **Nota al Pie Incorporada:**  
  *"Nota actuarial: Pérdida mensual calculada sobre pensión contributiva pura sin PGU. Modelo de difusión estocástica con 10.000 simulaciones vectorizadas en NumPy."*

---

## 4. Estado de la Suite de Pruebas Unitarias

Se incorporó [`tests/test_viz.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/tests/test_viz.py) validando la existencia física de los 13 archivos exportados y la correcta construcción de las figuras Plotly:

```bash
uv run pytest
```
```text
tests/test_actuarial.py .....                                            [ 20%]
tests/test_attribution.py .....                                          [ 40%]
tests/test_etl_marts.py .                                                [ 44%]
tests/test_risk_metrics.py .....                                         [ 64%]
tests/test_schemas.py ....                                               [ 80%]
tests/test_scrapers.py ...                                               [ 92%]
tests/test_viz.py ..                                                     [100%]

============================== 25 passed in 1.41s ==============================
```

---

## 5. Próximos Pasos: Fase 4 (Aplicación Interactiva en Streamlit)

Con todos los motores analíticos, datasets procesados y gráficos interactivos listos, la base está preparada para la **Fase 4**:
1. **`app/Home.py`:** Landing page ejecutiva con KPIs principales y navegación.
2. **`app/pages/1_Calculadora_Actuarial.py`:** Panel interactivo del afiliado (saldo, AFP, edad, sexo, sueldo) con KPIs de daño patrimonial, recorte de pensión vitalicia y fan chart interactivo de Monte Carlo con slider de retorno futuro esperado.
3. **`app/pages/2_Auditoria_Derivados_y_Swaps.py`:** Waterfall interactivo, termómetro de duración y explicación didáctica del desarme regulatorio al 5 de noviembre.
4. **`app/pages/3_Ranking_y_Efecto_Manada_AFP.py`:** Heatmap de correlación interactivo, tabla comparativa de las 7 AFP y descarga de reportes personalizados.
