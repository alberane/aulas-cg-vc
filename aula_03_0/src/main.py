import glfw
from OpenGL.GL import *
import numpy as np
import math

# --- Funções para compilar Shaders ---
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type) # Cria um shader do tipo especificado
    glShaderSource(shader, source)
    glCompileShader(shader) # Compila o shader
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception(f"Erro na compilação do shader: {glGetShaderInfoLog(shader).decode()}")
    return shader

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = compile_shader(vertex_src, GL_VERTEX_SHADER) # Compila o shader de vértices
    fragment_shader = compile_shader(fragment_src, GL_FRAGMENT_SHADER)

    program = glCreateProgram() # Cria um programa de shader
    glAttachShader(program, vertex_shader) # Anexa o shader de vértices
    glAttachShader(program, fragment_shader) # Anexa o shader de fragmentos
    glLinkProgram(program) # Linka os shaders no programa
    if not glGetProgramiv(program, GL_LINK_STATUS): # Verifica se o link foi bem-sucedido
        raise Exception(f"Erro no link do programa: {glGetProgramInfoLog(program).decode()}")

    glDeleteShader(vertex_shader) # Limpa os shaders após o link
    glDeleteShader(fragment_shader)
    return program

def main():
    # --- Inicialização do GLFW ---
    if not glfw.init():
        return

    window_width, window_height = 800, 600
    window = glfw.create_window(window_width, window_height, "Aula 3: Transformações 2D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window) # Torna o contexto OpenGL atual para a janela

    # --- Carregar Shaders ---
    with open("vertex_shader.glsl", "r") as f:
        vertex_shader_source = f.read()
    with open("fragment_shader.glsl", "r") as f:
        fragment_shader_source = f.read()

    shader_program = create_shader_program(vertex_shader_source, fragment_shader_source) # Cria o programa de shader
    glUseProgram(shader_program) # Ativa o programa de shader

    # --- Definir a geometria do quadrado ---
    # Vértices de um quadrado centrado na origem
    vertices = np.array([
        -0.5, -0.5,  # Vértice inferior esquerdo
         0.5, -0.5,  # Vértice inferior direito
         0.5,  0.5,  # Vértice superior direito
        -0.5,  0.5   # Vértice superior esquerdo
    ], dtype=np.float32)

    # Índices para desenhar o quadrado usando dois triângulos
    indices = np.array([
        0, 1, 2,  # Primeiro triângulo
        2, 3, 0   # Segundo triângulo
    ], dtype=np.uint32)

    # --- Configurar Buffers (VAO, VBO, EBO) ---
    VAO = glGenVertexArrays(1) # Gerar um Vertex Array Object
    VBO = glGenBuffers(1) # Gerar um Vertex Buffer Object
    EBO = glGenBuffers(1) # Gerar um Element Buffer Object

    glBindVertexArray(VAO) # Ativar o VAO

    glBindBuffer(GL_ARRAY_BUFFER, VBO) # Ativar o VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # Envia os dados dos vértices para o VBO

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO) # Ativar o EBO
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW) # Envia os dados dos índices para o EBO

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0)) # Define o layout dos atributos do vértice
    glEnableVertexAttribArray(0) # Ativa o atributo de vértice 0 (posição)

    glBindBuffer(GL_ARRAY_BUFFER, 0) # Desativa o VBO
    glBindVertexArray(0) # Desativa o VAO

    # Obter a localização do uniform da matriz de transformação no shader
    transform_loc = glGetUniformLocation(shader_program, "u_transform")

    # --- Loop Principal de Renderização ---
    while not glfw.window_should_close(window):
        # Limpar a tela
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Ativar o programa de shader
        glUseProgram(shader_program)

        # --- Calcular Matrizes de Transformação ---
        time_value = glfw.get_time()

        # 1. Matriz de Escala: Animação de "pulsação"
        scale_factor = (math.sin(time_value * 2) + 1.5) / 2.5 # Varia entre 0.2 e 1.0
        scale_mat = np.array([
            [scale_factor, 0, 0, 0],
            [0, scale_factor, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # 2. Matriz de Rotação: Gira continuamente
        angle = time_value
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rotation_mat = np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a,  cos_a, 0, 0],
            [0,     0,     1, 0],
            [0,     0,     0, 1]
        ], dtype=np.float32)

        # 3. Matriz de Translação: Move em um círculo
        trans_x = math.cos(time_value) * 0.5
        trans_y = math.sin(time_value) * 0.5
        translation_mat = np.array([
            [1, 0, 0, trans_x],
            [0, 1, 0, trans_y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # --- Composição das Matrizes ---
        # Ordem: Escala -> Rotação -> Translação
        # No código (multiplicação de matrizes), a ordem é inversa: T @ R @ S
        transform_matrix = translation_mat @ rotation_mat @ scale_mat

        # Enviar a matriz composta para o shader
        glUniformMatrix4fv(transform_loc, 1, GL_TRUE, transform_matrix) # GL_TRUE porque NumPy usa 'row-major' order

        # --- Desenhar o objeto ---
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None) # Desenha o quadrado usando os índices

        # Trocar buffers e processar eventos
        glfw.swap_buffers(window)
        glfw.poll_events()

    # --- Limpeza ---
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader_program)
    glfw.terminate()

if __name__ == "__main__":
    main()