import numpy as np

# Ângulo em graus e radianos
theta = 45
rad = np.deg2rad(theta)

# Ponto original em coordenadas homogêneas
p = np.array([1, 0, 1])

# Matriz de rotação
R = np.array([
    [np.cos(rad), -np.sin(rad), 0],
    [np.sin(rad),  np.cos(rad), 0],
    [0,           0,            1]
])

# A rotação é uma transformação geométrica que gira um ponto em torno da origem
# (ou de outro ponto, se ajustado) em um determinado ângulo. Em coordenadas homogêneas,
# a rotação pode ser representada por uma matriz que, ao ser multiplicada pelo vetor do ponto,
# resulta em um novo ponto rotacionado. A matriz de rotação é construída usando funções trigonométricas
# (seno e cosseno) para calcular as novas coordenadas do ponto após a rotação.
#
# A matriz de rotação é definida como:
# R = [[cos(θ), -sin(θ), 0],
#      [sin(θ),  cos(θ), 0],
#      [0,       0,      1]]
# onde θ é o ângulo de rotação em radianos. A multiplicação da matriz de rotação pela coordenada homogênea
# do ponto resulta em um novo ponto que foi rotacionado pelo ângulo θ em torno da origem.

# Aplica a rotação
p_rotacionado = R @ p
print("Ponto original:", p)
print("Ponto rotacionado (45°):", p_rotacionado)