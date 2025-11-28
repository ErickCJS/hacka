from flask import Blueprint, jsonify, request
from app.detection.camera_processor import procesar_rtsp

detector_bp = Blueprint("detector", __name__)

@detector_bp.route("/api/detectar", methods=["POST"])
def detectar_vehiculo():
    data = request.json
    rtsp = data.get("rtsp_url")

    result = procesar_rtsp(rtsp)

    return jsonify(result)
