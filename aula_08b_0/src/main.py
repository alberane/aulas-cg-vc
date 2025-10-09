import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuração Inicial ---
# 1. Certifique-se de ter uma imagem chamada 'exemplo.jpg' no mesmo diretório.
#    (Se não tiver, crie um arquivo fictício ou substitua o nome do arquivo).
NOME_ARQUIVO = 'exemplo.jpg'

# Cria um arquivo fictício se o exemplo não existir (apenas para o código rodar)
if not os.path.exists(NOME_ARQUIVO):
    print(f"ATENÇÃO: Arquivo '{NOME_ARQUIVO}' não encontrado. Criando um array numpy de 100x100 para demonstração.")
    # Cria um array 3D de 100x100 com 3 canais de cor (BGR), preenchido com azul
    imagem_ficticia = np.full((100, 100, 3), [255, 0, 0], dtype=np.uint8)  # B=255, G=0, R=0 (Azul)
    cv2.imwrite(NOME_ARQUIVO, imagem_ficticia)


def carregar_e_converter_imagem(caminho_da_imagem):
    """
    Carrega uma imagem e demonstra suas propriedades e conversões de cor.
    """
    # 1. Leitura da Imagem
    imagem_bgr = cv2.imread(caminho_da_imagem)

    # Verifica se a imagem foi carregada corretamente
    if imagem_bgr is None:
        print(f"Erro: Não foi possível carregar a imagem em '{caminho_da_imagem}'")
        return

    print("--- Propriedades da Imagem Original (BGR) ---")
    print(f"Dimensões (formato): {imagem_bgr.shape} (Altura, Largura, Canais)")
    print(f"Tipo de dados: {imagem_bgr.dtype} (Geralmente uint8, 0-255)")
    print(f"Tamanho total (pixels): {imagem_bgr.size}")
    print(f"Valor do pixel (10, 50) [B, G, R]: {imagem_bgr[10, 50]}")

    # 2. Conversão para Escala de Cinza
    imagem_cinza = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)
    print("\n--- Propriedades da Imagem em Tons de Cinza ---")
    print(f"Dimensões (formato): {imagem_cinza.shape} (Altura, Largura)")
    print(f"Valor do pixel (10, 50): {imagem_cinza[10, 50]}")

    # 3. Conversão para HSV (Matiz, Saturação, Valor)
    imagem_hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)
    print("\n--- Propriedades da Imagem HSV ---")
    print(f"Dimensões (formato): {imagem_hsv.shape} (Altura, Largura, Canais: H, S, V)")
    print(f"Valor do pixel (10, 50) [H, S, V]: {imagem_hsv[10, 50]}")

    # 4. Salvando a Imagem
    cv2.imwrite('exemplo_cinza.jpg', imagem_cinza)
    print("\nImagem 'exemplo_cinza.jpg' salva com sucesso.")

    # 5. Visualização com Matplotlib
    imagem_rgb = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(imagem_rgb)
    plt.title('Original (RGB)')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(imagem_cinza, cmap='gray')
    plt.title('Escala de Cinza')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    imagem_hsv_rgb = cv2.cvtColor(imagem_hsv, cv2.COLOR_HSV2RGB)
    plt.imshow(imagem_hsv_rgb)
    plt.title('HSV (Visualizado como RGB)')
    plt.axis('off')

    plt.show()


# Execução da função principal
carregar_e_converter_imagem(NOME_ARQUIVO)


# --- Exemplo de Manipulação de Pixels e Canais ---
def manipular_brilho_e_canais(caminho_da_imagem):
    """
    Demonstra a manipulação de brilho e a separação de canais.
    """
    imagem = cv2.imread(caminho_da_imagem)

    if imagem is None:
        print(f"Erro: Não foi possível carregar a imagem em '{caminho_da_imagem}'")
        return

    # Separando os canais (B, G, R)
    azul, verde, vermelho = cv2.split(imagem)

    # Aumentando o brilho
    fator_brilho = 50
    matriz_brilho = np.ones(imagem.shape, dtype="uint8") * fator_brilho
    imagem_brilhante = cv2.add(imagem, matriz_brilho)

    # Removendo o canal azul
    imagem_sem_azul = imagem.copy()
    imagem_sem_azul[:, :, 0] = 0  # Canal 0 (B)

    # Visualização
    figura, eixos = plt.subplots(2, 3, figsize=(15, 8))

    eixos[0, 0].imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    eixos[0, 0].set_title('Original')
    eixos[0, 0].axis('off')

    eixos[0, 1].imshow(azul, cmap='gray')
    eixos[0, 1].set_title('Canal Azul')
    eixos[0, 1].axis('off')

    eixos[0, 2].imshow(vermelho, cmap='gray')
    eixos[0, 2].set_title('Canal Vermelho')
    eixos[0, 2].axis('off')

    eixos[1, 0].imshow(cv2.cvtColor(imagem_brilhante, cv2.COLOR_BGR2RGB))
    eixos[1, 0].set_title(f'Brilho +{fator_brilho}')
    eixos[1, 0].axis('off')

    eixos[1, 1].imshow(cv2.cvtColor(imagem_sem_azul, cv2.COLOR_BGR2RGB))
    eixos[1, 1].set_title('Canal Azul Removido')
    eixos[1, 1].axis('off')

    eixos[1, 2].axis('off')
    eixos[1, 2].set_title('Exemplo de Processamento')

    plt.tight_layout()
    plt.show()


# Execução da segunda função
manipular_brilho_e_canais(NOME_ARQUIVO)
