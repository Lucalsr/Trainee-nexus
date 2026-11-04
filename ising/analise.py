"""Medida de observaveis termodinamicos e estimativa da temperatura critica."""

from __future__ import annotations

import math

import numpy as np

from .modelo import calcular_energia_total, calcular_magnetizacao, criar_rede_aleatoria
from .simulacao import equilibrar_rede, passo_metropolis

TC_TEORICO = 2.0 / math.log(1.0 + math.sqrt(2.0))


def medir_temperatura(
    T: float,
    L: int,
    termalizacao: int,
    medicoes: int,
    J: float,
    h: float,
    rng: np.random.Generator,
    sweeps_entre_medidas: int = 1,
) -> dict[str, float]:
    """Equilibra a rede em T e mede energia, magnetizacao, C e chi.

    Energia e magnetizacao sao por spin. O calor especifico e a
    susceptibilidade saem das flutuacoes de E e M (k_B = 1):
    C = Var(E) / (N T^2) e chi = (<M^2> - <|M|>^2) / (N T).
    """
    if medicoes < 2:
        raise ValueError("Use pelo menos duas medicoes.")
    if sweeps_entre_medidas < 1:
        raise ValueError("sweeps_entre_medidas deve ser positivo.")

    N = L * L
    rede = criar_rede_aleatoria(L, rng)
    equilibrar_rede(rede, T, termalizacao, J, h, rng)

    energias = np.empty(medicoes)
    magnetizacoes = np.empty(medicoes)
    for k in range(medicoes):
        for _ in range(sweeps_entre_medidas):
            passo_metropolis(rede, T, J, h, rng)
        energias[k] = calcular_energia_total(rede, J, h)
        magnetizacoes[k] = calcular_magnetizacao(rede)

    abs_M = np.abs(magnetizacoes)
    return {
        "T": float(T),
        "energia": float(energias.mean() / N),
        "magnetizacao": float(abs_M.mean() / N),
        "calor_especifico": float(energias.var() / (N * T**2)),
        "susceptibilidade": float(((magnetizacoes**2).mean() - abs_M.mean() ** 2) / (N * T)),
    }


def varrer_temperaturas(
    temperaturas: list[float],
    L: int,
    termalizacao: int,
    medicoes: int,
    J: float,
    h: float,
    rng: np.random.Generator,
    sweeps_entre_medidas: int = 1,
    progresso=None,
) -> dict[str, np.ndarray]:
    """Mede os observaveis em cada temperatura e devolve um vetor por coluna.

    `progresso`, se informado, e chamado como progresso(feitas, total, T)
    ao fim de cada temperatura.
    """
    linhas = []
    for k, T in enumerate(temperaturas, start=1):
        linhas.append(medir_temperatura(T, L, termalizacao, medicoes, J, h, rng, sweeps_entre_medidas))
        if progresso is not None:
            progresso(k, len(temperaturas), T)
    return {chave: np.array([linha[chave] for linha in linhas]) for chave in linhas[0]}


def estimar_tc(dados: dict[str, np.ndarray]) -> dict[str, float]:
    """Estima Tc pela posicao do pico do calor especifico e da susceptibilidade."""
    T = dados["T"]
    tc_c = float(T[np.argmax(dados["calor_especifico"])])
    tc_chi = float(T[np.argmax(dados["susceptibilidade"])])
    media = (tc_c + tc_chi) / 2
    return {
        "tc_calor_especifico": tc_c,
        "tc_susceptibilidade": tc_chi,
        "tc_estimado": media,
        "tc_teorico": TC_TEORICO,
        "erro_relativo": abs(media - TC_TEORICO) / TC_TEORICO,
    }


def grade_temperaturas(
    minimo: float = 1.0, maximo: float = 4.0, passo: float = 0.2, passo_fino: float = 0.05
) -> list[float]:
    """Grade de T mais densa perto de Tc (entre 2.0 e 2.6)."""
    grossa = np.arange(minimo, maximo + 1e-9, passo)
    fina = np.arange(2.0, 2.6 + 1e-9, passo_fino)
    todas = np.unique(np.round(np.concatenate([grossa, fina]), 4))
    return [float(t) for t in todas]
