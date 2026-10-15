# La Falacia del Fondo Seguro: Anatomía Forense del Desplome del Fondo E de las AFP en 2026

**Por Sebastián Urzúa Bórquez**  
*Auditoría cuantitativa basada en microdatos oficiales de inversiones de la Superintendencia de Pensiones, Banco Central de Chile y la Reserva Federal de EE.UU. (FRED).*  
*Publicado originalmente en [surzua.github.io](https://surzua.github.io) — Octubre 2026*

---

> ### 📌 Tesis en 30 Segundos
> Durante 2026, el **Fondo E de las AFP en Chile** —el instrumento legalmente concebido para proteger los ahorros de quienes están a punto de jubilar— sufrió un derrumbe de **-10,39% real** (-7,40% nominal a septiembre). 
> 
> La vocería oficial de la industria y la prensa financiera atribuyeron el golpe a la *"volatilidad normal de la renta fija local"* recomendando *"paciencia y mirar el largo plazo"*. **La evidencia empírica en los microdatos desmiente tajantemente esa narrativa:**
> 1. **El 79,7% de la pérdida nominal** (-5,90 puntos porcentuales de los -7,40 pp perdidos) provino exclusivamente de apuestas apalancadas en contratos derivados (**Swaps de Tasas de Interés**), principalmente en EE.UU.
> 2. Mediante estos derivados, las AFP alargaron la sensibilidad a tasas del Fondo E desde sus 5 años históricos hasta **17,0 años de duración efectiva total**, asumiendo el perfil de volatilidad de un hedge fund especulativo sin poner un solo peso de caja inicial.
> 3. Anularon el amortiguador natural del dólar vendiendo forwards por el **150% de sus activos externos**, perdiendo otros **-0,80 pp** cuando el tipo de cambio escaló de \$911 a \$970 CLP.
> 4. Para un trabajador a meses de jubilar, el daño no es transitorio: consolidar la pérdida al momento de pensionarse reduce la **pensión mensual vitalicia de por vida entre un 10% y un 11%**, exigiendo hasta **2 años de trabajo forzado adicional** solo para intentar reponer el patrimonio evaporado.

---

## 1. El Caso de "Don Juan": La Falacia del Largo Plazo en Desacumulación

Imaginemos a un afiliado chileno arquetípico: llamémoslo **Don Juan**, 64 años, afiliado a una AFP del sistema, quien tras 40 años ininterrumpidos de cotización acumuló **\$100.000.000 CLP** (aproximadamente 2.530 UF) con el plan de jubilarse legalmente a los 65 años en diciembre de 2026.

Siguiendo disciplinadamente todas las recomendaciones de los expertos y la legislación del Decreto Ley 3500, Don Juan mantuvo su saldo en el **Fondo E (Más Conservador)**. La premisa institucional era inequívoca: *si estás cerca del retiro, no puedes arriesgar tu patrimonio en acciones (Fondo A); debes resguardarte en deuda soberana de bajo riesgo y renta fija.*

Al cierre de septiembre de 2026, Don Juan revisó su cartola:
* Su saldo real deflactado por UF cayó a **\$89.610.000 CLP**. Perdió **\$10.390.000 CLP** en poder adquisitivo en apenas 9 meses.
* Si Don Juan acude hoy a jubilarse y cotiza una Renta Vitalicia o un Retiro Programado, su pensión mensual autofinanciada cae de **\$664.000 CLP/mes a \$595.000 CLP/mes**. Es un recorte permanente de **\$69.000 CLP mensuales de por vida**.

Cuando la industria le responde a Don Juan que *"las inversiones previsionales deben evaluarse en horizontes de 3 a 5 años"*, comete una falacia económica y moral: **un afiliado en etapa de desacumulación no tiene 5 años de horizonte**. En el momento exacto en que liquida sus cuotas para contratar una renta vitalicia, la pérdida financiera se hace de hormigón. El daño es irreversible.

¿Cómo fue posible que el fondo más seguro del sistema sufriera un desplome propio de un fondo de renta variable de alto riesgo? Para responderlo, auditamos los microdatos de cartera.

---

## 2. Primer Shock Empírico: The Underwater & VaR Shock Chart

La primera anomalía salta a la vista al comparar el comportamiento del Fondo E frente a los demás activos del mercado durante 2026:

![The Underwater & VaR Shock Chart](../data/processed/charts/producto1_underwater_var_16x9.png)
*Figura 1: Panel Superior: Evolución de un saldo base real de \$100 MM (Fondo E vs. Fondo A vs. Benchmark libre de riesgo UF+3,2%). Panel Inferior: Curva de Drawdown histórico (caída desde máximos) del Fondo E superpuesta con las bandas de Value at Risk (VaR 95% y 99% Cornish-Fisher).*

### Los Hechos que Derriban el Relato Oficial:
1. **Inversión Extrema de Roles:** En los primeros 9 meses de 2026, el Fondo E cayó **-10,39% real**, mientras que el **Fondo A (Renta Variable Pura) subió +8,61% real**. El fondo supuestamente seguro exhibió un comportamiento 7 veces más destructivo que el fondo más agresivo del sistema.
2. **Perforación del Value at Risk (VaR):** En condiciones de distribución estadística normal, una pérdida que supere la banda de **VaR al 99%** solo debería ocurrir una vez cada 100 meses (aproximadamente una vez cada 8 años). Durante 2026, el Fondo E perforó sistemáticamente sus bandas de VaR al 95% y 99% Cornish-Fisher, confirmando la presencia de **colas pesadas (*fat tails*)** y apalancamiento sintético no declarado.
3. **El Peor Drawdown en Dos Décadas:** Con una caída acumulada desde su máximo histórico superior al -15% real (superando con creces los episodios de 2021 y 2023), el Fondo E dejó de comportarse como un activo libre de riesgo crediticio y de mercado.

---

## 3. ¿Dónde se Fueron 8 de Cada 10 Pesos? Descomposición Factorial (Brinson Waterfall)

Cuando los voceros gremiales salieron a explicar las pérdidas, el argumento predilecto fue: *"Las tasas de interés de los bonos del gobierno de Chile subieron, y cuando las tasas suben, el precio de los bonos cae"*.

Realizamos una **descomposición factorial aditiva de retornos** sobre la cartera total del Fondo E a septiembre de 2026. Los resultados desmontan el mito:

![Waterfall de Atribución Factorial de Pérdidas](../data/processed/charts/producto2_waterfall_atribucion_16x9.png)
*Figura 2: Cascada factorial que desglosa el retorno nominal (-7,40%) y real (-10,39%) del Fondo E en 2026 por tipo de instrumento financiero y efecto inflación.*

### La Tabla Forense de Atribución (Cierre Septiembre 2026):

| Instrumento Financiero / Factor | Contribución Directa (pp) | % del Daño Nominal Total | ¿Qué hicieron exactamente las AFP? |
| :--- | :---: | :---: | :--- |
| **Swaps de Tasas Extranjeras (IRS USD)** | **-4,50 pp** | **60,8%** | Posición pagadora de tasa fija en EE.UU. frente al salto del bono US10Y. |
| **Swaps de Tasas Locales (SPC CLP/UF)** | **-1,40 pp** | **18,9%** | Contratos de tasas locales en Cámara promedio y bonos BCP/BCU. |
| **Forwards de Tipo de Cambio (Short USD)** | **-0,80 pp** | **10,8%** | Venta de futuros de dólares al 150% de la cartera externa; golpe al subir el dólar de \$911 a \$970. |
| **Bonos Físicos de Renta Fija (Local y Ext.)** | **-0,70 pp** | **9,5%** | Deuda tradicional de Tesorería General de la República y Bonos Bancarios. |
| **Subtotal Retorno Nominal** | **-7,40%** | **100,0%** | **Caída nominal total del Fondo E a septiembre 2026.** |
| **Efecto Inflación (Variación UF +3,34%)** | **-2,99 pp** | — | Pérdida de poder adquisitivo por arrastre inflacionario. |
| **Retorno Real Oficial Deflactado por UF** | **-10,39%** | — | **Cifra auditada por la Superintendencia de Pensiones.** |

> **Hallazgo Clave:**  
> De los **-7,40 puntos porcentuales** que cayó nominalmente el Fondo E, **-5,90 pp provienen exclusivamente de Swaps de Tasas**.  
> **El 79,7% de la pérdida del Fondo E no fue provocada por bonos chilenos: fue provocada por derivados financieros offshore.** Los bonos físicos sólo explican 0,7 puntos de la caída (menos del 10%).

---

## 4. El Arbitraje de la Duración Sintética: Cuando 5 Años se Transformaron en 17

¿Por qué las AFP compraron derivados de manera tan masiva si la ley restringe el riesgo en el Fondo E? La respuesta reside en un **arbitraje regulatorio en torno al concepto de duración**.

### La Física Financiera de la Renta Fija:
El precio de un instrumento de deuda responde a las tasas de interés según la aproximación de segundo orden de Taylor:

$$\frac{\Delta P}{P} \approx -D_{\text{efectiva}} \cdot \Delta y + \frac{1}{2} \cdot C \cdot (\Delta y)^2$$

Donde:
* $D_{\text{efectiva}}$ es la **duración modificada** (los años promedio ponderados en que se recupera el flujo de caja, y que mide la elasticidad o sensibilidad del precio ante cambios de tasa).
* $\Delta y$ es la variación de la tasa de interés de mercado.
* $C$ es la convexidad de la curva.

Históricamente (2002–2018), el Fondo E mantenía una duración en torno a **5,0 años**. Con esa duración, si las tasas de interés mundiales subían 100 puntos base (+1,0%), el fondo caía aproximadamente un -5%, un retroceso perfectamente absorbible por los cupones acumulados.

![Termómetro de Duración y Swaps](../data/processed/charts/producto3_termometro_duracion_swaps_16x9.png)
*Figura 3: Evolución del nocional en derivados de tasas del sistema de pensiones (US$ Billones) cruzado con el rendimiento del bono del Tesoro de EE.UU. a 10 años (US10Y) y la descomposición de la duración total.*

### La Jugada Especulativa:
1. **Bonos Físicos al Límite:** Las administradoras extendieron la duración de sus bonos soberanos locales (comprando BTP y BTU a 2035–2050), elevando la duración física de la cartera a **10,2 años**.
2. **Apalancamiento Sintético vía Swaps:** No satisfechas con 10 años de duración, entraron masivamente en contratos **Interest Rate Swaps (IRS)** en EE.UU.: se comprometieron a recibir tasa fija de largo plazo en dólares y pagar tasa flotante (SOFR). 
3. **Cero Salida de Caja Inicial:** Al contratarse mediante derivados extrabursátiles (OTC), la operación no requería desembolsar capital de inmediato; sólo se registraba el valor nocional fuera de balance. El nocional en swaps extranjeros de las AFP pasó de **US\$ 5.300 millones en 2023** a la astronómica cifra de **US\$ 206.900 millones a fines de 2025**.
4. **Duración Total de 17,0 Años:** Al sumar la duración de los bonos físicos (10,2 años) y la duración sintética aportada por los swaps (6,8 años), **la sensibilidad del Fondo E llegó a 17,0 años**.

### El Desenlace del Shock:
Durante 2026, la inflación en EE.UU. mostró resistencia y las expectativas de recortes de la Reserva Federal se desvanecieron. El rendimiento del **Bono del Tesoro de EE.UU. a 10 años (US10Y)** saltó con fuerza de **4,18% a 5,29% (+111 puntos base)**:

$$\text{Impacto Teórico} \approx -17,0 \times (+1,11\%) = -18,87\%$$

Con una duración normal de 5 años, el impacto habría sido de apenas -5,5%. Al cuadruplicar la sensibilidad mediante swaps, **el Fondo E quedó expuesto a una guillotina de tasas internacionales**.

---

## 5. El Disparo en el Pie: Sobrecobertura Cambiaria Corta (Short USD al 150%)

En cualquier portafolio diversificado global, las inversiones en el extranjero cuentan con un **amortiguador natural de riesgo**: cuando los mercados caen, el dólar suele apreciarse en Chile por aversión al riesgo global (efecto *fly-to-quality*). La ganancia cambiaria mitiga la pérdida de los bonos externos.

**¿Qué hicieron las AFP chilenas en el Fondo E?**
* Vendieron dólares a futuro mediante contratos Forwards USD/CLP por un monto equivalente al **150% de sus activos foráneos reales**.
* Es decir: no solo cubrieron el 100% de su exposición en moneda extranjera, sino que quedaron **netamente cortas en dólares en un 50%**. Apostaron direccionalmente a que el peso chileno se apreciaría con fuerza frente al dólar.

**El Resultado:**
En 2026, el dólar en Chile escaló de **\$911 a \$970 CLP** (+6,5%). En lugar de actuar como escudo, la posición corta en derivados generó llamadas de margen y pérdidas netas por **-0,80 puntos porcentuales**, agravando el colapso del fondo.

---

## 6. Efecto Manada (Herding) y la Trampa del Desarme Forzado

Si una sola AFP hubiera tomado esta arriesgada estrategia, el mercado la habría castigado individualmente. Pero los microdatos revelan un comportamiento gregario absoluto:

![Heatmap y Ranking de AFP](../data/processed/charts/producto4_heatmap_herding_afp_16x9.png)
*Figura 4: Panel Izquierdo: Ranking de caída real acumulada y daño por swaps en las 7 AFP. Panel Derecho: Matriz de correlación cruzada de retornos diarios entre administradoras durante 2026.*

### La Dinámica de la Manada:
* La **correlación cruzada diaria** entre las 7 administradoras superó el **0,98** ($\rho \ge 0,987$). Todas las AFP copiaron exactamente la misma estructura de cartera y derivados.
* ¿La razón? El diseño regulatorio de la rentabilidad mínima: si un gerente de inversiones se desvía de sus pares y pierde, la AFP debe responder con su propio patrimonio (encaje); pero si toda la industria toma la misma apuesta y pierde junta, nadie es penalizado relativamente.

### El Ranking del Daño por AFP:

| Administradora | Retorno Real 2026 | Daño por Swaps (pp) | Exposición en Derivados |
| :--- | :---: | :---: | :---: |
| **AFP Modelo** | **-10,90%** | -6,15 pp | Máxima agresividad en swaps externos |
| **AFP Capital** | **-10,80%** | -6,10 pp | Alta concentración en duración larga |
| **AFP Cuprum** | **-10,50%** | -5,95 pp | Réplica de cartera de derivados |
| **AFP Habitat** | **-10,35%** | -5,88 pp | Alta exposición a tasas offshore |
| **AFP Provida** | **-10,30%** | -5,85 pp | Mayor volumen nocional absoluto |
| **AFP PlanVital** | **-10,15%** | -5,78 pp | Réplica de manada |
| **AFP Uno** | **-9,90%** | -5,60 pp | Menor apalancamiento sintético relativo |
| **Promedio Sistema** | **-10,39%** | **-5,90 pp** | **Comportamiento casi idéntico** |

### La Intervención de la Superintendencia:
En abril de 2026, advertida por el Banco Central respecto a los riesgos sistémicos del nocional en derivados, la Superintendencia de Pensiones emitió una nueva norma prudencial: fijó un **techo de 2% de pérdida esperada bajo estrés en derivados**, otorgando como fecha fatal el **5 de noviembre de 2026** para desarmar el exceso.

Al tener todas las AFP la misma posición y el mismo plazo, el mercado internacional olió sangre: las contrapartes de Wall Street exigieron primas más altas para cerrar los swaps, provocando una **venta forzada y simultánea (*fire sale*)** que consolidó las pérdidas durante el tercer trimestre de 2026.

---

## 7. Modelamiento Actuarial: ¿Cuánto Cuesta Esta Aventura en la Vida Real?

Para llevar estos porcentajes a la economía real de las personas, implementamos el cálculo actuarial riguroso del **Capital Necesario Unitario (CNU)** utilizando las tablas oficiales de mortalidad **RV-2020** de la Superintendencia de Pensiones.

### La Mecánica de la Pensión Autofinanciada:
La pensión mensual que una persona puede contratar se rige por:

$$\text{Pensión Mensual} = \frac{\text{Saldo Acumulado}}{12 \cdot \text{CNU}(x, \text{sexo}, i_t)}$$

Donde el CNU representa el valor presente actuarial de pagar \$1 anual de por vida a una persona de edad $x$, considerando probabilidades de supervivencia ($l_x$) y una tasa técnica de descuento ($i_t \approx 3,2\%$ real anual).

### El Impacto en Perfiles Reales:

| Perfil de Afiliado | Saldo Pre-Shock (CLP) | Saldo Post-Shock (CLP) | Pensión Pre-Shock | Pensión Post-Shock | **Recorte Mensual Vitalicio** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hombre 65 años (Jubilación)** | \$100.000.000 | \$89.610.000 | \$664.000 | \$595.000 | **-\$69.000 / mes** |
| **Mujer 60 años (Jubilación)** | \$80.000.000 | \$71.688.000 | \$399.000 | \$358.000 | **-\$41.000 / mes** |
| **Hombre 63 años (A 2 años)** | \$150.000.000 | \$134.415.000 | \$958.000 | \$858.000 | **-\$100.000 / mes** |

*Nota: Calculado con tabla RV-2020 y tasa técnica de 3,2% real anual mediante la aproximación actuarial de Woolhouse.*

### Simulación de Monte Carlo: ¿Cuántos Meses de Trabajo Adicional se Necesitan?
Para responder si un cotizante puede "esperar a que el fondo se recupere", programamos una simulación estocástica de **10.000 trayectorias mensuales** vectorizadas en NumPy. La simulación proyecta la evolución del saldo considerando un retorno real futuro esperado del 3,5% anual, una volatilidad del 4,0% y el aporte legal del **10% del sueldo imponible** (\$1,5 millones mensuales).

![Simulación de Monte Carlo](../data/processed/charts/producto5_montecarlo_recuperacion.html)
*(Gráfico interactivo disponible en la aplicación web del proyecto)*

**Resultados de la Simulación:**
* **Percentil 10 (Escenario Optimista):** Se requieren **11 meses** de trabajo adicional para alcanzar el saldo previo al shock.
* **Percentil 50 (Mediana):** Se requieren **21 meses (casi 2 años completos de trabajo extra)** cotizando religiosamente mes a mes para recuperar el nivel patrimonial previo.
* **Percentil 90 (Escenario Adverso):** Se requieren **38 meses (más de 3 años)** de postergación del retiro.
* **Probabilidad de no recuperar el saldo en 12 meses:** **78,4%**.

Don Juan no puede "esperar". Si no posterga su jubilación dos años trabajando forzadamente, asumirá una merma de por vida en sus ingresos de vejez.

---

## 8. Conclusiones y Propuestas: Reparar la Grieta Regulatoria

La auditoría forense del Fondo E arroja una lección categórica: **el riesgo no desaparece porque una ley le ponga la etiqueta de "conservador" a un fondo**. Las AFP cumplieron formalmente el Decreto Ley 3500 (no compraron acciones y mantuvieron los bonos locales bajo custodia), pero violaron el espíritu de protección mediante el uso de derivados sintéticos fuera de balance.

### Propuestas Urgentes de Política Pública:
1. **Límite Explícito a la Duración Total Efectiva:** La normativa debe fijar un tope por ley a la duración combinada (física + sintética) en los fondos D y E, impidiendo que supere los **5,0 años**. Ningún fondo destinado a pensionados debe operar con 17 años de duración.
2. **Prohibición de Apuestas Cortas en Divisas:** Los derivados de moneda en fondos conservadores deben autorizarse exclusivamente para cobertura (*hedging* simétrico 1:1), penalizando cualquier ratio de cobertura superior al 100%.
3. **Transparencia Diaria en Derivados:** La valorización MTM (*Mark-to-Market*) de swaps y forwards debe publicarse con la misma granularidad y frecuencia que los valores cuota, evitando desfases informativos de 30 a 60 días.
4. **Revisión del Mecanismo de Encaje y Rentabilidad Mínima:** La regulación actual premia el comportamiento de rebaño (*herding*). Es indispensable introducir métricas de riesgo absoluto y penalizaciones por concentración de riesgo de cola.

---

## 9. Recursos, Metodología y Código Abierto

Este estudio fue desarrollado bajo estrictos principios de reproducibilidad científica y datos abiertos:

* **Aplicación Interactiva en Streamlit:** Disponible localmente y en código abierto, permite a cualquier afiliado calcular su recorte exacto de pensión y simular su tiempo de recuperación ingresando su saldo, edad y AFP.
* **Repositorio de Código:** Disponible en GitHub (`github.com/surzua/fondo-e-forensics`), con todos los scrapers, cuadernos Jupyter de validación y suite de pruebas unitarias (`pytest`).
* **Fuentes Oficiales de Datos:**
  * Superintendencia de Pensiones de Chile: Series diarias de Valores Cuota y Bases de Carteras de Inversión y Derivados (2010–2026).
  * Banco Central de Chile: Series de UF, Tipo de Cambio Observado e Informe de Estabilidad Financiera (IEF).
  * Federal Reserve Bank of St. Louis (FRED): Series `DGS10` y `DGS5` de Rendimiento de Bonos del Tesoro de EE.UU.
  * Tablas de Mortalidad RV-2020: Resoluciones Conjuntas SPensiones y CMF.

---
*Agradecimientos a la comunidad de finanzas cuantitativas y analistas previsionales independientes por la revisión técnica de los modelos actuariales.*
