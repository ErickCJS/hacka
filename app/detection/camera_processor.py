import cv2
from app.detection.recognition_manager import RecognitionManager

recognizer = RecognitionManager()

def procesar_rtsp(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        return {"error": "No se pudo conectar a la cámara"}

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"error": "No se pudo leer el frame"}

    detecciones = recognizer.procesar_frame(frame)
    return detecciones
