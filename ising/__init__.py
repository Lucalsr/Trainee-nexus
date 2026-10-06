"""Pacote da simulacao do modelo de Ising 2D."""

from .modelo import calcular_delta_E, calcular_energia_total, calcular_magnetizacao, criar_rede_aleatoria
from .simulacao import equilibrar_rede, passo_metropolis, simular_temperatura
from .verificacao import validar_modelo
from .visualizacao import criar_animacao, salvar_painel_temperaturas

__all__ = [
    "calcular_delta_E",
    "calcular_energia_total",
    "calcular_magnetizacao",
    "criar_animacao",
    "criar_rede_aleatoria",
    "equilibrar_rede",
    "passo_metropolis",
    "salvar_painel_temperaturas",
    "simular_temperatura",
    "validar_modelo",
]
