"""
Contrastes clásicos de aleatoriedad (tema 2) para el LCG x_{i+1} = 16807 x_i mod (2^31-1).
Métodos de Simulación (MUIA, UPM) - Enunciado 9, Ejercicio 1. Grupo 9.

Uso:  python contrastes_clasicos.py [semilla] [N]
Genera: resultados/clasicos_seed<semilla>.md y las figuras en figuras/.
"""
import sys
from pathlib import Path

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A, M = 16807, 2**31 - 1
ALPHA = 0.05


def lcg(seed: int, n: int) -> np.ndarray:
    """Devuelve n valores u_i = x_i/M. Bucle exacto en enteros (Python), luego numpy."""
    x = seed % M or 1
    out = np.empty(n, dtype=np.int64)
    for i in range(n):
        x = (A * x) % M
        out[i] = x
    return out / M


def chi2_frecuencias(u, k=100):
    obs = np.bincount(np.minimum((u * k).astype(int), k - 1), minlength=k)
    return stats.chisquare(obs)


def ks_uniforme(u):
    return stats.kstest(u, "uniform")


def serial_pares(u, d=10):
    """Test serial: pares no solapados (u_{2i}, u_{2i+1}) en una rejilla d x d."""
    v = u[: len(u) // 2 * 2].reshape(-1, 2)
    idx = np.minimum((v * d).astype(int), d - 1)
    obs = np.bincount(idx[:, 0] * d + idx[:, 1], minlength=d * d)
    return stats.chisquare(obs)


def rachas_arriba_abajo(u):
    """Test de rachas ascendentes/descendentes (número total de rachas, aproximación normal)."""
    s = np.sign(np.diff(u))
    s = s[s != 0]
    runs = 1 + np.count_nonzero(s[1:] != s[:-1])
    n = len(u)
    mu = (2 * n - 1) / 3
    var = (16 * n - 29) / 90
    z = (runs - mu) / np.sqrt(var)
    return runs, z, 2 * stats.norm.sf(abs(z))


def huecos(u, a=0.0, b=0.5, tmax=10):
    """Test de huecos (gap test): longitud entre visitas sucesivas a [a,b)."""
    p = b - a
    hits = np.flatnonzero((u >= a) & (u < b))
    gaps = np.diff(hits) - 1
    obs = np.bincount(np.minimum(gaps, tmax), minlength=tmax + 1)
    probs = np.array([p * (1 - p) ** t for t in range(tmax)] + [(1 - p) ** tmax])
    return stats.chisquare(obs, probs * obs.sum())


def autocorrelacion(u, lag=1):
    r = np.corrcoef(u[:-lag], u[lag:])[0, 1]
    z = r * np.sqrt(len(u) - lag)
    return r, z, 2 * stats.norm.sf(abs(z))


def figuras(u, seed, figdir: Path):
    figdir.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(u, bins=50, density=True, color="#4C72B0", edgecolor="white")
    ax.axhline(1, color="k", ls="--", lw=1, label="densidad U(0,1)")
    ax.set(xlabel="u", ylabel="densidad", title=f"Histograma de {len(u):,} valores (semilla {seed})")
    ax.legend()
    fig.tight_layout(); fig.savefig(figdir / "histograma.png", dpi=150); plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(11, 5))
    axs[0].scatter(u[:-1][:20000], u[1:][:20000], s=0.5, color="#4C72B0")
    axs[0].set(xlabel="$u_i$", ylabel="$u_{i+1}$", title="Pares consecutivos (20.000 puntos)")
    # Zoom: en una franja estrecha se ven las rectas del retículo (u_{i+1} = 16807 u_i - k)
    mask = u[:-1] < 0.001
    axs[1].scatter(u[:-1][mask], u[1:][mask], s=1, color="#C44E52")
    axs[1].set(xlabel="$u_i$", ylabel="$u_{i+1}$", title="Zoom $u_i<0.001$: estructura en retículo")
    fig.tight_layout(); fig.savefig(figdir / "pares.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    stats.probplot(u[:5000], dist="uniform", plot=ax)
    ax.set_title("Gráfico P-P/Q-Q frente a U(0,1) (5.000 valores)")
    fig.tight_layout(); fig.savefig(figdir / "qq.png", dpi=150); plt.close(fig)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1_000_000
    here = Path(__file__).resolve().parent
    u = lcg(seed, n)

    filas = []
    def fila(nombre, estad, p):
        filas.append((nombre, estad, p, "No se rechaza H0" if p > ALPHA else "Se rechaza H0"))

    r = chi2_frecuencias(u); fila("Chi-cuadrado de frecuencias (100 clases)", f"χ² = {r.statistic:.2f}", r.pvalue)
    r = ks_uniforme(u);      fila("Kolmogorov-Smirnov frente a U(0,1)", f"D = {r.statistic:.5f}", r.pvalue)
    r = serial_pares(u);     fila("Serial de pares (rejilla 10×10)", f"χ² = {r.statistic:.2f}", r.pvalue)
    runs, z, p = rachas_arriba_abajo(u); fila("Rachas ascendentes/descendentes", f"R = {runs}, z = {z:.3f}", p)
    r = huecos(u);           fila("Huecos (intervalo [0, 0.5))", f"χ² = {r.statistic:.2f}", r.pvalue)
    rho, z, p = autocorrelacion(u); fila("Autocorrelación de retardo 1", f"r = {rho:.5f}, z = {z:.3f}", p)

    resdir = here / "resultados"; resdir.mkdir(exist_ok=True)
    lines = [f"# Contrastes clásicos — LCG 16807 mod 2^31−1, semilla {seed}, N = {n:,}\n",
             f"Media = {u.mean():.6f} (teórica 0.5), varianza = {u.var(ddof=1):.6f} (teórica {1/12:.6f})\n",
             "| Contraste | Estadístico | p-valor | Decisión (α = 0.05) |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c:.4f} | {d} |" for a, b, c, d in filas]
    texto = "\n".join(lines) + "\n"
    (resdir / f"clasicos_seed{seed}.md").write_text(texto, encoding="utf-8")
    print(texto)

    figuras(u, seed, here / "figuras")
    print("Figuras guardadas en", here / "figuras")


if __name__ == "__main__":
    main()
