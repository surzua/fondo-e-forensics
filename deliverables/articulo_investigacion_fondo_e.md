# La Falacia del Fondo Seguro: Anatomía Forense del Desplome del Fondo E de las AFP en 2026

**Por Sebastián Urzúa Bórquez**  
*Auditoría cuantitativa basada en microdatos oficiales de inversiones de la Superintendencia de Pensiones, Banco Central de Chile y la Reserva Federal de EE.UU. (FRED).*  
*Publicado originalmente en [surzua.github.io](https://surzua.github.io) — Octubre 2026*  
*📖 ¿Primera vez leyendo sobre bonos, swaps o duración? Te recomendamos comenzar por la [Guía Esencial de Finanzas: Cómo Entender la Crisis del Fondo E sin ser Economista](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/deliverables/guia_didactica_finanzas_fondo_e.md).*

---

> ### 📌 Tesis en 30 Segundos
> Esta semana, el sistema de pensiones chileno vivió un terremoto institucional sin precedentes: la **Superintendencia de Pensiones formuló cargos e inició un proceso sancionatorio histórico contra las siete administradoras del sistema (Capital, Cuprum, Habitat, Modelo, Planvital, Provida y UNO)** por presunta vulneración del deber fiduciario, lealtad y diligencia (**Artículo 147 del D.L. 3.500** y **NCG N° 340**), tras confirmarse un agujero de valorización estimado en **US$ 7.700 millones** en los fondos conservadores.
> 
> Durante los primeros nueve meses de 2026, el **Fondo E** —el instrumento concebido por ley como el refugio inexpugnable para los trabajadores a punto de jubilarse— se desplomó un **-10,39% real** (-7,40% nominal).
> 
> Mientras el gremio de las AFP se defendió públicamente en *La Tercera* y *Diario Financiero* argumentando que *"no fueron apuestas especulativas"*, culpando al alza de tasas de la Reserva Federal y afirmando que *"no hay pérdidas definitivas, sino alzas y bajas en su valorización que se revertirán en el mediano y largo plazo"*, **esta auditoría forense abre la caja negra de los microdatos para contrastar el discurso público con la evidencia matemática:**
> 
> 1. **La autopsia matemática:** El desplome no fue provocado por la deuda local ni por un castigo genérico de Wall Street. **El 79,7% de la pérdida nominal total** (-5,90 pp de los -7,40 pp perdidos) provino exclusivamente de apuestas en contratos de **Swaps de Tasas de Interés (IRS)** en EE.UU. y derivados locales. Los bonos soberanos chilenos físicos apenas explicaron el 9,5% (-0,7 pp) de la caída.
> 2. **El arbitraje regulatorio:** No fue un inocente "calce de pasivos" ante la menor liquidez de bonos locales tras los retiros, como alega el gremio. Las AFP aprovecharon vacíos en la normativa para estirar la sensibilidad del Fondo E desde sus 5 años históricos hasta **17,0 años de duración efectiva total**, asumiendo el perfil de riesgo de un hedge fund apalancado mediante derivados OTC fuera de balance a costo cero de caja inicial, sumado a una sobrecobertura corta en dólares (Short USD) al 150% que dinamitó el amortiguador cambiario.
> 3. **La falacia del "largo plazo" en desacumulación:** El argumento gremial de que *"las valorizaciones se recuperan esperando 3 a 5 años"* es una falacia actuarial destructiva. Quien liquida sus fondos hoy para contratar una renta vitalicia consolida una **merma irreversible de por vida de 10% a 11% en su pensión mensual vitalicia**, exigiendo hasta **21 meses (casi 2 años) de trabajo forzado adicional** solo para intentar reponer el patrimonio evaporado.
> 4. **El dilema de la sanción:** Las multas administrativas que pueda aplicar el regulador irán a beneficio fiscal. El debate urgente es cómo se resarce el daño patrimonial concreto a los jubilados de 2026 y si los directores de las AFP deberán responder con su patrimonio personal, tal como advirtió el Ministerio de Hacienda.

---

## 1. El Caso de "Don Juan" y la Respuesta a la Asociación de AFP

En recientes declaraciones de prensa a *La Tercera* y *Diario Financiero* (octubre de 2026), los principales voceros de la Asociación de AFP —su presidente ejecutivo, **León Fernández de Castro**, y su gerente de estudios, **Roberto Fuentes**— salieron al paso del proceso sancionatorio afirmando que en el sistema de pensiones *"no hay pérdidas o ganancias definitivas, sino alzas y bajas en su valorización"* y que históricamente estas fluctuaciones contables se revierten en el mediano y largo plazo.

Para evaluar la validez de este axioma, aterricémoslo en la realidad de un afiliado de carne y hueso: llamémoslo **Don Juan**, 64 años, quien tras 40 años de cotizaciones ininterrumpidas acumuló **$100.000.000 CLP** (aproximadamente 2.530 UF) con el plan de jubilarse a los 65 años en diciembre de 2026.

Siguiendo disciplinadamente el mandato del Decreto Ley 3.500 y todas las recomendaciones institucionales, Don Juan mantuvo su saldo en el **Fondo E (Más Conservador)**. La promesa republicana era clara: *si estás a meses del retiro, no debes arriesgarte en acciones (Fondo A); debes proteger tu esfuerzo de toda una vida en renta fija segura.*

Al cierre de septiembre de 2026, la realidad demolió la promesa:
* Su saldo real deflactado por UF cayó a **$89.610.000 CLP**. Don Juan perdió **$10.390.000 CLP** de poder adquisitivo en solo 9 meses.
* Si Don Juan acude hoy a jubilarse y cotiza una Renta Vitalicia o un Retiro Programado, su pensión mensual autofinanciada cae de **$664.000 CLP/mes a $595.000 CLP/mes**. Es un recorte permanente de **$69.000 CLP mensuales de por vida**.

> **La falacia económica:**  
> Un afiliado en etapa de acumulación (25 o 35 años) puede esperar que el ciclo económico revierta una baja de valorización contable. **Un trabajador en etapa de desacumulación no tiene 5 años de horizonte.**  
> En el instante exacto en que Don Juan se pensiona o traspasa sus cuotas a una compañía de seguros, la "baja de valorización" se liquida en el mercado y se transforma en una pérdida de hormigón armado. No hay reversión futura posible para él.

---

## 2. Primer Shock Empírico: The Underwater & VaR Shock Chart

La magnitud de la anomalía ocurrida en 2026 queda en evidencia al comparar el comportamiento del Fondo E frente a los demás activos del mercado chileno:

![The Underwater & VaR Shock Chart](../data/processed/charts/producto1_underwater_var_16x9.png)
*Figura 1: Panel Superior: Evolución de un saldo base real de $100 MM (Fondo E vs. Fondo A vs. Benchmark libre de riesgo UF+3,2%). Panel Inferior: Curva de Drawdown histórico del Fondo E superpuesta con las bandas de Value at Risk (VaR 95% y 99% Cornish-Fisher).*

### Los Hechos que Derriban el Relato de "Riesgo Normal":
1. **Inversión Extrema de Roles:** En los primeros 9 meses de 2026, el Fondo E se desplomó un **-10,39% real**, mientras que el **Fondo A (Renta Variable Pura) subió +8,61% real**. El instrumento catalogado por ley como el más seguro exhibió una dinámica destructiva 7 veces superior a la del fondo más agresivo del sistema.
2. **Perforación Sistemática del Value at Risk (VaR):** Bajo una distribución normal de rendimientos, una pérdida que traspase la banda de **VaR al 99%** debería ocurrir apenas una vez cada 100 meses (más de 8 años). En 2026, el Fondo E perforó de forma continua sus límites de VaR al 95% y 99% Cornish-Fisher, certificando la presencia de **colas pesadas (*fat tails*)** inducidas por apalancamiento sintético no transparente.
3. **El Peor Drawdown en Dos Décadas:** Con una caída acumulada desde máximos que superó el -15% real (dejando atrás los shocks de 2021 y 2023), el Fondo E dejó de operar como un vehículo de preservación de capital para comportarse como un activo especulativo de renta fija ultra-larga.

---

## 3. Descomposición Factorial (Brinson Waterfall): ¿Dónde se Fueron 8 de Cada 10 Pesos?

En sus descargos públicos, la Asociación de AFP argumentó que las pérdidas obedecieron a la falta de títulos de deuda local tras los retiros del 10% y a un shock macroeconómico internacional inevitable originado por las alzas de tasas de la Reserva Federal.

Para someter esta coartada a escrutinio científico, desarrollamos una **descomposición factorial aditiva de retornos** sobre la cartera desagregada del Fondo E al cierre del tercer trimestre de 2026. Los resultados desmontan de raíz la tesis del "shock fortuito en bonos tradicionales":

![Waterfall de Atribución Factorial de Pérdidas](../data/processed/charts/producto2_waterfall_atribucion_16x9.png)
*Figura 2: Cascada factorial que desglosa el retorno nominal (-7,40%) y real (-10,39%) del Fondo E en 2026 por tipo de instrumento financiero y efecto inflación.*

### La Tabla Forense de Atribución (Cierre Septiembre 2026):

| Instrumento Financiero / Factor | Contribución Directa (pp) | % del Daño Nominal Total | Estrategia Real Ejecutada por las AFP |
| :--- | :---: | :---: | :--- |
| **Swaps de Tasas Extranjeras (IRS USD)** | **-4,50 pp** | **60,8%** | Posición pagadora de tasa fija en EE.UU. apostando a recortes agresivos de la Fed. |
| **Swaps de Tasas Locales (SPC CLP/UF)** | **-1,40 pp** | **18,9%** | Contratos de swaps promedio Cámara y swaps contra bonos BCP/BCU. |
| **Forwards de Tipo de Cambio (Short USD)** | **-0,80 pp** | **10,8%** | Venta de futuros de dólares al 150% de activos foráneos; golpe al subir el dólar de \$911 a \$970. |
| **Bonos Físicos de Renta Fija (Local y Ext.)** | **-0,70 pp** | **9,5%** | Cartera de deuda soberana de Tesorería, bonos bancarios y corporativos grado de inversión. |
| **Subtotal Retorno Nominal** | **-7,40%** | **100,0%** | **Caída nominal total del Fondo E a septiembre 2026.** |
| **Efecto Inflación (Variación UF +3,34%)** | **-2,99 pp** | — | Pérdida de poder adquisitivo por arrastre inflacionario. |
| **Retorno Real Oficial Deflactado por UF** | **-10,39%** | — | **Cifra auditada y sancionada por la Superintendencia de Pensiones.** |

> 🔍 **Hallazgo Clave que Sustenta los Cargos de la Superintendencia:**  
> De los **-7,40 puntos porcentuales** que cayó nominalmente el Fondo E, **-5,90 pp provienen exclusivamente de Swaps de Tasas**.  
> **El 79,7% de la pérdida del Fondo E no fue provocada por bonos soberanos ni corporativos: fue provocada por derivados offshore.** Los bonos físicos chilenos solo explican 0,7 puntos de la caída (menos de 1 de cada 10 pesos perdidos).

---

## 4. El Arbitraje de la Duración Sintética: Cuando 5 Años se Transformaron en 17

El gremio de las AFP justificó el uso masivo de derivados como una técnica legítima para *"capturar tasas de largo plazo y calzar carteras ante la menor profundidad del mercado local tras los retiros"*. Sin embargo, el análisis cuantitativo de la elasticidad de cartera desmiente que se haya tratado de un calce prudente.

### La Física Financiera de la Renta Fija:
La sensibilidad del precio de un portafolio de deuda ante variaciones en la tasa de interés se rige por:

$$\frac{\Delta P}{P} \approx -D_{\text{efectiva}} \cdot \Delta y + \frac{1}{2} \cdot C \cdot (\Delta y)^2$$

Donde $D_{\text{efectiva}}$ es la **duración modificada** (sensibilidad porcentual ante un movimiento del 1% en tasas) y $C$ es la convexidad.

Históricamente (2002–2020), el Fondo E operó con una duración en torno a **5,0 años**. Con esa estructura, si las tasas de interés globales subían 100 puntos base (+1,0%), el fondo cedía cerca de un -5%, merma que era amortiguada en pocos meses por el devengo de los cupones.

![Termómetro de Duración y Swaps](../data/processed/charts/producto3_termometro_duracion_swaps_16x9.png)
*Figura 3: Evolución del nocional en derivados de tasas del sistema de pensiones (US$ Billones) cruzado con el rendimiento del bono del Tesoro de EE.UU. a 10 años (US10Y) y la duración total combinada.*

### La Jugada Especulativa Fuera de Balance:
1. **Bonos Físicos al Límite:** Las administradoras extendieron la duración de su deuda soberana comprando bonos de Tesorería a 2035–2050 (BTP y BTU), llevando la duración física a **10,2 años**.
2. **Apalancamiento Sintético vía Swaps OTC:** En lugar de detenerse allí, las 7 AFP entraron masivamente en contratos **Interest Rate Swaps (IRS)** en Wall Street: recibieron tasa fija de largo plazo y pagaron tasa flotante (SOFR).
3. **Explosión del Nocional sin Desembolso de Caja:** Al ser instrumentos extrabursátiles (OTC), no requerían desembolso de capital al inicio, eludiendo los límites directos de inversión en balance. El nocional en derivados de tasas saltó de **US$ 5.300 millones en 2023** a la astronómica cifra de **US$ 206.900 millones a fines de 2025**.
4. **Duración Agregada de 17,0 Años:** Al sumar la duración física (10,2 años) y la sintética aportada por los swaps (6,8 años), **el Fondo E alcanzó una sensibilidad de 17,0 años**.

### El Desenlace: La Trampa de Tasas
Cuando la inflación en EE.UU. persistió y la Fed mantuvo una política restrictiva, el rendimiento del **Bono del Tesoro a 10 años (US10Y)** saltó de **4,18% a 5,29% (+111 puntos base)**:

$$\text{Impacto Teórico} \approx -17,0 \times (+1,11\%) = -18,87\%$$

Con una duración reglamentaria prudente de 5 años, el impacto habría sido de apenas -5,5%. Al cuadruplicar la sensibilidad mediante swaps, **las administradoras expusieron los ahorros de los jubilados a un riesgo equivalente al de un fondo soberano de alto riesgo o un hedge fund global**.

---

## 5. El Disparo en el Pie: Sobrecobertura Cambiaria Corta (Short USD al 150%)

En la gestión profesional de carteras internacionales, los activos foráneos cuentan con un **estabilizador automático**: en episodios de tensión financiera global o alzas de tasas de la Fed, los capitales buscan refugio en el dólar (*flight-to-quality*), lo que hace subir el tipo de cambio en Chile (CLP se deprecia). La ganancia cambiaria mitiga la caída en el precio de los bonos externos.

**¿Qué hicieron las AFP chilenas en el Fondo E?**
* Vendieron dólares a futuro a través de contratos Forwards USD/CLP por un monto equivalente al **150% de sus activos foráneos reales**.
* Lejos de realizar una cobertura prudente (100%), quedaron **netamente cortas en dólares en un 50%**. Efectuaron una apuesta direccional a que el peso chileno se apreciaría con fuerza.

**El Fiasco:**
En 2026, el dólar en Chile escaló de **$911 a $970 CLP** (+6,5%). En vez de amortiguar el golpe, la posición corta generó llamadas de margen y pérdidas netas directas por **-0,80 puntos porcentuales (-$750 millones de dólares)**, despojando a los afiliados del seguro natural del tipo de cambio.

---

## 6. Efecto Manada (Herding), Formulación de Cargos y la Trampa del Desarme

La homogeneidad de la conducta en la industria explica por qué la Superintendencia de Pensiones formuló cargos de manera simultánea contra las 7 AFP:

![Heatmap y Ranking de AFP](../data/processed/charts/producto4_heatmap_herding_afp_16x9.png)
*Figura 4: Panel Izquierdo: Ranking de caída real acumulada y daño por swaps en las 7 administradoras. Panel Derecho: Matriz de correlación cruzada de retornos diarios durante 2026.*

### La Dinámica de Rebaño:
* La **correlación cruzada diaria** de retornos entre las 7 AFP promedió **0,987**. Todas las administradoras clonaron la misma estructura de duración sintética y posiciones en derivados.
* **El incentivo perverso del encaje:** El diseño regulatorio de la rentabilidad mínima castiga con el patrimonio propio (encaje) a la administradora que se desvíe del promedio de la industria y pierda. En cambio, si toda la manada toma la misma apuesta imprudente y se estrella junta, ninguna AFP queda en desventaja relativa frente al resto.

### El Ranking del Daño Sancionado:

| Administradora | Retorno Real 2026 | Daño por Swaps (pp) | Exposición en Derivados |
| :--- | :---: | :---: | :---: |
| **AFP Modelo** | **-10,90%** | -6,15 pp | Máxima agresividad en nocional offshore |
| **AFP Capital** | **-10,80%** | -6,10 pp | Mayor sobreponderación en duración larga |
| **AFP Cuprum** | **-10,50%** | -5,95 pp | Réplica sistemática de derivados |
| **AFP Habitat** | **-10,35%** | -5,88 pp | Alta exposición a contratos IRS en EE.UU. |
| **AFP Provida** | **-10,30%** | -5,85 pp | Mayor volumen nocional nominal del sistema |
| **AFP PlanVital** | **-10,15%** | -5,78 pp | Réplica de manada |
| **AFP Uno** | **-9,90%** | -5,60 pp | Menor apalancamiento sintético relativo |
| **Promedio Sistema** | **-10,39%** | **-5,90 pp** | **Conducta colectiva coordinada** |

### La Fecha Fatal del 5 de Noviembre:
Alertada por los informes de estabilidad financiera del Banco Central, la Superintendencia emitió una norma que impuso un **techo de 2% de pérdida esperada bajo estrés en derivados**, fijando como plazo perentorio el **5 de noviembre de 2026** para desarmar el exceso de contratos.

Al tener todas las administradoras posiciones idénticas y la misma fecha límite, las contrapartes internacionales en Wall Street conocían de antemano la urgencia de venta. El desarme forzado (*fire sale*) se realizó con amplios castigos de liquidez, cristalizando las pérdidas durante el tercer trimestre de 2026.

---

## 7. Modelamiento Actuarial: El Daño Irreversible en la Pensión de Don Juan

Para traducir los porcentajes a la mesa de las familias chilenas, implementamos el cálculo estricto del **Capital Necesario Unitario (CNU)** mediante las tablas oficiales de mortalidad **RV-2020** de la Superintendencia de Pensiones.

### La Mecánica de la Renta Vitalicia:
La pensión mensual autofinanciada que puede contratar un afiliado está dada por:

$$\text{Pensión Mensual} = \frac{\text{Saldo Acumulado}}{12 \cdot \text{CNU}(x, \text{sexo}, i_t)}$$

Donde el CNU representa el valor presente actuarial de un flujo unitario vitalicio a la edad $x$, considerando probabilidades de supervivencia ($l_x$) y la tasa de descuento técnico ($i_t \approx 3,2\%$ real anual mediante aproximación de Woolhouse).

### La Factura Real de las Apuestas en Derivados:

| Perfil de Afiliado | Saldo Pre-Shock (CLP) | Saldo Post-Shock (CLP) | Pensión Pre-Shock | Pensión Post-Shock | **Recorte Mensual Vitalicio** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hombre 65 años (Jubilación)** | \$100.000.000 | \$89.610.000 | \$664.000 | \$595.000 | **-\$69.000 / mes de por vida** |
| **Mujer 60 años (Jubilación)** | \$80.000.000 | \$71.688.000 | \$399.000 | \$358.000 | **-\$41.000 / mes de por vida** |
| **Hombre 63 años (A 2 años)** | \$150.000.000 | \$134.415.000 | \$958.000 | \$858.000 | **-\$100.000 / mes de por vida** |

### Simulación de Monte Carlo: ¿Cuánto Cuesta "Esperar"?
Frente a la recomendación de la Asociación de AFP de *"esperar que el ciclo se recupere"*, ejecutamos una simulación de Monte Carlo de **10.000 trayectorias estocásticas mensuales**. Consideramos un retorno real futuro esperado del 3,5% anual, volatilidad histórica del 4,0% y la continuidad del aporte previsional del **10% del sueldo imponible** (\$1,5 millones mensuales).

![Simulación de Monte Carlo](../data/processed/charts/producto5_montecarlo_recuperacion.html)
*(Gráfico interactivo disponible en la aplicación web del proyecto)*

**Resultados de la Simulación:**
* **Percentil 10 (Escenario Favorable):** Requiere **11 meses** de trabajo adicional para recuperar el saldo previo.
* **Percentil 50 (Mediana):** Requiere **21 meses (casi 2 años completos de trabajo extra)** cotizando religiosamente mes a mes solo para volver al punto de partida.
* **Percentil 90 (Escenario Adverso):** Exige **38 meses (más de 3 años)** de postergación del retiro.
* **Probabilidad empírica de no recuperar el patrimonio en 1 año:** **78,4%**.

---

## 8. Más Allá del Proceso Sancionatorio: ¿Quién le Responde a los Jubilados?

La decisión de la Superintendencia de Pensiones de formular cargos contra las administradoras marca un punto de inflexión necesario, pero deja abierto el problema de fondo: **las sanciones administrativas concluyen en multas que se pagan a la Tesorería General de la República (beneficio fiscal), no en una restitución del saldo a los afiliados dañados**.

Tal como advirtió el Ministerio de Hacienda en la prensa esta semana, el marco legal abre la puerta a que los directores de las AFP respondan con su propio patrimonio si se determina que actuaron con negligencia respecto de sus deberes fiduciarios. Sin embargo, para cerrar la grieta que permitió esta catástrofe, se requieren medidas estructurales inmediatas:

1. **Límite Legal Estricto a la Duración Combinada:** La ley debe prohibir taxativamente que la duración total (física + sintética) de los fondos D y E supere los **5,0 años**. No puede permitirse que un fondo de desacumulación opere con 17 años de sensibilidad.
2. **Prohibición de Derivados Especulativos en Fondos Conservadores:** Los derivados de tasas y monedas en los fondos D y E deben restringirse exclusivamente a coberturas simétricas 1:1, sancionando cualquier ratio superior al 100% (como el short USD al 150%).
3. **Mecanismo de Compensación por Incumplimiento Fiduciario:** Si se acredita infracción al artículo 147 del D.L. 3.500, el patrimonio del encaje de las AFP debe destinarse prioritariamente a compensar el menor valor cuota consolidado por los afiliados que jubilaron durante 2026.
4. **Reforma al Esquema de Rentabilidad Mínima:** Desarticular el incentivo al comportamiento de rebaño (*herding*), introduciendo métricas de riesgo absoluto y penalizaciones por concentración de colas pesadas.

---

## 9. Recursos, Metodología y Código Abierto

Este estudio fue desarrollado bajo estrictos principios de reproducibilidad científica y datos abiertos:

* **Aplicación Interactiva en Streamlit:** Disponible en código abierto, permite a cualquier afiliado calcular su recorte exacto de pensión y simular su tiempo de recuperación ingresando su saldo, edad y AFP.
* **Repositorio de Código:** Disponible en GitHub (`github.com/surzua/fondo-e-forensics`), con todos los scrapers, cuadernos Jupyter de validación y suite de pruebas unitarias (`pytest`).
* **Fuentes Oficiales Auditadas:**
  * Superintendencia de Pensiones de Chile: Series diarias de Valores Cuota y Bases de Carteras de Inversión y Derivados (2010–2026).
  * Banco Central de Chile: Series de UF, Tipo de Cambio Observado e Informe de Estabilidad Financiera (IEF).
  * Federal Reserve Bank of St. Louis (FRED): Series `DGS10` y `DGS5` de Rendimiento de Bonos del Tesoro de EE.UU.
  * Tablas de Mortalidad RV-2020: Resoluciones Conjuntas SPensiones y CMF.

---
*Contacto y análisis cuantitativo: [surzua.github.io](https://surzua.github.io)*
