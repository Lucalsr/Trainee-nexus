"""Pacote da simulacao do modelo de Ising 2D."""

from .analise import estimar_tc, grade_temperaturas, medir_temperatura, varrer_temperaturas
from .modelo import calcular_delta_E, calcular_energia_total, calcular_magnetizacao, criar_rede_aleatoria
from .simulacao import equilibrar_rede, passo_metropolis, simular_temperatura
from .verificacao import validar_modelo
from .visualizacao import criar_animacao, salvar_grafico_observaveis, salvar_painel_temperaturas

__all__ = [
    "calcular_delta_E",
    "calcular_energia_total",
    "calcular_magnetizacao",
    "criar_animacao",
    "criar_rede_aleatoria",
    "equilibrar_rede",
    "estimar_tc",
    "grade_temperaturas",
    "medir_temperatura",
    "passo_metropolis",
    "salvar_grafico_observaveis",
    "salvar_painel_temperaturas",
    "simular_temperatura",
    "validar_modelo",
    "varrer_temperaturas",
]
