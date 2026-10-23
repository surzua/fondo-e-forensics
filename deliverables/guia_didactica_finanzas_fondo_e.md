# Guía didáctica: cómo leer una investigación de datos sobre el Fondo E

**Por Sebastián Urzúa Bórquez**

*Complemento pedagógico de [Investigar la caída del Fondo E con datos públicos](articulo_investigacion_fondo_e.md) — octubre de 2026*

> **Propósito.** No necesitas convertirte en especialista financiero para leer una investigación de datos. Esta guía entrega el vocabulario mínimo para entender las preguntas, los gráficos, los supuestos y las limitaciones del caso Fondo E. Su objetivo no es aconsejarte qué hacer con tus ahorros.

## 1. Antes de empezar: tres etiquetas que cambian la lectura

Una investigación responsable distingue entre:

| Etiqueta | Qué significa | Ejemplo |
| --- | --- | --- |
| **Dato observado** | Una cifra publicada para una fecha y definición determinada. | La rentabilidad real acumulada del Fondo E a septiembre de 2026. |
| **Estimación** | Un cálculo que depende de datos y decisiones metodológicas. | La contribución estimada de un grupo de instrumentos al retorno. |
| **Escenario** | Una simulación de “qué podría pasar si…”. | Una trayectoria de saldo bajo supuestos de retorno y aporte. |

Confundirlas es una fuente frecuente de malos debates. Un escenario no es una promesa; una estimación no es una sentencia; un dato observado no explica por sí solo una causa.

## 2. El caso de estudio en una frase

El Fondo E es el multifondo más conservador del sistema chileno. Su caída real acumulada de -10,39% entre enero y septiembre de 2026 es el punto de partida del proyecto. El interés didáctico no está en memorizar la cifra, sino en preguntar: **¿cómo llegamos a una explicación que otra persona pueda revisar?**

## 3. Valor cuota, retorno nominal y retorno real

Tu saldo previsional se expresa en cuotas. Una cuota representa una parte del fondo común y su valor cambia con los activos que posee el fondo.

- **Retorno nominal:** cambio en pesos corrientes.
- **Retorno real:** cambio después de considerar inflación; en Chile suele expresarse deflactando por la UF.

La comparación correcta exige mismo período y misma unidad. No corresponde contrastar una cifra mensual nominal con una cifra acumulada real y extraer una conclusión.

> Pregunta útil al leer un gráfico: ¿la serie está en pesos, UF, porcentaje nominal o porcentaje real, y cuál es su fecha de corte?

## 4. Bonos y tasas: por qué “renta fija” no equivale a precio fijo

Un bono es una deuda: quien lo emite promete pagos y devolución del capital bajo ciertas condiciones. Si las tasas que ofrecen bonos nuevos suben, un bono antiguo con menor tasa puede bajar de precio para seguir siendo atractivo en el mercado.

La relación es una regla de orientación, no una explicación completa de un resultado: también importan plazo, inflación, riesgo de crédito, liquidez y moneda.

## 5. Duración: una medida de sensibilidad, no una bola de cristal

La duración aproximada resume cuánto podría cambiar el precio de una cartera si cambian las tasas:

$$\frac{\Delta P}{P} \approx -D\,\Delta y$$

Si la duración es mayor, el precio suele ser más sensible a una variación de tasas. La fórmula es una aproximación para cambios pequeños. No incluye todos los efectos que ocurren en una cartera real; por eso se usa para explorar sensibilidad, no para asegurar una pérdida o una ganancia futura.

## 6. Derivados y cobertura: preguntas antes de concluir

Un derivado es un contrato cuyo valor depende de otra variable, como una tasa o un tipo de cambio. Puede servir para cobertura, ajuste de exposición o especulación; su nombre no permite deducir el propósito.

Un **swap de tasas** intercambia flujos calculados con distintas tasas. Un **forward de moneda** fija un precio de intercambio futuro. Para interpretarlos en datos hay que conocer, como mínimo:

1. el monto nocional y la exposición neta;
2. la fecha, moneda y vencimiento;
3. qué riesgo pretende cubrir;
4. cómo se valoriza;
5. qué parte de la cartera física acompaña.

Una tabla de nocionales sin ese contexto no permite concluir cuánto se ganó, perdió o arriesgó.

## 7. Atribución: dividir una variación no es asignar culpa

La atribución intenta descomponer un retorno total en componentes, por ejemplo tasa, moneda, renta fija y derivados. Es útil porque obliga a declarar una regla de clasificación y verificar que las partes sumen aproximadamente el total.

También tiene límites: un mismo movimiento puede afectar varios componentes, los precios pueden tener rezagos y las posiciones pueden cambiar dentro del período. Por eso la frase correcta es “el modelo estima esta contribución bajo estos supuestos”, no “este componente prueba la causa”.

## 8. VaR, drawdown y correlación: tres gráficos, tres preguntas

| Métrica | Pregunta que ayuda a responder | Lo que no permite afirmar por sí sola |
| --- | --- | --- |
| **Drawdown** | ¿Cuánto cayó una serie desde su máximo previo? | Qué provocó la caída o cuándo se recuperará. |
| **VaR** | Bajo un modelo y nivel de confianza, ¿qué pérdida es inusual? | Que las pérdidas mayores sean imposibles. |
| **Correlación** | ¿Qué tan juntas se movieron dos series en una muestra? | Que una cause la otra o que exista coordinación. |

En el proyecto, estos gráficos se usan para formular mejores preguntas, no para cerrar la discusión.

## 9. Escenarios previsionales: información, no recomendación

Un modelo actuarial o una simulación Monte Carlo puede mostrar cómo un saldo cambia bajo supuestos de edad, tasa, aportes, rentabilidad y mortalidad. Cambiar uno de esos parámetros puede modificar mucho el resultado.

Por eso una simulación debe publicar sus supuestos y evitar dos expresiones engañosas: “pensión exacta” y “tiempo garantizado de recuperación”. Las decisiones previsionales son personales y deben contrastarse con fuentes oficiales y asesoría habilitada cuando corresponda.

## 10. Cómo revisar un resultado antes de compartirlo

Usa este checklist:

- ¿La fuente es primaria y la fecha de corte está visible?
- ¿La cifra es nominal o real? ¿Mensual o acumulada?
- ¿Es un dato observado, una estimación o un escenario?
- ¿El gráfico declara período, unidades, definición y fuente?
- ¿El modelo dice qué supuestos usó y qué no puede concluir?
- ¿Existe código, una tabla de respaldo o una forma de replicarlo?

Si varias respuestas son “no”, conviene tratar el resultado como una hipótesis o una pieza de comunicación, no como evidencia final.

## Diccionario breve

| Concepto | Definición simple |
| --- | --- |
| **UF** | Unidad que permite expresar valores considerando inflación. |
| **Valor cuota** | Valor de una participación en un fondo. |
| **Renta fija** | Instrumentos de deuda con pagos definidos, cuyos precios pueden fluctuar. |
| **Duración** | Sensibilidad aproximada del precio de una cartera a tasas. |
| **Nocional** | Monto de referencia usado para calcular flujos de un derivado; no necesariamente efectivo invertido. |
| **Cobertura** | Posición que busca reducir una exposición existente. |
| **Drawdown** | Caída desde un máximo previo. |
| **VaR** | Medida de pérdida estimada bajo un modelo y nivel de confianza. |
| **Correlación** | Grado de movimiento conjunto entre series en una muestra. |
| **Reproducibilidad** | Capacidad de ejecutar el mismo proceso y revisar o replicar un resultado. |

## Paso siguiente

Lee la [investigación reproducible](articulo_investigacion_fondo_e.md) con esta pregunta en mente: **¿qué parte del argumento proviene directamente de los datos y qué parte proviene de las decisiones del modelo?**

La mejor contribución de una guía no es dar una respuesta definitiva: es ayudar a hacer preguntas mejores y a reconocer cuándo hace falta más evidencia.
