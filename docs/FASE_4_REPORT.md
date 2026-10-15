# 🚀 Informe de Cierre: Fase 4 — Aplicación Interactiva en Streamlit
**Proyecto:** Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")  
**Fecha:** Octubre 2026  
**Estado:** ✅ **Fase 4 Completada al 100% (Arquitectura Multipage + 3 Páginas Analíticas + Informes Descargables + 28 Tests en Verde)**

---

## 1. Resumen Ejecutivo de la Fase 4

En esta fase se construyó y desplegó la **plataforma interactiva multipágina en Streamlit**, llevando los modelos cuantitativos, la fábrica de gráficos y las fórmulas actuariales validadas en las Fases 1, 2 y 3 a una aplicación web interactiva con estética periodística financiera de nivel internacional (*Financial Times / Bloomberg Dark Mode*).

### Componentes Principales Implementados:
1. **Configuración de Tema Editorial ([`.streamlit/config.toml`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/.streamlit/config.toml)):**
   * Paleta oscura institucional: fondo `#0D1117`, tarjetas `#161B22`, texto `#F8FAFC`, acento principal en rojo carmesí `#D90429`.
2. **Biblioteca de Estilos y Componentes ([`app/components/ui.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/components/ui.py)):**
   * Inyección de CSS editorial con tipografía *Inter* y *JetBrains Mono*, tarjetas KPI con deltas semánticos (`delta-red`, `delta-amber`, `delta-green`), bloques explicativos destacados (*callout boxes*) e insignias forenses.
3. **Gestión de Estado Persistente ([`app/components/state.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/components/state.py)):**
   * Sincronización automática de variables del afiliado entre páginas mediante `st.session_state` (Saldo, AFP, Edad, Sexo, Edad de Retiro, Sueldo Imponible, Tasa Técnica).
   * Obtención dinámica del último valor de la Unidad de Fomento (`UF = $39.536,53`).
4. **Panel Lateral Reactivo ([`app/components/sidebar.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/components/sidebar.py)):**
   * Selector bidireccional de moneda (ingreso en **$ CLP** o en **UF** con conversión en tiempo real).
   * Selección de las 7 AFP (`MODELO`, `CAPITAL`, `CUPRUM`, `HABITAT`, `PROVIDA`, `PLANVITAL`, `UNO`) o el promedio `SISTEMA`.
   * Parámetros actuariales (edad legal automática según sexo: 65 años hombres / 60 años mujeres, sueldo imponible con cálculo del 10% de cotización legal, y slider de tasa técnica).
5. **Generador de Reportes de Auditoría Personalizados ([`app/components/report.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/components/report.py)):**
   * Exportación en **HTML ejecutivo autocontenido con estilos de impresión para PDF** (con Ctrl+P / Cmd+P).
   * Exportación de la matriz de variables individuales en formato **CSV**.

---

## 2. Estructura de las Páginas de la Aplicación

### 2.1. Portada Ejecutiva ([`app/Home.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/Home.py))
* **Encabezado Institucional:** Insignias forenses, título *"La Falacia del Fondo Seguro"* y resumen ejecutivo.
* **4 KPIs Superiores de Nivel Sistema:**
  * Retorno Real Oficial 2026: **`-10,39%`** (Caída 7x mayor que Fondo A).
  * Daño Atribuible a Swaps: **`-5,90 pp`** (79,7% de la pérdida nominal total).
  * Duración Total Efectiva: **`17,0 Años`** (3,4x sobre la duración histórica de 5 años).
  * Efecto Manada Inter-AFP: **`ρ > 0,98`** (100% de la industria replicó la estrategia).
* **Bloque de Alerta Regulatoria:** Contexto del oficio reservado de la Superintendencia de Pensiones, límite de estrés del 2% y plazo de desarme al **5 de noviembre de 2026**.
* **Navegador Interactivo a los 3 Módulos:** Tarjetas ejecutivas con enlaces directos hacia las páginas especializadas.

### 2.2. Módulo 1: Calculadora Actuarial ([`app/pages/1_Calculadora_Actuarial.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/pages/1_Calculadora_Actuarial.py))
* **4 KPIs de Daño Individual:**
  * **Pérdida Total en 2026:** Cuantificada en $ CLP en base al retorno específico de su AFP o del sistema.
  * **Pérdida por Swaps y Derivados:** ~80% de la pérdida nominal total.
  * **Recorte Permanente de Pensión:** Pérdida mensual vitalicia irreversible en su pensión contributiva autofinanciada.
  * **Meses de Trabajo Adicional:** Mediana P50 del tiempo requerido para reponer el capital perdido.
* **Simulación de Monte Carlo Interactiva:**
  * Sliders en vivo para el *Retorno Real Anual Futuro Esperado* (1,0% a 6,0%) y *Volatilidad* (2,0% a 8,0%).
  * Fan Chart interactivo de Plotly con las 40 trayectorias muestrales, cotización legal del 10% y cruce de metas de recuperación.
  * Métricas de percentiles P10 (optimista), P50 (mediana), P90 (severo) y probabilidad empírica de no recuperación en 10 años.
* **Desglose Actuarial y Tablas de Mortalidad RV-2020:**
  * Tabla con el Capital Necesario Unitario (CNU), fórmula de Woolhouse y pensión pre/post-shock.
* **Sección de Descarga:** Botones para generar el informe en HTML/PDF y la planilla CSV.

### 2.3. Módulo 2: Auditoría de Derivados y Swaps ([`app/pages/2_Auditoria_Derivados_y_Swaps.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/pages/2_Auditoria_Derivados_y_Swaps.py))
* **Métricas Principales:** Nocional pico (US$ 206,9B), daño por swaps (-5,9 pp), salto del US10Y (+111 bps) y ratio de sobrecobertura corta de USD (150%).
* **1. Waterfall Interactivo de Atribución Factorial (Producto 2):** Descomposición aditiva entre Swaps USD (-4,5 pp), Swaps Locales (-1,4 pp), Forwards USD (-0,8 pp), Bonos Físicos (-0,7 pp) e Inflación UF (-2,99 pp).
* **2. Termómetro de Duración y Swaps (Producto 3):** Explicación matemática de la sensibilidad de Taylor ($\Delta P/P \approx -D \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$) y por qué extender la duración a 17 años causó un daño 4x superior al histórico.
* **3. La Trampa de la Sobrecobertura Cambiaria:** Análisis didáctico de cómo vender futuros de dólares al 150% anuló el amortiguador cambiario cuando el dólar subió de $911 a $970 CLP.
* **4. Desarme Forzado al 5 de Noviembre:** Implicancias de la venta en bloque de derivados por el límite de estrés del 2%.

### 2.4. Módulo 3: Ranking y Efecto Manada ([`app/pages/3_Ranking_y_Efecto_Manada_AFP.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/app/pages/3_Ranking_y_Efecto_Manada_AFP.py))
* **1. The Underwater & VaR Shock Chart (Producto 1):** Doble panel interactivo comparando la trayectoria de $100 MM reales (Fondo E vs Fondo A) y el drawdown histórico con rupturas de VaR 99%.
* **2. Ranking Comparativo de las 7 Administradoras (Producto 4):** Gráfico de barras horizontales mostrando caídas reales (lideradas por AFP Modelo -10,9% y AFP Capital -10,8%) y daño atribuible a swaps.
* **3. Heatmap de Correlación Inter-AFP (Efecto Manada):** Matriz de correlación cruzada calculada en vivo con los microdatos diarios de 2026 ($\rho \ge 0,987$).
* **4. Matriz Comparativa Detallada:** Tabla con todas las variables por administradora y botón de descarga de la base completa en CSV.

---

## 3. Suite de Pruebas Unitarias y Verificación

Se agregaron pruebas exhaustivas en [`tests/test_app.py`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/tests/test_app.py) para validar el estado de la sesión, la recuperación de la UF, los componentes visuales y la exportación de reportes:

```bash
uv run pytest
```
```text
============================= test session starts ==============================
rootdir: /Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics
configfile: pyproject.toml
collected 28 items

tests/test_actuarial.py .....                                            [ 17%]
tests/test_app.py ...                                                    [ 28%]
tests/test_attribution.py .....                                          [ 46%]
tests/test_etl_marts.py .                                                [ 50%]
tests/test_risk_metrics.py .....                                         [ 67%]
tests/test_schemas.py ....                                               [ 82%]
tests/test_scrapers.py ...                                               [ 92%]
tests/test_viz.py ..                                                     [100%]

============================== 28 passed in 2.70s ==============================
```

Verificación del servidor web local:
```bash
curl -s -I http://localhost:8501
```
```text
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
```

---

## 4. Próxima Etapa: Fase 5 (Empaquetado Editorial y Kit Viral)

Con la aplicación web interactiva finalizada y disponible en `http://localhost:8501`, el proyecto está listo para la **Fase 5**:
1. Redacción del **Artículo Web de Divulgación e Investigación** (Markdown completo con citas metodológicas e incrustación de gráficos).
2. Construcción del **Kit Viral de LinkedIn / Redes Sociales** (Post principal, desglose lámina por lámina para carrusel en PDF/imágenes y primer comentario técnico).
