"""Interface de linha de comando do projeto."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .verificacao import validar_modelo
from .visualizacao import criar_animacao, salvar_painel_temperaturas


def main() -> int:
    parser = argparse.ArgumentParser(description="Etapa 1: Modelo de Ising com Metropolis")
    parser.add_argument("--lado", type=int, default=30, help="Tamanho L da rede L x L.")
    parser.add_argument("--sweeps", type=int, default=300, help="Sweeps para equilibrar cada temperatura.")
    parser.add_argument("--temperatura-animacao", type=float, default=2.0)
    parser.add_argument("--quadros", type=int, default=60, help="Numero de quadros do GIF.")
    parser.add_argument("--saida", type=Path, default=Path("resultados"))
    parser.add_argument("--semente", type=int, default=42, help="Semente para resultados reproduziveis.")
    parser.add_argument("--somente-teste", action="store_true", help="Executa somente os testes das formulas.")
    parser.add_argument("--sem-animacao", action="store_true", help="Gera somente o painel comparativo.")
    args = parser.parse_args()

    validar_modelo()
    if args.somente_teste:
        return 0
    if args.sweeps < 1:
        raise ValueError("Use pelo menos um sweep.")

    args.saida.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.semente)
    temperaturas = [1.0, 1.5, 2.0, 2.27, 2.5, 3.0, 3.5]

    painel = salvar_painel_temperaturas(
        args.saida / "painel_temperaturas.png",
        temperaturas,
        args.lado,
        args.sweeps,
        J=1.0,
        h=0.0,
        rng=rng,
    )
    print(f"Painel salvo em: {painel}")

    if not args.sem_animacao:
        animacao = criar_animacao(
            args.saida / f"evolucao_T_{args.temperatura_animacao:.2f}.gif",
            args.temperatura_animacao,
            args.lado,
            args.sweeps,
            args.quadros,
            sweeps_entre_quadros=5,
            J=1.0,
            h=0.0,
            rng=rng,
        )
        print(f"Animacao salva em: {animacao}")
    return 0
