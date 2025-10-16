import cv2
import numpy as np

# --- Configurações ---
WEBCAM_INDEX = 0      # 0 para a primeira webcam disponível
MIN_CONTOUR_AREA = 1000 # Área mínima do contorno para ser considerado movimento (Aumentar para reduzir ruído)
BLUR_KERNEL = (5, 5)  # Kernel para o filtro Gaussiano

# Variáveis para rastrear o histórico de área e tempo (Otimização para Direção)
historico_areas = []
MAX_HISTORICO = 15      # Aumentado o histórico para estabilizar a direção (15 frames)
MIN_AREA_DIF = 1500     # Diferença mínima de área absoluta para indicar aproximação/recuo

# --- Inicialização do Subtrator de Fundo MOG2 ---
# Aprende e mantém um modelo de fundo estável.
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

def inicializar_webcam():
    """Inicializa a captura da webcam."""
    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        exit()
    print("Webcam inicializada (MOG2). Pressione 'q' para sair.")
    return cap

def pre_processamento(frame):
    """Aplica o pré-processamento para detecção de movimento."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Suaviza a imagem para reduzir ruído, essencial antes do MOG2.
    blur = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
    return blur

def detectar_movimento_e_direcao(frame_atual, fgbg, historico_areas):
    """
    Detecta o movimento usando MOG2, encontra contornos e determina a direção.
    Retorna a máscara de movimento, a área do maior contorno, a bounding box e o status de direção.
    """
    frame_suave = pre_processamento(frame_atual)

    # 1. Subtração de Fundo (MOG2) - Gera uma máscara binária (foreground)
    mascara = fgbg.apply(frame_suave)

    # 2. Operações Morfológicas (Abertura/Fechamento) para limpar a máscara
    # (Remover pequenos ruídos e preencher buracos)
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations=1)
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    # 3. Encontrar contornos
    contornos, _ = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    maior_contorno = None
    max_area = 0
    bbox = None

    # Encontrar o maior contorno de movimento (filtrando por área mínima)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > MIN_CONTOUR_AREA and area > max_area:
            max_area = area
            maior_contorno = c
            bbox = cv2.boundingRect(c)

    # 4. Determinar a Direção (Aproximação ou Recuo)
    direcao_status = "Aguardando Movimento..."

    if maior_contorno is not None:
        historico_areas.append(max_area)

        # Manter apenas os últimos N frames para o histórico
        if len(historico_areas) > MAX_HISTORICO:
            historico_areas.pop(0)

            # Comparação da área atual com a média das áreas anteriores
            area_media_antiga = np.mean(historico_areas[:-1])
            area_atual = historico_areas[-1]

            diferenca_area = area_atual - area_media_antiga

            if diferenca_area > MIN_AREA_DIF:
                direcao_status = "APROXIMAÇÃO (Objeto Maior) >>"
            elif diferenca_area < -MIN_AREA_DIF:
                direcao_status = "<< RECUO (Objeto Menor)"
            else:
                direcao_status = "Movimento Lateral/Estático"

        # Desenhar a Bounding Box no frame original
        x, y, w, h = bbox
        cv2.rectangle(frame_atual, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame_atual, f"Area: {max_area:.0f}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame_suave, mascara, bbox, direcao_status

def aplicar_filtros_borda(frame, bbox):
    """Aplica os filtros Sobel e Canny na região do movimento."""

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    canny_img = np.zeros_like(gray)
    sobel_combinado = np.zeros_like(gray)

    # Aplicar filtros SOMENTE na região do Bounding Box (bbox)
    if bbox is not None:
        x, y, w, h = bbox
        # Define a região de interesse (ROI) com margem de segurança
        margin = 10
        x_min, y_min = max(0, x - margin), max(0, y - margin)
        x_max, y_max = min(frame.shape[1], x + w + margin), min(frame.shape[0], y + h + margin)

        regiao = blurred[y_min:y_max, x_min:x_max]

        if regiao.size > 0:
            # --- Filtro Canny ---
            # Thresholds ajustados para detecção de bordas mais finas
            edges_canny = cv2.Canny(regiao, 30, 90)
            canny_img[y_min:y_max, x_min:x_max] = edges_canny

            # --- Filtro Sobel ---
            sobel_x = cv2.Sobel(regiao, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(regiao, cv2.CV_64F, 0, 1, ksize=3)

            abs_sobel_x = cv2.convertScaleAbs(sobel_x)
            abs_sobel_y = cv2.convertScaleAbs(sobel_y)

            sobel_comb = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)
            sobel_combinado[y_min:y_max, x_min:x_max] = sobel_comb

    return canny_img, sobel_combinado

def exibir_resultados(frame_original, canny, sobel_comb, mascara, direcao_status):
    """Organiza e exibe os frames em janelas."""

    # Exibir status de direção em destaque no frame original
    cor_texto = (0, 0, 255) if "APROXIMAÇÃO" in direcao_status else (255, 0, 0) if "RECUO" in direcao_status else (255, 255, 0)

    cv2.putText(frame_original, f"DIRECAO: {direcao_status}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_texto, 2)

    # Converter Sobel e Canny para BGR para empilhamento colorido e adicionar texto
    canny_bgr = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    sobel_bgr = cv2.cvtColor(sobel_comb, cv2.COLOR_GRAY2BGR)
    mascara_bgr = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)

    cv2.putText(canny_bgr, "Canny Borda", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(sobel_bgr, "Sobel Borda", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(mascara_bgr, "Mascara MOG2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Empilhamento horizontal das visualizações
    borda_stack = np.hstack([canny_bgr, sobel_bgr, mascara_bgr])

    # Exibir todas as janelas
    cv2.imshow("01 - Original e Direcao", frame_original)
    cv2.imshow("02 - Detecao de Bordas e Mascara", borda_stack)

def loop_principal():
    """Função principal que gerencia a captura e o processamento de frames."""
    cap = inicializar_webcam()

    # O fgbg (MOG2) é inicializado globalmente

    while True:
        ret, frame_atual = cap.read()
        if not ret:
            break

        # Espelhar a imagem
        frame_atual = cv2.flip(frame_atual, 1)

        # 1. Detecção de Movimento (MOG2) e Direção (Área do Contorno)
        _, mascara_movimento, bbox, direcao_status = \
            detectar_movimento_e_direcao(frame_atual, fgbg, historico_areas)

        # 2. Aplicação dos Filtros de Borda (Sobel e Canny)
        canny_img, sobel_combinado = aplicar_filtros_borda(frame_atual, bbox)

        # 3. Exibição dos Resultados
        exibir_resultados(frame_atual, canny_img, sobel_combinado, mascara_movimento, direcao_status)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Limpeza ---
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    loop_principal()