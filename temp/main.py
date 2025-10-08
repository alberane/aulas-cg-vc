from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Vértices/faces
phi = (1.0 + math.sqrt(5.0)) / 2.0

ICOSAHEDRON_VERTICES = [
    [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
    [0, -1,  phi], [0,  1,  phi], [0, -1, -phi], [0,  1, -phi],
    [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1]
]

ICOSAHEDRON_FACES = [
    (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
    (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
    (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
    (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
]

# Cores para diferenciar faces
FACE_COLORS = [
    (1,0,0),(0,1,0),(0,0,1),
    (1,1,0),(1,0,1),(0,1,1),
    (0.9,0.5,0.2),(0.5,0.8,0.2),
    (0.8,0.2,0.5),(0.2,0.7,0.9),
    (0.7,0.7,0.7),(0.4,0.4,0.9),
    (0.9,0.6,0.1),(0.1,0.9,0.6),
    (0.6,0.1,0.9),(0.9,0.3,0.3),
    (0.3,0.9,0.3),(0.3,0.3,0.9),
    (0.7,0.5,0.3),(0.3,0.5,0.7)
]

# Animação
rotation_angle_x = 0.0
rotation_angle_y = 0.0
rotation_angle_z = 0.0
rotation_axis = 'y'

def draw_axes():
    """ Desenha os eixos X (vermelho), Y (verde) e Z (azul) """
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # X
    glColor3f(1.0, 0.0, 0.0); glVertex3f(0.0, 0.0, 0.0); glVertex3f(2.0, 0.0, 0.0)
    # Y
    glColor3f(0.0, 1.0, 0.0); glVertex3f(0.0, 0.0, 0.0); glVertex3f(0.0, 2.0, 0.0)
    # Z
    glColor3f(0.0, 0.0, 1.0); glVertex3f(0.0, 0.0, 0.0); glVertex3f(0.0, 0.0, 2.0)
    glEnd()

def draw_icosahedron():
    v = ICOSAHEDRON_VERTICES
    faces = ICOSAHEDRON_FACES

    # --- Faces preenchidas ---
    glBegin(GL_TRIANGLES)
    for i, (a, b, c) in enumerate(faces):
        glColor3fv(FACE_COLORS[i % len(FACE_COLORS)])
        glVertex3fv(v[a]); glVertex3fv(v[b]); glVertex3fv(v[c])
    glEnd()

    # --- Arestas (wireframe) ---
    edge_set = set()
    for a, b, c in faces:
        edge_set.update({tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((c,a)))})
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    for a, b in edge_set:
        glVertex3fv(v[a]); glVertex3fv(v[b])
    glEnd()

def display():
    global rotation_angle_x, rotation_angle_y, rotation_angle_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Câmera
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    glDisable(GL_DEPTH_TEST)
    draw_axes()
    glEnable(GL_DEPTH_TEST)

    glPushMatrix()

    # Aplica rotações acumuladas
    glRotatef(rotation_angle_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_angle_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_angle_z, 0.0, 0.0, 1.0)

    # Um scale
    glScalef(0.9, 0.9, 0.9)

    draw_icosahedron()
    glPopMatrix()

    glutSwapBuffers()

def reshape(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def animate(value):
    global rotation_angle_x, rotation_angle_y, rotation_angle_z, rotation_axis
    inc = 0.6  # velocidade
    if rotation_axis == 'x':
        rotation_angle_x = (rotation_angle_x + inc) % 360.0
    elif rotation_axis == 'y':
        rotation_angle_y = (rotation_angle_y + inc) % 360.0
    else:
        rotation_angle_z = (rotation_angle_z + inc) % 360.0

    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)  # ~60 FPS

def keyboard(key, x, y):
    """Controles:
       x/y/z -> alterna eixo de rotação
       espaço -> cicla eixo
       ESC -> sair
    """
    global rotation_axis
    if key in (b'x', b'X'):
        rotation_axis = 'x'
    elif key in (b'y', b'Y'):
        rotation_axis = 'y'
    elif key in (b'z', b'Z'):
        rotation_axis = 'z'
    elif key == b' ':
        rotation_axis = {'x':'y', 'y':'z', 'z':'x'}[rotation_axis]
    elif key == b'\x1b':  # ESC
        glutLeaveMainLoop()

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Icosaedro - Eixos + Rotacao")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, animate, 0)
    init_gl()
    glutMainLoop()


if __name__ == "__main__":
    main()