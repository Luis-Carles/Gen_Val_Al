# Ejercicio 1: generador IMSL y batería Diehard (aportación de Juan)

Esta carpeta reúne lo que hice para el Ejercicio 1, para que el grupo coja lo que le sirva para la memoria y la presentación. No modifica nada del resto del repo.

## Qué hay

| Fichero | Contenido |
|---|---|
| `lcg.c` | Generador x(i+1) = 16807 · x(i) mod (2³¹ − 1) en C, con dos implementaciones (aritmética de 64 bits y método de Schrage). `./lcg check` comprueba que x₁₀₀₀₀ = 1043618065 con semilla 1, el valor de control de Park y Miller. |
| `run_dieharder.sh` | Pasa los tests de Diehard incluidos en Dieharder, con tres semillas y dos formas de convertir a 32 bits, y lo compara con el `minstd` interno de Dieharder. |
| `contrastes_clasicos.py` | Contrastes clásicos del tema 2 (χ², Kolmogorov-Smirnov, serie, rachas, huecos y autocorrelación) y las figuras. |
| `resultados/resumen_diehard.md` | **Tabla de p-valores de todos los tests e interpretación.** Es lo más útil para la sección de resultados. |
| `resultados/*.txt` | Salida bruta de Dieharder de cada ejecución. |
| `resultados/clasicos_seed*.md` | Resultados de los contrastes clásicos. |
| `explicacion_3_tests.md` | **Explicación de tres contrastes**: Birthday spacings, Parking lot y Craps. Podéis usar cualquiera para vuestra parte. |
| `figuras/` | Gráfico de pares (uᵢ, uᵢ₊₁), histograma y Q-Q. |
| `memoria/memoria_ej1.tex` y `.pdf` | Borrador de memoria completa en LaTeX con el estilo de la ETSIINF, por si sirve de base para la versión final. |

## Cómo reproducirlo

En WSL o Linux, con `gcc` y `dieharder` instalados (`sudo apt install dieharder gcc`):

```bash
gcc -O2 -o lcg lcg.c && ./lcg check
bash run_dieharder.sh                      # unos 8 minutos
python contrastes_clasicos.py 12345 1000000
```

La memoria se compila con `pdflatex memoria_ej1` (dos pasadas) desde la carpeta `memoria/`.

## Resultado en una frase

El generador pasa los tests "geométricos" y de aplicación (birthday spacings, OPERM5, parking lot, esferas 2D y 3D, squeeze, runs y craps) y falla los que miran bits sueltos. El motivo es que solo produce 31 bits y Diehard espera 32, y en `resumen_diehard.md` está explicado con detalle. Además falla DNA incluso tratando bien los 31 bits, por la estructura en retículo de los generadores congruenciales.

## Nota sobre el tamaño de la muestra

Dieharder consume del orden de miles de millones de números con `-a`. Si se le pasa un fichero de 12 millones, lo rebobina y reutiliza los mismos números miles de veces (avisa con "The file file_input_raw was rewound N times"), y eso provoca fallos que no son del generador. Aquí se evita mandando los números por una tubería (`./lcg raw ... | dieharder -g 200`), con un flujo sin fin, así que nunca se repiten.
