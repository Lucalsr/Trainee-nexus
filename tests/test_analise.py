"""Testes das medidas de observaveis e da estimativa de Tc."""

import unittest

import numpy as np

from ising.analise import TC_TEORICO, estimar_tc, medir_temperatura


class TestAnalise(unittest.TestCase):
    def test_baixa_temperatura_fica_ordenada(self):
        rng = np.random.default_rng(1)
        r = medir_temperatura(1.0, 8, 200, 200, 1.0, 0.0, rng)
        self.assertGreater(r["magnetizacao"], 0.9)
        self.assertLess(r["energia"], -1.8)

    def test_alta_temperatura_fica_desordenada(self):
        rng = np.random.default_rng(1)
        r = medir_temperatura(5.0, 8, 200, 200, 1.0, 0.0, rng)
        self.assertLess(r["magnetizacao"], 0.4)

    def test_estimar_tc_usa_pico(self):
        T = np.array([1.0, 2.0, 3.0])
        dados = {"T": T, "calor_especifico": np.array([0.1, 1.0, 0.2]),
                 "susceptibilidade": np.array([0.1, 0.5, 2.0])}
        tc = estimar_tc(dados)
        self.assertEqual(tc["tc_calor_especifico"], 2.0)
        self.assertEqual(tc["tc_susceptibilidade"], 3.0)
        self.assertAlmostEqual(tc["tc_teorico"], TC_TEORICO)

    def test_poucas_medicoes_falha(self):
        with self.assertRaises(ValueError):
            medir_temperatura(2.0, 4, 10, 1, 1.0, 0.0, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
