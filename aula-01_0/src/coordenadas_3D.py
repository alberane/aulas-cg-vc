import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define pontos 3D
pontos = [(2, 2, 2), (3, 4, 5)]
x, y, z = zip(*pontos) # extrai as coordenadas x, y, z dos pontos

ax.scatter(x, y, z, color='red')
for i, (xi, yi, zi) in enumerate(pontos):
    ax.text(xi, yi, zi, f'P{i}({xi},{yi},{zi})')


# Projeta cada ponto nos planos XY, XZ e YZ com linhas tracejadas azuis
# for xi, yi, zi in pontos:
#     ax.plot([xi, xi], [yi, yi], [0, zi], linestyle='dashed', color='blue')  # projeção no plano XY
#     ax.plot([xi, xi], [0, yi], [zi, zi], linestyle='dashed', color='blue')  # projeção no plano XZ
#     ax.plot([0, xi], [yi, yi], [zi, zi], linestyle='dashed', color='blue')  # projeção no plano YZ


ax.set_title("Coordenadas 3D")
ax.set_xlabel("Plano X")
ax.set_ylabel("Plano Y")
ax.set_zlabel("Plano Z")
plt.savefig("imagens/coordenadas_3d.png")