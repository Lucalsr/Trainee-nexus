"""Funcoes do Hamiltoniano e da representacao da rede de Ising."""

from __future__ import annotations

import numpy as np


def _validar_rede(rede: np.ndarray) -> None:
    if rede.ndim != 2 or rede.shape[0] != rede.shape[1]:
        raise ValueError("A rede deve ser uma matriz quadrada.")


def calcular_energia_total(rede: np.ndarray, J: float = 1.0, h: float = 0.0) -> float:
    """Calcula a energia total da rede com contorno periodico.

    Cada ligacao e contada uma unica vez: com o vizinho abaixo e com o
    vizinho a direita.
    """
    _validar_rede(rede)
    interacoes = np.sum(rede * (np.roll(rede, -1, axis=0) + np.roll(rede, -1, axis=1)))
    return float(-J * interacoes - h * np.sum(rede))


def calcular_delta_E(
    rede: np.ndarray, i: int, j: int, J: float = 1.0, h: float = 0.0
) -> float:
    """Calcula a mudanca de energia causada pela inversao do spin (i, j)."""
    _validar_rede(rede)
    L = rede.shape[0]
    spin = rede[i, j]
    soma_vizinhos = (
        rede[(i - 1) % L, j]
        + rede[(i + 1) % L, j]
        + rede[i, (j - 1) % L]
        + rede[i, (j + 1) % L]
    )
    return float(2 * spin * (J * soma_vizinhos + h))


def calcular_magnetizacao(rede: np.ndarray) -> int:
    """Retorna a magnetizacao total, isto e, a soma de todos os spins."""
    _validar_rede(rede)
    return int(np.sum(rede))


def criar_rede_aleatoria(L: int, rng: np.random.Generator) -> np.ndarray:
    """Cria uma rede L x L com spins -1 e +1 equiprovaveis."""
    if L < 2:
        raise ValueError("O lado da rede deve ser pelo menos 2.")
    return rng.choice(np.array([-1, 1], dtype=np.int8), size=(L, L))
