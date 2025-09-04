import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Carregar arquivo MTL
def load_mtl(filename):
    materials = {}
    current_material = None

    try:
        with open(filename, 'r') as file: # Abrir arquivo MTL e ler linha por linha
            for line in file:
                if line.startswith('newmtl '):
                    current_material = line.split()[1] # Nome do material
                    materials[current_material] = {'color': [0.8, 0.8, 0.8]} # Cor padrão cinza
                elif line.startswith('Kd ') and current_material:
                    # Cor difusa
                    parts = line.split()
                    materials[current_material]['color'] = [float(parts[1]), float(parts[2]), float(parts[3])] # Definir cor do material
    except:
        print("Arquivo MTL não encontrado ou erro ao carregar")

    return materials

# Carregar arquivo OBJ
def load_obj(filename):
    vertices = []
    faces = []
    materials = {}

    # Tentar carregar MTL
    mtl_file = filename.replace('.obj', '.mtl')
    materials = load_mtl(mtl_file) # Carregar materiais do arquivo MTL

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # Vértices
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                # Faces - suporta triângulos e quads
                parts = line.split()[1:] # Ignorar o primeiro elemento 'f' no início
                face = [] # Lista para armazenar índices dos vértices da face
                for p in parts:
                    vertex_idx = int(p.split('/')[0]) - 1  # -1 porque OBJ usa base 1
                    face.append(vertex_idx) # Adicionar índice do vértice à face
                faces.append(face)

    print(f"Vértices: {vertices}")
    print(f"Faces: {faces}")
    return vertices, faces, materials

# Desenhar objeto
def draw_object(vertices, faces, materials):
    # Cor padrão
    glColor3f(0.1, 0.5, 0.0)  # Cor da superfície

    for face in faces:
        if len(face) == 3:  # Triângulo
            glBegin(GL_TRIANGLES)
        elif len(face) == 4:  # Quadrado
            glBegin(GL_QUADS)
        else:  # Polígono
            glBegin(GL_POLYGON)

        # Verificar se a face tem material associado
        for vertex_idx in face:
            if vertex_idx < len(vertices):
                glVertex3fv(vertices[vertex_idx])

        glEnd() # Finalizar desenho da face

    # Desenhar wireframe por cima
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(1, 0.5, 0)  # Cor para wireframe (RGB)

    # Desenhar faces novamente como wireframe
    for face in faces:
        if len(face) == 3:
            glBegin(GL_TRIANGLES)
        elif len(face) == 4:
            glBegin(GL_QUADS)
        else:
            glBegin(GL_POLYGON)

        # Desenhar vértices da face
        for vertex_idx in face:
            if vertex_idx < len(vertices):
                glVertex3fv(vertices[vertex_idx])

        glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # Voltar ao modo de preenchimento

def main():
    # Inicializar pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Visualizador de OBJs")

    # Configurar OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)  # Fundo cinza escuro

    # Configurar perspectiva
    glMatrixMode(GL_PROJECTION) # Mudar para matriz de projeção
    glLoadIdentity() # Limpar matriz de projeção
    gluPerspective(60, 800/600, 0.1, 100.0) # Perspectiva 60 graus, aspecto 800x600, near 0.1, far 100.0
    glMatrixMode(GL_MODELVIEW) # Voltar para matriz de modelo

    # Carregar modelo
    try:
        # Carregar cubo.obj para visualização usando 3 variáveis,
        # uma para vértices, outra para faces e a terceira para materiais
        vertices, faces, materials = load_obj("cubo-01.obj")
        print(f"Carregado: {len(vertices)} vértices, {len(faces)} faces")

        if not vertices:
            print("ERRO: Nenhum vértice encontrado!")
            sys.exit()
        if not faces:
            print("ERRO: Nenhuma face encontrada!")
            sys.exit()

    except Exception as e:
        print(f"Erro ao carregar cubo-01.obj: {e}")
        sys.exit()

    # Calcular centro do objeto para melhor visualização
    if vertices:
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        min_y = min(v[1] for v in vertices)
        max_y = max(v[1] for v in vertices)
        min_z = min(v[2] for v in vertices)
        max_z = max(v[2] for v in vertices)

        # Calcular centro e tamanho do objeto

        # Centro é a média dos valores mínimo e máximo de cada eixo
        # Tamanho é a maior distância entre os valores mínimo e máximo de cada eixo
        # Isso ajuda a centralizar o objeto na tela e ajustar o zoom
        # para que ele fique visível na janela
        center = [(min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2]
        size = max(max_x - min_x, max_y - min_y, max_z - min_z)

        print(f"Centro: {center}, Tamanho: {size}")

    # Variáveis de controle
    rotation_x, rotation_y = 20, 30  # Rotação inicial
    zoom = -15  # Zoom inicial mais afastado
    pan_x, pan_y = 0, 0
    dragging = False # Flag para arrastar com o mouse
    last_pos = (0, 0)

    print("\nControles:")
    print("Mouse: Arrastar para girar")
    print("Scroll: Zoom")
    print("Shift+Mouse: Pan")
    print("R: Reset câmera")
    print("ESC: Sair")

    clock = pygame.time.Clock() # Relógio para controlar FPS

    while True:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset câmera
                    rotation_x, rotation_y = 20, 30
                    zoom = -15
                    pan_x, pan_y = 0, 0

            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    dragging = True
                    last_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                dx, dy = x - last_pos[0], y - last_pos[1]

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT]:  # Pan com Shift
                    pan_x += dx * 0.02
                    pan_y -= dy * 0.02
                else:  # Rotação normal
                    rotation_y += dx * 0.5
                    rotation_x += dy * 0.5

                last_pos = (x, y)

            # Zoom com scroll
            elif event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 1.0
                zoom = max(-100, min(zoom, -1))  # Limitar zoom

        # Renderizar
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Aplicar transformações
        glTranslatef(pan_x, pan_y, zoom)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)

        # Desenha o cubo
        draw_object(vertices, faces, materials)

        pygame.display.flip() # Atualizar tela
        clock.tick(30) # Limitar o FPS

if __name__ == "__main__":
    main()