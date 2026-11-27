# Explicación de tres contrastes de la batería Diehard (borrador para la memoria)

**Idea general.** Cada contraste de Diehard calcula un estadístico cuya distribución es conocida si los números son i.i.d. U(0,1) (hipótesis nula H0). El resultado se convierte en un p-valor. Si H0 es cierta, los p-valores siguen una distribución U(0,1). Dieharder repite cada contraste muchas veces (`psamples`, normalmente 100) y aplica un contraste de Kolmogorov-Smirnov a ese conjunto de p-valores para obtener un p-valor final.

- Marca **WEAK** si el p-valor final es < 0,005 o > 0,995.
- Marca **FAILED** si es < 10⁻⁶ o > 1 − 10⁻⁶.
- Un p-valor muy próximo a 1 también es sospechoso: indica un ajuste "demasiado perfecto".

## 1. Birthday spacings (espaciado de cumpleaños)
- **Idea:** se toman m = 512 "cumpleaños" en un "año" de n = 2²⁴ días. Cada cumpleaños sale de 24 bits de un número aleatorio.
- **Estadístico:** se ordenan los cumpleaños, se calculan los espaciados entre cumpleaños consecutivos y se cuenta J, el número de espaciados que aparecen repetidos.
- **Distribución bajo H0:** J sigue aproximadamente una Poisson de parámetro λ = m³ / (4n) = 2.
- **Contraste:** se repite el experimento, se compara la frecuencia observada de J con la Poisson(2) mediante χ² y se obtiene un p-valor.
- **Por qué es relevante:** los generadores congruenciales tienen una estructura en retículo (ver la figura `pares.png`). Esa estructura hace que los espaciados se repitan más de lo esperado, y este es uno de los contrastes clásicos que los delata.

## 2. Parking lot (aparcamiento)
- **Idea:** en un cuadrado de lado 100 se intentan "aparcar" coches (círculos de radio 1) en posiciones aleatorias. Un intento falla si el coche choca con alguno ya aparcado.
- **Estadístico:** tras 12.000 intentos, el número k de coches aparcados con éxito.
- **Distribución bajo H0:** por simulación con generadores fiables se sabe que k ≈ N(3523; 21,9).
- **Contraste:** se tipifica z = (k − 3523) / 21,9, se repite el experimento y se contrasta con KS que los z siguen una N(0,1), o equivalentemente que los p-valores son uniformes.
- **Qué detecta:** dependencias entre coordenadas consecutivas (x, y). Si los puntos del plano no se reparten bien, caben más o menos coches de lo esperado.

## 3. Craps (juego de dados)
- **Idea:** se juegan 200.000 partidas de *craps*. Cada dado se obtiene de un número aleatorio, como ⌊6u⌋ + 1.
  - Primera tirada: se gana con 7 u 11 y se pierde con 2, 3 o 12.
  - Con cualquier otro resultado (el "punto"), se sigue tirando hasta repetir el punto (se gana) o sacar un 7 (se pierde).
- **Dos estadísticos:**
  1. *Número de victorias.* La probabilidad teórica de ganar es p = 244/495 ≈ 0,4929, así que el número de victorias ≈ N(np, np(1−p)) y se obtiene un p-valor normal.
  2. *Número de tiradas por partida* (agrupando 21 o más). Se compara con su distribución teórica mediante χ².
- **Qué detecta:** sesgos en la distribución discreta derivada y dependencias secuenciales. Es una prueba "de aplicación": simula un uso realista del generador.

## Bibliografía
- Marsaglia, G. (1995). *The Marsaglia Random Number CDROM including the Diehard Battery of Tests of Randomness.* Florida State University.
- Brown, R. G., Eddelbuettel, D., Bauer, D. (2003–2017). *Dieharder: A Random Number Test Suite*, v3.31.1.
- Park, S. K., Miller, K. W. (1988). Random number generators: good ones are hard to find. *Communications of the ACM*, 31(10), 1192–1201.
- Ríos Insua, D., Ríos Insua, S., Martín, J., Jiménez, A. (2008). *Simulación: Métodos y Aplicaciones*, 2.ª ed. RA-MA.
