#version 330 core
layout (location = 0) in vec2 a_position;
uniform mat4 u_transform;

void main()
{
    /*

    `gl_Position` é uma variável especial no vertex shader que define a posição do vértice na tela.
    O OpenGL usa essa posição para determinar onde desenhar o vértice no espaço de tela.
    A multiplicação `u_transform * vec4(a_position, 0.0, 1.0)` aplica uma transformação à posição do vértice.

    `u_transform` é uma matriz de transformação que pode incluir translações, rotações e escalas.

    `a_position` é a posição do vértice em coordenadas de espaço do objeto.
    O vetor `vec4(a_position, 0.0, 1.0)` converte as coordenadas 2D do vértice em um vetor 4D,
    onde `0.0` é a coordenada Z (profundidade) e `1.0` é a coordenada W (homogeneização).
    Isso é necessário porque o OpenGL trabalha com coordenadas 4D para realizar transformações adequadas.

    A multiplicação resulta em uma nova posição transformada que é então atribuída a `gl_Position`.
    Essa posição transformada é usada pelo OpenGL para determinar onde o vértice deve ser desenhado na tela.
    Portanto, ao definir `gl_Position`, você está especificando a posição final do vértice após todas as transformações aplicadas.

    */
    gl_Position = u_transform * vec4(a_position, 0.0, 1.0);
}