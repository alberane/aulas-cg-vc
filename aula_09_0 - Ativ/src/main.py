import cv2
import numpy as np

def aplicar_sobel(frame_gray):
    sobelx = cv2.Sobel(frame_gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(frame_gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    return sobel

def aplicar_canny(frame_gray, low=100, high=200):
    return cv2.Canny(frame_gray, low, high)

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a webcam.")
        return

    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sobel_edges = aplicar_sobel(frame_gray)
        canny_edges = aplicar_canny(frame_gray)

        cv2.imshow('Webcam - Original', frame)
        cv2.imshow('Bordas - Sobel', sobel_edges)
        cv2.imshow('Bordas - Canny', canny_edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
