"""Verificacoes deterministas das formulas do modelo."""

import numpy as np

from .modelo import calcular_delta_E, calcular_energia_total, calcular_magnetizacao


def validar_modelo() -> None:
    """Confirma valores conhecidos da rede fria e a definicao de Delta E."""
    L = 30
    J = 1.0
    rede_fria = np.ones((L, L), dtype=np.int8)

    energia = calcular_energia_total(rede_fria, J)
    magnetizacao = calcular_magnetizacao(rede_fria)
    delta_E = calcular_delta_E(rede_fria, 0, 0, J)

    assert energia == -2 * J * L * L
    assert magnetizacao == L * L
    assert delta_E == 8 * J

    rede_teste = rede_fria.copy()
    energia_antes = calcular_energia_total(rede_teste, J)
    delta_previsto = calcular_delta_E(rede_teste, 4, 7, J)
    rede_teste[4, 7] *= -1
    energia_depois = calcular_energia_total(rede_teste, J)
    assert energia_depois - energia_antes == delta_previsto

    print("Testes fisicos aprovados.")
    print(f"Energia da rede fria: {energia:.1f} (esperado: -1800.0)")
    print(f"Magnetizacao da rede fria: {magnetizacao} (esperado: 900)")
    print(f"Delta E ao inverter um spin: {delta_E:.1f} (esperado: 8.0)")
