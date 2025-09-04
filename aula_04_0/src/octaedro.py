from math import sqrt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ------------------------------
# Geometria do Octaedro
# ------------------------------
# Vértices: topo, 4 no "equador", e base
vertices = [
    (0.0,  1.0,  0.0),  # 0 topo
    (1.0,  0.0,  0.0),  # 1
    (0.0,  0.0,  1.0),  # 2
    (-1.0, 0.0,  0.0),  # 3
    (0.0,  0.0, -1.0),  # 4
    (0.0, -1.0,  0.0),  # 5 base
]

# Faces triangulares formadas pelos vértices
faces = [
    (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),    # metade superior
    (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4),    # metade inferior
]

# Cores para cada face
cores = [
    (1.0, 0.3, 0.3),
    (1.0, 0.6, 0.2),
    (1.0, 0.9, 0.2),
    (0.5, 1.0, 0.3),
    (0.3, 0.8, 1.0),
    (0.4, 0.5, 1.0),
    (0.7, 0.4, 1.0),
    (1.0, 0.4, 0.8),
]

# ------------------------------
# Estado da câmera e interação
# ------------------------------
rotacaoX, rotacaoY = 20.0, -30.0   # ângulos iniciais
distancia = 4.0                    # distância da câmera

def calcular_normal(a, b, c):
    """Calcula a normal de uma face (a,b,c) com produto vetorial."""
    ax, ay, az = a
    bx, by, bz = b
    cx, cy, cz = c
    ux, uy, uz = (bx - ax, by - ay, bz - az)
    vx, vy, vz = (cx - ax, cy - ay, cz - az)
    # U x V
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    comprimento = sqrt(nx*nx + ny*ny + nz*nz) or 1.0
    return (nx/comprimento, ny/comprimento, nz/comprimento)

def inicializar():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # Iluminação básica
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (3.0, 5.0, 8.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR,(0.4, 0.4, 0.4, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 32.0)

    glClearColor(0.07, 0.07, 0.09, 1.0)

def redimensionar(largura, altura):
    glViewport(0, 0, largura, altura if altura > 0 else 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, largura / float(altura if altura > 0 else 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def desenhar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuração da câmera
    gluLookAt(0.0, 0.0, distancia,   0.0, 0.0, 0.0,    0.0, 1.0, 0.0)

    # Rotação interativa
    glRotatef(rotacaoX, 1.0, 0.0, 0.0)
    glRotatef(rotacaoY, 0.0, 1.0, 0.0)

    # Desenha o octaedro
    glBegin(GL_TRIANGLES)
    for i, (v0, v1, v2) in enumerate(faces):
        a = vertices[v0]
        b = vertices[v1]
        c = vertices[v2]
        nx, ny, nz = calcular_normal(a, b, c)
        glNormal3f(nx, ny, nz)

        r, g, bcor = cores[i % len(cores)]
        glColor3f(r, g, bcor)

        glVertex3f(*a)
        glVertex3f(*b)
        glVertex3f(*c)
    glEnd()

    glutSwapBuffers()

def teclado(tecla, x, y):
    global rotacaoX, rotacaoY, distancia
    t = tecla.decode('utf-8').lower()
    if t == '\x1b':  # ESC
        glutLeaveMainLoop()
        return
    elif t == 'w':
        rotacaoX -= 5.0
    elif t == 's':
        rotacaoX += 5.0
    elif t == 'a':
        rotacaoY -= 5.0
    elif t == 'd':
        rotacaoY += 5.0
    elif t == 'q':
        distancia = max(1.5, distancia - 0.3)   # aproxima
    elif t == 'e':
        distancia = min(20.0, distancia + 0.3)  # afasta
    glutPostRedisplay()

def teclas_especiais(tecla, x, y):
    """Usa as setas para girar também."""
    global rotacaoX, rotacaoY
    if tecla == GLUT_KEY_UP:
        rotacaoX -= 5.0
    elif tecla == GLUT_KEY_DOWN:
        rotacaoX += 5.0
    elif tecla == GLUT_KEY_LEFT:
        rotacaoY -= 5.0
    elif tecla == GLUT_KEY_RIGHT:
        rotacaoY += 5.0
    glutPostRedisplay()

def principal():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 700)
    glutCreateWindow("Octaedro - PyOpenGL")

    inicializar()
    glutDisplayFunc(desenhar)
    glutReshapeFunc(redimensionar)
    glutKeyboardFunc(teclado)
    glutSpecialFunc(teclas_especiais)
    glutMainLoop()

if __name__ == "__main__":
    principal()
