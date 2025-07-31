import numpy as np

# Coordenada 2D cartesiana
p2d = np.array([3, 5])
print("Coordenada 2D:", p2d)

# Coordenada 3D cartesiana
p3d = np.array([3, 5, 7])
print("Coordenada 3D:", p3d)

# Coordenadas homogêneas adicionam um valor extra (geralmente 1) ao final do vetor,
# facilitando operações como translações e projeções porque permitem representar essas transformações
# como multiplicações de matrizes. Isso unifica o tratamento de rotações, escalas, translações e projeções em um único modelo matemático,
# tornando os cálculos mais simples e eficientes.
p2d_hom = np.append(p2d, 1)
print("Coordenada homogênea 2D:", p2d_hom)

# Coordenada homogênea 3D
p3d_hom = np.append(p3d, 1)
print("Coordenada homogênea 3D:", p3d_hom)