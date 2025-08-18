#version 330 core
out vec4 FragColor;
void main()
{
    /*
    `FragColor` é a variável de saída do fragment shader.
    Ela define a cor final de cada pixel (fragmento) que será desenhado na tela.
    Ao atribuir um valor a `FragColor`, você está dizendo ao OpenGL qual cor usar para aquele pixel.
    */
    FragColor = vec4(0.2, 0.5, 1.0, 1.0);
}