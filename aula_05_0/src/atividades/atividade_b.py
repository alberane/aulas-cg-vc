import cv2
import numpy as np

def gerar_paleta(bgr_base):
    """
    Gera uma paleta vertical de 5 tons de uma cor base BGR,
    variando o componente V no espaço HSV.
    """
    # Converte a cor base BGR para HSV
    cor_bgr = np.uint8([[bgr_base]])
    cor_hsv = cv2.cvtColor(cor_bgr, cv2.COLOR_BGR2HSV)[0][0]

    h, s, _ = cor_hsv

    # Valores de brilho (V) do mais escuro para o mais claro
    valores_v = np.linspace(50, 255, 5, dtype=np.uint8)

    # Dimensões da paleta
    altura, largura = 100, 200
    paleta = np.zeros((altura * 5, largura, 3), dtype=np.uint8)

    for i, v in enumerate(valores_v):
        # Cria a nova cor em HSV com o V atualizado
        nova_cor_hsv = np.array([[[h, s, v]]], dtype=np.uint8)
        nova_cor_bgr = cv2.cvtColor(nova_cor_hsv, cv2.COLOR_HSV2BGR)[0][0]

        # Preenche a faixa da paleta
        paleta[i * altura:(i + 1) * altura, :] = nova_cor_bgr

    return paleta


if __name__ == "__main__":
    # Exemplo: azul em BGR (255, 0, 0)
    cor_base = (255, 0, 0)

    paleta = gerar_paleta(cor_base)

    cv2.imshow("Paleta de Cores", paleta)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
