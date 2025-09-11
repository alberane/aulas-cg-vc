#!/usr/bin/env python3
"""
Visualizador de Modelos de Cor
Demonstra conversões entre RGB, HSV e CMYK com uma interface interativa.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import colorsys
from typing import Tuple

class VisualizadorModelosCor:
    """Classe para visualização e conversão entre modelos de cor."""

    def __init__(self):
        """Inicializa o visualizador com valores e configurações padrão."""
        self.figura, self.eixos = plt.subplots(2, 2, figsize=(12, 10))
        self.figura.suptitle('Visualizador de Modelos de Cor', fontsize=16, fontweight='bold')

        # Define a cor inicial como vermelho puro.
        self.cor_rgb: Tuple[float, float, float] = (1.0, 0.0, 0.0)


        # Configura os elementos gráficos da interface.
        self.configurar_graficos()
        self.criar_controles_deslizantes()
        self.atualizar_visualizacoes()

    def configurar_graficos(self):
        """Configura os títulos e limites dos subplots (gráficos)."""
        # Gráfico do espaço de cor RGB
        self.eixos[0, 0].set_title('Espaço de Cor RGB')
        self.eixos[0, 0].set_xlim(0, 1)
        self.eixos[0, 0].set_ylim(0, 1)

        # Gráfico do espaço de cor HSV
        self.eixos[0, 1].set_title('Espaço de Cor HSV')

        # Gráfico de barras CMYK
        self.eixos[1, 0].set_title('Valores CMYK')

        # Amostra da cor selecionada
        self.eixos[1, 1].set_title('Amostra de Cor')
        self.eixos[1, 1].axis('off')

    def criar_controles_deslizantes(self):
        """Cria e posiciona os controles deslizantes (sliders) para os canais RGB."""
        plt.subplots_adjust(bottom=0.25)

        # Define a posição de cada controle na janela.
        eixo_vermelho = plt.axes([0.2, 0.15, 0.5, 0.03])
        eixo_verde = plt.axes([0.2, 0.10, 0.5, 0.03])
        eixo_azul = plt.axes([0.2, 0.05, 0.5, 0.03])

        # Cria os sliders para cada cor.
        self.controle_vermelho = Slider(eixo_vermelho, 'Vermelho', 0.0, 1.0, valinit=self.cor_rgb[0], facecolor='red')
        self.controle_verde = Slider(eixo_verde, 'Verde', 0.0, 1.0, valinit=self.cor_rgb[1], facecolor='green')
        self.controle_azul = Slider(eixo_azul, 'Azul', 0.0, 1.0, valinit=self.cor_rgb[2], facecolor='blue')

        # Associa a função de atualização ao evento de mudança dos sliders.
        self.controle_vermelho.on_changed(self.atualizar_cor)
        self.controle_verde.on_changed(self.atualizar_cor)
        self.controle_azul.on_changed(self.atualizar_cor)

    def atualizar_cor(self, valor):
        """Atualiza a cor com base nos novos valores dos controles deslizantes."""
        self.cor_rgb = (
            self.controle_vermelho.val,
            self.controle_verde.val,
            self.controle_azul.val
        )
        self.atualizar_visualizacoes()




    def rgb_para_hsv(self, r: float, g: float, b: float) -> Tuple[float, float, float]:
        """Converte um valor de cor RGB para HSV."""
        return colorsys.rgb_to_hsv(r, g, b)

    def rgb_para_cmyk(self, r: float, g: float, b: float) -> Tuple[float, float, float, float]:
        """Converte um valor de cor RGB para CMYK."""
        # Se a cor for preto puro, o cálculo é direto.
        if r == 0 and g == 0 and b == 0:
            return 0, 0, 0, 1

        k = 1 - max(r, g, b)
        if k == 1:
            return 0, 0, 0, 1

        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

        return c, m, y, k

    def criar_visualizacao_rgb(self):
        """Cria e exibe a visualização do espaço de cor RGB."""
        self.eixos[0, 0].clear()
        self.eixos[0, 0].set_title('Espaço de Cor RGB')

        # Gera uma malha de pixels para o gradiente de cores.
        x = np.linspace(0, 1, 256)
        y = np.linspace(0, 1, 256)
        X, Y = np.meshgrid(x, y)

        # Cria uma imagem RGB onde Vermelho varia em Y, Verde em X e Azul é fixo.
        imagem_rgb = np.zeros((256, 256, 3))
        imagem_rgb[:, :, 0] = Y
        imagem_rgb[:, :, 1] = X
        imagem_rgb[:, :, 2] = self.cor_rgb[2]

        self.eixos[0, 0].imshow(imagem_rgb, origin='lower', extent=[0, 1, 0, 1])

        # Adiciona um marcador na posição da cor atual.
        self.eixos[0, 0].plot(self.cor_rgb[1], self.cor_rgb[0], 'wo', markersize=10,
                               markeredgecolor='black', markeredgewidth=2)

        self.eixos[0, 0].set_xlabel('Verde')
        self.eixos[0, 0].set_ylabel('Vermelho')

    def criar_visualizacao_hsv(self):
        """Cria e exibe a roda de cores do espaço HSV."""
        self.eixos[0, 1].clear()
        self.eixos[0, 1].set_title('Espaço de Cor HSV')

        h, s, v = self.rgb_para_hsv(*self.cor_rgb)

        # Gera coordenadas polares para a roda de cores.
        angulo = np.linspace(0, 2 * np.pi, 360)
        raio = np.linspace(0, 1, 100)
        T, R = np.meshgrid(angulo, raio)

        # Cria a imagem HSV convertendo cada ponto polar para RGB.
        # Python
        imagem_hsv = np.zeros((100, 360, 3))
        for i in range(100):
            for j in range(360):
                rgb = colorsys.hsv_to_rgb(float(T[i, j]) / (2 * np.pi), float(R[i, j]), float(v))
                imagem_hsv[i, j, :] = rgb


        self.eixos[0, 1].imshow(imagem_hsv, extent=[-1, 1, -1, 1], origin='lower')

        # Adiciona um marcador na posição da cor atual.
        posicao_x_atual = s * np.cos(h * 2 * np.pi)
        posicao_y_atual = s * np.sin(h * 2 * np.pi)
        self.eixos[0, 1].plot(posicao_x_atual, posicao_y_atual, 'wo', markersize=10,
                               markeredgecolor='black', markeredgewidth=2)

        self.eixos[0, 1].set_xlim(-1, 1)
        self.eixos[0, 1].set_ylim(-1, 1)
        self.eixos[0, 1].set_aspect('equal')

    def criar_barras_cmyk(self):
        """Cria o gráfico de barras para os valores CMYK."""
        self.eixos[1, 0].clear()
        self.eixos[1, 0].set_title('Valores CMYK')

        c, m, y, k = self.rgb_para_cmyk(*self.cor_rgb)

        cores = ['cyan', 'magenta', 'yellow', 'black']
        valores = [c, m, y, k]
        rotulos = ['C', 'M', 'Y', 'K']

        barras = self.eixos[1, 0].bar(rotulos, valores, color=cores, alpha=0.7)

        # Adiciona o valor numérico no topo de cada barra.
        for barra, valor in zip(barras, valores):
            altura = barra.get_height()
            self.eixos[1, 0].text(barra.get_x() + barra.get_width() / 2., altura + 0.01,
                                  f'{valor:.2f}', ha='center', va='bottom', fontweight='bold')

        self.eixos[1, 0].set_ylim(0, 1.1)
        self.eixos[1, 0].set_ylabel('Valor')

    def criar_amostra_cor(self):
        """Exibe um quadrado com a cor atual e seus valores numéricos."""
        self.eixos[1, 1].clear()
        self.eixos[1, 1].set_title('Amostra de Cor')

        # Desenha o retângulo com a cor selecionada.
        retangulo = plt.Rectangle((0.1, 0.1), 0.8, 0.8,
                                  facecolor=self.cor_rgb, edgecolor='black', linewidth=2)
        self.eixos[1, 1].add_patch(retangulo)

        # Converte a cor para os outros modelos para exibição.
        h, s, v = self.rgb_para_hsv(*self.cor_rgb)
        c, m, y, k = self.rgb_para_cmyk(*self.cor_rgb)

        texto_info = f"""RGB: ({self.cor_rgb[0]:.3f}, {self.cor_rgb[1]:.3f}, {self.cor_rgb[2]:.3f})
HSV: ({h:.3f}, {s:.3f}, {v:.3f})
CMYK: ({c:.3f}, {m:.3f}, {y:.3f}, {k:.3f})"""

        self.eixos[1, 1].text(0.5, 0.05, texto_info, ha='center', va='bottom',
                              fontsize=10, fontfamily='monospace',
                              bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        self.eixos[1, 1].set_xlim(0, 1)
        self.eixos[1, 1].set_ylim(0, 1)
        self.eixos[1, 1].axis('off')

    def atualizar_visualizacoes(self):
        """Atualiza todos os gráficos e a amostra de cor."""
        try:
            self.criar_visualizacao_rgb()
            self.criar_visualizacao_hsv()
            self.criar_barras_cmyk()
            self.criar_amostra_cor()
            plt.draw()
        except Exception as erro:
            print(f"Ocorreu um erro durante a atualização: {erro}")

    def exibir(self):
        """Mostra a janela principal do visualizador."""
        plt.show()

def principal():
    """Função principal que inicia e executa o programa."""
    print("Iniciando o Visualizador de Modelos de Cor...")
    print("Use os controles deslizantes para alterar os valores RGB e veja as mudanças.")

    try:
        visualizador = VisualizadorModelosCor()
        visualizador.exibir()
    except Exception as erro:
        print(f"Não foi possível inicializar o visualizador: {erro}")

if __name__ == "__main__":
    principal()