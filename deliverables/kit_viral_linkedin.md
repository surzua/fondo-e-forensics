# Kit de difusión: investigación de datos sobre el Fondo E

**Propósito:** presentar la investigación y la guía didáctica como un ejercicio de ciencia de datos reproducible. El tono es exploratorio y verificable; evita acusaciones, predicciones y consejos financieros personalizados.

**Fecha de referencia:** octubre de 2026; cifras con corte a septiembre de 2026, salvo que se actualice expresamente.

## 1. Post principal

Usar el texto de [post_linkedin_fondo_e.md](post_linkedin_fondo_e.md). Publicar la investigación, la guía y el repositorio en el primer comentario para mantener el cuerpo del post enfocado en la pregunta y el método.

## 2. Guion del carrusel — 8 láminas, formato 4:5

**Sistema visual:** fondo claro o oscuro de alto contraste, una idea por lámina, fuente legible y pie de página con la fecha de corte. Todo gráfico debe incluir fuente, período y una etiqueta que distinga “dato observado” de “resultado del modelo”.

### Lámina 1 — La pregunta

**Título:** ¿Cómo se investiga con datos una caída que está en la agenda pública?

**Bajada:** El Fondo E acumuló -10,39% real entre enero y septiembre de 2026. Este proyecto no entrega consejos financieros: documenta una forma reproducible de investigar la cifra.

**Pie:** Fuente del dato: Superintendencia de Pensiones. Corte: septiembre de 2026.

### Lámina 2 — Del titular al problema de datos

**Título:** Un titular no es una explicación

**Visual:** `Titular → pregunta → fuentes → validación → modelo → visualización → límites`

**Texto breve:** Antes de explicar un resultado, hay que verificar definiciones, períodos, cobertura y unidades. La pregunta guía: ¿qué componentes se pueden asociar a la variación observada bajo supuestos explícitos?

### Lámina 3 — Las fuentes y su trazabilidad

**Título:** Una investigación empieza por poder volver atrás

**Visual:** diagrama de orígenes públicos hacia el mart analítico.

**Texto breve:** Valores cuota y carteras (SP); UF y variables macro (Banco Central); series de mercado declaradas en el código. Cada transformación queda versionada y testeada.

### Lámina 4 — Qué validamos antes de modelar

**Título:** Calidad de datos antes de conclusiones

**Visual:** cuatro checks: fechas, duplicados, tipos/unidades y cobertura.

**Texto breve:** Una serie mal alineada o una cifra nominal comparada con una real puede producir una historia convincente y equivocada. Los contratos de datos y tests son parte del resultado.

### Lámina 5 — Cómo leer un gráfico de riesgo

**Título:** Un gráfico no habla por sí solo

**Visual:** usar `producto1_underwater_var_4x5.png` junto a una leyenda editorial.

**Leyenda sugerida:** “La visualización describe rendimientos y drawdowns bajo una definición concreta. Las bandas VaR son estimaciones de un modelo: no prueban por sí mismas una causa ni predicen el futuro.”

### Lámina 6 — Decomponer no es culpar

**Título:** La atribución propone una explicación cuantitativa

**Visual:** usar `producto2_waterfall_atribucion_4x5.png` y marcar “estimación del modelo”.

**Texto breve:** La atribución ayuda a preguntar por exposición a tasas, moneda, renta fija y derivados. Su lectura correcta depende de la clasificación de instrumentos, los precios usados y los supuestos del modelo.

### Lámina 7 — Dos materiales, dos públicos

**Título:** Investigación para replicar; guía para entender

| Investigación reproducible | Guía didáctica |
| --- | --- |
| Fuentes, pipeline, tests y limitaciones | Conceptos y cómo leer resultados |
| Para cuestionar y reproducir | Para entrar al tema sin jerga |

**CTA:** Ambos enlaces en el primer comentario.

### Lámina 8 — La conversación que queremos abrir

**Título:** Mejor pregunta, mejor debate

**Texto central:** ¿Qué hallazgo se sostiene al cambiar de período, fuente o supuesto? ¿Qué dato público falta para evaluar mejor el caso?

**CTA:** Revisa el código, la metodología y la guía. Comparte una fuente, una prueba de robustez o una mejora al análisis.

## 3. Primer comentario

```text
Enlaces del proyecto:

📘 Investigación reproducible: <URL_DE_LA_INVESTIGACION>
🧭 Guía didáctica: <URL_DE_LA_GUIA>
💻 Repositorio, fuentes y tests: <URL_DEL_REPOSITORIO>

La cifra de -10,39% corresponde a la rentabilidad real acumulada del Fondo E del sistema entre enero y septiembre de 2026. Los resultados de atribución, riesgo y escenarios dependen de los supuestos documentados y deben leerse como estimaciones reproducibles, no como una auditoría oficial, una conclusión jurídica o asesoría financiera.
```

## 4. Hilo para X / Threads

```text
1/5 El Fondo E acumuló -10,39% real a septiembre de 2026. En vez de tratar el dato como un veredicto, lo usé como caso de estudio: ¿cómo se investiga una caída pública con datos, trazabilidad y límites claros?

2/5 El repositorio parte por lo básico: fuentes públicas, fechas, unidades, controles de calidad y transformaciones reproducibles. Sin eso, incluso un gráfico correcto puede contar una historia equivocada.

3/5 Luego vienen los modelos: rendimiento real, drawdown, VaR, atribución y escenarios. Son herramientas para explorar hipótesis; sus resultados dependen de definiciones y supuestos que deben poder revisarse.

4/5 También publiqué una guía didáctica para entender valor cuota, inflación, bonos, duración, derivados y riesgo sin exigir formación financiera. El objetivo es mejorar la lectura de evidencia, no dar consejos de inversión.

5/5 Investigación, guía y código: <URLS>. ¿Qué prueba de robustez, fuente o visualización agregarías para hacer más claro y discutible este análisis?
```

## 5. Control editorial previo

- Confirmar la cifra y fecha de corte en la fuente oficial antes de publicar.
- No usar “culpa”, “apuesta”, “fraude”, “ilegal” o equivalentes como conclusiones de los modelos.
- Nombrar cada resultado como dato observado, estimación o escenario, según corresponda.
- No prometer que una calculadora estime una pensión “exacta”.
- Incluir el enlace a metodología y limitar respuestas personalizadas sobre decisiones previsionales.
