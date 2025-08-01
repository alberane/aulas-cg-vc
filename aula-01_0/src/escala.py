import numpy as np
import matplotlib.pyplot as plt

S = np.array([
    [2, 0, 0],
    [0, 0.5, 0],
    [0, 0, 1]
])
ponto = np.array([2, 2, 1])
novo_ponto = S @ ponto

plt.scatter(ponto[0], ponto[1], color='blue', label='Original')
plt.scatter(novo_ponto[0], novo_ponto[1], color='green', label='Escalado')
plt.legend()
plt.title("Escala 2D (sx=2, sy=0.5)")
plt.grid(True)
plt.savefig("escala.png")
