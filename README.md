# Etapa 1 - Modelo de Ising

Simulacao bidimensional do modelo de Ising usando o algoritmo de Metropolis.
O programa cria uma rede de spins, compara sete temperaturas e gera um painel
PNG e uma animacao GIF.

## Estrutura

```text
ising/
  modelo.py         # Hamiltoniano, Delta E, magnetizacao e rede inicial
  simulacao.py      # Sweep de Metropolis e equilibrio termico
  visualizacao.py   # Painel comparativo e GIF
  analise.py        # Energia, magnetizacao, C, chi e estimativa de Tc
  verificacao.py    # Testes fisicos basicos usados pelo programa
  cli.py            # Argumentos de linha de comando
Inicio.py           # Ponto de entrada
tests/              # Testes automatizados
```

## Rodar localmente

Instale Python 3.11 ou superior. Na pasta do projeto, execute:

```powershell
py -m pip install -r requirements.txt
py Inicio.py
```

Os arquivos serao salvos em `resultados/`:

- `painel_temperaturas.png`
- `evolucao_T_2.00.gif`

Com `--analise` (Etapa 2) o programa mede energia, magnetizacao, calor
especifico e susceptibilidade para varias temperaturas, salva
`observaveis_vs_T.png` e imprime a estimativa de Tc comparada ao valor
teorico (2,269). Nenhum CSV e gerado.

Comandos uteis:

```powershell
py Inicio.py --somente-teste
py Inicio.py --analise --lado 20 --sweeps 300 --medicoes 1000
py Inicio.py --lado 20 --sweeps 100 --quadros 30
py -m unittest discover -s tests
py -m jupyter lab
```

No Jupyter, abra `etapa1_ising.ipynb`.
