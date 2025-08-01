import numpy as np

# Fatores de escala
sx, sy = 2, 3

# Ponto original em coordenadas homogêneas
p = np.array([1, 2, 1])

# Matriz de escala
S = np.array([
    [sx, 0,  0],
    [0,  sy, 0],
    [0,  0,  1]
])

# A escala é uma transformação geométrica que altera o tamanho de um objeto
# em relação à origem. Em coordenadas homogêneas, a escala pode ser representada
# por uma matriz diagonal, onde os fatores de escala para cada eixo (x e y)
# são colocados na diagonal principal. A multiplicação dessa matriz pelo vetor do ponto
# resulta em um novo ponto que foi escalado pelos fatores especificados.
# A matriz de escala é definida como:
# S = [[sx, 0,  0],
#      [0,  sy, 0],
#      [0,  0,  1]]
# onde sx e sy são os fatores de escala para os eixos x e y, respectivamente.
# A multiplicação da matriz de escala pela coordenada homogênea do ponto
# resulta em um novo ponto que foi escalado pelos fatores sx e sy.


# Aplica a escala
p_escalado = S @ p
print("Ponto original:", p)
print("Ponto escalado:", p_escalado)