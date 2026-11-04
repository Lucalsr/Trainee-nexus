"""Geracao do painel comparativo e da animacao da rede de spins."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .modelo import criar_rede_aleatoria
from .simulacao import equilibrar_rede, simular_temperatura


def _importar_matplotlib():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
    except ModuleNotFoundError as erro:
        raise RuntimeError(
            "Para gerar imagens, instale as dependencias com: "
            "python -m pip install -r requirements.txt"
        ) from erro
    return plt, ListedColormap


def salvar_painel_temperaturas(
    caminho: Path,
    temperaturas: list[float],
    L: int,
    sweeps: int,
    J: float,
    h: float,
    rng: np.random.Generator,
) -> Path:
    """Salva uma configuracao equilibrada para cada temperatura."""
    plt, ListedColormap = _importar_matplotlib()
    cmap = ListedColormap(["#2166ac", "#e66101"])
    fig, eixos = plt.subplots(2, 4, figsize=(12, 6), constrained_layout=True)

    for eixo, T in zip(eixos.flat, temperaturas):
        rede, _, magnetizacao = simular_temperatura(T, L, sweeps, J, h, rng)
        eixo.imshow(rede, cmap=cmap, vmin=-1, vmax=1, interpolation="nearest")
        eixo.set_title(f"T = {T:.2f} | m = {magnetizacao:.2f}")
        eixo.set_xticks([])
        eixo.set_yticks([])

    for eixo in eixos.flat[len(temperaturas) :]:
        eixo.axis("off")

    fig.suptitle("Modelo de Ising: configuracoes apos equilibrio", fontsize=15)
    fig.savefig(caminho, dpi=160)
    plt.close(fig)
    return caminho


def criar_animacao(
    caminho: Path,
    T: float,
    L: int,
    sweeps_equilibrio: int,
    quadros: int,
    sweeps_entre_quadros: int,
    J: float,
    h: float,
    rng: np.random.Generator,
) -> Path:
    """Salva em GIF a evolucao de uma rede a uma temperatura fixa."""
    try:
        from PIL import Image
    except ModuleNotFoundError as erro:
        raise RuntimeError(
            "Para gerar o GIF, instale as dependencias com: "
            "python -m pip install -r requirements.txt"
        ) from erro
    if quadros < 2:
        raise ValueError("A animacao deve ter pelo menos dois quadros.")

    rede = criar_rede_aleatoria(L, rng)
    equilibrar_rede(rede, T, sweeps_equilibrio, J, h, rng)

    imagens = []
    escala = max(8, 360 // L)
    for _ in range(quadros):
        pixels = np.zeros((L, L, 3), dtype=np.uint8)
        pixels[rede == -1] = (33, 102, 172)
        pixels[rede == 1] = (230, 97, 1)
        imagem = Image.fromarray(pixels, mode="RGB")
        imagens.append(imagem.resize((L * escala, L * escala), Image.Resampling.NEAREST))
        equilibrar_rede(rede, T, sweeps_entre_quadros, J, h, rng)

    imagens[0].save(caminho, save_all=True, append_images=imagens[1:], duration=120, loop=0)
    return caminho


def salvar_grafico_observaveis(caminho: Path, dados: dict[str, np.ndarray], tc_teorico: float) -> Path:
    """Plota energia, |m|, calor especifico e susceptibilidade contra T."""
    plt, _ = _importar_matplotlib()
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    graficos = [
        ("energia", "Energia por spin"),
        ("magnetizacao", "Magnetizacao por spin |m|"),
        ("calor_especifico", "Calor especifico C"),
        ("susceptibilidade", "Susceptibilidade $\chi$"),
    ]
    fig, eixos = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    for eixo, (chave, rotulo) in zip(eixos.ravel(), graficos):
        eixo.plot(dados["T"], dados[chave], "o-", markersize=4)
        eixo.axvline(tc_teorico, color="red", linestyle="--", label=f"Tc teorico = {tc_teorico:.3f}")
        eixo.set_xlabel("T")
        eixo.set_ylabel(rotulo)
        eixo.grid(alpha=0.3)
    eixos[0, 0].legend()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho
