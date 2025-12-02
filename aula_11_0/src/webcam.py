import cv2
import time
from ultralytics import YOLO

def main():
    """
    Programa para detecção de objetos em tempo real usando YOLOv8 e webcam
    """

    # Carregar o modelo YOLO (usando YOLOv8n - versão nano, mais rápida)
    print("Carregando modelo YOLO...")
    model = YOLO('yolov8s.pt')

    # Inicializar webcam
    print("Inicializando webcam...")
    cap = cv2.VideoCapture(0)

    # Verificar se a webcam foi aberta corretamente
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam")
        return

    # Configurar resolução
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Pressione 'q' para sair")
    print("Detecção iniciada...")

    # Variáveis para calcular FPS
    prev_time = time.time()
    fps = 0

    try:
        while True:
            # Capturar frame da webcam
            ret, frame = cap.read()

            if not ret:
                print("Erro ao capturar frame")
                break

            # Realizar detecção com YOLO
            results = model(frame, verbose=False)

            # Obter o frame anotado com as detecções
            annotated_frame = results[0].plot()

            # Calcular FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # Adicionar informações na tela
            cv2.putText(annotated_frame, f'FPS: {int(fps)}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Exibir número de objetos detectados
            num_detections = len(results[0].boxes)
            cv2.putText(annotated_frame, f'Objetos: {num_detections}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Mostrar o frame em uma janela única
            cv2.imshow('YOLO - Deteccao de Objetos', annotated_frame)

            # Sair se pressionar 'q' ou ESC
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                print("Encerrando...")
                break

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário")

    finally:
        # Liberar recursos
        cap.release()
        cv2.destroyAllWindows()
        # Aguardar um momento para garantir que as janelas sejam fechadas
        cv2.waitKey(1)
        print("Programa finalizado")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}")
        print("\nCertifique-se de instalar as dependências:")
        print("pip install ultralytics opencv-python")