import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class CoordinateSystem:
    """
    Classe para demonstrar diferentes sistemas de coordenadas em OpenGL.
    """

    def __init__(self):
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.zoom = -5.0

    @staticmethod
    def setup_opengl():
        """Configurações iniciais do OpenGL."""
        glEnable(GL_DEPTH_TEST) # Ativar teste de profundidade
        glDepthFunc(GL_LESS) # Função de teste de profundidade
        glClearColor(0.1, 0.1, 0.1, 1.0) # Cor de fundo

        # Configurar iluminação básica
        glEnable(GL_LIGHTING) # Ativar iluminação
        glEnable(GL_LIGHT0) # Ativar luz 0

        light_pos = [2.0, 2.0, 2.0, 1.0] # Posição da luz
        light_ambient = [0.2, 0.2, 0.2, 1.0] # Luz ambiente
        light_diffuse = [0.8, 0.8, 0.8, 1.0] # Luz difusa

        glLightfv(GL_LIGHT0, GL_POSITION, light_pos) # Definir posição da luz
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient) # Definir luz ambiente
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse) # Definir luz difusa

    @staticmethod
    def draw_axis(length=2.0):
        """
        Desenha os eixos coordenados (X=vermelho, Y=verde, Z=azul).

        Args:
            length: Comprimento dos eixos
        """
        glDisable(GL_LIGHTING) # Desativar iluminação para desenhar eixos
        glLineWidth(3.0) # Definir largura da linha
        glBegin(GL_LINES) # Iniciar desenho de linhas

        # Eixo X (vermelho)
        glColor3f(1.0, 0.0, 0.0) # Cor vermelha
        glVertex3f(0.0, 0.0, 0.0) # Origem
        glVertex3f(length, 0.0, 0.0) # Ponto final do eixo X

        # Eixo Y (verde)
        glColor3f(0.0, 1.0, 0.0) # Cor verde
        glVertex3f(0.0, 0.0, 0.0) # Origem
        glVertex3f(0.0, length, 0.0) # Ponto final do eixo Y

        # Eixo Z (azul)
        glColor3f(0.0, 0.0, 1.0) # Cor azul
        glVertex3f(0.0, 0.0, 0.0) # Origem
        glVertex3f(0.0, 0.0, length) # Ponto final do eixo Z

        glEnd() # Finalizar desenho de linhas
        glEnable(GL_LIGHTING) # Reativar iluminação

    @staticmethod
    def draw_cube(size=0.5):
        """
        Desenha um cubo colorido.

        Args:
            size: Tamanho do cubo
        """
        glEnable(GL_COLOR_MATERIAL) # Ativar material de cor
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE) # Definir material de cor

        # Definir material
        specular = [0.3, 0.3, 0.3, 1.0] # Cor especular
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular) # Definir cor especular
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 30.0) # Brilho do material

        # Definir vértices e faces do cubo
        vertices = [
            [-size, -size, -size], [size, -size, -size],
            [size, size, -size], [-size, size, -size],
            [-size, -size, size], [size, -size, size],
            [size, size, size], [-size, size, size]
        ]

        faces = [
            [0, 1, 2, 3],  # Face traseira
            [4, 7, 6, 5],  # Face frontal
            [0, 4, 5, 1],  # Face inferior
            [2, 6, 7, 3],  # Face superior
            [0, 3, 7, 4],  # Face esquerda
            [1, 5, 6, 2]   # Face direita
        ]

        cores = [
            [1.0, 0.0, 0.0],  # Vermelho
            [0.0, 1.0, 0.0],  # Verde
            [0.0, 0.0, 1.0],  # Azul
            [1.0, 1.0, 0.0],  # Amarelo
            [1.0, 0.0, 1.0],  # Magenta
            [0.0, 1.0, 1.0]   # Ciano
        ]

        glBegin(GL_QUADS) # Iniciar desenho de quadrados
        for i, face in enumerate(faces):
            glColor3fv(cores[i]) # Definir cor da face
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx]) # Definir vértice da face
        glEnd() # Finalizar desenho de quadrados

        glDisable(GL_COLOR_MATERIAL) # Desativar material de cor

    @staticmethod
    def draw_grid(size=5, divisions=10):
        """
        Desenha uma grade no plano XZ.

        Args:
            size: Tamanho da grade
            divisions: Número de divisões
        """
        glDisable(GL_LIGHTING) # Desativar iluminação para desenhar grade
        glColor3f(0.3, 0.3, 0.3) # Cor da grade
        glLineWidth(1.0) # Definir largura da linha

        step = (2.0 * size) / divisions

        glBegin(GL_LINES) # Iniciar desenho de linhas
        for i in range(divisions + 1):
            pos = -size + i * step

            # Linhas paralelas ao eixo X
            glVertex3f(-size, 0.0, pos)
            glVertex3f(size, 0.0, pos)

            # Linhas paralelas ao eixo Z
            glVertex3f(pos, 0.0, -size)
            glVertex3f(pos, 0.0, size)

        glEnd()
        glEnable(GL_LIGHTING) # Reativar iluminação

    def display(self):
        """Função de renderização."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpar buffers

        # Configurar matriz de projeção
        glMatrixMode(GL_PROJECTION) # Mudar para matriz de projeção
        glLoadIdentity() # Carregar matriz identidade
        gluPerspective(45.0, 1.0, 0.1, 100.0) # Perspectiva de 45 graus gluPerspective

        # Configurar matriz de visualização
        glMatrixMode(GL_MODELVIEW) # Mudar para matriz de visualização
        glLoadIdentity() # Carregar matriz identidade
        glTranslatef(0.0, 0.0, self.zoom) # Aplicar zoom
        glRotatef(self.rotation_x, 1.0, 0.0, 0.0) # Rotacionar em torno do eixo X
        glRotatef(self.rotation_y, 0.0, 1.0, 0.0) # Rotacionar em torno do eixo Y

        # Desenhar elementos da cena
        self.draw_grid()
        self.draw_axis()

        # Desenhar cubos em diferentes posições (sistema mundial)
        positions = [
            [0.0, 0.0, 0.0],    # Origem
            [2.0, 0.0, 0.0],    # Eixo X
            [0.0, 2.0, 0.0],    # Eixo Y
            [0.0, 0.0, 2.0],    # Eixo Z
            [1.5, 1.5, 1.5]     # Diagonal
        ]

        for pos in positions:
            glPushMatrix() # Salvar matriz atual
            glTranslatef(pos[0], pos[1], pos[2]) # Transladar para a posição
            self.draw_cube(0.3) # Desenhar cubo
            glPopMatrix() # Restaurar matriz anterior

        glutSwapBuffers() # Trocar buffers para exibir a cena

    def keyboard(self, key, x, y):
        """Manipulação de teclado."""
        if key == b'\x1b': # ESC para sair
            try:
                glutLeaveMainLoop()  # Tenta sair do loop principal do GLUT
            except Exception:
                pass
            return # Sair da aplicação
        elif key == b'r':
            self.rotation_x = 0.0
            self.rotation_y = 0.0
            self.zoom = -5.0

        glutPostRedisplay() # Solicitar redrawing da tela

    # Teclas para rotação e zoom
    def special_keys(self, key, x, y):
        """Manipulação de teclas especiais."""
        if key == GLUT_KEY_UP:
            self.rotation_x -= 5.0
        elif key == GLUT_KEY_DOWN:
            self.rotation_x += 5.0
        elif key == GLUT_KEY_LEFT:
            self.rotation_y -= 5.0
        elif key == GLUT_KEY_RIGHT:
            self.rotation_y += 5.0
        elif key == GLUT_KEY_PAGE_UP:
            self.zoom += 0.5
        elif key == GLUT_KEY_PAGE_DOWN:
            self.zoom -= 0.5

        glutPostRedisplay() # Solicitar redrawing da tela

    def run(self):
        """Executa a aplicação OpenGL."""
        glutInit(sys.argv) # Inicializa GLUT
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # Modo de exibição
        glutInitWindowSize(800, 600) # Tamanho da janela
        glutInitWindowPosition(100, 100) # Posição da janela
        glutCreateWindow(b"Sistemas de Coordenadas - CG") # Cria a janela

        self.setup_opengl() # Configurações iniciais do OpenGL

        glutDisplayFunc(self.display) # Função de renderização
        glutKeyboardFunc(self.keyboard) # Manipulação de teclado
        glutSpecialFunc(self.special_keys) # Manipulação de teclas especiais
        glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h)) # Redimensionamento da janela

        print("Controles:")
        print("- Setas: Rotacionar câmera")
        print("- Page Up/Down: Zoom")
        print("- 'r': Reset camera")
        print("- ESC: Sair")

        glutMainLoop() # Inicia o loop principal do GLUT

if __name__ == "__main__":
    sistema = CoordinateSystem() # Cria instância do sistema de coordenadas
    sistema.run() # Executa a aplicação OpenGL