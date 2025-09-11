import cv2
import numpy as np

# Variáveis globais
hsv_target = None   # Cor alvo em HSV
tolerance = np.array([10, 50, 50])  # Tolerância para H, S e V

# Função de callback do mouse
def pick_color(event, x, y, flags, param):
    global hsv_target
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_target = hsv_frame[y, x]
        print(f"Cor alvo HSV selecionada: {hsv_target}")

# Captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Exibir a janela da câmera e permitir clique
    cv2.imshow('Camera', frame)
    cv2.setMouseCallback('Camera', pick_color, frame)

    mask = None
    if hsv_target is not None:
        # Definir limites inferior e superior com tolerância
        lower = np.maximum(hsv_target - tolerance, [0, 0, 0])
        upper = np.minimum(hsv_target + tolerance, [179, 255, 255])

        # Criar máscara
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower, upper)
        cv2.imshow('Mascara', mask)

    # Sair ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
