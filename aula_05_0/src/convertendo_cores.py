import cv2
import numpy as np

def executar():
    # Cria uma imagem preta de 400x600 com 3 canais de cor (BGR)
    # Lembrete: o OpenCV usa o padrão BGR por padrão, não RGB!
    largura, altura = 600, 400
    imagem_bgr = np.zeros((altura, largura, 3), dtype=np.uint8)

    # --- Desenhando retângulos coloridos na imagem BGR ---
    # Cores no formato BGR (Azul, Verde, Vermelho)
    VERMELHO_BGR = (0, 0, 255)
    VERDE_BGR = (0, 255, 0)
    AZUL_BGR = (255, 0, 0)
    AMARELO_BGR = (0, 255, 255)

    # Preenche regiões da imagem com cores sólidas
    imagem_bgr[50:150, 50:250] = VERMELHO_BGR     # Retângulo vermelho
    imagem_bgr[50:150, 350:550] = VERDE_BGR       # Retângulo verde
    imagem_bgr[250:350, 50:250] = AZUL_BGR        # Retângulo azul
    imagem_bgr[250:350, 350:550] = AMARELO_BGR    # Retângulo amarelo

    cv2.imshow("Imagem Original (BGR)", imagem_bgr)

    # --- Conversão para o modelo HSV ---
    imagem_hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)

    # Importante: os valores de HSV no OpenCV são escalonados assim:
    # H (Matiz): 0-179 (para caber em 8 bits)
    # S (Saturação): 0-255
    # V (Valor/Brilho): 0-255

    # Separa os canais H, S e V
    canal_h, canal_s, canal_v = cv2.split(imagem_hsv)

    # Mostra cada canal em escala de cinza
    cv2.imshow("Canal H (Matiz)", canal_h)
    cv2.imshow("Canal S (Saturacao)", canal_s)
    cv2.imshow("Canal V (Valor/Brilho)", canal_v)

    print("Pressione qualquer tecla para sair...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    executar()
