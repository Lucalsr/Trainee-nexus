"""Interface de linha de comando do projeto."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .analise import TC_TEORICO, estimar_tc, grade_temperaturas, varrer_temperaturas
from .verificacao import validar_modelo
from .visualizacao import criar_animacao, salvar_grafico_observaveis, salvar_painel_temperaturas


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
    parser.add_argument("--analise", action="store_true", help="Etapa 2: mede observaveis, plota e estima Tc.")
    parser.add_argument("--medicoes", type=int, default=1000, help="Medidas por temperatura na analise.")
    args = parser.parse_args()

    validar_modelo()
    if args.somente_teste:
        return 0
    if args.sweeps < 1:
        raise ValueError("Use pelo menos um sweep.")

    args.saida.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.semente)

    if args.analise:
        print("Medindo observaveis (pode levar alguns minutos)...")
        dados = varrer_temperaturas(
            grade_temperaturas(),
            args.lado,
            args.sweeps,
            args.medicoes,
            J=1.0,
            h=0.0,
            rng=rng,
            progresso=lambda k, total, T: print(f"  [{k}/{total}] T = {T:.2f}", flush=True),
        )
        grafico = salvar_grafico_observaveis(args.saida / "observaveis_vs_T.png", dados, TC_TEORICO)
        print(f"Grafico salvo em: {grafico}")
        tc = estimar_tc(dados)
        print(f"Tc (pico de C):   {tc['tc_calor_especifico']:.3f}")
        print(f"Tc (pico de chi): {tc['tc_susceptibilidade']:.3f}")
        print(f"Tc estimado: {tc['tc_estimado']:.3f} | teorico: {tc['tc_teorico']:.3f} "
              f"| erro: {tc['erro_relativo']:.1%}")
        return 0

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
