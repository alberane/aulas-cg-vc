import numpy as np

# Define quatro pontos de um quadrado
pontos = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

def rotacionar(pontos, angulo_graus):
    angulo_rad = np.deg2rad(angulo_graus)
    matriz_rot = np.array([
        [np.cos(angulo_rad), -np.sin(angulo_rad)],
        [np.sin(angulo_rad),  np.cos(angulo_rad)]
    ])
    return pontos @ matriz_rot.T

def transladar(pontos, deslocamento):
    return pontos + deslocamento

# Teste: rotaciona 90 graus e translada em (2, 3)
pontos_rot = rotacionar(pontos, 90)
pontos_final = transladar(pontos_rot, np.array([2, 3]))

print("Pontos originais:\n", pontos)
print("Após rotação de 90°:\n", pontos_rot)
print("Após translação (2,3):\n", pontos_final)