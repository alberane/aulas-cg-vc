import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# ========== CONFIGURAÇÕES ==========
LARGURA_JANELA, ALTURA_JANELA = 1000, 700
MODO_PROJECAO = "PERSPECTIVA"
VELOCIDADE_ROTACAO = 2
FIGURA_ATUAL = "cubo"

# ========== CORES ==========
COR_BRANCO = (1.0, 1.0, 1.0)
COR_VERMELHO = (1.0, 0.2, 0.2)
COR_VERDE = (0.2, 1.0, 0.2)
COR_AZUL = (0.2, 0.2, 1.0)
COR_AMARELO = (1.0, 1.0, 0.2)
COR_CIANO = (0.2, 1.0, 1.0)
COR_MAGENTA = (1.0, 0.2, 1.0)

# ========== GEOMETRIAS 3D ==========
class GeometriaBasica:
    """Classe base para geometrias 3D."""
    def __init__(self, nome):
        self.nome = nome
        self.vertices = np.array([], dtype=np.float32)
        self.arestas = []
        self.cores_vertices = []

    def desenhar(self):
        """Desenha a geometria usando wireframe."""
        glBegin(GL_LINES)
        for i, aresta in enumerate(self.arestas):
            indice1, indice2 = aresta
            cor = self.cores_vertices[i % len(self.cores_vertices)]
            glColor3fv(cor)
            glVertex3fv(self.vertices[indice1])
            glVertex3fv(self.vertices[indice2])
        glEnd()


class Cubo(GeometriaBasica):
    """Um cubo vibrante com cores nas arestas."""
    def __init__(self):
        super().__init__("Cubo")
        self.vertices = np.array([
            [1, -1, -1], [1,  1, -1], [-1,  1, -1], [-1, -1, -1],
            [1, -1,  1], [1,  1,  1], [-1, -1,  1], [-1,  1,  1]
        ], dtype=np.float32)

        self.arestas = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 7), (7, 6), (6, 4),
            (0, 4), (1, 5), (2, 7), (3, 6)
        )

        self.cores_vertices = [
            COR_VERMELHO, COR_VERDE, COR_AZUL, COR_AMARELO,
            COR_CIANO, COR_MAGENTA, COR_BRANCO
        ]


class Piramide(GeometriaBasica):
    """Uma pirâmide colorida."""
    def __init__(self):
        super().__init__("Pirâmide")
        self.vertices = np.array([
            [0,  2, 0],      # Ápice
            [1, -1,  1],     # Base
            [-1, -1,  1],
            [-1, -1, -1],
            [1, -1, -1]
        ], dtype=np.float32)

        self.arestas = (
            (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 2), (2, 3), (3, 4), (4, 1)
        )

        self.cores_vertices = [
            COR_AMARELO, COR_VERMELHO, COR_VERDE, COR_AZUL, COR_CIANO
        ]


class Octaedro(GeometriaBasica):
    """Um octaedro (dois tetraedros unidos)."""
    def __init__(self):
        super().__init__("Octaedro")
        self.vertices = np.array([
            [0,  1.5, 0],     # Topo
            [1.5, 0, 0],      # Direita
            [0, 0,  1.5],     # Frente
            [-1.5, 0, 0],     # Esquerda
            [0, 0, -1.5],     # Trás
            [0, -1.5, 0]      # Fundo
        ], dtype=np.float32)

        self.arestas = (
            (0, 1), (0, 2), (0, 3), (0, 4),
            (5, 1), (5, 2), (5, 3), (5, 4),
            (1, 2), (2, 3), (3, 4), (4, 1)
        )

        self.cores_vertices = [
            COR_MAGENTA, COR_CIANO, COR_VERDE, COR_AMARELO,
            COR_AZUL, COR_VERMELHO
        ]


class Cilindro(GeometriaBasica):
    """Um cilindro wireframe (ideal para demonstrar projeção)."""
    def __init__(self, raio=1.0, altura=2.0, segmentos=16):
        super().__init__("Cilindro")

        # Criar vértices
        vertices_lista = []
        for i in range(segmentos):
            angulo = 2 * math.pi * i / segmentos
            x = raio * math.cos(angulo)
            z = raio * math.sin(angulo)
            vertices_lista.append([x, altura/2, z])      # Topo
            vertices_lista.append([x, -altura/2, z])     # Base

        self.vertices = np.array(vertices_lista, dtype=np.float32)

        # Criar arestas
        arestas_lista = []
        for i in range(segmentos):
            idx_atual = (i * 2) % (segmentos * 2)
            idx_prox = ((i + 1) * 2) % (segmentos * 2)

            # Arestas circulares no topo e base
            arestas_lista.append((idx_atual, idx_prox))
            arestas_lista.append((idx_atual + 1, idx_prox + 1))
            # Arestas verticais
            arestas_lista.append((idx_atual, idx_atual + 1))

        self.arestas = tuple(arestas_lista)

        # Cores alternadas
        self.cores_vertices = [COR_CIANO, COR_MAGENTA]


# ========== FUNÇÕES DE RENDERIZAÇÃO ==========
def configurar_projecao():
    """Configura a matriz de projeção."""
    global MODO_PROJECAO

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if MODO_PROJECAO == "PERSPECTIVA":
        gluPerspective(45, (LARGURA_JANELA / ALTURA_JANELA), 0.1, 50.0)
    elif MODO_PROJECAO == "ORTOGRAFICA":
        glOrtho(-4, 4, -3, 3, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, -8, 0, 0, 0, 0, 1, 0)


def desenhar_grid(tamanho=5, linhas=10):
    """Desenha um grid de referência no chão."""
    glColor3fv((0.4, 0.4, 0.4))
    glBegin(GL_LINES)
    for i in range(-linhas, linhas + 1):
        escala = tamanho / linhas
        coord = i * escala
        glVertex3f(-tamanho, -2.5, coord)
        glVertex3f(tamanho, -2.5, coord)
        glVertex3f(coord, -2.5, -tamanho)
        glVertex3f(coord, -2.5, tamanho)
    glEnd()


def desenhar_eixos():
    """Desenha os eixos X, Y, Z para referência."""
    glLineWidth(2)
    glBegin(GL_LINES)

    # Eixo X - Vermelho
    glColor3fv(COR_VERMELHO)
    glVertex3f(-3, 0, 0)
    glVertex3f(3, 0, 0)

    # Eixo Y - Verde
    glColor3fv(COR_VERDE)
    glVertex3f(0, -3, 0)
    glVertex3f(0, 3, 0)

    # Eixo Z - Azul
    glColor3fv(COR_AZUL)
    glVertex3f(0, 0, -3)
    glVertex3f(0, 0, 3)

    glEnd()
    glLineWidth(1)


def mostrar_informacoes(fonte, tela_pygame, modo, figura):
    """Exibe informações na tela usando pygame."""
    texto_modo = f"Modo: {modo} | Figura: {figura}"
    texto_controle = "P: Alternar Projeção | SETAS: Trocar Figura"
    texto_dica = "Observe a diferença de profundidade entre as projeções!"

    surf_modo = fonte.render(texto_modo, True, (255, 255, 255))
    surf_controle = fonte.render(texto_controle, True, (200, 200, 200))
    surf_dica = fonte.render(texto_dica, True, (100, 200, 255))

    tela_pygame.blit(surf_modo, (10, 10))
    tela_pygame.blit(surf_controle, (10, 35))
    tela_pygame.blit(surf_dica, (10, 60))


# ========== FUNÇÃO PRINCIPAL ==========
def principal():
    """Função principal - Loop de renderização."""
    global MODO_PROJECAO, FIGURA_ATUAL

    pygame.init()
    tela_pygame = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA),
                                          DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Visualizador de Projeções 3D")
    fonte = pygame.font.Font(None, 24)

    glClearColor(0.1, 0.1, 0.15, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    configurar_projecao()

    # Criar as figuras
    figuras = {
        "cubo": Cubo(),
        "piramide": Piramide(),
        "octaedro": Octaedro(),
        "cilindro": Cilindro()
    }

    rotacao_x, rotacao_y, rotacao_z = 0, 0, 0
    relogio = pygame.time.Clock()
    executando = True

    print("=" * 60)
    print("VISUALIZADOR DE PROJEÇÕES EM COMPUTAÇÃO GRÁFICA")
    print("=" * 60)
    print(f"Modo: {MODO_PROJECAO}")
    print(f"Figura: {FIGURA_ATUAL.upper()}")
    print("Controles:")
    print("  P - Alternar entre Projeção Perspectiva e Ortográfica")
    print("  <-- --> - Trocar figura (Cubo, Pirâmide, Octaedro, Cilindro)")
    print("  ESC - Sair")
    print("=" * 60)

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            if evento.type == pygame.KEYDOWN:
                # Alternar projeção
                if evento.key == pygame.K_p:
                    MODO_PROJECAO = "ORTOGRAFICA" if MODO_PROJECAO == "PERSPECTIVA" else "PERSPECTIVA"
                    configurar_projecao()
                    print(f"Projeção alterada para: {MODO_PROJECAO}")

                # Trocar figuras
                if evento.key == pygame.K_LEFT:
                    figuras_nomes = list(figuras.keys())
                    idx_atual = figuras_nomes.index(FIGURA_ATUAL)
                    FIGURA_ATUAL = figuras_nomes[(idx_atual - 1) % len(figuras_nomes)]
                    print(f"Figura alterada para: {FIGURA_ATUAL.upper()}")

                if evento.key == pygame.K_RIGHT:
                    figuras_nomes = list(figuras.keys())
                    idx_atual = figuras_nomes.index(FIGURA_ATUAL)
                    FIGURA_ATUAL = figuras_nomes[(idx_atual + 1) % len(figuras_nomes)]
                    print(f"Figura alterada para: {FIGURA_ATUAL.upper()}")

                if evento.key == pygame.K_ESCAPE:
                    executando = False

        # Atualizar rotações
        rotacao_x = (rotacao_x + VELOCIDADE_ROTACAO * 0.5) % 360
        rotacao_y = (rotacao_y + VELOCIDADE_ROTACAO * 0.8) % 360
        rotacao_z = (rotacao_z + VELOCIDADE_ROTACAO * 0.3) % 360

        # Limpar tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Renderizar
        glPushMatrix()

        # Grid de referência
        desenhar_grid()

        # Eixos de referência
        desenhar_eixos()

        # Aplicar transformações
        glTranslatef(0, -0.5, 0)
        glRotatef(rotacao_x, 1, 0, 0)
        glRotatef(rotacao_y, 0, 1, 0)
        glRotatef(rotacao_z, 0, 0, 1)

        # Desenhar figura atual
        figuras[FIGURA_ATUAL].desenhar()

        glPopMatrix()

        # Renderizar informações 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, LARGURA_JANELA, ALTURA_JANELA, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        mostrar_informacoes(fonte, tela_pygame, MODO_PROJECAO, FIGURA_ATUAL.upper())
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        relogio.tick(30)

    pygame.quit()

if __name__ == "__main__":
    principal()