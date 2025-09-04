# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Variáveis globais para a animação
angulo_rotacao_x = 0.0
angulo_rotacao_y = 0.0

def desenhar_eixos():
    """ Desenha os eixos X (vermelho), Y (verde) e Z (azul) """
    glLineWidth(2.0) # glLineWidth(2.0) Define a largura da linha
    glBegin(GL_LINES) # glBegin(GL_LINES) Inicia a definição de linhas
    # Eixo X em Vermelho
    glColor3f(1.0, 0.0, 0.0) # Define a cor atual (RGB)
    glVertex3f(0.0, 0.0, 0.0) # Especifica um vértice em 3D com coordenadas (x, y, z)
    glVertex3f(2.0, 0.0, 0.0)
    # Eixo Y em Verde
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 2.0, 0.0)
    # Eixo Z em Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 2.0)
    glEnd()

def desenhar_cubo():
    """ Desenha um cubo colorido de 1 unidade centrado na origem """
    # Vértices do cubo
    vertices = [
        [ 0.5, -0.5, -0.5], [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5], [-0.5, -0.5, -0.5],
        [ 0.5, -0.5,  0.5], [ 0.5,  0.5,  0.5], [-0.5, -0.5,  0.5], [-0.5,  0.5,  0.5]
    ]
    # Arestas que conectam os vértices para formar as faces
    # O Formato é (vértice_inicial, vértice_final)
    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0), # Face frontal
        (4, 5), (5, 7), (7, 6), (6, 4), # Face traseira
        (0, 4), (1, 5), (2, 7), (3, 6)  # Arestas de conexão
    ]
    # Cores para cada face
    cores = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1)
    ]
    # Faces do cubo (índices dos vértices)
    # São 4 vértices por face, por isso vamos usar GL_QUADS abaixo
    faces = [
        (0, 1, 2, 3), (4, 5, 7, 6), (0, 3, 6, 4),
        (1, 2, 7, 5), (3, 2, 7, 6), (0, 1, 5, 4)
    ]

    glBegin(GL_QUADS) # Inicia a definição de quadriláteros
    for i, face_atual in enumerate(faces):
        glColor3fv(cores[i])
        for indice_vertice in face_atual:
            glVertex3fv(vertices[indice_vertice])
    glEnd()

    # Desenha as arestas em preto para melhor visualização
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for aresta in arestas:
        for indice_vertice in aresta:
            glVertex3fv(vertices[indice_vertice])
    glEnd()


def exibir():
    """ Função principal de desenho (callback) """

    global angulo_rotacao_x, angulo_rotacao_y

    # Limpa os buffers de cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reinicia a matriz de transformação atual (ModelView)
    glLoadIdentity()

    # Configuração da Câmera (Matriz de Visão - View Matrix)
    # Posição da câmera: (5, 5, 5)
    # Ponto para onde a câmera olha: (0, 0, 0)
    # Vetor "up" da câmera: (0, 1, 0) (eixo Y)
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    # --- Início das Transformações do Modelo (Matriz de Modelo - Model Matrix) ---

    # 1. Translação: Move o objeto para longe da origem do mundo
    glTranslatef(0.0, 0.0, 0.0) # Essa função move o objeto nas direções x, y e z

    # 2. Rotação: Gira o objeto em torno de seu próprio centro
    # A ordem importa! Rotacionar em Y e depois em X é diferente do contrário.
    glRotatef(angulo_rotacao_y, 0.0, 1.0, 0.0) # Gira em torno do eixo Y
    glRotatef(angulo_rotacao_x, 1.0, 0.0, 0.0) # Gira em torno do eixo X

    # 3. Escala: Altera o tamanho do objeto
    # Aumenta o tamanho do cubo em 1.5x em todas as direções
    glScalef(1.5, 1.5, 1.5)

    # --- Fim das Transformações do Modelo ---

    # Desenha os eixos do sistema de coordenadas do objeto transformado
    desenhar_eixos()
    # Desenha o cubo
    desenhar_cubo()

    # Troca os buffers (desenho duplo) para exibir a cena
    glutSwapBuffers()

def redimensionar(largura, altura):
    """ Função de redimensionamento da janela (callback) """
    if altura == 0:
        altura = 1

    # Define a área de desenho (viewport) para a janela inteira
    glViewport(0, 0, largura, altura)

    # Define a matriz de Projeção
    glMatrixMode(GL_PROJECTION) # Muda para a matriz de Projeção
    glLoadIdentity() # Reinicia a matriz de Projeção

    # Define a projeção em perspectiva
    # fov = 45 graus, aspect ratio = largura/altura, near plane = 0.1, far plane = 50.0
    gluPerspective(45.0, float(largura) / float(altura), 0.1, 50.0)

    # Retorna para a matriz ModelView para as operações de desenho
    glMatrixMode(GL_MODELVIEW)

def animar(value):
    """ Callback para animação """
    global angulo_rotacao_x, angulo_rotacao_y

    # Atualiza os ângulos de rotação
    angulo_rotacao_x += 0.5
    angulo_rotacao_y += 0.5

    # Garante que os ângulos não cresçam indefinidamente
    if angulo_rotacao_x > 360:
        angulo_rotacao_x -= 360
    if angulo_rotacao_y > 360:
        angulo_rotacao_y -= 360

    # Solicita um redesenho da cena
    glutPostRedisplay()

    # Registra o próximo timer para a animação
    # glutTimerFunc(tempo_em_milisegundos, função_callback, valor)
    glutTimerFunc(16, animar, 0) # Aproximadamente 60 FPS (1000/16)

def principal():
    """ Função principal """
    # Inicializa o GLUT
    glutInit(sys.argv)

    # Define o modo de display (duplo buffer, cores RGBA, buffer de profundidade)
    # GLUT_RGBA: Usa cores RGBA
    # GLUT_DOUBLE: Usa duplo buffer
    # GLUT_DEPTH: Habilita o buffer de profundidade
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # Define o tamanho e a posição inicial da janela
    glutInitWindowSize(1024, 768)
    glutInitWindowPosition(100, 100)

    # Cria a janela com um título
    glutCreateWindow("Aula 4: Transformacoes Geometricas 3D")

    # Registra as funções de callback
    glutDisplayFunc(exibir)
    glutReshapeFunc(redimensionar)
    glutTimerFunc(16, animar, 0)

    # Ativa o teste de profundidade para renderização 3D correta
    # Experimente comentar essa linha para perceber a diferença
    glEnable(GL_DEPTH_TEST)

    # Define a cor de fundo (preto)
    # glClearColor(r, g, b, a) Define a cor de fundo (RGBA)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Inicia o loop principal do GLUT
    glutMainLoop()

if __name__ == "__main__":
    principal()