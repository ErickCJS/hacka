import cv2
from app.detection.vehicle_detector import VehicleDetector
from app.detection.plate_detector import PlateDetector
from app.detection.color_detector import ColorDetector

class RecognitionManager:

    def __init__(self):
        self.vehiculos = VehicleDetector()
        self.placas = PlateDetector()
        self.colores = ColorDetector()

    def procesar_frame(self, frame):
        """Retorna lista de detecciones completas"""
        detecciones = []

        vehiculos = self.vehiculos.detectar(frame)

        for v in vehiculos:
            x1, y1, x2, y2 = v["bbox"]
            crop = frame[y1:y2, x1:x2]

            placa = self.placas.detectar_placa(crop)
            color = self.colores.detectar_color(crop)
            tipo = v["tipo"]

            detecciones.append({
                "tipo": tipo,
                "color": color,
                "placa": placa,
                "bbox": v["bbox"]
            })

        return detecciones
