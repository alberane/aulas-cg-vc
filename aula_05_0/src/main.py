import sys

import pygame
from OpenGL.GL import *
from pygame.locals import *


def desenhar_quadrado(x, y, tamanho, cor, transparencia=1.0):
    """
    Desenha um quadrado 2D com uma cor e transparência específicas.
    :param x: Posição x do centro do quadrado
    :param y: Posição y do centro do quadrado
    :param tamanho: Metade do lado do quadrado
    :param cor: Tupla (r, g, b) da cor
    :param transparencia: Valor de transparência (0.0 a 1.0)
    """
    glColor4f(cor[0], cor[1], cor[2], transparencia)  # Define a cor (RGBA)

    glBegin(GL_QUADS)
    glVertex2f(x - tamanho, y - tamanho)  # Vértice inferior esquerdo
    glVertex2f(x + tamanho, y - tamanho)  # Vértice inferior direito
    glVertex2f(x + tamanho, y + tamanho)  # Vértice superior direito
    glVertex2f(x - tamanho, y + tamanho)  # Vértice superior esquerdo
    glEnd()


def executar():
    pygame.init()
    janela = (800, 600)
    pygame.display.set_mode(janela, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Aula 5: Modelos de Cores com OpenGL")

    # Configuração inicial do OpenGL
    glOrtho(0, janela[0], 0, janela[1], -1, 1)  # Projeção 2D

    # Habilita o blending (mistura de cores) para transparência
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Definição de cores
    VERMELHO = (1, 0, 0)
    VERDE = (0, 1, 0)
    AZUL = (0, 0, 1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Cor de fundo cinza escuro

        # --- Seção 1: Cores primárias sólidas ---
        desenhar_quadrado(150, 450, 50, VERMELHO)
        desenhar_quadrado(270, 450, 50, VERDE)
        desenhar_quadrado(390, 450, 50, AZUL)

        # --- Seção 2: Mistura de cores aditivas ---
        tamanho = 80
        transparencia = 0.7  # Transparência para ver a sobreposição

        # Amarelo (Vermelho + Verde)
        desenhar_quadrado(200, 200, tamanho, VERMELHO, transparencia)
        desenhar_quadrado(250, 200, tamanho, VERDE, transparencia)

        # Ciano (Verde + Azul)
        desenhar_quadrado(450, 200, tamanho, VERDE, transparencia)
        desenhar_quadrado(500, 200, tamanho, AZUL, transparencia)

        # Magenta (Vermelho + Azul)
        desenhar_quadrado(325, 120, tamanho, VERMELHO, transparencia)
        desenhar_quadrado(375, 120, tamanho, AZUL, transparencia)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    executar()
