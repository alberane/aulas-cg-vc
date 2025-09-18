import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# --- Definição da Geometria do Cubo ---

# 8 vértices do cubo
vertices = (
    (1, -1, -1),   # 0
    (1, 1, -1),    # 1
    (-1, 1, -1),   # 2
    (-1, -1, -1),  # 3
    (1, -1, 1),    # 4
    (1, 1, 1),     # 5
    (-1, -1, 1),   # 6
    (-1, 1, 1)     # 7
)

# 12 arestas que conectam os vértices
arestas = (
    (0, 1), (0, 3), (0, 4),
    (2, 1), (2, 3), (2, 7),
    (6, 3), (6, 4), (6, 7),
    (5, 1), (5, 4), (5, 7)
)

# 6 faces quadradas, definidas pelos índices dos vértices
faces = (
    (0, 1, 2, 3),  # Face traseira
    (3, 2, 7, 6),  # Face esquerda
    (6, 7, 5, 4),  # Face frontal
    (4, 5, 1, 0),  # Face direita
    (1, 5, 7, 2),  # Face superior
    (0, 4, 6, 3)   # Face inferior
)

# Cores para cada uma das 6 faces
cores = (
    (1, 0, 0),  # Vermelho
    (0, 1, 0),  # Verde
    (0, 0, 1),  # Azul
    (1, 1, 0),  # Amarelo
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Ciano
)


def desenha_cubo():
    """
    Função para renderizar o cubo face por face.
    """
    # Usamos GL_QUADS para desenhar as faces quadradas.
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        # Define a cor para a face atual
        glColor3fv(cores[i])
        for vertice_idx in face:
            # Passa cada vértice da face para o OpenGL
            glVertex3fv(vertices[vertice_idx])
    glEnd()

    # Opcional: desenhar as arestas em preto para dar contorno
    glColor3fv((0, 0, 0)) # Cor preta
    glBegin(GL_LINES)
    for aresta in arestas:
        for vertice_idx in aresta:
            glVertex3fv(vertices[vertice_idx])
    glEnd()


def main():
    """
    Função principal que inicializa o PyGame e o OpenGL,
    e entra no loop de renderização.
    """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Aula 6 - Modelagem de um Cubo")

    # Configuração da perspectiva da câmera
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Move a câmera para trás para ver o cubo
    # glTranslatef(x, y, z)
    glTranslatef(0.0, 0.0, -5)

    # Habilita o teste de profundidade para renderização 3D correta.
    # É importante para objetos sólidos. Ele funciona comparando a profundidade
    # de cada pixel e garantindo que apenas o pixel mais próximo da câmera.
    glEnable(GL_DEPTH_TEST)

    # Loop principal do programa
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Rotação do objeto ao longo do tempo para melhor visualização
        # glRotatef(angulo, x, y, z)
        glRotatef(1, 3, 1, 1) # Gira 1 grau a cada frame nos eixos x, y, z

        # Limpa o buffer de cor e de profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Chama a função que desenha o cubo
        desenha_cubo()

        # Atualiza a tela
        pygame.display.flip() # Troca os buffers (double buffering)
        pygame.time.wait(10) # Pequena pausa para controlar a velocidade de rotação


if __name__ == "__main__":
    main()