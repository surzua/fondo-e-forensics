# Laboratorio de ciencia de datos: Fondo E

Este repositorio documenta una investigación reproducible sobre la caída del Fondo E de las AFP chilenas durante 2026. No pretende convertir a quien lo lee en especialista financiero ni entregar recomendaciones de inversión o previsión: usa un caso público y contingente para mostrar cómo se formula, implementa, valida y comunica una investigación con datos.

El caso sigue siendo relevante. A septiembre de 2026, la rentabilidad real acumulada del Fondo E del sistema fue de **-10,39%**, mientras las autoridades han solicitado antecedentes y se discuten responsabilidades y medidas regulatorias. La cifra y el debate público justifican estudiarlo; no sustituyen el análisis de los datos ni permiten anticipar sus conclusiones.

> **Alcance.** Los resultados de este repositorio son estimaciones reproducibles construidas a partir de fuentes públicas y supuestos explícitos. No constituyen una auditoría oficial, una imputación de responsabilidades, asesoría financiera, previsional o legal, ni una recomendación para cambiarse de fondo.

---

## Qué se investiga

La pregunta no es “quién tiene razón” antes de mirar los datos. Es cómo descomponer una variación relevante de rentabilidad de forma trazable y con límites claros.

El proyecto explora, entre otras, estas preguntas:

1. ¿Cómo cambian los resultados al limpiar, deflactar y alinear series de distintas fuentes públicas?
2. ¿Qué parte de la variación observada puede asociarse, bajo un modelo explícito, a renta fija, tasas, moneda y derivados?
3. ¿Qué señales de concentración o co-movimiento aparecen entre administradoras?
4. ¿Cómo comunicar duración, derivados, riesgo de cola y horizonte previsional sin confundir una estimación con un hecho probado?
5. ¿Qué pruebas, visualizaciones y documentación permiten que otra persona cuestione o replique el análisis?

El Fondo E es el caso de estudio; el entregable principal es el proceso de ciencia de datos: ingestión, contratos de datos, controles de calidad, transformación, modelamiento, visualización, reproducibilidad y comunicación responsable de incertidumbre.

---

## Entregables para dos lecturas complementarias

| Entregable | Para qué sirve |
| --- | --- |
| [Investigación reproducible](deliverables/articulo_investigacion_fondo_e.md) | Expone la pregunta, fuentes, decisiones de modelamiento, resultados, limitaciones y cómo replicar o refutar los hallazgos. |
| [Guía didáctica](deliverables/guia_didactica_finanzas_fondo_e.md) | Explica los conceptos mínimos y, sobre todo, cómo leer gráficos, supuestos y resultados sin requerir formación financiera. |
| [Post de LinkedIn](deliverables/post_linkedin_fondo_e.md) | Presenta ambos materiales como una historia de investigación de datos, no como una credencial de experto financiero. |
| [Kit de difusión](deliverables/kit_viral_linkedin.md) | Guion de carrusel, comentario y hilo centrados en método, evidencia y preguntas abiertas. |

---

## Estructura del repositorio

```text
fondo-e-forensics/
├── deliverables/               # Investigación, guía didáctica y piezas de difusión
├── docs/                       # Especificación técnica y reportes de fases
├── data/
│   ├── raw/                    # Insumos descargados; no se modifican
│   ├── interim/                # Datos estandarizados y limpios
│   └── processed/              # Paneles, tablas y gráficos reproducibles
├── notebooks/                  # Bitácora secuencial de exploración y validación
├── src/
│   ├── scrapers/               # Adquisición de datos con trazabilidad
│   ├── etl/                    # Limpieza, cruces y mart analítico
│   ├── models/                 # Métricas, atribución y escenarios actuariales
│   ├── viz/                    # Gráficos estáticos e interactivos
│   └── schemas.py              # Contratos y validaciones de datos
├── app/                        # Explorador interactivo en Streamlit
└── tests/                      # Pruebas de transformación, modelos y visualización
```

---

## Cómo se trabaja con los datos

1. **Trazabilidad de fuentes.** Se descargan valores cuota y carteras desde la Superintendencia de Pensiones; UF y variables macroeconómicas desde el Banco Central; y series de mercado desde fuentes declaradas en el código.
2. **Calidad antes de cálculo.** Los esquemas, controles de cobertura temporal, tipos de dato y tests buscan detectar rupturas antes de publicar una cifra.
3. **Transformaciones visibles.** La deflactación por UF, los cruces temporales y las agregaciones se implementan en `src/`, no solo en una planilla o gráfico final.
4. **Modelos como aproximaciones.** La atribución, VaR/CVaR, duración y simulaciones dependen de supuestos. Se deben leer junto con sus definiciones y límites, no como causalidad demostrada.
5. **Comunicación verificable.** Cada visualización debe poder rastrearse a una fuente, una transformación y una pregunta del análisis.

---

## Instalación y reproducción

El proyecto utiliza `uv` para gestionar el entorno.

```bash
git clone <url-del-repositorio>
cd fondo-e-forensics

make setup    # instala dependencias
make scrape   # actualiza fuentes públicas
make etl      # construye el mart analítico
make test     # ejecuta validaciones y pruebas
make app      # abre el explorador Streamlit
```

Al actualizar datos, registra la fecha de extracción y revisa los tests antes de comparar resultados con una versión anterior.

---

## Fuentes y actualidad del caso

- [Rentabilidad real de los fondos — Superintendencia de Pensiones](https://www71.spensiones.cl/apps/rentabilidad/getRentabilidad.php?tiprent=FP)
- [Caída del Fondo E y procedimientos en curso — Ministerio del Trabajo, reportado por Chócale](https://chocale.cl/2026/10/ministerio-del-trabajo-oficia-a-la-superintendencia-de-pensiones-caida-del-fondo-e/)
- [Contexto de mercado y composición de cartera — Diario Financiero](https://www.df.cl/mercados/pensiones/que-le-pasa-al-fondo-e-selectivo-mas-conservador-del-sistema-acumula)

Las fuentes externas cambian. Antes de reutilizar una cifra o publicar una conclusión, ejecuta el pipeline, conserva la fecha de corte y verifica si existen nuevos antecedentes regulatorios u oficiales.
