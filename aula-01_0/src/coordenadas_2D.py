import matplotlib.pyplot as plt

# Define pontos 2D
pontos = [(1, 2), (3, 4), (5, 1), (2, 5)]

x, y = zip(*pontos)

plt.scatter(x, y, color='blue')

for i, (xi, yi) in enumerate(pontos):
    plt.text(xi + 0.1, yi + 0.1, f'P{i}({xi},{yi})')

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title("Coordenadas 2D Cartesiano")
plt.grid(True)
plt.savefig("imagens/coordenadas_2d.png")
