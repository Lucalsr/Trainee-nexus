"""Testes automatizados do nucleo fisico e da simulacao."""

import unittest

import numpy as np

from ising.modelo import calcular_delta_E, calcular_energia_total, calcular_magnetizacao
from ising.simulacao import passo_metropolis


class TestModeloIsing(unittest.TestCase):
    def setUp(self):
        self.rede_fria = np.ones((4, 4), dtype=np.int8)

    def test_rede_fria_tem_energia_e_magnetizacao_conhecidas(self):
        self.assertEqual(calcular_energia_total(self.rede_fria), -32.0)
        self.assertEqual(calcular_magnetizacao(self.rede_fria), 16)

    def test_delta_e_equivale_a_diferenca_de_energias(self):
        antes = calcular_energia_total(self.rede_fria)
        delta = calcular_delta_E(self.rede_fria, 0, 0)
        self.rede_fria[0, 0] *= -1
        depois = calcular_energia_total(self.rede_fria)
        self.assertEqual(depois - antes, delta)

    def test_temperatura_invalida_falha(self):
        with self.assertRaises(ValueError):
            passo_metropolis(self.rede_fria, T=0.0)

    def test_sweep_em_rede_fria_baixa_temperatura_nao_inverte_spins(self):
        rng = np.random.default_rng(42)
        aceitos = passo_metropolis(self.rede_fria, T=0.1, rng=rng)
        self.assertEqual(aceitos, 0)
        np.testing.assert_array_equal(self.rede_fria, np.ones((4, 4), dtype=np.int8))


if __name__ == "__main__":
    unittest.main()
