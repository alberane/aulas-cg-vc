# -*- coding: utf-8 -*-
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Variáveis globais para a animação
rotation_angle_x = 0.0
rotation_angle_y = 0.0

def draw_axes():
    """ Desenha os eixos X (vermelho), Y (verde) e Z (azul) """
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # Eixo X em Vermelho
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
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

def draw_cube():
    """ Desenha um cubo colorido de 1 unidade centrado na origem """
    # Vértices do cubo
    vertices = [
        [ 0.5, -0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [-0.5,  0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5,  0.5],
        [-0.5, -0.5,  0.5],
        [-0.5,  0.5,  0.5]
    ]
    # Arestas que conectam os vértices para formar as faces
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), # Face frontal
        (4, 5), (5, 7), (7, 6), (6, 4), # Face traseira
        (0, 4), (1, 5), (2, 7), (3, 6)  # Arestas de conexão
    ]
    # Cores para cada face
    colors = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1)
    ]
    # Faces do cubo (índices dos vértices)
    faces = [
        (0, 1, 2, 3), (4, 5, 7, 6), (0, 3, 6, 4),
        (1, 2, 7, 5), (3, 2, 7, 6), (0, 1, 5, 4)
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex_index in face:
            glVertex3fv(vertices[vertex_index])
    glEnd()

    # Desenha as arestas em preto para melhor visualização
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_index in edge:
            glVertex3fv(vertices[vertex_index])
    glEnd()


def display():
    """ Função principal de desenho (callback) """
    global rotation_angle_x, rotation_angle_y

    # Limpa os buffers de cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reseta a matriz de transformação atual (ModelView)
    glLoadIdentity()

    # Configuração da Câmera (Matriz de Visão - View Matrix)
    # Posição da câmera: (5, 5, 5)
    # Ponto para onde a câmera olha: (0, 0, 0)
    # Vetor "up" da câmera: (0, 1, 0) (eixo Y)
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    # --- Início das Transformações do Modelo (Matriz de Modelo - Model Matrix) ---

    # 1. Translação: Move o objeto para longe da origem do mundo
    # O cubo será transladado em -1.5 no eixo Z.
    glTranslatef(0.0, 0.0, 0)

    # 2. Rotação: Gira o objeto em torno de seu próprio centro
    # A ordem importa! Rotacionar em Y e depois em X é diferente do contrário.
    glRotatef(rotation_angle_y, 0.0, 1.0, 0.0) # Gira em torno do eixo Y
    glRotatef(rotation_angle_x, 1.0, 0.0, 0.0) # Gira em torno do eixo X

    # 3. Escala: Altera o tamanho do objeto
    # Aumenta o tamanho do cubo em 1.5x em todas as direções
    glScalef(1.5, 1.5, 1.5)

    # --- Fim das Transformações do Modelo ---

    # Desenha os eixos do sistema de coordenadas do objeto transformado
    draw_axes()
    # Desenha o cubo
    draw_cube()

    # Troca os buffers (desenho duplo) para exibir a cena
    glutSwapBuffers()

def reshape(width, height):
    """ Função de redimensionamento da janela (callback) """
    if height == 0:
        height = 1

    # Define a área de desenho (viewport) para a janela inteira
    glViewport(0, 0, width, height)

    # Define a matriz de Projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define a projeção em perspectiva
    # fov = 45 graus, aspect ratio = width/height, near plane = 0.1, far plane = 50.0
    gluPerspective(45.0, float(width) / float(height), 0.1, 50.0)

    # Retorna para a matriz ModelView para as operações de desenho
    glMatrixMode(GL_MODELVIEW)

def animate(value):
    """ Callback para animação """
    global rotation_angle_x, rotation_angle_y

    # Atualiza os ângulos de rotação
    rotation_angle_x += 0.5
    rotation_angle_y += 0.4

    # Garante que os ângulos não cresçam indefinidamente
    if rotation_angle_x > 360:
        rotation_angle_x -= 360
    if rotation_angle_y > 360:
        rotation_angle_y -= 360

    # Solicita um redesenho da cena
    glutPostRedisplay()

    # Registra o próximo timer para a animação
    glutTimerFunc(8, animate, 0) # Aproximadamente 60 FPS (1000/16)

def main():
    """ Função principal """
    # Inicializa o GLUT
    glutInit(sys.argv)

    # Define o modo de display (duplo buffer, cores RGBA, buffer de profundidade)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # Define o tamanho e a posição inicial da janela
    glutInitWindowSize(1920, 1080)
    glutInitWindowPosition(100, 100)

    # Cria a janela com um título
    glutCreateWindow(b"Aula 4: Transformacoes Geometricas 3D")

    # Registra as funções de callback
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(8, animate, 0)

    # Ativa o teste de profundidade para renderização 3D correta
    glEnable(GL_DEPTH_TEST)

    # Define a cor de fundo (preto)
    glClearColor(1, 0.5, 0.1, 1.0)

    # Inicia o loop principal do GLUT
    glutMainLoop()

if __name__ == "__main__":
    main()