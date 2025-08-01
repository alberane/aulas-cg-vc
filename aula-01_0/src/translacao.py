import numpy as np
import matplotlib.pyplot as plt

ponto = np.array([2, 3, 1])
T = np.array([
    [1, 0, 2],
    [0, 1, 1],
    [0, 0, 1]
])
novo_ponto = T @ ponto

plt.scatter(ponto[0], ponto[1], color='blue', label='Original')
plt.scatter(novo_ponto[0], novo_ponto[1], color='red', label='Transladado')
plt.legend()
plt.title("Translação 2D")
plt.grid(True)
plt.savefig("translacao.png")
