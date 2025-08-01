import numpy as np
import matplotlib.pyplot as plt

theta = np.radians(45)
R = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0, 0, 1]
])
ponto = np.array([2, 1, 1])
novo_ponto = R @ ponto

plt.scatter(ponto[0], ponto[1], color='blue', label='Original')
plt.scatter(novo_ponto[0], novo_ponto[1], color='orange', label='Rotacionado')
plt.legend()
plt.title("Rotação 2D (45°)")
plt.grid(True)
plt.savefig("rotacao.png")
