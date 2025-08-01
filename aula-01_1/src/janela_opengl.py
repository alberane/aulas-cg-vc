"""
Aula 1 - Introdução à Computação Gráfica - ALberane
Primeiro programa: Janela OpenGL básica com triângulo colorido

Este programa demonstra:
1. Configuração básica do OpenGL
2. Criação de uma janela gráfica
3. Renderização de um triângulo simples
4. Loop de renderização básico
"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys

class HelloOpenGL:
    def __init__(self, width=800, height=600, title="Minha Primeira Janela OpenGL"):
        """
        Inicializa a aplicação OpenGL

        Args:
            width: Largura da janela
            height: Altura da janela
            title: Título da janela
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = None

        # Dados do triângulo (coordenadas normalizadas -1 a 1)
        self.vertices = np.array([
            # Posição (x, y, z)    # Cor (R, G, B)
            -0.5, -0.5, 0.0,       1.0, 0.0, 0.0,  # Vértice inferior esquerdo (Vermelho)
             0.5, -0.5, 0.0,       0.0, 1.0, 0.0,  # Vértice inferior direito (Verde)
             0.0,  0.5, 0.0,       0.0, 0.0, 1.0   # Vértice superior (Azul)
        ], dtype=np.float32)

        self.vao = None  # Vertex Array Object
        self.vbo = None  # Vertex Buffer Object
        self.shader_program = None

    def init_glfw(self):
        """Inicializa GLFW e cria a janela"""
        # Inicializar GLFW
        if not glfw.init():
            print("Erro: Não foi possível inicializar GLFW")
            sys.exit(1)

        # Configurar contexto OpenGL (versão 3.3 Core Profile)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # Criar janela
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            print("Erro: Não foi possível criar a janela")
            glfw.terminate()
            sys.exit(1)

        # Tornar o contexto OpenGL ativo
        glfw.make_context_current(self.window)

        # Configurar callback para redimensionamento
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)

        print(f"OpenGL Version: {glGetString(GL_VERSION).decode()}")
        print(f"GLSL Version: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode()}")

    def framebuffer_size_callback(self, window, width, height):
        """Callback chamado quando a janela é redimensionada"""
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height

    def create_shaders(self):
        """Cria e compila os shaders vertex e fragment"""

        # Vertex Shader - processa cada vértice
        vertex_shader_source = """
        #version 330 core
        
        // Atributos de entrada
        layout (location = 0) in vec3 aPos;    // Posição do vértice
        layout (location = 1) in vec3 aColor;  // Cor do vértice
        
        // Saída para o fragment shader
        out vec3 vertexColor;
        
        void main() {
            // Definir posição final do vértice
            gl_Position = vec4(aPos, 1.0);
            
            // Passar cor para o fragment shader
            vertexColor = aColor;
        }
        """

        # Fragment Shader - calcula cor final de cada pixel
        fragment_shader_source = """
        #version 330 core
        
        // Entrada do vertex shader
        in vec3 vertexColor;
        
        // Cor final do fragmento
        out vec4 FragColor;
        
        void main() {
            // Definir cor final (RGB + Alpha)
            FragColor = vec4(vertexColor, 1.0);
        }
        """

        # Compilar vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)

        # Verificar erros de compilação
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader).decode()
            print(f"Erro na compilação do Vertex Shader: {error}")
            sys.exit(1)

        # Compilar fragment shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)

        # Verificar erros de compilação
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader).decode()
            print(f"Erro na compilação do Fragment Shader: {error}")
            sys.exit(1)

        # Criar programa shader e linkar
        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, fragment_shader)
        glLinkProgram(self.shader_program)

        # Verificar erros de linkagem
        if not glGetProgramiv(self.shader_program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.shader_program).decode()
            print(f"Erro na linkagem do programa: {error}")
            sys.exit(1)

        # Limpar shaders (já foram linkados ao programa)
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        print("Shaders compilados e linkados com sucesso!")

    def setup_vertex_data(self):
        """Configura os dados de vértices na GPU"""
        # Gerar Vertex Array Object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Gerar Vertex Buffer Object (VBO)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # Enviar dados dos vértices para a GPU
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Configurar atributo de posição (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Configurar atributo de cor (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        # Desvincular VAO
        glBindVertexArray(0)

        print("Dados de vértices configurados!")

    def render(self):
        """Função de renderização principal"""
        # Limpar o buffer de cor
        glClearColor(0.2, 0.3, 0.3, 1.0)  # Cor de fundo (cinza-azulado)
        glClear(GL_COLOR_BUFFER_BIT)

        # Usar nosso programa shader
        glUseProgram(self.shader_program)

        # Vincular VAO e desenhar o triângulo
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)  # Desenhar 3 vértices como triângulo

        # Desvincular VAO
        glBindVertexArray(0)

    def run(self):
        """Loop principal da aplicação"""
        print("Iniciando aplicação OpenGL...")

        # Inicializar GLFW e criar janela
        self.init_glfw()

        # Configurar shaders
        self.create_shaders()

        # Configurar dados de vértices
        self.setup_vertex_data()

        print("Aplicação inicializada! Pressione ESC para sair...")

        # Loop de renderização
        while not glfw.window_should_close(self.window):
            # Processar eventos
            glfw.poll_events()

            # Verificar se ESC foi pressionado
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)

            # Renderizar cena
            self.render()

            # Trocar buffers (double buffering)
            glfw.swap_buffers(self.window)

        self.cleanup()

    def cleanup(self):
        """Limpa recursos antes de sair"""
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
        if self.shader_program:
            glDeleteProgram(self.shader_program)

        glfw.terminate()
        print("Aplicação finalizada!")

def main():
    """Função principal"""
    try:
        app = HelloOpenGL(
            width=800,
            height=600,
            title="Aula 1 - Primeiro Programa OpenGL"
        )
        app.run()
    except Exception as e:
        print(f"Erro durante execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()