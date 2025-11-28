from ultralytics import YOLO
import cv2

class VehicleDetector:

    def __init__(self):
        # Modelo preentrenado en COCO
        self.model = YOLO("yolov8n.pt")

        # Clases vehiculares relevantes
        self.vehicle_classes = {
            2: "car",         # auto
            3: "motorcycle",  # moto
            5: "bus",         # bus
            7: "truck"        # camión
        }

    def detectar(self, frame):
        """Detecta vehículos en un frame"""
        resultados = self.model(frame, verbose=False)

        vehiculos = []

        for r in resultados:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in self.vehicle_classes:

                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    vehiculos.append({
                        "tipo": self.vehicle_classes[cls],
                        "bbox": [int(x1), int(y1), int(x2), int(y2)]
                    })

        return vehiculos
