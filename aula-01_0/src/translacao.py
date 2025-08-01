import numpy as np

# Translação é uma transformação geométrica que move um ponto de um lugar para outro no espaço,
# sem alterar sua orientação, tamanho ou forma. No contexto de coordenadas homogêneas,
# a translação pode ser representada por uma matriz que, ao ser multiplicada pelo vetor do ponto,
# resulta em um novo ponto transladado.

# Ponto original em coordenadas homogêneas
p = np.array([2, 3, 1])

# Matriz de translação (tx=4, ty=5)
T = np.array([
    [1, 0, 4],
    [0, 1, 5],
    [0, 0, 1]
])

# A translação aconteceu porque multiplicamos a matriz de translação 'T' pelo vetor
# do ponto 'p' em coordenadas homogêneas.
#
# A matriz 'T' adiciona os valores 'tx=4' e 'ty=5' às coordenadas x e y do ponto original, respectivamente.
#
# Assim, o ponto '[2, 3, 1]' se torna '[2+4, 3+5, 1]', resultando em '[6, 8, 1]'.
#
# Isso ocorre porque, em coordenadas homogêneas, a última coluna da matriz de translação
# representa o deslocamento aplicado ao ponto.

# Aplica a translação
p_transladado = T @ p
print("Ponto original:", p)
print("Ponto transladado:", p_transladado)

