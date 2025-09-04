from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angulo = [0]

# Vértices do cubo
vertices = [
    [1, 1, 1],   # 0
    [1, 1, -1],  # 1
    [1, -1, -1], # 2
    [1, -1, 1],  # 3
    [-1, 1, 1],  # 4
    [-1, 1, -1], # 5
    [-1, -1, -1],# 6
    [-1, -1, 1], # 7
]

# Faces do cubo (cada face tem 4 vértices)
faces = [
    [0,1,2,3], # Direita
    [4,5,6,7], # Esquerda
    [0,1,5,4], # Topo
    [3,2,6,7], # Base
    [0,3,7,4], # Frente
    [1,2,6,5], # Fundo
]

# Cores para cada face
cores = [
    [1,0,0], # Vermelho
    [0,1,0], # Verde
    [0,0,1], # Azul
    [1,1,0], # Amarelo
    [1,0,1], # Magenta
    [0,1,1], # Ciano
]

def desenhar_cubo():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(cores[i])
        for vertice in face:
            glVertex3fv(vertices[vertice])
    glEnd()

def exibir():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(angulo[0], 1, 1, 0)
    desenhar_cubo()
    glutSwapBuffers()

def atualizar():
    angulo[0] += 1
    glutPostRedisplay()

def redimensionar(largura, altura):
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, largura/altura if altura > 0 else 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def principal():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Cubo OpenGL Colorido")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1)
    glutDisplayFunc(exibir)
    glutIdleFunc(atualizar)
    glutReshapeFunc(redimensionar)
    glutMainLoop()

if __name__ == "__main__":
    principal()