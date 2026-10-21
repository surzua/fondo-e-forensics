# 📱 Kit Viral de Publicación: Redes Sociales & LinkedIn
**Proyecto:** Auditoría Cuantitativa del Fondo E ("La Falacia del Fondo Seguro")  
**Autor:** Sebastián Urzúa Bórquez  
**Formato de Campaña:** Post Principal + Carrusel PDF (10 Láminas en 4:5) + Primer Comentario Técnico + Hilo para X/Twitter  
**Fecha:** Octubre 2026

---

## 1. Post Principal de Alto Impacto (LinkedIn)

> **Instrucciones para publicar:**  
> Copia y pega el siguiente texto en LinkedIn. Sube el archivo PDF generado a partir del guion de 10 láminas (ver sección 2) como documento adjunto. **NO incluyas enlaces externos en el cuerpo del post** (el algoritmo de LinkedIn reduce el alcance); colócalos en el primer comentario tal como se especifica en la sección 3.

```text
¿Te dijeron que la caída de -10,39% del Fondo E en 2026 fue "volatilidad normal de los bonos chilenos y un shock exógeno de la Fed" donde solo queda "esperar 5 años"?

La prensa financiera encendió las primeras alarmas al detectar un saldo negativo de US$ 899 millones en derivados. Pero nadie había abierto la caja negra para auditar el impacto real.

Audité los microdatos públicos de la Superintendencia de Pensiones y el Banco Central. La evidencia matemática desmiente el relato oficial:

👉 8 de cada 10 pesos perdidos NO fueron por bonos de Chile.
Fueron por apuestas apalancadas en derivados internacionales.

Aquí los 4 hallazgos forenses que la industria no te contó (desliza el carrusel 📊):

1️⃣ El 79,7% del desplome vino de Swaps de Tasas
De la caída nominal de -7,40%, -5,90 puntos porcentuales provienen exclusivamente de contratos de Swaps (IRS en EE.UU. y swaps locales). Los bonos físicos solo explican 0,7 puntos.

2️⃣ Transformaron un fondo de 5 años en uno de 17 años de duración
Aprovechando un vacío regulatorio, las AFP contrataron más de US$ 200.000 millones en swaps fuera de balance. Cuadruplicaron la sensibilidad del Fondo E a las tasas de Wall Street. Cuando el bono del Tesoro de EE.UU. subió de 4,18% a 5,29%, el fondo sufrió un shock propio de un hedge fund.

3️⃣ Anularon el amortiguador del dólar vendiendo futuros al 150%
En vez de dejar que el dólar mitigara las caídas externas, las AFP sobrecubrieron la cartera foránea vendiendo dólares a futuro por el 150% de sus activos. Cuando el dólar subió de $911 a $970, perdieron otros -0,80 pp.

4️⃣ Para quien jubila hoy, el daño es IRREVERSIBLE
Recomendar "mirar a 5 años" a un cotizante de 64 años es una falacia. Si jubilas hoy, liquidas tus cuotas en el fondo del pozo. Según las tablas actuariales oficiales RV-2020:
• Un saldo de $100 MM perdió más de $10,3 MM en poder adquisitivo.
• La pensión vitalicia se recorta en -$69.000 CLP al mes para siempre (-10,4%).
• En nuestra simulación de Monte Carlo (10.000 trayectorias), la mediana para reponer ese capital exige 21 MESES DE TRABAJO FORZADO EXTRA cotizando el 10% de tu sueldo.

La manada completa (Modelo, Capital, Cuprum, Habitat, Provida, PlanVital y Uno) replicó la misma apuesta (correlación diaria > 0,98). Y cuando la Superintendencia fijó un tope de 2% de pérdida en estrés para el 5 de noviembre, salieron todas juntas a vender en bloque.

Desliza el carrusel completo para ver los números, los gráficos de atribución factorial y la matriz por AFP ➡️

En el primer comentario les dejo el link al artículo completo en mi blog y a la calculadora interactiva en Streamlit donde puedes estimar tu recorte exacto de pensión.

¿Crees que los fondos conservadores deberían tener un límite legal de duración? Los leo en comentarios.

---
#Pensiones #AFP #FondoE #FinanzasChile #Inversiones #DataScience #Actuarial #EconomíaChilena
```

---

## 2. Guion del Carrusel (10 Láminas / Slides para PDF en Formato 4:5)

> **Especificaciones de Diseño:**  
> Formato vertical **1080 x 1350 px (relación de aspecto 4:5)**.  
> Fondo oscuro institucional (`#0D1117`), acentos en Rojo Carmesí (`#D90429`) y texto blanco (`#F8FAFC`).  
> Los gráficos de apoyo corresponden a los archivos `.png` en 300 DPI ya generados en [`data/processed/charts/`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/data/processed/charts).

---

### 📄 Lámina 1: Portada (Hook Visual)
* **Categoría Superior:** `AUDITORÍA FORENSE DE PENSIONES`
* **Título Principal:** **LA FALACIA DEL FONDO SEGURO**
* **Subtítulo:** ¿Por qué el Fondo E de las AFP se derrumbó un -10,39% en 2026?
* **Elemento Visual Central:** Insignia de advertencia + KPI destacado: **`-10,39% Real a Septiembre 2026`**.
* **Texto al Pie:** *"Desliza para ver la evidencia empírica en los microdatos oficiales de la Superintendencia de Pensiones y Banco Central."*

---

### 📄 Lámina 2: El Relato Oficial vs. La Realidad
* **Título:** **Dicen A, la Data Dice B**
* **Columna Izquierda (La Narrativa Oficial):**
  * *"Fue el alza de tasas locales y un shock exógeno de la Fed."*
  * *"Las inversiones previsionales deben evaluarse a 3 o 5 años."*
  * *"El Fondo E es 86% bonos chilenos; es volatilidad normal."*
* **Columna Derecha (La Evidencia en los Microdatos):**
  * ❌ Solo el 9,5% de la pérdida vino de bonos físicos chilenos.
  * ⚠️ El 79,7% vino de swaps de tasas offshore (con duración de 17 años).
  * 🛑 Un afiliado a 6 meses de jubilar **NO TIENE 5 AÑOS**: el recorte pensional es permanente.
* **Pie de Lámina:** *Desliza para ver la descomposición matemática ➡️*

---

### 📄 Lámina 3: The Underwater Chart (Riesgo Extremo)
* **Título:** **¿Fondo Conservador? Perforó su VaR 99%**
* **Imagen / Gráfico:** Incrustar recorte del gráfico [`producto1_underwater_var_4x5.png`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/data/processed/charts/producto1_underwater_var_4x5.png).
* **Puntos Clave:**
  * **Inversión Extrema de Roles:** En 2026, el Fondo E cayó **-10,39%**, mientras el Fondo A (Renta Variable pura) subió **+8,61%**.
  * **Pérdida Real:** Un saldo inicial de \$100 MM terminó en **\$89,6 MM**, evaporando \$10,3 MM en poder de compra.
  * **Ruptura Estadística:** Perforó de forma continua las bandas de Value at Risk al 99%, revelando un riesgo de cola ajeno a un fondo de retiro.

---

### 📄 Lámina 4: ¿Dónde se Fue el Dinero? (Atribución Factorial)
* **Título:** **8 de Cada 10 Pesos se Perdieron en Swaps**
* **Imagen / Gráfico:** Incrustar recorte del gráfico [`producto2_waterfall_atribucion_4x5.png`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/data/processed/charts/producto2_waterfall_atribucion_4x5.png).
* **Desglose de la Caída Nominal (-7,40%):**
  * 🔴 **Swaps de Tasas en EE.UU.:** `-4,50 pp` (60,8% de la pérdida)
  * 🔴 **Swaps de Tasas Locales:** `-1,40 pp` (18,9% de la pérdida)
  * 🟠 **Forwards de Tipo de Cambio:** `-0,80 pp` (10,8% de la pérdida)
  * 🔵 **Bonos Físicos de Renta Fija:** `-0,70 pp` (Solo el 9,5%)
* **Conclusión:** *El colapso no fue por bonos locales: fue por derivados internacionales.*

---

### 📄 Lámina 5: La Trampa de la Duración Sintética
* **Título:** **De 5 Años a 17 Años de Duración**
* **Imagen / Gráfico:** Incrustar recorte del gráfico [`producto3_termometro_duracion_swaps_4x5.png`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/data/processed/charts/producto3_termometro_duracion_swaps_4x5.png).
* **Puntos Clave:**
  * La duración histórica del Fondo E era de **~5,0 años**.
  * Las AFP estiraron los bonos físicos a **10,2 años** y le sumaron **6,8 años sintéticos en swaps**, alcanzando **17,0 años de duración total**.
  * Pasaron de US\$ 5.300M a más de **US\$ 206.900 millones** en swaps a fines de 2025.
  * Cuando la tasa a 10 años de EE.UU. (US10Y) subió de 4,18% a 5,29% (+111 bps), el fondo sufrió un shock propio de un bono a 30 años.

---

### 📄 Lámina 6: El Disparo en el Pie Cambiario
* **Título:** **Short USD al 150%: Anularon el Amortiguador**
* **Esquema Didáctico:**
  * **Cómo funciona normalmente:** Si los mercados externos caen, el dólar sube en Chile y la ganancia por tipo de cambio amortigua el golpe.
  * **Qué hicieron las AFP:** Vendieron futuros de dólares (*Forwards Short*) por el **150% del valor de sus activos externos**. Quedaron cortas netas en dólares.
  * **El Desenlace:** El dólar escaló de **\$911 a \$970 CLP** (+6,5%). En lugar de compensar, la posición en derivados restó **-0,80 pp adicionales**.

---

### 📄 Lámina 7: Efecto Manada Inter-AFP
* **Título:** **La Manada: Todas Hicieron lo Mismo**
* **Imagen / Gráfico:** Incrustar recorte del gráfico [`producto4_heatmap_herding_afp_4x5.png`](file:///Users/sebastianfelipeurzuaborquez/Proyectos/fondo-e-forensics/data/processed/charts/producto4_heatmap_herding_afp_4x5.png).
* **Ranking de Caídas Reales 2026:**
  * 🥇 AFP Modelo: `-10,90%`
  * 🥈 AFP Capital: `-10,80%`
  * 🥉 AFP Cuprum: `-10,50%`
  * AFP Habitat: `-10,35%` | AFP Provida: `-10,30%` | AFP PlanVital: `-10,15%` | AFP Uno: `-9,90%`
* **Correlación Cruzada Diaria:** Superior a **0,98** entre todas las AFP. El incentivo perverso de la rentabilidad mínima llevó a toda la industria a tomar la misma apuesta de cola.

---

### 📄 Lámina 8: El Golpe Actuarial a tu Pensión
* **Título:** **El Daño Actuarial es Irreversible**
* **Fórmula Previsional:**
  $$\text{Pensión} = \frac{\text{Saldo}}{12 \times \text{CNU}}$$
* **Tabla de Impacto Real (Tabla de Mortalidad Oficial RV-2020 / Tasa 3,2%):**
  * **Hombre 65 años (\$100 MM de saldo):**  
    Pierde **\$10,4 MM** de patrimonio $\rightarrow$ Recorte vitalicio de **-\$69.000 CLP/mes** de por vida (-10,4%).
  * **Mujer 60 años (\$80 MM de saldo):**  
    Pierde **\$8,3 MM** de patrimonio $\rightarrow$ Recorte vitalicio de **-\$41.000 CLP/mes** de por vida (-10,4%).
* **Conclusión:** Si te jubilas hoy, la pérdida de pensión no se recupera nunca.

---

### 📄 Lámina 9: Simulación de Monte Carlo
* **Título:** **¿Cuántos Años Extra Tienes que Trabajar?**
* **Metodología:** 10.000 trayectorias estocásticas mensuales con cotización legal del 10% del sueldo (\$1,5 MM imponible) y retorno futuro del 3,5% real.
* **Tiempos de Recuperación Patrimonial:**
  * 🟢 **Escenario Optimista (P10):** 11 meses de trabajo extra.
  * 🟡 **Mediana del Sistema (P50):** **21 MESES (Casi 2 años de trabajo forzado)** solo para empatar el saldo previo al shock.
  * 🔴 **Escenario Adverso (P90):** 38 meses (más de 3 años).
  * ⚠️ **Probabilidad de no recuperar en 1 año:** **78,4%**.

---

### 📄 Lámina 10: Conclusiones y Llamado a la Acción
* **Título:** **El Riesgo no Desaparece por Ley**
* **3 Reformas Urgentes:**
  1. **Techo Legal de Duración:** Limitar la duración combinada (física + swaps) a máximo 5 años en Fondos D y E.
  2. **Prohibición de Cortos en Moneda:** Forwards solo permitidos para cobertura simétrica 1:1 (nunca sobrecobertura al 150%).
  3. **Fin a la Manada:** Reformar el mecanismo de encaje para castigar la toma coordinada de riesgos de cola.
* **Llamado a la Acción (CTA):**
  * 🔗 Revisa el artículo completo y calcula tu recorte en la app interactiva (enlace en el primer comentario).
  * 💬 *¿Conocías el uso de swaps en tu fondo de pensión? Comparte este post para que más afiliados conozcan la data.*

---

## 3. Primer Comentario Técnico (First Comment)

```text
Gracias a todos por el interés y el debate técnico. 

Para mantener la rigurosidad y transparencia absoluta de la auditoría, aquí están los enlaces públicos y el sustento metodológico:

📊 1. Calculadora Actuarial Interactiva (Web App en Streamlit):
Prueba con tu propio saldo, AFP, edad y sueldo imponible para estimar tu recorte mensual y el tiempo de recuperación con Monte Carlo:
👉 [https://surzua.github.io/fondo-e-forensics] (o tu enlace de despliegue local/Cloud)

📖 2. Artículo Completo de Investigación (con fórmulas de Taylor, Woolhouse y tablas RV-2020):
👉 https://surzua.github.io/blog/la-falacia-del-fondo-seguro

💡 3. Guía Didáctica de Finanzas (Para entender Bonos, Swaps y Duración desde cero con metáforas cotidianas):
👉 https://surzua.github.io/blog/guia-finanzas-fondo-e

💻 4. Código Fuente Abierto y Microdatos en GitHub:
Todo el pipeline de datos (scrapers de SPensiones, series macro del Banco Central, modelos de atribución y tests en pytest) es 100% reproducible y auditable:
👉 https://github.com/surzua/fondo-e-forensics

📌 Aclaración técnica para gestores y analistas:
• Los valores cuota y carteras fueron deflactados diariamente con la UF oficial del Banco Central.
• La duración total de 17 años corresponde a la suma de la duración modificada de los bonos físicos de la cartera nacional (~10,2 años) más la duración sintética generada por la posición neta en contratos IRS en USD (~6,8 años), calculada según la metodología estándar de la BIS y el Banco Central.
• El Capital Necesario Unitario (CNU) utiliza las tablas oficiales RV-2020 y una tasa técnica de descuento del 3,2% real anual (Compendio de Normas de la Superintendencia de Pensiones).

¡Cualquier duda técnica o retroalimentación sobre los modelos es bienvenida!
```

---

## 4. Hilo de Impacto para X (Twitter) [7 Tweets]

```text
1/7 🧵 ¿Te dijeron que el desplome del Fondo E de las AFP en 2026 (-10,39% real) fue "volatilidad normal de bonos locales y shock inevitable de la Fed" donde solo queda "esperar 5 años"?

La prensa alertó un saldo de -US$ 899M en derivados. Audité los microdatos públicos: la evidencia desmiente el relato oficial. Abrimos hilo 👇

2/7 💣 1. El 80% de la pérdida NO fue por bonos locales:
De la caída nominal de -7,40%, -5,90 puntos porcentuales provienen exclusivamente de apuestas en DERIVADOS (Swaps de tasas de interés en EE.UU. y locales). Los bonos físicos solo explican 0,7 puntos.

3/7 📈 2. De 5 años a 17 años de duración:
Las AFP llevaron el nocional en swaps extranjeros de US$ 5.300M a más de US$ 200.000M a fines de 2025. 
Al sumar bonos físicos (10,2 años) + swaps (6,8 años), la duración del Fondo E llegó a 17 años. El perfil de un fondo especulativo a costa de los jubilados.

4/7 💵 3. Anularon el escudo del dólar:
En vez de dejar que el dólar amortiguara las pérdidas externas, vendieron futuros de dólares por el 150% de sus activos foráneos (posición corta). Cuando el dólar subió de $911 a $970, perdieron otros -0,80 pp.

5/7 👥 4. La manada (Herding):
Todas las AFP hicieron exactamente la misma apuesta: correlación diaria superior a 0,98.
Ranking de caídas: Modelo (-10,9%), Capital (-10,8%), Cuprum (-10,5%), Habitat (-10,3%), Provida (-10,3%), PlanVital (-10,1%), Uno (-9,9%).

6/7 👴 5. Para quien jubila hoy, el daño es IRREVERSIBLE:
Decirle "mira a 5 años" a un cotizante a meses del retiro es una trampa. 
Con tablas RV-2020, un saldo de $100 MM pierde $10,3 MM en poder adquisitivo y sufre un recorte vitalicio de -$69.000/mes para siempre.

7/7 🎯 Simulamos 10.000 trayectorias de Monte Carlo: reponer ese capital exige 21 MESES DE TRABAJO EXTRA cotizando el 10% del sueldo.

Calcula tu recorte en la app interactiva y lee la auditoría completa aquí:
👉 https://surzua.github.io
RT si crees que la duración del Fondo E debe limitarse por ley.
```
