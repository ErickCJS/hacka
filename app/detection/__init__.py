"""
Módulo de Detección Vehicular
Incluye lectura de cámaras, OCR de placas, detección de color y tipo de vehículo.
"""

from .detector_manager import DetectorManager
from .plate_detector import PlateDetector
from .vehicle_detector import VehicleDetector
from .camera_stream import CameraStream

__all__ = [
    "DetectorManager",
    "PlateDetector",
    "VehicleDetector",
    "CameraStream"
]
