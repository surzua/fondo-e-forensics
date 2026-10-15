# 🚀 MASTER PLAN & SPECIFICATION: Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

## 1. Contexto del Proyecto y Tesis Analítica
**Objetivo Principal:** Construir un ecosistema de productos de datos (artículo técnico interactivo, visualizaciones de alta densidad para LinkedIn y una Web App en Streamlit) que audite el colapso del **Fondo E de las AFP en Chile durante 2026 (-10,39% real a septiembre)**, contrastando la narrativa oficial de la industria con los microdatos públicos de tenencia de cartera y derivados.

### Tesis Central ("Dicen A, la Data dice B")
* **Narrativa Oficial (Prensa Generalista y Vocerías AFP):** *"El Fondo E es el refugio conservador para afiliados próximos a jubilar. Las caídas puntuales de 2026 se deben a la volatilidad normal de la renta fija local y deben evaluarse con un horizonte de inversión de largo plazo (3 a 5 años)."*
* **Evidencia Empírica en los Microdatos:**
  1. **Apalancamiento Sintético en Derivados (80% del daño):** De la caída nominal acumulada a septiembre (-7,4%), **5,9 puntos porcentuales** provienen exclusivamente de contratos **Swaps de Tasas de Interés** (-4,5 pp en swaps de tasas externas en USD y -1,4 pp en swaps locales). Los bonos físicos explican una fracción marginal.
  2. **Duración Oculta de Renta Variable:** Mediante swaps (recibiendo tasa fija larga en USD y pagando tasa flotante), las AFP extendieron la duración efectiva del Fondo E desde ~5 años (histórico) hasta **10,2 años en bonos físicos y hasta 17 años incluyendo derivados**. Cuando el bono del Tesoro de EE.UU. a 10 años (US10Y) subió de 4,18% a 5,29%, el Fondo E sufrió un drawdown propio de un fondo especulativo.
  3. **Destrucción del Amortiguador Cambiario (Short USD al 150%):** El Fondo E vendió dólares a futuro mediante Forwards por hasta el **150% de su cartera internacional** (sobrecobertura neta corta en USD). Al subir el tipo de cambio de $911 a $970 CLP/USD, en vez de compensar la caída externa, los forwards restaron otros **0,8 puntos porcentuales**.
  4. **La Falacia del Largo Plazo en Fase de Desacumulación:** Un cotizante a 6 meses de jubilar no tiene horizonte de recuperación. Liquidar cuotas con un drawdown de -10,39% para contratar una Renta Vitalicia o iniciar un Retiro Programado consolida una **pérdida patrimonial y pensional perpetua e irreversible**.

### 1.1. Marco Normativo y Régimen de Inversión (D.L. 3500 vs. Realidad 2026)
Para comprender la dinámica de la cartera, es indispensable contrastar las restricciones legales del Decreto Ley 3500 y el Régimen de Inversión de la Superintendencia de Pensiones frente a la realidad operativa:
* **Renta Variable (Límite Legal: Máx 5%):** Cumplido nominalmente (0% a 1%). El Fondo E no tenía acciones.
* **Renta Fija Nacional (Mayoritaria):** ~86% del fondo invertido en títulos de Tesorería General de la República (BTP/BTU), Bonos Bancarios y Bonos Corporativos.
* **Inversión Extranjera (Límite Legal: Hasta 35%):** Cumplido físicamente (solo ~13,6% en bonos internacionales).
* **El Vacío Normativo en Duración:** La normativa histórica **no fijaba un techo a la duración modificada** de los instrumentos de renta fija. Las AFP alargaron la cartera de bonos físicos a **10,2 años** mediante deuda soberana de largo plazo (BTP/BTU a 2035–2050).
* **El Arbitraje en Derivados (Capítulo III.I Compendio SPensiones):** Los Swaps de Tasas de Interés (IRS) estaban autorizados para "cobertura y gestión eficiente". Al recibir tasa fija larga en USD y pagar tasa flotante SOFR, las AFP incorporaron **~6,8 años de duración sintética a costo cero de caja**, elevando la duración total a **17 años**. Cumplieron la letra de la ley mientras asumían un riesgo de tasa de interés propio de un fondo especulativo.
* **Sobrecobertura Cambiaria Neta:** La regulación exige acotar el descalce de moneda extranjera. Las AFP no solo cubrieron el 100% de sus activos en USD, sino que vendieron dólares a futuro (Forwards Short USD) por hasta el **150% de su cartera foránea**, quedando cortas en dólares en un año donde el tipo de cambio escaló de $911 a $970 CLP/USD.
* **La Intervención del Regulador (Abril–Noviembre 2026):** En abril de 2026, la Superintendencia dictó una nueva norma fijando un **tope de 2% de pérdida esperada bajo estrés en derivados**, otorgando como plazo perentorio el **5 de noviembre de 2026** para desarmar el exceso de exposición. Este límite gatilló un desarme forzado y coordinado de posiciones (*herding*), consolidando la caída de -10,39%.

## 2. Catálogo de Productos Analíticos (Deliverables)

El proyecto generará **5 productos analíticos principales** que alimentarán tanto el artículo web como la estrategia viral en LinkedIn y la aplicación en Streamlit:

### Producto 1: "The Underwater & VaR Shock Chart" (Gráfico de Alta Densidad para LinkedIn/Web)
* **Qué es:** Un gráfico compuesto de doble panel vertical.
  * **Panel Superior:** Evolución de un saldo base de $100.000.000 CLP reales (ajustados por UF) desde 2019 a octubre de 2026 comparando Fondo E vs. Fondo A vs. Depósito a Plazo Renovable (UF + tasa libre de riesgo).
  * **Panel Inferior (Underwater / Drawdown Chart):** Caída porcentual desde el máximo histórico previo (*Peak-to-Trough*) del Fondo E, superponiendo bandas de **Value at Risk (VaR Histórico y Cornish-Fisher al 95% y 99%)** y marcando con anotaciones las declaraciones del regulador y de los gerentes de inversión.
* **Impacto:** Demuestra visualmente que el "fondo conservador" rompió su propio VaR al 99% en múltiples ocasiones, exhibiendo un riesgo de cola (*tail risk*) superior al de la renta variable local en ventanas críticas.

### Producto 2: Cascada de Descomposición Factorial de Pérdidas (Brinson / Return Attribution Waterfall)
* **Qué es:** Un gráfico Waterfall interactivo y estático de alta resolución que desglosa milimétricamente el retorno nominal (-7,4%) y real (-10,39%) de 2026 por clase de activo e instrumento:
  * Renta Fija Soberana y Corporativa Local (Bonos físicos)
  * Renta Fija Internacional
  * **Swaps de Tasas Extranjeras (IRS USD 5Y/10Y)**
  * **Swaps de Tasas Locales (SPC CLP/UF)**
  * **Forwards de Tipo de Cambio (Posición Corta Neta USD/CLP)**
  * Efecto Inflación (Variación UF)
* **Impacto:** Desmonta la excusa de que "cayeron los bonos chilenos" al mostrar que el bloque dominante de pérdidas proviene de derivados offshore.

### Producto 3: Termómetro de "Duración Sintética Oculta" y Exposición en Swaps (2015–2026)
* **Qué es:** Visualización de área apilada y doble eje que muestra:
  1. El crecimiento exponencial del nocional en Swaps de tasas extranjeras del sistema (pasando de US$ 5.300 millones en agosto 2023 a US$ 107.100 millones en 2024 y US$ 206.900 millones a fines de 2025) cruzado con el rendimiento del US Treasury 10Y.
  2. La descomposición de la **Duración Efectiva Total** del Fondo E: Duración Base en Bonos Físicos (~10,2 años) + Duración Sintética por Derivados (~6,8 años) = **17 años de sensibilidad a tasas**.

### Producto 4: Matriz de "Efecto Manada" por AFP (Heatmap & Ranking de Agresividad)
* **Qué es:** Comparativa transversal entre las 7 AFP (Capital, Cuprum, Habitat, Modelo, PlanVital, Provida, Uno) en el Fondo E:
  * Caída real acumulada en 2026 (desde -9,9% en Uno hasta -10,9% en Modelo y -10,8% en Capital).
  * Peso relativo de pérdidas por Swaps sobre el patrimonio del Fondo E de cada administradora.
  * Ratio de sobrecobertura cambiaria (Forwards vendidos / Activos en moneda extranjera).
  * Correlación cruzada de retornos diarios entre AFP (demostrando comportamiento gregario o *herding*).

### Producto 5: Calculadora Interactiva de "Daño Actuarial Irreversible" (Core de la App en Streamlit)
* **Qué es:** Herramienta interactiva donde el usuario ingresa:
  1. Saldo acumulado en el Fondo E (CLP o UF).
  2. AFP actual.
  3. Edad, sexo y meses restantes para jubilar.
  4. Sueldo imponible actual.
* **Outputs Calculados en Tiempo Real:**
  * **Pérdida Patrimonial Neta ($ CLP):** Total perdido en 2026 y cuánto de ese monto se perdió específicamente en apuestas con Swaps y Forwards.
  * **Recorte Mensual Perpetuo de Pensión ($ CLP/mes):** Cálculo actuarial utilizando el **Capital Necesario Unitario (CNU)** con tablas de mortalidad oficiales (RV-2020 de la SPensiones) y tasa técnica vigente de Retiro Programado / Renta Vitalicia.
  * **Simulación de Monte Carlo de "Trabajo Forzado Extra":** Proyección estocástica (10.000 trayectorias) que calcula cuántos **meses o años adicionales de cotización** necesita trabajar la persona para recuperar el nivel de pensión que tenía antes del desplome de 2026.

---

## 3. Arquitectura del Repositorio y Estándares de Ingeniería

El agente debe inicializar y mantener la siguiente estructura de directorios estricta, separando la exploración (Notebooks) del código de producción (`src/`) y la capa de presentación (`app/`):

```text
fondo-e-audit/
├── README.md
├── AGENT_MASTER_PLAN.md          # Este documento rector
├── pyproject.toml                # Gestión de dependencias (uv / poetry)
├── .env.example                  # Variables de entorno (ej. credenciales API BCentral si aplica)
├── Makefile                      # Comandos rápidos (make scrape, make etl, make test, make app)
├── data/
│   ├── raw/                      # Datos crudos inmutables descargados por los scrapers
│   │   ├── spensiones_cuotas/    # CSVs originales de valores cuota y patrimonio
│   │   ├── spensiones_carteras/  # ZIPs/CSVs de carteras mensuales y derivados
│   │   ├── bcentral/             # Series de UF, TPM, BCP10, BCU10, IEF
│   │   ├── market/               # Parquet/CSV de US10Y (^TNX) y USD/CLP
│   │   └── actuarial/            # Tablas completas de mortalidad RV-2020 (hombres/mujeres)
│   ├── interim/                  # Datos limpios y estandarizados en formato Parquet
│   └── processed/                # Tablas analíticas finales:
│       ├── master_daily_panel.parquet           # Panel continuo diario (cuotas, UF, FX, US10Y, retornos reales)
│       ├── monthly_audit_checkpoints.parquet    # Cierres mensuales auditados (prensa y reportes oficiales)
│       └── afp_derivatives_panel.parquet        # Exposición, swaps, duración y sobrecobertura por AFP
├── notebooks/                    # Checkpoints obligatorios de validación científica
│   ├── 01_ingesta_y_auditoria_calidad.ipynb
│   ├── 02_anatomia_drawdown_y_var_fondo_e.ipynb
│   ├── 03_descomposicion_derivados_swaps_forwards.ipynb
│   ├── 04_efecto_manada_comparativa_afps.ipynb
│   └── 05_modelo_actuarial_cnu_y_montecarlo.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py                 # Rutas (Pathlib), constantes, URLs base y parámetros globales
│   ├── schemas.py                # Contratos de datos con Pydantic / Pandera
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py               # Cliente HTTP con retries, backoff exponencial, User-Agent rotation y caché local
│   │   ├── spensiones_cuota.py   # Scraper de series diarias de Valor Cuota y Patrimonio
│   │   ├── spensiones_cartera.py # Scraper de carteras mensuales, renta fija y derivados
│   │   ├── bcentral_macro.py     # Extractor de UF, curvas soberanas locales e IEF
│   │   └── market_benchmarks.py  # Extractor de US Treasury (FRED/yfinance) y divisas
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── clean_cuotas.py       # Deflactación por UF, cálculo de retornos logarítmicos y reales
│   │   ├── clean_carteras.py     # Cruce de posiciones en derivados, duración y forwards
│   │   └── build_ analytical_mart.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── risk_metrics.py       # Cálculo de Drawdown, VaR (Histórico, Paramétrico, Cornish-Fisher), CVaR, Volatilidad Rolling
│   │   ├── attribution.py        # Descomposición factorial de retornos (Bonos vs Swaps vs FX)
│   │   └── actuarial.py          # Cálculo de CNU (RV-2020), anualidades y Simulación de Monte Carlo
│   └── viz/
│       ├── __init__.py
│       ├── theme.py              # Paleta corporativa/editorial de alto contraste (estilo FT / Economist / Dark Mode)
│       ├── charts_social.py      # Exportación de PNG/SVG en 300 DPI para LinkedIn y Web
│       └── charts_interactive.py # Figuras Plotly para incrustar en Streamlit y blog
├── app/
│   ├── Home.py                   # Entrypoint de la aplicación Streamlit
│   ├── components/               # Tarjetas KPI, sliders y tablas formateadas
│   └── pages/
│       ├── 1_Calculadora_Actuarial.py
│       ├── 2_Auditoria_Derivados_y_Swaps.py
│       └── 3_Ranking_y_Efecto_Manada_AFP.py
└── tests/
    ├── test_scrapers.py
    ├── test_schemas.py
    └── test_actuarial_math.py
```

### Reglas de Calidad de Código (Software & Data Science Best Practices)
1. **Tipado Estático y Validación:** Todo el código en `src/` debe usar *Type Hints* (`typing`) y docstrings formato Google. Cada dataset transformado debe validarse con **Pandera** o **Pydantic** antes de guardarse en `data/interim/` o `data/processed/`.
2. **Idempotencia y Caché en Scraping:** Ningún scraper debe volver a descargar un archivo si ya existe en `data/raw/` con hash válido, a menos que se pase el flag `force_refresh=True`.
3. **Almacenamiento Eficiente:** Los archivos crudos se guardan en su formato nativo (CSV/ZIP/JSON) en `data/raw/`. Todo archivo procesado debe guardarse en **Apache Parquet** (`.parquet`) para preservar tipos de datos (`datetime64`, `float64`) y acelerar la carga en Streamlit.
4. **Cero Valores Hardcodeados sin Respaldo:** Si un dato agregado proviene de un informe oficial (ej. IEF del Banco Central o reporte de atribución de septiembre 2026), debe estar parametrizado de forma transparente y documentada en `src/config.py` o en una tabla de referencia auditable.

---

## 4. Especificación Técnica de Scrapers y Extracción de Datos

El agente debe implementar los siguientes módulos de extracción en `src/scrapers/` manejando correctamente la codificación chilena (`latin-1` / `cp1252` vs `utf-8`), separadores de punto y coma (`;`), puntos de miles y comas decimales.

### 4.1. Scraper 1: Series Diarias de Valor Cuota y Patrimonio (`spensiones_cuota.py`)
* **Fuente:** Centro de Estadísticas de la Superintendencia de Pensiones (`spensiones.cl`).
* **Mecanismo de Extracción:**
  * La Superintendencia publica los valores cuota diarios por año y por tipo de fondo (A, B, C, D, E) mediante descargas directas CSV o consultas POST/GET en su portal de series históricas (`https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php` y endpoints de datos abiertos en `safpstats`).
  * **Estrategia Dual (Direct CSV + Scraper BeautifulSoup/Playwright):**
    1. Consultar directamente los archivos planos anuales/históricos de valores cuota para los fondos `A`, `C` y `E` desde 2010 hasta octubre de 2026.
    2. Parsear la estructura típica del CSV de SPensiones:
       * Separador: `;`
       * Decimales: `,` | Miles: `.`
       * Columnas por cada AFP (`CAPITAL`, `CUPRUM`, `HABITAT`, `MODELO`, `PLANVITAL`, `PROVIDA`, `UNO`): `Valor Cuota` y `Valor Fondo (Patrimonio en MM$o miles de$)`.
    3. Calcular el **Valor Cuota Promedio Ponderado del Sistema** diario usando el patrimonio de cada AFP como ponderador:
       $$VC_{sistema, t} = \sum_{i=1}^{N} \left( VC_{i, t} \cdot \frac{\text{Patrimonio}_{i, t}}{\sum_{j=1}^{N} \text{Patrimonio}_{j, t}} \right)$$

### 4.2. Scraper 2: Carteras Mensuales, Duración y Derivados (`spensiones_cartera.py`)
* **Fuente:** Reportes Mensuales de Inversiones y Rentabilidad de los Fondos de Pensiones + Base de Cartera Agregada y por AFP (`spensiones.cl/portal/institucional/594/w3-propertyvalue-9921.html` / sección Estadísticas de Inversiones).
* **Qué datos exactos extraer:**
  1. **Exposición en Derivados (Swaps y Forwards):**
     * Valorización neta (Mark-to-Market en MM US$) y nocional de **Swaps extranjeros de tasas de interés**, **Swaps extranjeros de moneda**, **Swaps nacionales de tasas** y **Forwards de monedas** para el Fondo E y el sistema total (evolución mensual 2023–septiembre 2026).
  2. **Composición de Cartera del Fondo E (Nacional vs. Extranjera):**
     * Porcentaje en Bonos de Tesorería (40,2% de la cartera nacional en sep-2026), Bonos Bancarios (21,3%), Bonos de Empresas (21,9%) y exposición extranjera (13,6%).
  3. **Cobertura Cambiaria (Ratio Forwards USD / Activos USD):**
     * Serie mensual del porcentaje de activos en dólares cubiertos mediante ventas a futuro (mostrando la escalada desde 47% en dic-2025 a 121% en jul-2026 y ~150% en sep-2026).
  4. **Duración de la Cartera de Renta Fija Nacional:**
     * Serie histórica de duración en años de los instrumentos de deuda local del Fondo E (evolución desde ~5 años en 2009 a 7,2 en 2017 y >10,2 años en 2025–2026).
* **Manejo de Archivos y Automatización de ZIPs:** Automatizar la descarga de los archivos `.zip` / `.csv` / `.xls` mensuales de la Superintendencia. El scraper debe descomprimir el ZIP directamente en memoria (`io.BytesIO` / `zipfile.ZipFile`) o en `data/raw/spensiones_carteras/`, autodetectar la codificación (`latin-1`/`utf-8`), procesar las tablas de derivados, composición y duración, y estructurarlas limpiamente. Incluir un módulo de ingesta de respaldo con los vectores auditados del cierre de septiembre 2026 en caso de bloqueo por firewall (WAF/Cloudflare) o cambios de URL en el servidor de la Superintendencia.

### 4.3. Scraper 3: Series Macroeconómicas Locales y UF (`bcentral_macro.py`)
* **Fuente Primaria:** API REST / Portal de Estadísticas del Banco Central de Chile (`si3.bcentral.cl`) y `mindicador.cl/api` (como API JSON rápida sin autenticación para UF y Dólar Observado).
* **Series a Extraer:**
  * **UF Diaria (`uf`):** Indispensable para transformar todos los valores cuota nominales a **rentabilidad real en UF** día a día:
    $$R_{\text{real}, t} = \frac{VC_t / UF_t}{VC_{t-1} / UF_{t-1}} - 1$$
  * **Dólar Observado (`dolar`):** Serie diaria CLP/USD (verificando el salto de $911 a $970 en 2026).
  * **Tasas de Bonos del Banco Central en UF y Pesos (BCU-5, BCU-10, BCP-10):** Para contrastar cuánto se movió la tasa local frente a la tasa de EE.UU.

### 4.4. Scraper 4: Benchmarks Internacionales de Tasas (`market_benchmarks.py`)
* **Fuente:** `yfinance` y `pandas_datareader` (FRED - Federal Reserve Economic Data).
* **Tickers a Extraer (Frecuencia Diaria, 2018–Octubre 2026):**
  * `^TNX` o serie FRED `DGS10`: Rendimiento del Bono del Tesoro de EE.UU. a 10 años (US 10Y Treasury Yield). Es la variable explicativa número 1 de las pérdidas en Swaps extranjeros de las AFP (subida de 4,18% a 5,29%, con un shock de +54 pb en septiembre 2026).
  * `DGS5` (FRED) / `^FVX`: Rendimiento del Bono del Tesoro de EE.UU. a 5 años.
  * `TLT` (iShares 20+ Year Treasury Bond ETF): Para comparar la volatilidad y el drawdown del Fondo E chileno contra un ETF de bonos del Tesoro de EE.UU. de ultra larga duración.

---

## 5. Estrategia de Notebooks (Hitos de Exploración y Validación)

El agente **NO debe escribir la aplicación final a ciegas**. Debe construir y ejecutar secuencialmente **5 Jupyter Notebooks** en la carpeta `notebooks/`. Cada notebook actúa como un laboratorio de validación científica y genera artefactos intermedios.

### 📓 Notebook 01: `01_ingesta_y_auditoria_calidad.ipynb`
* **Propósito:** Ejecutar todos los scrapers, validar la integridad de las series temporales, tratar días festivos (Chile vs. EE.UU.), verificar que no existan *missing values* ni saltos espurios y deflactar los valores cuota por la UF diaria.
* **Checkpoints de Validación:**
  * Confirmar que la variación real acumulada del Fondo E entre el 31 de diciembre de 2025 y el 30 de septiembre de 2026 coincide con el **-10,39% real (-7,4% nominal)** reportado oficialmente (-4,92% real solo en septiembre).
  * Exportar `data/interim/cuotas_reales_diarias.parquet` y `data/interim/macro_benchmarks.parquet`.

### 📓 Notebook 02: `02_anatomia_drawdown_y_var_fondo_e.ipynb`
* **Propósito:** Calcular la serie histórica de Drawdowns (*Underwater Curve*), la volatilidad anualizada móvil (ventana de 30 y 90 días) y las métricas de riesgo de cola: **VaR Histórico, VaR Paramétrico y VaR Modificado de Cornish-Fisher (95% y 99%)**, además del **Expected Shortfall (CVaR)**.
* **Hipótesis a Demostrar:**
  * Comparar los 3 únicos episodios de pérdidas severas del Fondo E en enero-septiembre desde su creación: **2021 (-11,06%)**, **2023 (-4,91%)** y **2026 (-10,39%)**.
  * Demostrar que la relación Retorno/Riesgo (Sharpe y Sortino Ratio) del Fondo E colapsó y que su drawdown en 2026 superó al del Fondo A (+8,61% en el mismo período).
* **Output Visual:** Prototipo del **Producto 1 (Underwater & VaR Shock Chart)**.

### 📓 Notebook 03: `03_descomposicion_derivados_swaps_forwards.ipynb`
* **Propósito:** Auditar la cartera de inversiones y modelar matemáticamente cómo los derivados amplificaron las pérdidas.
* **Modelamiento Matemático a Incluir:**
  1. **Ecuación de Sensibilidad por Duración Efectiva y Convexidad:**
     $$\frac{\Delta P}{P} \approx -\left(D_{\text{bonos}} + D_{\text{swaps}}\right) \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$$
     Demostrar cómo pasar de $D = 7,2$ años a $D_{\text{total}} \approx 17$ años provocó que un alza de ~111 pb en el US10Y devastara el valor cuota.
  2. **Atribución de Pérdidas 2026:** Estructurar la tabla exacta de contribución donde los Swaps extranjeros restan **-4,5 pp**, los Swaps locales **-1,4 pp** (totalizando **-5,9 pp**, el 80% de la caída nominal de -7,4%) y los Forwards de dólar restan **-0,8 pp** debido a la posición corta de 150% en USD.
  3. **Regresión Rolling (Beta a Tasas de EE.UU.):** Correr una regresión lineal móvil entre los retornos semanales del Fondo E y los cambios en el rendimiento del bono del Tesoro de EE.UU. a 10 años ($\Delta \text{US10Y}$) desde 2018 a 2026, demostrando visualmente cómo el Beta del Fondo E chileno hacia la Reserva Federal se disparó entre 2024 y 2026.
* **Output Visual:** Prototipos de los **Productos 2 y 3 (Waterfall de Atribución + Termómetro de Duración y Swaps)**.

### 📓 Notebook 04: `04_efecto_manada_comparativa_afps.ipynb`
* **Propósito:** Analizar la dispersión y el comportamiento gregario (*herding behavior*) entre las 7 AFP.
* **Análisis a Realizar:**
  * Comparar las caídas reales del Fondo E en 2026 por AFP (AFP Modelo -10,9%, AFP Capital -10,8%, Cuprum, Habitat, Provida, PlanVital, hasta AFP Uno con -9,9%) y el impacto específico de los swaps por gestora.
  * Calcular la matriz de correlación de retornos diarios entre las 7 AFP y el *Tracking Error* entre ellas para demostrar cómo el incentivo regulatorio/competitivo ("si crees que las tasas están altas, quieres tener más tasa que el de al lado") llevó a toda la industria a tomar la misma apuesta direccional apalancada.
  * Modelar el impacto del límite regulatorio de abril/noviembre 2026 (tope de 2% de pérdida esperada bajo estrés en derivados fijado por la Superintendencia con fecha límite 5 de noviembre), mostrando cómo forzó un desarme simultáneo de posiciones.
* **Output Visual:** Prototipo del **Producto 4 (Heatmap y Ranking de AFP)**.

### 📓 Notebook 05: `05_modelo_actuarial_cnu_y_montecarlo.ipynb`
* **Propósito:** Construir el motor matemático que traduce la caída porcentual del Fondo E en **pérdida de pensión mensual vitalicia** y **años extra de trabajo necesario**.
* **Metodología Actuarial y Estocástica:**
  1. **Cálculo del Capital Necesario Unitario (CNU):** Implementar el cálculo actuarial riguroso a partir de la tabla completa de mortalidad **RV-2020** (hombres y mujeres, edades 0 a 110, $l_x, q_x, p_x, D_x, N_x$) alojada en `data/raw/actuarial/tabla_rv2020.csv`, con tasa técnica de descuento anual parametrizable ($i_t \approx 3,0\% - 3,4\%$ real anual):
     $$\text{Pensión Mensual} = \frac{\text{Saldo Acumulado}}{12 \cdot \text{CNU}(x, \text{sexo}, i_t)}$$
  2. **Simulación de Monte Carlo para Recuperación Patrimonial:**
     * Para un afiliado con saldo inicial $S_0$ que sufre un shock de $-10,39\%$ quedando en $S_1 = S_0 \cdot (1 - 0,1039)$, simular $M = 10.000$ trayectorias mensuales futuras vectorizadas en NumPy (`shape: (10000, n_meses)`) usando un proceso de difusión con saltos o *Bootstrap* histórico de retornos reales mensuales más el aporte mensual del $10\%$ del sueldo imponible.
     * Determinar la distribución de probabilidad del **Tiempo de Recuperación ($T_{\text{rec}}$ en meses)** en los percentiles P10 (escenario optimista), P50 (mediana) y P90 (escenario adverso).
* **Output:** Validación completa del módulo `src/models/actuarial.py` que alimentará la aplicación en Streamlit.

---

## 6. Roadmap de Ejecución Paso a Paso para Antigravity

El agente debe ejecutar este proyecto siguiendo estrictamente estas **5 Fases Secuenciales**. Al finalizar cada fase, debe verificar que los tests pasen y que los artefactos existan en disco.

### Fase 0: Inicialización del Entorno, Git y Configuración Base
1. Inicializar el repositorio Git y configurar `.gitignore` bajo estándares profesionales para Python/Data Science (excluyendo `.venv/`, caches, descargas crudas pesadas y preservando tablas de referencia actuariales).
2. Crear la estructura completa de carpetas detallada en la Sección 3 (incluyendo `data/raw/actuarial/`).
3. Configurar el entorno virtual con `uv` (`pyproject.toml`) instalando: `pandas`, `polars`, `numpy`, `scipy`, `statsmodels`, `requests`, `httpx`, `beautifulsoup4`, `lxml`, `yfinance`, `pydantic`, `pandera`, `plotly`, `matplotlib`, `seaborn`, `kaleido`, `streamlit`, `pytest`, `jupyter`, `ipykernel`.
4. Escribir `src/config.py` con rutas absolutas dinámicas (`pathlib.Path`), paleta de colores editorial y parámetros de auditoría documentados.

### Fase 1: Construcción de Scrapers e Ingesta de Datos (`src/scrapers/`)
1. Implementar `src/scrapers/base.py` con manejo de sesiones HTTP, reintentos automáticos (`urllib3.util.retry` o `tenacity`), cabeceras realistas y caché en `data/raw/`.
2. Implementar `spensiones_cuota.py`, `spensiones_cartera.py`, `bcentral_macro.py` y `market_benchmarks.py`.
3. **Regla de Resiliencia Crítica:** Dado que los portales gubernamentales chilenos (`spensiones.cl` / `bcentral.cl`) ocasionalmente aplican bloqueos anti-bot o cambian enlaces de archivos ZIP mensuales, cada scraper debe incluir:
   * Un extractor en vivo (web scraping / API).
   * Un validador de integridad del archivo descargado.
   * Un generador/cargador de respaldo (*fallback dataset*) calibrado exactamente con las series reales y las cifras oficiales auditadas de los reportes de la Superintendencia de Pensiones, Banco Central (IEF) y CLAPES UC a octubre de 2026, garantizando que el pipeline analítico nunca se detenga por un error HTTP 403/503 externo.
4. Ejecutar y validar **Notebook 01 (`01_ingesta_y_auditoria_calidad.ipynb`)**.

### Fase 2: Procesamiento ETL, Contratos de Datos y Motores Cuantitativos (`src/etl/` y `src/models/`)
1. Implementar los esquemas de validación en `src/schemas.py`.
2. Construir el pipeline ETL que cruza las cuotas diarias del Fondo E, la UF diaria, el tipo de cambio CLP/USD y la tasa del Tesoro de EE.UU. a 10 años (`US10Y`), generando `data/processed/master_daily_panel.parquet` y `data/processed/afp_derivatives_panel.parquet`.
3. Programar los módulos cuantitativos en `src/models/`:
   * `risk_metrics.py` (Drawdown, VaR Histórico, VaR Cornish-Fisher, CVaR, Rolling Beta contra US10Y).
   * `attribution.py` (Descomposición del retorno de 2026 entre bonos físicos, swaps de tasas externas, swaps locales y forwards cambiarios).
   * `actuarial.py` (Cálculo de CNU por edad/sexo y motor de Monte Carlo vectorizado en NumPy para estimar meses de trabajo extra).
4. Ejecutar y documentar **Notebooks 02, 03, 04 y 05**, asegurándose de que todas las celdas corran sin errores y dejen guardados sus outputs e insights.

### Fase 3: Fábrica de Visualizaciones Editoriales (`src/viz/`)
1. Configurar en `src/viz/theme.py` un diseño visual de nivel periodístico financiero (inspirado en *Financial Times* / *Bloomberg*):
   * Tipografía limpia (`Inter`, `Roboto` o `IBM Plex Sans`).
   * Colores semánticos claros: Rojo carmesí (`#D90429`) para pérdidas por Swaps/Derivados, Azul acero (`#2B2D42`) para bonos físicos, Ámbar (`#F77F00`) para Forwards USD, Gris neutro para comparativas.
   * Subtítulos explicativos que declaren el hallazgo directo en el encabezado de cada gráfico, notas al pie con la fuente exacta (*"Fuente: Elaboración propia en base a microdatos de Cartera y Valores Cuota de la Superintendencia de Pensiones, IEF del Banco Central y Reserva Federal (FRED). Datos a octubre de 2026."*).
2. Generar automáticamente en `data/processed/charts/` las imágenes estáticas en alta resolución (PNG 300 DPI, formato 16:9 para el blog y formato 4:5 vertical para carrusel de LinkedIn) y los archivos JSON/HTML interactivos de Plotly para los **Productos 1, 2, 3 y 4**.

### Fase 4: Desarrollo de la Aplicación Interactiva en Streamlit (`app/`)
1. Construir una aplicación multipágina o basada en pestañas (*Tabs*) con diseño ejecutivo (`layout="wide"`), estructurada así:
   * **Sidebar (Panel de Control del Afiliado):** Inputs para Saldo Acumulado ($ CLP o UF), AFP actual, Edad, Sexo, Edad planeada de jubilación y Sueldo Imponible mensual.
   * **Tab 1 — Tu Impacto Patrimonial y Actuarial (El Gancho Ciudadano):**
     * 4 KPIs superiores con deltas en rojo: Pérdida Total en 2026 ($ CLP), Pérdida atribuible exclusivamente a Derivados/Swaps ($ CLP), Recorte Permanente en tu Pensión Mensual ($ CLP/mes de por vida) y Meses de Trabajo Extra requeridos (Mediana Monte Carlo).
     * Gráfico interactivo del abanico de trayectorias de Monte Carlo mostrando cuándo se recupera el capital bajo distintos escenarios de tasas.
   * **Tab 2 — La Auditoría Forense (¿Por qué cayó el Fondo Seguro?):**
     * Gráfico Waterfall de descomposición de pérdidas (Swaps EE.UU. -4,5 pp, Swaps Locales -1,4 pp, Forwards USD -0,8 pp, Bonos físicos).
     * Gráfico de Duración Efectiva (10,2 años en bonos + 6,8 años sintéticos en swaps = 17 años) cruzado con el salto del Bono del Tesoro de EE.UU. a 10 años (de 4,18% a 5,29%).
     * Explicación didáctica de la sobrecobertura cambiaria (venta de dólares a futuro al 150% que eliminó el amortiguador del tipo de cambio cuando el dólar subió de $911 a $970).
   * **Tab 3 — Riesgo Extremo (Underwater & VaR) y Ranking de AFP:**
     * Gráfico Underwater histórico comparando el Fondo E con el Fondo A y mostrando las rupturas del VaR al 99%.
     * Tabla y Heatmap comparativo de las 7 AFP mostrando cuáles administradoras lideraron las pérdidas por swaps (Modelo, Capital, Cuprum) y el cronograma del desarme forzado por el límite de estrés del 2% de la Superintendencia de Pensiones con plazo al 5 de noviembre.
2. Incluir un botón de **"Descargar Reporte de Auditoría Personalizado (CSV/HTML)"** y tarjetas listas para compartir en redes sociales.

### Fase 5: Empaquetado Editorial (Artículo Web + Kit Viral LinkedIn) y Testing
1. Escribir y ejecutar tests unitarios en `tests/` (`pytest`) verificando que las fórmulas de atribución sumen exactamente el retorno total, que el CNU sea consistente con edades de 55 a 70 años y que la simulación de Monte Carlo converja en menos de 1,5 segundos.
2. Generar en una carpeta `deliverables/` el borrador final en Markdown del **Artículo para la Página Web** (con los enlaces a los gráficos interactivos y citas exactas a los datos) y el **Kit de Publicación para LinkedIn** (Post principal, texto del carrusel lámina por lámina y primer comentario técnico).

---

## 7. Instrucciones de Inicio para el Agente (Prompt de Arranque)

> **Directiva para Antigravity:**
> Lee este archivo `AGENT_MASTER_PLAN.md` completo. Comienza inmediatamente con la **Fase 0** y la **Fase 1**. Crea la estructura de directorios, configura las dependencias, implementa los módulos de extracción en `src/scrapers/` y genera el primer notebook `notebooks/01_ingesta_y_auditoria_calidad.ipynb`. Ejecuta el código para verificar que los datasets se generen limpiamente en `data/interim/` antes de avanzar a la Fase 2. Avísame al completar cada fase mostrando un resumen de las métricas validadas.
