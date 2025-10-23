import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image

def load_and_preprocess_image(img_path, target_size=(224, 224)):
    """
    Carrega uma imagem usando OpenCV e a pré-processa para o modelo Keras.
    """
    # Carregar imagem com OpenCV
    # OpenCV carrega imagens no formato BGR
    img_cv = cv2.imread(img_path)
    if img_cv is None:
        print(f"Erro: Não foi possível carregar a imagem em {img_path}")
        return None

    # Redimensionar a imagem para o tamanho esperado pelo modelo
    img_resized = cv2.resize(img_cv, target_size)

    # Converter BGR (OpenCV) para RGB (Keras/TensorFlow)
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    # Converter a imagem para um array NumPy
    img_array = keras_image.img_to_array(img_rgb)

    # Expandir dimensões para criar um "batch" de 1 imagem
    # O modelo espera (batch_size, height, width, channels)
    # Nosso array está (height, width, channels) -> (1, height, width, channels)
    img_expanded = np.expand_dims(img_array, axis=0)

    # Aplicar o pré-processamento específico do MobileNetV2
    # (Normaliza os pixels para o intervalo [-1, 1])
    img_preprocessed = preprocess_input(img_expanded)

    return img_preprocessed, img_cv

def classify_image(model, preprocessed_img, original_img_cv, top_n=3):
    """
    Realiza a predição e exibe os resultados na imagem original.
    """
    # Fazer a predição
    predictions = model.predict(preprocessed_img)

    # Decodificar as predições
    # Converte as probabilidades em rótulos legíveis (ex: 'tráfego')
    decoded_preds = decode_predictions(predictions, top=top_n)[0]

    print("Predições:")

    # Preparar o texto para exibir na imagem
    text_lines = []
    for i, (imagenet_id, label, prob) in enumerate(decoded_preds):
        text = f"{i+1}: {label} ({prob*100:.2f}%)"
        print(text)
        text_lines.append(text)

    # Desenhar o resultado na imagem original (usando OpenCV)
    (h, w) = original_img_cv.shape[:2]

    # Adiciona um fundo preto no topo para legibilidade
    overlay_height = (len(text_lines) * 20) + 15
    cv2.rectangle(original_img_cv, (0, 0), (w, overlay_height), (0, 0, 0), -1)

    for i, line in enumerate(text_lines):
        y_pos = 15 + i * 20
        cv2.putText(original_img_cv, line, (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibir a imagem
    cv2.imshow("Classificacao de Imagem", original_img_cv)
    print("\nPressione qualquer tecla para fechar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # Carregar o modelo pré-treinado (Classificação Principalmente)
    # (Será baixado automaticamente na primeira execução)
    # Documentação - https://keras.io/api/applications/mobilenet/#mobilenet-mobilenetv2-and-mobilenetv3
    print("Carregando modelo MobileNetV2...")
    model = MobileNetV2(weights='imagenet')
    print("Modelo carregado.")

    # 2. Escolher uma imagem de entrada
    # (Ex: uma foto de um cachorro, carro, teclado, etc.)
    image_path = "sample_images/rua3.jpg" # Use um caminho válido

    # Tentar criar uma imagem de exemplo se o caminho não existir
    try:
        if not tf.io.gfile.exists(image_path):
            print(f"Aviso: Caminho {image_path} não encontrado.")
            print("Tentando baixar uma imagem de exemplo...")
            image_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg"
            image_path_obj = tf.keras.utils.get_file('grace_hopper.jpg', origin=image_url)
            # Para o nosso script, precisamos copiá-lo para o local esperado
            import os
            if not os.path.exists('sample_images'):
                os.makedirs('sample_images')
            import shutil
            shutil.copy(image_path_obj, image_path)
            print(f"Imagem de exemplo salva em {image_path}")

    except Exception as e:
        print(f"Erro ao baixar imagem de exemplo: {e}")
        print("Por favor, forneça um caminho válido para a variável 'image_path'")
        return

    # 3. Carregar e pré-processar
    preprocessed_img, original_img = load_and_preprocess_image(image_path)

    if preprocessed_img is None:
        return

    # 4. Classificar e exibir
    classify_image(model, preprocessed_img, original_img)

if __name__ == "__main__":
    main()