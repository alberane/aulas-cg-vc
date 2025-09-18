import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# --- Definição da Geometria do Cubo ---

# Vetores normais para cada uma das 6 faces do cubo
normais = (
    (0, 0, -1),  # Face traseira
    (-1, 0, 0),  # Face esquerda
    (0, 0, 1),   # Face frontal
    (1, 0, 0),   # Face direita
    (0, 1, 0),   # Face superior
    (0, -1, 0)   # Face inferior
)

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
    """Renderiza o cubo face por face."""
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normais[i])
        glColor3fv(cores[i])
        for vertice_idx in face:
            glVertex3fv(vertices[vertice_idx])
    glEnd()

    # Desenhar as arestas em preto para dar contorno
    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for aresta in arestas:
        for vertice_idx in aresta:
            glVertex3fv(vertices[vertice_idx])
    glEnd()


def main():
    """Inicializa o PyGame e o OpenGL, e entra no loop de renderização."""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Aula 6 - Modelagem de um Cubo")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)

    glEnable(GL_DEPTH_TEST)


    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # Configuração da luz 0 (GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        desenha_cubo()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
