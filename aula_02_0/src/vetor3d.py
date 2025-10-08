import math
import numpy as np


class Vector3D:
    """
    Classe para representar e manipular vetores 3D em computação gráfica.
    Suporta operações básicas como soma, subtração, multiplicação por escalar,
    cálculo de magnitude, normalização, produto escalar e produto vetorial.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        Inicializa um vetor 3D.

        Args:
            x, y, z: Componentes do vetor
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        """Soma de vetores."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtração de vetores."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """Multiplicação por escalar."""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __str__(self):
        """Representação em string."""
        return f"Vector3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def magnitude(self):
        """Calcula a magnitude (norma) do vetor."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Retorna o vetor normalizado (unitário)."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x/mag, self.y/mag, self.z/mag)

    def dot(self, other):
        """Produto escalar (dot product)."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Produto vetorial (cross product)."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def angle_with(self, other):
        """Calcula o ângulo entre dois vetores (em radianos)."""
        dot_product = self.dot(other)
        mags = self.magnitude() * other.magnitude()
        if mags == 0:
            return 0
        cos_angle = dot_product / mags
        # Garantir que o valor esteja no domínio de arccos
        cos_angle = max(-1, min(1, cos_angle))
        return math.acos(cos_angle)

    def to_numpy(self):
        """Converte para array NumPy."""
        return np.array([self.x, self.y, self.z])

# Exemplo de uso da classe Vector3D
def demonstrar_operacoes_vetoriais():
    """Demonstra as operações básicas com vetores."""
    print("=== Demonstração de Operações Vetoriais ===\n")

    # Criar vetores
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)

    print(f"Vetor 1: {v1}")
    print(f"Vetor 2: {v2}")
    print()

    # Operações básicas
    soma = v1 + v2
    print(f"Soma: {soma}")

    subtracao = v2 - v1
    print(f"Subtração (v2 - v1): {subtracao}")

    escalar = v1 * 2.5
    print(f"V1 × 2.5: {escalar}")
    print()

    # Produtos
    dot_product = v1.dot(v2)
    print(f"Produto escalar: {dot_product:.2f}")

    cross_product = v1.cross(v2)
    print(f"Produto vetorial: {cross_product}")
    print()

    # Magnitude e normalização
    print(f"Magnitude de v1: {v1.magnitude():.2f}")
    v1_normalizado = v1.normalize()
    print(f"V1 normalizado: {v1_normalizado}")
    print(f"Magnitude de v1 normalizado: {v1_normalizado.magnitude():.2f}")
    print()

    # Ângulo entre vetores
    angulo_rad = v1.angle_with(v2)
    angulo_deg = math.degrees(angulo_rad)
    print(f"Ângulo entre v1 e v2: {angulo_rad:.2f} rad ({angulo_deg:.2f}°)")

if __name__ == "__main__":
    demonstrar_operacoes_vetoriais()