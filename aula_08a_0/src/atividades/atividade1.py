import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# --- Variáveis de Configuração ---
LARGURA_JANELA, ALTURA_JANELA = 800, 600
MODO_PROJECAO = "PERSPECTIVA"  # Modo de projeção inicial

# --- Geometria do Cubo ---
vertices_cubo = np.array([
    [1, -1, -1], [1,  1, -1], [-1,  1, -1], [-1, -1, -1],
    [1, -1,  1], [1,  1,  1], [-1, -1,  1], [-1,  1,  1]
], dtype=np.float32)

arestas_cubo = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 7), (3, 6)
)

def desenhar_cubo_wireframe():
    """Desenha um cubo no modo wireframe (linhas)."""
    glColor3fv((1.0, 1.0, 1.0))  # Cor branca para o wireframe
    glBegin(GL_LINES)
    for aresta in arestas_cubo:
        for indice_vertice in aresta:
            glVertex3fv(vertices_cubo[indice_vertice])
    glEnd()

def configurar_projecao():
    """
    Define a matriz de projeção (glMatrixMode(GL_PROJECTION)).
    Aplica glOrtho para Ortográfica ou gluPerspective para Perspectiva.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Zera a matriz de projeção

    if MODO_PROJECAO == "PERSPECTIVA":
        # Projeção Perspectiva: simula profundidade (frustum)
        gluPerspective(45, (LARGURA_JANELA / ALTURA_JANELA), 0.1, 50.0)
        print("Modo: PERSPECTIVA (Sensação de profundidade)")

    elif MODO_PROJECAO == "ORTOGRAFICA":
        # Projeção Ortográfica: preserva dimensões
        glOrtho(-3, 3, -3, 3, 0.1, 50.0)
        print("Modo: ORTOGRÁFICA (Dimensões preservadas)")

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Posição da Câmera: LookAt(posição, alvo, cima)
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)

def principal():
    """Função principal: inicialização e loop de renderização."""
    global MODO_PROJECAO

    pygame.init()
    pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA), DOUBLEBUF | OPENGL)

    glClearColor(0.15, 0.15, 0.15, 1.0)  # Cor de fundo cinza-escuro
    glEnable(GL_DEPTH_TEST)  # Habilita o buffer de profundidade

    configurar_projecao()

    rotacao_x, rotacao_y = 0, 0
    translacao_x, translacao_y = 0, 0
    relogio = pygame.time.Clock()

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            if evento.type == pygame.KEYDOWN:
                # Alterna o modo de projeção ao pressionar a tecla P
                if evento.key == pygame.K_p:
                    MODO_PROJECAO = "ORTOGRAFICA" if MODO_PROJECAO == "PERSPECTIVA" else "PERSPECTIVA"
                    configurar_projecao()

        # Rotação do objeto
        rotacao_x = (rotacao_x + 0.5) % 360
        rotacao_y = (rotacao_y + 0.8) % 360

        translacao_x = (translacao_x + 0.01) % 3  # Move para a direita
        # translacao_y = (translacao_y + 0.005) % 3  # Move para cima

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # --- Aplicação das Transformações Locais (ModelView) ---
        glPushMatrix()
        glTranslatef(translacao_x, translacao_y, 0) # Translação
        # glRotate(rotacao_x, 1, 0, 0)  # Rotação no eixo X
        # glRotate(rotacao_y, 0, 1, 0)  # Rotação no eixo Y

        desenhar_cubo_wireframe()

        glPopMatrix()  # Restaura a matriz ModelView

        pygame.display.flip()
        relogio.tick(30)

    pygame.quit()

if __name__ == "__main__":
    principal()
