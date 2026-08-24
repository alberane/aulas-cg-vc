import turtle

def desenha_triangulo(tartaruga, vertices):
    """Desenha um triângulo conectando uma lista de vértices."""
    tartaruga.penup()
    tartaruga.goto(vertices[0][0], vertices[0][1])
    tartaruga.pendown()
    for vertice in vertices[1:]:
        tartaruga.goto(vertice[0], vertice[1])
    tartaruga.goto(vertices[0][0], vertices[0][1])
    tartaruga.penup()

# Configuração inicial da tela
tela = turtle.Screen()
tela.bgcolor("white")
tela.title("Transformações Geométricas com Turtle")

# Criando nossa tartaruga
t = turtle.Turtle()
t.speed(3)
t.pensize(3)

# Vértices do nosso triângulo original (em azul)
vertices_originais = [[0, 50], [-50, -50], [50, -50]]

# Desenhando o triângulo original
t.pencolor("blue")
desenha_triangulo(t, vertices_originais)





# Para manter a janela aberta
turtle.done()