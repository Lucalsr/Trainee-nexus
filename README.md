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

Comandos uteis:

```powershell
py Inicio.py --somente-teste
py Inicio.py --lado 20 --sweeps 100 --quadros 30
py -m unittest discover -s tests
py -m jupyter lab
```

No Jupyter, abra `etapa1_ising.ipynb`.

## Rodar com Docker

Com Docker Desktop instalado e em execucao:

```powershell
docker build -t ising-etapa1 .
docker run --rm -v "${PWD}/resultados:/app/resultados" ising-etapa1
```

O segundo comando monta a pasta local `resultados/` no conteiner, para que o
PNG e o GIF sejam preservados no seu computador.

Para executar apenas os testes dentro do conteiner:

```powershell
docker run --rm ising-etapa1 python -m unittest discover -s tests
```

Para iniciar o Jupyter no conteiner:

```powershell
docker run --rm -p 8888:8888 -v "${PWD}:/app" ising-etapa1 `
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Abra o endereco exibido pelo Jupyter no navegador.
