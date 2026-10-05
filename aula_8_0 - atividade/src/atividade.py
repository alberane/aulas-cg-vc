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
# Construção do Modelo Geométrico Base (Pirâmide de base quadrada)
VERTICES = np.array([
    [0.0, 1.0, 0.0],  # 0: Topo
    [-1.0, -1.0, 1.0],  # 1: Frente-Esquerda
    [1.0, -1.0, 1.0],  # 2: Frente-Direita
    [1.0, -1.0, -1.0],  # 3: Trás-Direita
    [-1.0, -1.0, -1.0]  # 4: Trás-Esquerda
], dtype=np.float32)

FACES = [
    (0, 1, 2),  # Face Frente
    (0, 2, 3),  # Face Direita
    (0, 3, 4),  # Face Trás
    (0, 4, 1),  # Face Esquerda
    (1, 4, 3),  # Base triângulo 1
    (1, 3, 2)  # Base triângulo 2
]


# =====================================================================
# PARTE 2: TRANSFORMAÇÕES GEOMÉTRICAS E ÁLGEBRA LINEAR
# =====================================================================
def mat_translation(tx, ty, tz):
    """ Matriz 4x4 de Translação em coordenadas homogêneas """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def mat_scale(sx, sy, sz):
    """ Matriz 4x4 de Escala em coordenadas homogêneas """
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# =====================================================================
# PARTE 3: ILUMINAÇÃO, VETORES NORMAIS E MODELOS DE COR (OPENCV)
# =====================================================================
def compute_normal(v0, v1, v2):
    """ Cálculo de Normais: N = (V1 - V0) x (V2 - V0) """
    u = v1 - v0
    v = v2 - v0
    n = np.cross(u, v)
    norm = np.linalg.norm(n)
    if norm > 0:
        n = n / norm
    return n


def get_color_from_opencv(hue_value):
    """
    Utiliza OpenCV para gerar uma cor baseada em limites de matriz (HSV).
    Converte para RGB normalizado [0, 1] para o OpenGL.
    """
    # O valor de Hue no OpenCV varia de 0 a 179
    hsv = np.uint8([[[hue_value, 200, 255]]])
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return rgb[0][0][0] / 255.0, rgb[0][0][1] / 255.0, rgb[0][0][2] / 255.0


def setup_lighting():
    """ Configuração de Iluminação e Sombreamento """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)  # Habilita teste de profundidade
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Componentes da luz ambiente, difusa e especular
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)


# =====================================================================
# PARTE 4: INTERATIVIDADE AVANÇADA COM QUATÉRNIOS E TRACKBALL VIRTUAL
# =====================================================================
class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, q):
        """ Composição de rotações multiplicando quatérnios """
        w = self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z
        x = self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y
        y = self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x
        z = self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w
        return Quaternion(w, x, y, z)

    def to_matrix(self):
        """ Converter para matriz de rotação 4x4 (Layout para OpenGL) """
        xx, xy, xz, xw = self.x ** 2, self.x * self.y, self.x * self.z, self.x * self.w
        yy, yz, yw = self.y ** 2, self.y * self.z, self.y * self.w
        zz, zw = self.z ** 2, self.z * self.w

        m = np.identity(4, dtype=np.float32)
        m[0, 0] = 1 - 2 * (yy + zz)
        m[0, 1] = 2 * (xy - zw)
        m[0, 2] = 2 * (xz + yw)

        m[1, 0] = 2 * (xy + zw)
        m[1, 1] = 1 - 2 * (xx + zz)
        m[1, 2] = 2 * (yz - xw)

        m[2, 0] = 2 * (xz - yw)
        m[2, 1] = 2 * (yz + xw)
        m[2, 2] = 1 - 2 * (xx + yy)

        # O OpenGL utiliza layout de coluna, logo aplicamos a transposta
        return m.T


def map_to_sphere(mouse_x, mouse_y, width, height):
    """ Mapeamento de Coordenadas 2D para a Hemisfério 3D (Trackball) """
    nx = (2.0 * mouse_x - width) / width
    ny = (height - 2.0 * mouse_y) / height
    r2 = nx * nx + ny * ny

    if r2 <= 1.0:
        nz = math.sqrt(1.0 - r2)
    else:
        mag = math.sqrt(r2)
        nx /= mag
        ny /= mag
        nz = 0.0
    return np.array([nx, ny, nz])


# =====================================================================
# LOOP PRINCIPAL DO APLICATIVO
# =====================================================================
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Aplicação Interativa 3D - Computação Gráfica")

    # Configurar projeção em perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    setup_lighting()

    # Espaço da Câmera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 2, 5,  # Posição da Câmera
              0, 0, 0,  # Foco
              0, 1, 0)  # Vetor Up

    # Variáveis de Controle
    current_quat = Quaternion()
    is_dragging = False
    last_mouse_pos = None

    # Cor inicial usando OpenCV
    hue_val = 100
    obj_color = get_color_from_opencv(hue_val)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Capturar eventos de clique e arraste do mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_dragging = True
                    last_mouse_pos = map_to_sphere(event.pos[0], event.pos[1], display[0], display[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    current_mouse_pos = map_to_sphere(event.pos[0], event.pos[1], display[0], display[1])

                    # Determinar eixo de rotação via produto vetorial
                    axis = np.cross(last_mouse_pos, current_mouse_pos)
                    mag = np.linalg.norm(axis)

                    if mag > 1e-5:
                        axis = axis / mag
                        # Determinar ângulo via produto escalar
                        dot = np.dot(last_mouse_pos, current_mouse_pos)
                        dot = max(-1.0, min(1.0, dot))
                        angle = math.acos(dot)

                        # Construir quatérnio unitário (q = [cos(a/2), sin(a/2)*v])
                        s = math.sin(angle / 2.0)
                        rot_quat = Quaternion(math.cos(angle / 2.0), axis[0] * s, axis[1] * s, axis[2] * s)

                        # Multiplicar pelo quatérnio atual para acumular a orientação
                        current_quat = rot_quat.multiply(current_quat)

                    last_mouse_pos = current_mouse_pos

            # Interatividade dinâmica: alterar cor de material via OpenCV (Setas Direita/Esquerda)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hue_val = (hue_val + 10) % 180
                    obj_color = get_color_from_opencv(hue_val)
                elif event.key == pygame.K_LEFT:
                    hue_val = (hue_val - 10) % 180
                    obj_color = get_color_from_opencv(hue_val)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Converter quatérnio final acumulado em matriz 4x4 e enviar ao pipeline
        rot_matrix = current_quat.to_matrix()
        glMultMatrixf(rot_matrix)

        # Renderização do Modelo 3D com Normais
        glColor3f(*obj_color)
        glBegin(GL_TRIANGLES)
        for face in FACES:
            v0, v1, v2 = VERTICES[face[0]], VERTICES[face[1]], VERTICES[face[2]]

            # Aplicar vetor normal da face
            normal = compute_normal(v0, v1, v2)
            glNormal3fv(normal)

            # Desenhar os vértices
            glVertex3fv(v0)
            glVertex3fv(v1)
            glVertex3fv(v2)
        glEnd()

        glPopMatrix()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()