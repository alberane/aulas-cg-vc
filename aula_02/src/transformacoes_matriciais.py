import matplotlib.pyplot as plt
import numpy as np

class TransformationMatrix:
    """
    Classe para criar e manipular matrizes de transformação 4x4.
    """

    def __init__(self, matrix=None):
        """
        Inicializa a matriz de transformação.

        Args:
            matrix: Matriz 4x4 opcional. Se None, cria matriz identidade.
        """
        if matrix is None:
            self.matrix = np.eye(4, dtype=np.float32)
        else:
            self.matrix = np.array(matrix, dtype=np.float32)

    @staticmethod
    def identity():
        """Retorna matriz identidade."""
        return TransformationMatrix()

    @staticmethod
    def translation(x, y, z):
        """
        Cria matriz de translação.

        Args:
            x, y, z: Deslocamentos nos eixos X, Y e Z
        """
        matrix = np.eye(4, dtype=np.float32)
        matrix[0, 3] = x
        matrix[1, 3] = y
        matrix[2, 3] = z
        return TransformationMatrix(matrix)

    @staticmethod
    def scale(sx, sy, sz):
        """
        Cria matriz de escala.

        Args:
            sx, sy, sz: Fatores de escala para X, Y e Z
        """
        matrix = np.eye(4, dtype=np.float32)
        matrix[0, 0] = sx
        matrix[1, 1] = sy
        matrix[2, 2] = sz
        return TransformationMatrix(matrix)

    @staticmethod
    def rotation_x(angle_rad):
        """
        Cria matriz de rotação em torno do eixo X.

        Args:
            angle_rad: Ângulo em radianos
        """
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        matrix = np.eye(4, dtype=np.float32)
        matrix[1, 1] = cos_a
        matrix[1, 2] = -sin_a
        matrix[2, 1] = sin_a
        matrix[2, 2] = cos_a
        return TransformationMatrix(matrix)

    @staticmethod
    def rotation_y(angle_rad):
        """
        Cria matriz de rotação em torno do eixo Y.

        Args:
            angle_rad: Ângulo em radianos
        """
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        matrix = np.eye(4, dtype=np.float32)
        matrix[0, 0] = cos_a
        matrix[0, 2] = sin_a
        matrix[2, 0] = -sin_a
        matrix[2, 2] = cos_a
        return TransformationMatrix(matrix)

    @staticmethod
    def rotation_z(angle_rad):
        """
        Cria matriz de rotação em torno do eixo Z.

        Args:
            angle_rad: Ângulo em radianos
        """
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        matrix = np.eye(4, dtype=np.float32)
        matrix[0, 0] = cos_a
        matrix[0, 1] = -sin_a
        matrix[1, 0] = sin_a
        matrix[1, 1] = cos_a
        return TransformationMatrix(matrix)

    def __mul__(self, other):
        """Multiplicação de matrizes."""
        if isinstance(other, TransformationMatrix):
            result_matrix = np.dot(self.matrix, other.matrix)
            return TransformationMatrix(result_matrix)
        else:
            raise TypeError("Operação suportada apenas entre TransformationMatrix")

    def transform_point(self, point):
        """
        Aplica a transformação a um ponto 3D.

        Args:
            point: Lista ou array [x, y, z]

        Returns:
            Ponto transformado [x, y, z]
        """
        # Converter para coordenadas homogêneas
        homogeneous_point = np.array([point[0], point[1], point[2], 1.0])

        # Aplicar transformação
        transformed = np.dot(self.matrix, homogeneous_point)

        # Retornar coordenadas cartesianas
        return transformed[:3] / transformed[3]

    def __str__(self):
        """Representação em string da matriz."""
        return str(self.matrix)

# Função para visualizar transformações
def visualizar_transformacoes():
    """Demonstra transformações aplicadas a um cubo."""
    print("=== Demonstração de Transformações Matriciais ===\n")

    # Definir vértices de um cubo unitário
    vertices_cubo = np.array([
        [-0.5, -0.5, -0.5],  # 0
        [ 0.5, -0.5, -0.5],  # 1
        [ 0.5,  0.5, -0.5],  # 2
        [-0.5,  0.5, -0.5],  # 3
        [-0.5, -0.5,  0.5],  # 4
        [ 0.5, -0.5,  0.5],  # 5
        [ 0.5,  0.5,  0.5],  # 6
        [-0.5,  0.5,  0.5],  # 7
    ])

    # Criar diferentes transformações
    transformacoes = {
        "Original": TransformationMatrix.identity(),
        "Translação": TransformationMatrix.translation(2, 1, 0),
        "Escala": TransformationMatrix.scale(1.5, 0.5, 2.0),
        "Rotação Z": TransformationMatrix.rotation_z(np.pi/4),
        "Composta": (TransformationMatrix.translation(1, 1, 0) *
                    TransformationMatrix.rotation_z(np.pi/6) *
                    TransformationMatrix.scale(1.2, 1.2, 0.8))
    }

    # Configurar a visualização
    fig = plt.figure(figsize=(15, 12))

    for i, (nome, transformacao) in enumerate(transformacoes.items()):
        ax = fig.add_subplot(2, 3, i+1, projection='3d')

        # Aplicar transformação aos vértices
        vertices_transformados = np.array([
            transformacao.transform_point(v) for v in vertices_cubo
        ])

        # Plotar os vértices
        ax.scatter(vertices_transformados[:, 0],
                  vertices_transformados[:, 1],
                  vertices_transformados[:, 2],
                  c='red', s=50)

        # Desenhar as arestas do cubo
        arestas = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Face inferior
            [4, 5], [5, 6], [6, 7], [7, 4],  # Face superior
            [0, 4], [1, 5], [2, 6], [3, 7]   # Arestas verticais
        ]

        for aresta in arestas:
            pontos = vertices_transformados[aresta]
            ax.plot(pontos[:, 0], pontos[:, 1], pontos[:, 2], 'b-', alpha=0.6)

        ax.set_title(f'{nome}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Definir limites iguais para todos os eixos
        ax.set_xlim([-2, 4])
        ax.set_ylim([-2, 3])
        ax.set_zlim([-2, 3])

    plt.tight_layout()
    plt.savefig("imagens/grafico_demo.png")
    # plt.show()

    # Demonstrar composição de transformações
    print("Exemplo de composição de transformações:")
    print("T(1,0,0) * R_z(π/4) * S(2,1,1)\n")

    # Criar transformações individuais
    T = TransformationMatrix.translation(1, 0, 0)
    R = TransformationMatrix.rotation_z(np.pi/4)
    S = TransformationMatrix.scale(2, 1, 1)

    # Compor as transformações
    transformacao_composta = T * R * S

    print("Matriz resultante da composição:")
    print(transformacao_composta)

if __name__ == "__main__":
    visualizar_transformacoes()