# Propuesta de Publicación para LinkedIn

**Título sugerido / Gancho:**  
*Anatomía Forense del Desplome del Fondo E: Los microdatos que desmienten el relato de las AFP tras la formulación de cargos de la Superintendencia.*

---

### Texto del Post (Listo para copiar y pegar)

🚨 **Terremoto en las AFP: ¿Fue realmente un "shock externo inevitable" o una apuesta apalancada fuera de balance?**

Esta semana la Superintendencia de Pensiones remeció al mercado al formular cargos históricos contra las 7 administradoras del sistema (Capital, Cuprum, Habitat, Modelo, Planvital, Provida y UNO) por presunto incumplimiento de deberes fiduciarios (Art. 147 DL 3.500 y NCG 340), tras el agujero de US$ 7.700 millones en los fondos D y E.

Frente a esto, la Asociación de AFP salió a blindarse en prensa (*La Tercera* y *Diario Financiero*), argumentando que *"no fueron apuestas especulativas, sino calce de carteras ante la falta de bonos locales tras los retiros"* y que *"no hay pérdidas reales, sino fluctuaciones de valorización que se recuperan en el largo plazo"*.

Como analista cuantitativo, decidí no quedarme en la discusión de cuñas de prensa y **abrí la caja negra de los microdatos diarios de cartera e inversión en derivados (2010–2026)** de la Superintendencia de Pensiones, Banco Central y la Reserva Federal (FRED). 

La matemática forense arroja conclusiones categóricas que derriban el relato oficial:

1️⃣ **La autopsia de las pérdidas: 8 de cada 10 pesos se fueron en Swaps**  
De los -7,40 puntos porcentuales de caída nominal (-10,39% real) del Fondo E a septiembre de 2026, **el 79,7% (-5,90 pp) provino exclusivamente de Swaps de Tasas de Interés (IRS) offshore**. Los bonos físicos chilenos solo explicaron el 9,5% (-0,7 pp). No fue un colapso de la deuda local; fue una pérdida masiva en derivados en Wall Street.

2️⃣ **El arbitraje de la duración: cuando 5 años se transformaron en 17**  
El Fondo E fue diseñado para tener una sensibilidad de 5 años. Mediante contratos OTC fuera de balance a costo cero de caja inicial (el nocional saltó de US$ 5.300M a más de US$ 200.000M), las administradoras llevaron la duración efectiva combinada a **17,0 años**. Un fondo concebido por ley para proteger a personas a meses del retiro asumió el perfil de riesgo de un hedge fund.

3️⃣ **El tiro en el pie del dólar: Short USD al 150%**  
En Chile, cuando las tasas suben o hay estrés global, el dólar sube y amortigua la renta fija extranjera. Las AFP vendieron dólares a futuro por el 150% de sus activos externos: quedaron cortas en moneda estadounidense, perdiendo el seguro natural y sumando -0,80 pp adicionales de pérdida cuando el dólar escaló a $970.

4️⃣ **Comportamiento de rebaño absoluto ($\rho = 0,987$)**  
Todas las AFP clonaron exactamente la misma estructura de cartera y derivados. El incentivo perverso del encaje premia perder todos juntos antes que desviarse del promedio de la industria.

5️⃣ **La falacia del largo plazo en la jubilación: El caso "Don Juan"**  
Decirle a un afiliado que *"las bajas de valorización se recuperan esperando 3 a 5 años"* es una falacia actuarial destructiva. Un afiliado de 64 años que acumuló $100 MM para jubilarse hoy **no tiene 5 años de horizonte**. Al liquidar sus cuotas para contratar una renta vitalicia, la pérdida se hace de hormigón:
* Saldo cae a $89,6 MM.
* Su pensión mensual sufre un **recorte irreversible de -$69.000 CLP de por vida (-11% vitalicio)**.
* Nuestra simulación estocástica de Monte Carlo (10.000 trayectorias) demuestra que se requieren **21 meses (casi 2 años) de trabajo forzado adicional** solo para intentar reponer el saldo evaporado.

⚖️ **El debate que viene:**  
Las sanciones administrativas de la Superintendencia terminarán en multas a beneficio fiscal (Tesorería). Pero esas multas no le devuelven un solo peso a Don Juan ni a los jubilados de 2026. Es indispensable discutir la responsabilidad patrimonial y una reforma urgente que ponga un límite legal por ley a la duración total en los fondos conservadores.

---

📊 **Investigación abierta y reproducible:**  
He liberado el estudio completo, los modelos actuariales, los scrapers de microdatos y un simulador interactivo para que cualquier afiliado pueda calcular su impacto personal exacto.

🔗 **Artículo completo y gráficos:** [surzua.github.io](https://surzua.github.io)  
💻 **Código abierto en GitHub:** [github.com/surzua/fondo-e-forensics](https://github.com/surzua/fondo-e-forensics)

¿Qué opinan ustedes? ¿Deberían existir topes legales estrictos a la duración sintética en fondos de desacumulación? Los leo en los comentarios.

---
#Pensiones #AFP #FondoE #FinanzasCuantitativas #Economia #Inversiones #Chile #SuperintendenciadePensiones #DataScience
