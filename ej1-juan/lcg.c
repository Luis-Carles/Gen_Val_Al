/*
 * Generador congruencial multiplicativo de IMSL (Park & Miller, "minimal standard"):
 *     x_{i+1} = 16807 * x_i mod (2^31 - 1),     u_i = x_i / (2^31 - 1) en (0,1)
 *
 * Métodos de Simulación (MUIA, UPM) - Práctica, Enunciado 9, Ejercicio 1. Grupo 9.
 *
 * Uso:
 *   ./lcg check                 Verifica la implementación (x_10000 con x_0 = 1 debe ser 1043618065)
 *   ./lcg txt  <semilla> <N>    Escribe N valores u_i en (0,1), uno por línea (texto)
 *   ./lcg raw  <semilla> [N] [modo]
 *                               Escribe enteros de 32 bits en binario por stdout (para dieharder -g 200).
 *                               N = 0 o ausente -> flujo infinito.
 *                               modo = u32   : floor(u_i * 2^32)        (por defecto)
 *                                      shift : x_i << 1  (el bit menos significativo vale siempre 0)
 *
 * Compilar:  gcc -O2 -o lcg lcg.c
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define A 16807u
#define M 2147483647u          /* 2^31 - 1 */
#define Q 127773u              /* M / A   (método de Schrage) */
#define R 2836u                /* M % A */

/* Versión directa con aritmética de 64 bits. */
static inline uint32_t lcg_next64(uint32_t x) {
    return (uint32_t)(((uint64_t)A * x) % M);
}

/* Versión de Schrage: solo usa enteros de 32 bits con signo, sin desbordamiento. */
static inline int32_t lcg_next_schrage(int32_t x) {
    int32_t hi = x / (int32_t)Q, lo = x % (int32_t)Q;
    int32_t t = (int32_t)A * lo - (int32_t)R * hi;
    return t > 0 ? t : t + (int32_t)M;
}

static int check(void) {
    uint32_t x = 1; int32_t y = 1;
    for (int i = 0; i < 10000; i++) {
        x = lcg_next64(x);
        y = lcg_next_schrage(y);
        if ((uint32_t)y != x) { fprintf(stderr, "Discrepancia en i=%d\n", i); return 1; }
    }
    printf("x_10000 = %u (esperado 1043618065) -> %s\n", x, x == 1043618065u ? "OK" : "ERROR");
    printf("Version 64 bits y Schrage coinciden en las 10000 iteraciones.\n");
    return x == 1043618065u ? 0 : 1;
}

static uint32_t parse_seed(const char *s) {
    unsigned long v = strtoul(s, NULL, 10) % M;
    if (v == 0) { fprintf(stderr, "La semilla debe estar en [1, 2^31-2]; se usa 1.\n"); v = 1; }
    return (uint32_t)v;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "Uso: %s check | txt <semilla> <N> | raw <semilla> [N] [u32|shift]\n", argv[0]); return 2; }

    if (!strcmp(argv[1], "check")) return check();

    if (!strcmp(argv[1], "txt") && argc >= 4) {
        uint32_t x = parse_seed(argv[2]);
        unsigned long long n = strtoull(argv[3], NULL, 10);
        for (unsigned long long i = 0; i < n; i++) {
            x = lcg_next64(x);
            printf("%.10f\n", (double)x / (double)M);
        }
        return 0;
    }

    if (!strcmp(argv[1], "raw") && argc >= 3) {
        uint32_t x = parse_seed(argv[2]);
        unsigned long long n = argc >= 4 ? strtoull(argv[3], NULL, 10) : 0;
        int shift = argc >= 5 && !strcmp(argv[4], "shift");
        enum { BUF = 1 << 16 };
        static uint32_t buf[BUF];
        unsigned long long done = 0;
        for (;;) {
            size_t k = 0;
            while (k < BUF && (n == 0 || done < n)) {
                x = lcg_next64(x);
                buf[k++] = shift ? (x << 1)
                                 : (uint32_t)(((uint64_t)x << 32) / M);   /* floor(u * 2^32) */
                done++;
            }
            if (k == 0) break;
            if (fwrite(buf, sizeof(uint32_t), k, stdout) != k) break;   /* dieharder cerró la tubería */
        }
        return 0;
    }

    fprintf(stderr, "Argumentos no válidos.\n");
    return 2;
}
