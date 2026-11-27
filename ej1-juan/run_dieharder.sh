#!/usr/bin/env bash
# Pasa los tests de la batería Diehard (incluidos en Dieharder) al generador LCG 16807 mod 2^31-1.
# Uso (en WSL/Linux, desde esta carpeta):   bash run_dieharder.sh
# Requisitos: sudo apt install -y dieharder gcc
set -euo pipefail
cd "$(dirname "$0")"
gcc -O2 -o lcg lcg.c
./lcg check
mkdir -p resultados

# Tests Diehard de Dieharder: 0..16 (se excluye 14 'diehard_sums', marcado por su autor como no fiable)
TESTS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 15 16)
SEEDS=(12345 987654321 20261130)

for s in "${SEEDS[@]}"; do
  out="resultados/diehard_lcg_u32_seed${s}.txt"
  : > "$out"
  echo "== LCG (floor(u*2^32)), semilla $s =="
  for t in "${TESTS[@]}"; do
    ./lcg raw "$s" 0 u32 | dieharder -g 200 -d "$t" -c ' ' -D test_name -D ntuple -D tsamples -D psamples -D pvalues -D assessment >> "$out" 2>/dev/null || true
  done
  cat "$out"
done

# Variante con x<<1 (bit bajo siempre 0) para mostrar el efecto de los 31 bits
s=${SEEDS[0]}
out="resultados/diehard_lcg_shift_seed${s}.txt"; : > "$out"
echo "== LCG (x<<1), semilla $s =="
for t in "${TESTS[@]}"; do
  ./lcg raw "$s" 0 shift | dieharder -g 200 -d "$t" -c ' ' -D test_name -D ntuple -D tsamples -D psamples -D pvalues -D assessment >> "$out" 2>/dev/null || true
done
cat "$out"

# Comprobación cruzada con el generador 'minstd' interno de Dieharder (mismo a=16807, m=2^31-1)
out="resultados/diehard_minstd_interno.txt"; : > "$out"
echo "== minstd interno de Dieharder, semilla ${SEEDS[0]} =="
for t in "${TESTS[@]}"; do
  dieharder -g minstd -S "${SEEDS[0]}" -d "$t" -c ' ' -D test_name -D ntuple -D tsamples -D psamples -D pvalues -D assessment >> "$out" 2>/dev/null || true
done
cat "$out"
echo "Resultados guardados en ./resultados"
