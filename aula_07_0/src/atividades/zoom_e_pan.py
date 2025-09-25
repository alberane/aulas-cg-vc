# visualizador_completo.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# --- Funções de Quatérnios (traduzidas) ---

def normalizar(vetor):
    """Normaliza um vetor."""
    norma = np.linalg.norm(vetor)
    if norma == 0:
        return vetor
    return vetor / norma

def quaternio_de_eixo_angulo(eixo, angulo):
    """Cria um quatérnio a partir de um eixo e ângulo."""
    eixo = normalizar(eixo)
    meio_angulo = angulo / 2.0
    w = np.cos(meio_angulo)
    x, y, z = eixo * np.sin(meio_angulo)
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
    xx, yy, zz = x*x, y*y, z*z
    xy, xz, yz = x*y, x*z, y*z
    wx, wy, wz = w*x, w*y, w*z
    return np.array([
        [1 - 2*(yy + zz), 2*(xy - wz),     2*(xz + wy),     0],
        [2*(xy + wz),     1 - 2*(xx + zz), 2*(yz - wx),     0],
        [2*(xz - wy),     2*(yz + wx),     1 - 2*(xx + yy), 0],
        [0,               0,               0,               1]
    ], dtype=np.float32)

# --- Funções do Trackball (traduzidas) ---

def projetar_na_esfera(x, y, largura, altura):
    """Mapeia as coordenadas 2D da tela para um vetor 3D na hemisfera."""
    coord_x = (2.0 * x / largura) - 1.0
    coord_y = 1.0 - (2.0 * y / altura)
    d_quadrado = coord_x**2 + coord_y**2
    if d_quadrado <= 1.0:
        coord_z = np.sqrt(1.0 - d_quadrado)
    else:
        coord_x, coord_y = normalizar(np.array([coord_x, coord_y]))
        coord_z = 0.0
    return np.array([coord_x, coord_y, coord_z])

# --- Classe Principal com Zoom e Pan ---

class VisualizadorAvancado:
    def __init__(self):
        self.largura, self.altura = 800, 600

        # --- Variáveis de estado para interações ---
        # Rotação (Trackball)
        self.rastreando_rotacao = False
        self.ultima_pos_rotacao = None
        self.rotacao_atual = np.array([1.0, 0.0, 0.0, 0.0]) # Identidade

        # Panorâmica (Pan)
        self.rastreando_pan = False
        self.ultima_pos_pan = None
        self.vetor_pan = np.array([0.0, 0.0, 0.0])

        # Zoom
        self.nivel_zoom = -15.0

        # Inicializa Pygame, GLUT e OpenGL
        pygame.init()
        glutInit()
        pygame.display.set_mode((self.largura, self.altura), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Trackball com Zoom e Panorâmica")

        self.inicializar_gl()

    def inicializar_gl(self):
        """Configurações iniciais do OpenGL."""
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glColor3f(0.8, 0.5, 0.2)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -1.0, 1.0, 5.0, 60.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def desenhar_cena(self):
        """Desenha a cena."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        # 1. Aplica o Zoom e a Panorâmica (transformações da câmera/visão)
        glTranslatef(self.vetor_pan[0], self.vetor_pan[1], self.nivel_zoom)

        # 2. Aplica a rotação do trackball (transformação do modelo)
        matriz_rotacao = quat_para_matriz(self.rotacao_atual)
        glMultMatrixf(matriz_rotacao.T)

        # 3. Desenha o objeto
        glutSolidTeapot(2.5)

        pygame.display.flip()

    def processar_evento(self, evento):
        """Processa um único evento do Pygame."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Rotação (botão esquerdo)
            if evento.button == 1:
                self.rastreando_rotacao = True
                self.ultima_pos_rotacao = projetar_na_esfera(evento.pos[0], evento.pos[1], self.largura, self.altura)
            # Panorâmica (botão direito)
            elif evento.button == 3:
                self.rastreando_pan = True
                self.ultima_pos_pan = evento.pos
            # Zoom (roda de rolagem)
            elif evento.button == 4: # Rolar para cima
                self.nivel_zoom = min(-5.1, self.nivel_zoom + 0.5)
            elif evento.button == 5: # Rolar para baixo
                self.nivel_zoom = max(-50.0, self.nivel_zoom - 0.5)

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                self.rastreando_rotacao = False
            elif evento.button == 3:
                self.rastreando_pan = False

        elif evento.type == pygame.MOUSEMOTION:
            if self.rastreando_rotacao:
                self.processar_rotacao(evento)
            if self.rastreando_pan:
                self.processar_pan(evento)

    def processar_rotacao(self, evento):
        """Calcula a rotação do trackball."""
        pos_atual = projetar_na_esfera(evento.pos[0], evento.pos[1], self.largura, self.altura)
        if np.allclose(self.ultima_pos_rotacao, pos_atual):
            return
        eixo = np.cross(self.ultima_pos_rotacao, pos_atual)
        angulo = np.arccos(np.dot(self.ultima_pos_rotacao, pos_atual))
        delta_rotacao = quaternio_de_eixo_angulo(eixo, angulo * 2.0)
        self.rotacao_atual = multiplicar_quat(delta_rotacao, self.rotacao_atual)
        self.ultima_pos_rotacao = pos_atual

    def processar_pan(self, evento):
        """Calcula o movimento de panorâmica."""
        pos_atual = evento.pos
        dx = pos_atual[0] - self.ultima_pos_pan[0]
        dy = pos_atual[1] - self.ultima_pos_pan[1]

        # Inverte dy porque o eixo Y da tela é invertido
        # A sensibilidade do pan é ajustada com base na distância da câmera
        sensibilidade = 0.001 * abs(self.nivel_zoom)
        self.vetor_pan[0] += dx * sensibilidade
        self.vetor_pan[1] -= dy * sensibilidade

        self.ultima_pos_pan = pos_atual

    def executar(self):
        """Loop principal do programa."""
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                self.processar_evento(evento)

            self.desenhar_cena()

        pygame.quit()

if __name__ == '__main__':
    # Para executar, certifique-se de ter as bibliotecas instaladas:
    # pip install numpy PyOpenGL PyOpenGL-accelerate pygame
    visualizador = VisualizadorAvancado()
    visualizador.executar()
