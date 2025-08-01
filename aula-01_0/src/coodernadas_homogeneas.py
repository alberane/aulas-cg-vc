import numpy as np

ponto_2d = np.array([3, 4])
ponto_2d_h = np.append(ponto_2d, 1)

ponto_3d = np.array([1, 2, 3])
ponto_3d_h = np.append(ponto_3d, 1)

print("Ponto 2D:", ponto_2d)
print("Coordenada Homogênea 2D:", ponto_2d_h)

print("Ponto 3D:", ponto_3d)
print("Coordenada Homogênea 3D:", ponto_3d_h)
