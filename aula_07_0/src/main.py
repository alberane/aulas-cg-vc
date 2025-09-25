import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# --- Funções de Quatérnios ---

def normalizar(vetor):
    """Normaliza um vetor."""
    norma = np.linalg.norm(vetor) # Calcula a norma (magnitude) do vetor
    if norma == 0:
        return vetor
    return vetor / norma

def quaternio_de_eixo_angulo(eixo, angulo):
    """Cria um quatérnio a partir de um eixo e ângulo."""
    eixo = normalizar(eixo)
    meio_angulo = angulo / 2.0
    w = np.cos(meio_angulo) # Componente escalar do quatérnio
    x, y, z = eixo * np.sin(meio_angulo) # Componentes vetoriais do quatérnio
    return np.array([w, x, y, z])

def multiplicar_quat(q1, q2):
    """Multiplica dois quatérnios."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def quat_para_matriz(q):
    """Converte um quatérnio para uma matriz de rotação 4x4."""
    w, x, y, z = q
    # Pré-calcular para eficiência
    # Isso ajuda a evitar cálculos repetidos na matriz
    # Os quadros dos componentes são usados várias vezes
    xx, yy, zz = x*x, y*y, z*z
    xy, xz, yz = x*y, x*z, y*z
    wx, wy, wz = w*x, w*y, w*z

    return np.array([
        [1 - 2*(yy + zz), 2*(xy - wz),     2*(xz + wy),     0],
        [2*(xy + wz),     1 - 2*(xx + zz), 2*(yz - wx),     0],
        [2*(xz - wy),     2*(yz + wx),     1 - 2*(xx + yy), 0],
        [0,               0,               0,               1]
    ], dtype=np.float32)

# --- Funções do Trackball ---

def projetar_na_esfera(x, y, largura, altura):
    """Mapeia as coordenadas 2D da tela para um vetor 3D na hemisfera."""
    # Normaliza as coordenadas para o intervalo [-1, 1]
    # O eixo Y é invertido porque as coordenadas da tela crescem para baixo
    coord_x = (2.0 * x / largura) - 1.0
    coord_y = 1.0 - (2.0 * y / altura)

    # Calcula o quadrado do comprimento do vetor 2D a partir do centro
    d_quadrado = coord_x**2 + coord_y**2

    if d_quadrado <= 1.0:
        # Se estiver dentro do círculo unitário, calcula Z
        coord_z = np.sqrt(1.0 - d_quadrado)
    else:
        # Se estiver fora, projeta para o ponto mais próximo na borda
        # Isso mantém a rotação suave quando o mouse está fora do círculo
        coord_x, coord_y = normalizar(np.array([coord_x, coord_y])) * 1.0
        coord_z = 0.0

    return np.array([coord_x, coord_y, coord_z])

# --- Classe Principal ---

class VisualizadorTrackball:
    def __init__(self):
        self.largura, self.altura = 800, 600
        self.rastreando = False # Indica se o mouse está sendo rastreado
        self.ultima_posicao = None # Última posição do mouse na esfera

        # Quatérnio que armazena a orientação atual do objeto
        self.rotacao_atual = np.array([1.0, 0.0, 0.0, 0.0]) # Identidade

        # Inicializa Pygame, GLUT e OpenGL
        pygame.init()
        glutInit()
        pygame.display.set_mode((self.largura, self.altura), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Trackball com Quatérnios")

        self.inicializar_gl()

    def inicializar_gl(self):
        """Configurações iniciais do OpenGL."""
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Configura a iluminação
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])

        # Configura o material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glColor3f(0.8, 0.5, 0.2) # Cor do bule

        # Configura a câmera (perspectiva)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # glFrustum(left, right, bottom, top, near, far) - Define um frustum para a perspectiva.
        # Frustum é um tronco, é uma pirâmide truncada que define o volume visível.
        glFrustum(-1.0, 1.0, -1.0, 1.0, 5.0, 60.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Move a câmera para trás para podermos ver o objeto
        glTranslatef(0.0, 0.0, -15.0)

    def desenhar_cena(self):
        """Desenha a cena."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix() # Salva a matriz atual de modelagem

        # Aplica a rotação do trackball a partir do quatérnio
        matriz_rotacao = quat_para_matriz(self.rotacao_atual)
        glMultMatrixf(matriz_rotacao.T) # OpenGL espera a matriz transposta

        # Desenha o bule de chá
        glutSolidTeapot(2.5)

        glPopMatrix() # Restaura a matriz de modelagem
        pygame.display.flip() # Atualiza a tela

    def executar(self):
        """Loop principal do programa."""
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1: # Botão esquerdo do mouse
                        self.rastreando = True
                        self.ultima_posicao = projetar_na_esfera(evento.pos[0], evento.pos[1], self.largura, self.altura)
                elif evento.type == pygame.MOUSEBUTTONUP:
                    if evento.button == 1:
                        self.rastreando = False
                elif evento.type == pygame.MOUSEMOTION:
                    if self.rastreando:
                        posicao_atual = projetar_na_esfera(evento.pos[0], evento.pos[1], self.largura, self.altura)

                        # Evita calcular rotação se a posição não mudou
                        if np.allclose(self.ultima_posicao, posicao_atual):
                            continue

                        # Calcula o eixo e o ângulo da rotação momentânea
                        # np.cross calcula o produto vetorial de dois vetores
                        eixo = np.cross(self.ultima_posicao, posicao_atual)
                        # np.dot calcula o produto escalar de dois vetores
                        # np.arccos retorna o arco cosseno (ângulo em radianos)
                        angulo = np.arccos(np.dot(self.ultima_posicao, posicao_atual))

                        # Cria o quatérnio para esta rotação
                        delta_rotacao = quaternio_de_eixo_angulo(eixo, angulo * 2.0) # Fator de sensibilidade

                        # Compõe a nova rotação com a orientação atual
                        self.rotacao_atual = multiplicar_quat(delta_rotacao, self.rotacao_atual)

                        self.ultima_posicao = posicao_atual

            self.desenhar_cena()

        pygame.quit()

if __name__ == '__main__':
    visualizador = VisualizadorTrackball()
    visualizador.executar()
