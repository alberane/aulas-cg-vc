import cv2
from ultralytics import YOLO
import sys

def detectar_objetos(caminho_imagem):
    """
    Detecta objetos em uma imagem usando YOLO

    Args:
        caminho_imagem: Caminho para o arquivo de imagem
    """

    # Carregar o modelo YOLO
    print("Carregando modelo YOLO...")
    model = YOLO('yolov8m.pt')

    # Carregar a imagem
    print(f"Carregando imagem: {caminho_imagem}")
    imagem = cv2.imread(caminho_imagem)

    if imagem is None:
        print("Erro: Não foi possível carregar a imagem")
        print("Verifique se o caminho está correto")
        return

    # Realizar detecção
    print("Detectando objetos...")
    results = model(imagem)

    # Obter informações das detecções
    detections = results[0].boxes

    # Mostrar resultados no console
    print(f"\n{'='*50}")
    print(f"OBJETOS DETECTADOS: {len(detections)}")
    print(f"{'='*50}\n")

    if len(detections) > 0:
        for i, box in enumerate(detections):
            # Obter informações da detecção
            classe_id = int(box.cls[0])
            confianca = float(box.conf[0])
            nome_classe = model.names[classe_id]

            # Obter coordenadas da caixa
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            print(f"{i+1}. {nome_classe.upper()}")
            print(f"   Confiança: {confianca*100:.1f}%")
            print(f"   Posição: ({int(x1)}, {int(y1)}) -> ({int(x2)}, {int(y2)})")
            print()
    else:
        print("Nenhum objeto detectado na imagem")

    # Obter imagem anotada com as detecções
    imagem_anotada = results[0].plot()

    # Redimensionar se a imagem for muito grande
    altura, largura = imagem_anotada.shape[:2]
    max_dim = 1200

    if largura > max_dim or altura > max_dim:
        escala = max_dim / max(largura, altura)
        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)
        imagem_anotada = cv2.resize(imagem_anotada, (nova_largura, nova_altura))

    # Exibir a imagem
    cv2.imshow('Detecção de Objetos - YOLO', imagem_anotada)
    print(f"{'='*50}")
    print("Pressione qualquer tecla para fechar a janela")
    print(f"{'='*50}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Salvar imagem com detecções
    nome_saida = caminho_imagem.rsplit('.', 1)[0] + '_detectado.jpg'
    cv2.imwrite(nome_saida, imagem_anotada)
    print(f"\nImagem salva como: {nome_saida}")

def main():
    """Função principal"""

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python script.py <caminho_da_imagem>")
        print("\nExemplo:")
        print("  python script.py foto.jpg")
        print("  python script.py C:/imagens/minha_foto.png")

        # Permitir entrada manual se não houver argumento
        print("\nOu digite o caminho da imagem agora:")
        caminho = input("Caminho: ").strip()

        if not caminho:
            print("Nenhum caminho fornecido. Encerrando.")
            return
    else:
        caminho = sys.argv[1]

    # Detectar objetos
    detectar_objetos(caminho)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário")
    except Exception as e:
        print(f"\nErro: {e}")
        print("\nCertifique-se de instalar as dependências:")
        print("pip install ultralytics opencv-python")