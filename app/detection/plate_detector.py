import easyocr
import cv2

class PlateDetector:

    def __init__(self):
        self.reader = easyocr.Reader(['es'], gpu=False)

    def detectar_placa(self, frame):
        resultados = self.reader.readtext(frame)

        for (_, texto, _) in resultados:
            texto = texto.upper().replace(" ", "")

            # Validación simple de placa peruana
            if len(texto) >= 5 and "-" in texto or texto.isalnum():
                return texto

        return None
