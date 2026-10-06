"""Algoritmo de Metropolis e rotinas de simulacao."""

from __future__ import annotations

import numpy as np

from .modelo import calcular_delta_E, calcular_energia_total, calcular_magnetizacao, criar_rede_aleatoria


def passo_metropolis(
    rede: np.ndarray,
    T: float,
    J: float = 1.0,
    h: float = 0.0,
    rng: np.random.Generator | None = None,
) -> int:
    """Executa um sweep de Metropolis e retorna o numero de flips aceitos.

    Um sweep realiza L^2 tentativas, portanto cada spin e selecionado uma vez
    em media. A rede e modificada no proprio lugar.
    """
    if T <= 0:
        raise ValueError("A temperatura T deve ser maior que zero.")
    if rng is None:
        rng = np.random.default_rng()

    L = rede.shape[0]
    aceitos = 0
    for _ in range(L * L):
        i = rng.integers(L)
        j = rng.integers(L)
        delta_E = calcular_delta_E(rede, i, j, J, h)

        if delta_E <= 0 or rng.random() < np.exp(-delta_E / T):
            rede[i, j] *= -1
            aceitos += 1

    return aceitos


def equilibrar_rede(
    rede: np.ndarray,
    T: float,
    sweeps: int,
    J: float,
    h: float,
    rng: np.random.Generator,
) -> None:
    """Evolui uma rede por varios sweeps, sem guardar configuracoes."""
    if sweeps < 1:
        raise ValueError("O numero de sweeps deve ser positivo.")
    for _ in range(sweeps):
        passo_metropolis(rede, T, J, h, rng)


def simular_temperatura(
    T: float,
    L: int,
    sweeps: int,
    J: float,
    h: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, float, float]:
    """Cria, equilibra e mede uma configuracao para uma temperatura."""
    rede = criar_rede_aleatoria(L, rng)
    equilibrar_rede(rede, T, sweeps, J, h, rng)
    energia_por_spin = calcular_energia_total(rede, J, h) / rede.size
    magnetizacao_por_spin = calcular_magnetizacao(rede) / rede.size
    return rede, energia_por_spin, magnetizacao_por_spin
