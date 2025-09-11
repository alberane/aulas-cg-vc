import sys
import pygame
from OpenGL.GL import *
from pygame.locals import *

def executar():
    pygame.init()
    janela = (800, 600)
    pygame.display.set_mode(janela, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Exemplo 1: Triângulo com Interpolação de Cores")

    # Configuração inicial do OpenGL
    glOrtho(0, janela[0], 0, janela[1], -1, 1)  # Projeção 2D

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Cor de fundo cinza escuro

        # --- Desenho do triângulo ---
        glBegin(GL_TRIANGLES)

        glColor3f(1, 0, 0)  # Vértice 1 - Vermelho
        glVertex2f(400, 450)

        glColor3f(0, 1, 0)  # Vértice 2 - Verde
        glVertex2f(300, 250)

        glColor3f(0, 0, 1)  # Vértice 3 - Azul
        glVertex2f(500, 250)

        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    executar()
