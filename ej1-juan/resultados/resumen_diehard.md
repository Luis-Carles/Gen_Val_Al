# Resultados de la batería Diehard (Dieharder 3.31.1) — LCG 16807 mod 2³¹−1

**Configuración.** Para cada contraste, Dieharder calcula 100 p-valores (`psamples` = 100) y los resume en un p-valor final mediante Kolmogorov-Smirnov. Criterio: WEAK si p < 0,005 o p > 0,995; FAILED si p < 10⁻⁶ o p > 1 − 10⁻⁶. Se excluye `diehard_sums`, que su autor marca como *Do Not Use*. Los tests *runs* y *craps* dan dos p-valores cada uno.

Columnas:
- **u32 (s1–s3):** nuestro generador con `w = floor(u·2³²)` y semillas 12345, 987654321 y 20261130.
- **shift:** nuestro generador con `w = x << 1`, semilla 12345.
- **minstd:** el generador `minstd` interno de Dieharder (mismo a = 16807 y m = 2³¹−1), semilla 12345.

| Test | u32 s1 | u32 s2 | u32 s3 | shift | minstd |
|---|---|---|---|---|---|
| birthdays | 0,665 ✅ | 0,351 ✅ | 0,528 ✅ | 0,505 ✅ | 0,974 ✅ |
| operm5 | 0,315 ✅ | 0,814 ✅ | 0,445 ✅ | 0,315 ✅ | 0,054 ✅ |
| rank_32x32 | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,996 ⚠️ |
| rank_6x8 | 0,266 ✅ | 0,178 ✅ | 0,431 ✅ | 0,000 ❌ | 0,809 ✅ |
| bitstream | 0,515 ✅ | 0,701 ✅ | 0,350 ✅ | 0,000 ❌ | 0,202 ✅ |
| opso | 2·10⁻⁵ ⚠️ | 0,012 ✅ | 0,007 ✅ | 0,000 ❌ | 2·10⁻⁵ ⚠️ |
| oqso | 6·10⁻⁷ ❌ | 1·10⁻⁶ ⚠️ | 0,004 ⚠️ | 0,000 ❌ | 9·10⁻⁴ ⚠️ |
| dna | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ |
| count_1s_str | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,871 ✅ |
| count_1s_byt | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,000 ❌ | 0,704 ✅ |
| parking_lot | 0,008 ✅ | 0,015 ✅ | 0,048 ✅ | 0,008 ✅ | 0,008 ✅ |
| 2dsphere | 0,019 ✅ | 0,034 ✅ | 0,492 ✅ | 0,019 ✅ | 0,019 ✅ |
| 3dsphere | 0,152 ✅ | 0,508 ✅ | 0,188 ✅ | 0,152 ✅ | 0,152 ✅ |
| squeeze | 0,325 ✅ | 0,293 ✅ | 0,614 ✅ | 0,325 ✅ | 0,325 ✅ |
| runs (1) | 0,080 ✅ | 0,364 ✅ | 0,972 ✅ | 0,080 ✅ | 0,080 ✅ |
| runs (2) | 0,751 ✅ | 0,996 ⚠️ | 0,222 ✅ | 0,751 ✅ | 0,751 ✅ |
| craps (victorias) | 0,532 ✅ | 0,988 ✅ | 0,425 ✅ | 0,532 ✅ | 0,532 ✅ |
| craps (tiradas) | 0,041 ✅ | 0,164 ✅ | 0,490 ✅ | 0,041 ✅ | 0,041 ✅ |
| **PASSED / WEAK / FAILED** | 12 / 1 / 5 | 12 / 2 / 4 | 13 / 1 / 4 | 10 / 0 / 8 | 14 / 3 / 1 |

✅ PASSED · ⚠️ WEAK · ❌ FAILED. Los valores 0,000 son p < 10⁻⁸.

## Interpretación

1. **La implementación es correcta.** Los tests que trabajan con valores uniformes en coma flotante (parking lot, esferas 2D/3D, squeeze, runs, craps) dan **p-valores idénticos hasta el último decimal** para nuestro generador (semilla 12345) y para el `minstd` interno de Dieharder con la misma semilla. Por tanto, generan exactamente la misma secuencia. A esto se suma que x₁₀₀₀₀ = 1043618065 coincide con el valor de control de Park y Miller.

2. **Los tests "geométricos" y de aplicación se superan siempre:** birthday spacings, OPERM5, parking lot, distancias mínimas en 2D y 3D, squeeze, runs y craps. Es decir, **como fuente de números U(0,1) para simular, el generador funciona razonablemente bien**. Lo confirman también los contrastes clásicos (χ², KS, serial, rachas, huecos y autocorrelación), que no rechazan H0 con ninguna semilla.

3. **Los tests "a nivel de bit" fallan, y se puede explicar por qué.** El generador solo produce 31 bits (m = 2³¹−1), pero Diehard espera enteros de 32 bits:
   - Con `x << 1`, el bit menos significativo es **siempre 0**. Por eso fallan todos los tests que miran bits: rangos binarios, bitstream, OPSO, OQSO, DNA y count-the-1s.
   - Con `floor(u·2³²)`, como 2³²/m = 2 + 2/m, resulta w = 2x + ⌊2x/m⌋. Así que **el bit 0 coincide siempre con el bit 31** (comprobado numéricamente en 200.000 valores, sin una sola excepción). Ese bit redundante crea una dependencia lineal exacta entre dos columnas de la matriz 32×32, y por eso **el test de rango 32×32 falla siempre**. También fallan count-the-1s, que cuentan unos por byte.
   - Dieharder sabe que su `minstd` interno tiene 31 bits y compone las palabras a partir de los bits válidos. Por eso pasa rank_32x32 (aunque sale WEAK) y count-the-1s.

4. **Un fallo propio del generador.** Incluso con el tratamiento correcto de los 31 bits (columna minstd), el **test DNA falla** y OPSO/OQSO salen WEAK. Estos tests buscan "palabras" solapadas formadas por pocos bits de números consecutivos, y detectan la estructura en retículo de los generadores congruenciales (ver `figuras/pares.png`). Es la limitación conocida del "estándar mínimo": su periodo es corto (2³¹−2 ≈ 2,1·10⁹) y Dieharder consume una parte apreciable de él.

5. **Conclusión.** El generador de IMSL es adecuado para simulaciones moderadas que usan u ∈ (0,1) directamente, pero **no supera la batería completa de Diehard**. No conviene usarlo cuando importan los bits individuales, para criptografía ni para simulaciones que necesitan más de unos cientos de millones de números. Los generadores modernos (Mersenne Twister, PCG, xoshiro) superan estas baterías.

## Reproducir
```
gcc -O2 -o lcg lcg.c && ./lcg check
bash run_dieharder.sh          # en WSL/Linux con dieharder instalado (≈ 8 min)
python contrastes_clasicos.py 12345 1000000
```
