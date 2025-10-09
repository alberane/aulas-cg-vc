import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuração Inicial ---
NOME_ARQUIVO = 'exemplo.jpg'

# Cria uma imagem fictícia azul caso o arquivo não exista (para teste)
if not os.path.exists(NOME_ARQUIVO):
    print(f"ATENÇÃO: Arquivo '{NOME_ARQUIVO}' não encontrado. Criando imagem fictícia 100x100.")
    imagem_ficticia = np.full((100, 100, 3), [255, 0, 0], dtype=np.uint8)  # BGR: azul
    cv2.imwrite(NOME_ARQUIVO, imagem_ficticia)


# --- Função Principal ---
def exibir_canal_verde(caminho_da_imagem):
    """
    Exibe apenas o canal verde de uma imagem colorida (BGR).
    """
    # 1. Leitura da imagem
    imagem_bgr = cv2.imread(caminho_da_imagem)

    if imagem_bgr is None:
        print(f"Erro: Não foi possível carregar a imagem em '{caminho_da_imagem}'")
        return

    # 2. Separação dos canais B, G e R
    canal_azul, canal_verde, canal_vermelho = cv2.split(imagem_bgr)

    # 3. Criação de matrizes de zeros para os canais azul e vermelho
    zeros = np.zeros_like(canal_verde)

    # 4. Combinação dos canais (somente verde visível)
    imagem_somente_verde = cv2.merge([zeros, canal_verde, zeros])

    # 5. Conversão para RGB (para exibir corretamente com Matplotlib)
    imagem_rgb = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2RGB)
    imagem_verde_rgb = cv2.cvtColor(imagem_somente_verde, cv2.COLOR_BGR2RGB)

    # 6. Exibição das imagens
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(imagem_rgb)
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(imagem_verde_rgb)
    plt.title('Canal Verde')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


# --- Execução ---
if __name__ == "__main__":
    print("Atividade 2 - Filtragem de Cor Simples")
    exibir_canal_verde(NOME_ARQUIVO)
