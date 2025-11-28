from ..models.camara import Camara
from ..models.deteccion import Deteccion
from app import db
from ..detection.camera_stream import CameraStream
from ..detection.plate_detector import PlateDetector
from ..detection.vehicle_detector import VehicleDetector

class DetectorManager:

    def __init__(self):
        self.placas = PlateDetector()
        self.vehiculos = VehicleDetector()

    def analizar_camara(self, camara: Camara):
        stream = CameraStream(camara.rtsp_url)

        frame = stream.get_frame()
        stream.release()

        if frame is None:
            return None

        placa = self.placas.detectar_placa(frame)
        color = self.vehiculos.detectar_color(frame)
        tipo = self.vehiculos.detectar_tipo(frame)

        if not placa:
            return None

        # guardar detección
        registro = Deteccion(
            placa=placa,
            color=color,
            tipo=tipo,
            id_camara=camara.id
        )
        db.session.add(registro)
        db.session.commit()

        return registro
