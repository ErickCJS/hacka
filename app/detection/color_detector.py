import cv2
import numpy as np

class ColorDetector:

    def detectar_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        colores = {
            "rojo": [(0, 50, 50), (10, 255, 255)],
            "amarillo": [(20, 50, 50), (35, 255, 255)],
            "verde": [(45, 50, 50), (85, 255, 255)],
            "azul": [(100, 50, 50), (130, 255, 255)],
            "negro": [(0, 0, 0), (180, 255, 50)],
            "blanco": [(0, 0, 200), (180, 20, 255)],
            "gris": [(0, 0, 60), (180, 30, 200)],
        }

        for nombre, (lower, upper) in colores.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            ratio = cv2.countNonZero(mask) / (frame.size / 3)

            if ratio > 0.05:
                return nombre
        
        return "desconocido"
