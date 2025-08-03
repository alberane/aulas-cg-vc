# README - Visualizador de Cubo OBJ com OpenGL e Pygame

Este projeto demonstra como carregar, visualizar e manipular um cubo exportado do Blender no formato OBJ usando Python, OpenGL e Pygame.

## Funcionalidades

- Carregamento de arquivos OBJ e MTL (materiais).
- Renderização 3D do cubo com preenchimento e wireframe.
- Manipulação da câmera: rotação, zoom e pan.
- Controle por mouse e teclado.
- Fundo da janela configurável (cinza por padrão).

## Requisitos

- Python 3.x
- Pygame
- PyOpenGL

Instale as dependências com:

```
pip install pygame PyOpenGL
```

## Como usar

1. Exporte seu cubo do Blender como OBJ (com triangulação).
2. Coloque os arquivos `cubo-01.obj` e `cubo-01.mtl` na pasta `src`.
3. Execute o script:

```
python src/cubo.py
```

## Controles

- **Mouse:** arraste para girar o cubo.
- **Scroll:** zoom in/out.
- **Shift + Mouse:** pan (mover visão).
- **R:** resetar câmera.
- **ESC:** sair.

## Estrutura dos arquivos

- `cubo.py`: código principal do visualizador.
- `cubo-01.obj`: modelo 3D exportado do Blender.
- `cubo-01.mtl`: materiais do modelo.

## Observações

- O cubo é centralizado e ajustado automaticamente para melhor visualização.
- As cores dos materiais podem ser alteradas no arquivo MTL ou diretamente no código.

---

Aula prática de visualização 3D com Python, OpenGL e Pygame.