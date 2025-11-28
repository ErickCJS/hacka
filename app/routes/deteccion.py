from flask import Blueprint, jsonify
from ..models.camara import Camara
from ..detection.detector_manager import DetectorManager

deteccion_bp = Blueprint("deteccion", __name__)

@deteccion_bp.route("/probar/<int:id_camara>", methods=["GET"])
def probar(id_camara):
    cam = Camara.query.get(id_camara)
    manager = DetectorManager()
    r = manager.analizar_camara(cam)

    if r:
        return jsonify({
            "placa": r.placa,
            "color": r.color,
            "tipo": r.tipo,
            "camara": cam.nombre
        })

    return jsonify({"mensaje": "Sin detección"})
