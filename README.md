# 🏛️ Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")

Ecosistema de investigación cuantitativa, análisis forense de datos y herramientas interactivas sobre el colapso del **Fondo E de las Administradoras de Fondos de Pensiones (AFP) en Chile durante 2026 (-10,39% real a septiembre)**.

---

## 🎯 Tesis Central: "Dicen A, la Data dice B"

* **Narrativa Oficial (Regulador y Vocerías AFP):** *"El Fondo E es el refugio conservador para afiliados próximos a jubilar. Las caídas de 2026 obedecen a pérdidas de capital por alza de tasas en títulos de deuda local y a un shock exógeno inevitable de la Fed; deben evaluarse con paciencia y horizonte de 3 a 5 años."*
* **La Alerta Inicial de Prensa:** La prensa financiera (*La Tercera*) levantó las primeras banderas rojas al detectar un saldo neto de **-US$ 899,7 millones en derivados**, pero sin desentrañar la caja negra de la atribución ni su impacto en pensiones.
* **Evidencia Empírica en los Microdatos (Nuestra Auditoría):**
  1. **Apalancamiento Sintético en Derivados (80% del daño):** De la caída nominal acumulada a septiembre (-7,4%), **5,9 puntos porcentuales** provienen exclusivamente de contratos **Swaps de Tasas de Interés** (-4,5 pp en swaps externos en USD y -1,4 pp en swaps locales). La deuda física local solo explica 0,7 pp (9,5%).
  2. **Duración Oculta (Sensibilidad Extrema a Tasas):** Mediante swaps (recibiendo tasa fija en USD y pagando tasa flotante SOFR), las AFP alargaron la duración efectiva del Fondo E desde ~5 años históricos hasta **10,2 años en bonos físicos y 17 años con derivados**. Al subir el US Treasury 10Y de 4,18% a 5,29%, el fondo sufrió un shock similar al de un fondo especulativo de renta variable.
  3. **Destrucción del Amortiguador Cambiario (Short USD al 150%):** El Fondo E vendió dólares a futuro mediante Forwards por hasta el **150% de sus activos en moneda extranjera**, quedando con una posición corta neta. Al escalar el tipo de cambio de $911 a $970 CLP/USD, los forwards restaron otros **0,8 puntos porcentuales**.
  4. **La Falacia del Largo Plazo en Desacumulación:** Afiliados a meses de jubilar no tienen horizonte de recuperación. Retirarse o contratar una Renta Vitalicia bajo un drawdown de -10,39% consolida una **pérdida patrimonial y pensional perpetua e irreversible (recorte de 10% a 11% en la pensión vitalicia de por vida)**.

---

## 📂 Estructura del Repositorio

```text
fondo-e-forensics/
├── docs/
│   └── SPECIFICATIONS.md        # Especificación técnica maestra del proyecto
├── data/
│   ├── raw/                     # Datos crudos inmutables (cuotas, carteras, macro, FRED, tablas actuariales)
│   │   ├── spensiones_cuotas/
│   │   ├── spensiones_carteras/
│   │   ├── bcentral/
│   │   ├── market/
│   │   └── actuarial/           # Tabla de mortalidad oficial RV-2020 (hombres/mujeres)
│   ├── interim/                 # Datos estandarizados limpios en formato Parquet
│   └── processed/               # Datasets analíticos finales:
│       ├── master_daily_panel.parquet
│       ├── monthly_audit_checkpoints.parquet
│       └── afp_derivatives_panel.parquet
├── notebooks/                   # Laboratorio científico secuencial (Checkpoints 01 a 05)
├── src/
│   ├── config.py                # Rutas dinámicas, paletas corporativas y parámetros de auditoría
│   ├── schemas.py               # Contratos de datos con Pydantic y Pandera
│   ├── scrapers/                # Clientes HTTP, lectura de ZIPs y fallbacks calibrados
│   ├── etl/                     # Deflactación por UF, cruce de derivados y mart analítico
│   ├── models/                  # Métricas de riesgo (VaR/CVaR), atribución y motor actuarial Monte Carlo
│   └── viz/                     # Gráficos de alta resolución (300 DPI) y figuras Plotly
├── app/                         # Web App interactiva en Streamlit
└── tests/                       # Suite de pruebas unitarias
```

---

## 🚀 Instalación y Puesta en Marcha

Este proyecto utiliza `uv` para la gestión ultra veloz y determinista del entorno virtual.

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd fondo-e-forensics

# 2. Configurar el entorno virtual e instalar dependencias
make setup

# 3. Ejecutar los scrapers e ingesta de datos
make scrape

# 4. Construir el mart analítico (ETL)
make etl

# 5. Ejecutar la suite de tests
make test

# 6. Lanzar la aplicación interactiva Streamlit
make app
```

---

## 📊 Metodología y Fuentes de Datos
* **Valores Cuota y Carteras Mensuales:** Superintendencia de Pensiones de Chile (`spensiones.cl`).
* **Indicadores Macroeconómicos:** Banco Central de Chile (UF, Dólar Observado, Curvas BCP/BCU) e Informes de Estabilidad Financiera (IEF).
* **Tasas Internacionales:** Federal Reserve Economic Data (FRED) y Yahoo Finance (US10Y, US5Y, TLT).
* **Mortalidad y Actuarial:** Tablas de Mortalidad oficiales RV-2020 / MI-2020 (Superintendencia de Pensiones / Comisión para el Mercado Financiero).
