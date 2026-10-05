"""
Código reescrito com variáveis, objetos, funções e classes traduzidos para o português,
mantendo todos os recursos e lógica da aplicação original presente no arquivo atividade.py[cite: 1].
"""

import sys
import math
import numpy as np
import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# =====================================================================
# PARTE 1: MODELAGEM GEOMÉTRICA BASE
# =====================================================================
# Construção do Modelo Geométrico Base (Pirâmide de base quadrada)[cite: 1]
VERTICES_PIRAMIDE = np.array([
    [0.0, 1.0, 0.0],  # 0: Topo
    [-1.0, -1.0, 1.0],  # 1: Frente-Esquerda
    [1.0, -1.0, 1.0],  # 2: Frente-Direita
    [1.0, -1.0, -1.0],  # 3: Trás-Direita
    [-1.0, -1.0, -1.0]  # 4: Trás-Esquerda
], dtype=np.float32)

FACES_PIRAMIDE = [
    (0, 1, 2),  # Face Frontal
    (0, 2, 3),  # Face Direita
    (0, 3, 4),  # Face Traseira
    (0, 4, 1),  # Face Esquerda
    (1, 4, 3),  # Triângulo 1 da Base
    (1, 3, 2)  # Triângulo 2 da Base
]


# =====================================================================
# PARTE 2: TRANSFORMAÇÕES GEOMÉTRICAS E ÁLGEBRA LINEAR
# =====================================================================
def matriz_translacao(tx, ty, tz):
    """ Retorna uma Matriz 4x4 de Translação em coordenadas homogêneas[cite: 1]. """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def matriz_escala(sx, sy, sz):
    """ Retorna uma Matriz 4x4 de Escala em coordenadas homogêneas[cite: 1]. """
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# =====================================================================
# PARTE 3: ILUMINAÇÃO, VETORES NORMAIS E MODELOS DE COR (OPENCV)
# =====================================================================
def calcular_normal(v0, v1, v2):
    """ Cálculo de Vetores Normais usando produto vetorial: N = (V1 - V0) x (V2 - V0)[cite: 1]. """
    vetor_u = v1 - v0
    vetor_v = v2 - v0
    normal = np.cross(vetor_u, vetor_v)
    magnitude_normal = np.linalg.norm(normal)

    if magnitude_normal > 0:
        normal = normal / magnitude_normal
    return normal


def obter_cor_pelo_opencv(valor_matiz):
    """
    Utiliza a biblioteca OpenCV para gerar uma cor baseada no canal Matiz (HSV)[cite: 1].
    O valor gerado é convertido para RGB normalizado entre 0 e 1, compatível com OpenGL[cite: 1].
    """
    # O limite do valor de Matiz (Hue) no OpenCV é de 0 a 179[cite: 1]
    cor_hsv = np.uint8([[[valor_matiz, 200, 255]]])
    cor_rgb = cv2.cvtColor(cor_hsv, cv2.COLOR_HSV2RGB)

    vermelho = cor_rgb[0][0][0] / 255.0
    verde = cor_rgb[0][0][1] / 255.0
    azul = cor_rgb[0][0][2] / 255.0

    return vermelho, verde, azul


def configurar_iluminacao():
    """ Habilita e configura os parâmetros de Iluminação, Sombreamento e Profundidade[cite: 1]. """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Definição dos componentes da luz ambiente, difusa, especular e posicionamento[cite: 1]
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)


# =====================================================================
# PARTE 4: INTERATIVIDADE AVANÇADA COM QUATÉRNIOS E TRACKBALL VIRTUAL
# =====================================================================
class Quaternio:
    """ Representação matemática de rotações para evitar problemas como o Gimbal Lock[cite: 1]. """

    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def multiplicar(self, outro_quaternio):
        """ Realiza a composição de duas rotações multiplicando os quatérnios[cite: 1]. """
        novo_w = self.w * outro_quaternio.w - self.x * outro_quaternio.x - self.y * outro_quaternio.y - self.z * outro_quaternio.z
        novo_x = self.w * outro_quaternio.x + self.x * outro_quaternio.w + self.y * outro_quaternio.z - self.z * outro_quaternio.y
        novo_y = self.w * outro_quaternio.y - self.x * outro_quaternio.z + self.y * outro_quaternio.w + self.z * outro_quaternio.x
        novo_z = self.w * outro_quaternio.z + self.x * outro_quaternio.y - self.y * outro_quaternio.x + self.z * outro_quaternio.w
        return Quaternio(novo_w, novo_x, novo_y, novo_z)

    def para_matriz_opengl(self):
        """ Converte o quatérnio para uma matriz de rotação 4x4 no layout exigido pelo OpenGL[cite: 1]. """
        xx, xy, xz, xw = self.x ** 2, self.x * self.y, self.x * self.z, self.x * self.w
        yy, yz, yw = self.y ** 2, self.y * self.z, self.y * self.w
        zz, zw = self.z ** 2, self.z * self.w

        matriz = np.identity(4, dtype=np.float32)
        matriz[0, 0] = 1 - 2 * (yy + zz)
        matriz[0, 1] = 2 * (xy - zw)
        matriz[0, 2] = 2 * (xz + yw)

        matriz[1, 0] = 2 * (xy + zw)
        matriz[1, 1] = 1 - 2 * (xx + zz)
        matriz[1, 2] = 2 * (yz - xw)

        matriz[2, 0] = 2 * (xz - yw)
        matriz[2, 1] = 2 * (yz + xw)
        matriz[2, 2] = 1 - 2 * (xx + yy)

        # O OpenGL utiliza o layout de ordenação por coluna, por isso a matriz deve ser transposta[cite: 1]
        return matriz.T


def mapear_coordenadas_para_esfera(mouse_x, mouse_y, largura_tela, altura_tela):
    """ Mapeia as coordenadas 2D do mouse para uma hemisfério 3D simulando um Trackball[cite: 1]. """
    coord_normalizada_x = (2.0 * mouse_x - largura_tela) / largura_tela
    coord_normalizada_y = (altura_tela - 2.0 * mouse_y) / altura_tela
    raio_quadrado = coord_normalizada_x ** 2 + coord_normalizada_y ** 2

    if raio_quadrado <= 1.0:
        coord_normalizada_z = math.sqrt(1.0 - raio_quadrado)
    else:
        magnitude = math.sqrt(raio_quadrado)
        coord_normalizada_x /= magnitude
        coord_normalizada_y /= magnitude
        coord_normalizada_z = 0.0

    return np.array([coord_normalizada_x, coord_normalizada_y, coord_normalizada_z])


# =====================================================================
# LOOP PRINCIPAL DO APLICATIVO
# =====================================================================
def funcao_principal():
    pygame.init()
    dimensoes_tela = (800, 600)
    pygame.display.set_mode(dimensoes_tela, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Aplicação Interativa 3D - Computação Gráfica")

    # Configuração de câmera: projeção em perspectiva[cite: 1]
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (dimensoes_tela[0] / dimensoes_tela[1]), 0.1, 50.0)

    configurar_iluminacao()

    # Ajuste do espaço e posição da câmera na cena[cite: 1]
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 2, 5,  # Posição onde a câmera está
              0, 0, 0,  # Ponto para onde a câmera aponta (Foco)
              0, 1, 0)  # Orientação do vetor Para Cima (Up)

    # Inicialização das variáveis de controle de interatividade[cite: 1]
    quaternio_acumulado = Quaternio()
    arrastando_mouse = False
    ultima_posicao_esfera_mouse = None

    # Inicialização da cor do objeto usando OpenCV[cite: 1]
    valor_matiz_atual = 100
    cor_renderizacao = obter_cor_pelo_opencv(valor_matiz_atual)

    controle_tempo = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gerenciamento de eventos de clique e movimento do mouse[cite: 1]
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    arrastando_mouse = True
                    ultima_posicao_esfera_mouse = mapear_coordenadas_para_esfera(evento.pos[0], evento.pos[1],
                                                                                 dimensoes_tela[0], dimensoes_tela[1])

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastando_mouse = False

            elif evento.type == pygame.MOUSEMOTION:
                if arrastando_mouse:
                    posicao_atual_esfera_mouse = mapear_coordenadas_para_esfera(evento.pos[0], evento.pos[1],
                                                                                dimensoes_tela[0], dimensoes_tela[1])

                    # Determinação do eixo de rotação através do produto vetorial[cite: 1]
                    eixo_rotacao = np.cross(ultima_posicao_esfera_mouse, posicao_atual_esfera_mouse)
                    magnitude_eixo = np.linalg.norm(eixo_rotacao)

                    if magnitude_eixo > 1e-5:
                        eixo_rotacao = eixo_rotacao / magnitude_eixo

                        # Determinação do ângulo de rotação através do produto escalar[cite: 1]
                        produto_escalar = np.dot(ultima_posicao_esfera_mouse, posicao_atual_esfera_mouse)
                        produto_escalar = max(-1.0, min(1.0, produto_escalar))
                        angulo_rotacao = math.acos(produto_escalar)

                        # Construção do quatérnio unitário correspondente ao movimento (q = [cos(a/2), sen(a/2)*v])[cite: 1]
                        seno_meio_angulo = math.sin(angulo_rotacao / 2.0)
                        quaternio_movimento = Quaternio(
                            math.cos(angulo_rotacao / 2.0),
                            eixo_rotacao[0] * seno_meio_angulo,
                            eixo_rotacao[1] * seno_meio_angulo,
                            eixo_rotacao[2] * seno_meio_angulo
                        )

                        # Multiplicação para acumular a nova orientação à orientação existente[cite: 1]
                        quaternio_acumulado = quaternio_movimento.multiplicar(quaternio_acumulado)

                    ultima_posicao_esfera_mouse = posicao_atual_esfera_mouse

            # Alteração dinâmica de cor do material usando os direcionais do teclado[cite: 1]
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    valor_matiz_atual = (valor_matiz_atual + 10) % 180
                    cor_renderizacao = obter_cor_pelo_opencv(valor_matiz_atual)
                elif evento.key == pygame.K_LEFT:
                    valor_matiz_atual = (valor_matiz_atual - 10) % 180
                    cor_renderizacao = obter_cor_pelo_opencv(valor_matiz_atual)

        # Limpeza dos buffers de cor e de profundidade antes de cada quadro[cite: 1]
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Conversão do quatérnio final para matriz 4x4 e aplicação no pipeline de renderização[cite: 1]
        matriz_rotacao_final = quaternio_acumulado.para_matriz_opengl()
        glMultMatrixf(matriz_rotacao_final)

        # Processo de renderização do modelo 3D calculando vetores normais para reflexão de luz[cite: 1]
        glColor3f(*cor_renderizacao)
        glBegin(GL_TRIANGLES)
        for face in FACES_PIRAMIDE:
            vertice_0 = VERTICES_PIRAMIDE[face[0]]
            vertice_1 = VERTICES_PIRAMIDE[face[1]]
            vertice_2 = VERTICES_PIRAMIDE[face[2]]

            # Cálculo e aplicação do vetor normal da face atual[cite: 1]
            vetor_normal_face = calcular_normal(vertice_0, vertice_1, vertice_2)
            glNormal3fv(vetor_normal_face)

            # Desenho dos vértices que compõem a face[cite: 1]
            glVertex3fv(vertice_0)
            glVertex3fv(vertice_1)
            glVertex3fv(vertice_2)
        glEnd()

        glPopMatrix()
        pygame.display.flip()

        # Limite da taxa de atualização travado em 60 quadros por segundo[cite: 1]
        controle_tempo.tick(60)


if __name__ == "__main__":
    funcao_principal()