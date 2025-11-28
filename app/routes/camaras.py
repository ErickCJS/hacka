# app/routes/camaras.py
from flask import Blueprint, jsonify
from app.models.camara import Camara
from app import db
from flask import request


camaras_bp = Blueprint("camaras", __name__)

@camaras_bp.route("/api/camaras", methods=["GET"])
def listar_camaras():
    camaras = Camara.query.all()
    data = []
    for c in camaras:
        data.append({
            "id": c.id,
            "nombre": c.nombre,
            "lat": c.lat,
            "lon": c.lon,
            "estado": c.estado,
            "sector": getattr(c, "sector", None)  # si luego lo agregas
        })
    return jsonify(data)


@camaras_bp.route("/api/camaras/<int:id>", methods=["GET"])
def obtener_camara(id):
    camara = Camara.query.get(id)
    if not camara:
        return jsonify({"error": "Cámara no encontrada"}), 404

    return jsonify({
        "id": camara.id,
        "nombre": camara.nombre,
        "lat": camara.lat,
        "lon": camara.lon,
        "estado": camara.estado,
        "rtsp_url": camara.rtsp_url
    }), 200


@camaras_bp.route("/api/camaras", methods=["POST"])
def registrar_camara():
    data = request.json

    try:
        nueva = Camara(
            nombre=data.get("nombre"),
            rtsp_url=data.get("rtsp_url"),
            lat=data.get("lat"),
            lon=data.get("lon"),
            estado=data.get("estado", "activa")
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({"mensaje": "Cámara registrada correctamente"}), 201

    except Exception as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error": "No se pudo registrar la cámara"}), 500


@camaras_bp.route("/api/camaras/<int:id>", methods=["PUT"])
def actualizar_camara(id):
    camara = Camara.query.get(id)
    if not camara:
        return jsonify({"error": "Cámara no encontrada"}), 404

    data = request.json

    camara.nombre = data.get("nombre", camara.nombre)
    camara.rtsp_url = data.get("rtsp_url", camara.rtsp_url)
    camara.lat = data.get("lat", camara.lat)
    camara.lon = data.get("lon", camara.lon)
    camara.estado = data.get("estado", camara.estado)

    try:
        db.session.commit()
        return jsonify({"mensaje": "Cámara actualizada"}), 200

    except Exception as e:
        print("Error:", e)
        db.session.rollback()
        return jsonify({"error": "No se pudo actualizar"}), 500


@camaras_bp.route("/api/camaras/<int:id>", methods=["DELETE"])
def eliminar_camara(id):
    camara = Camara.query.get(id)
    if not camara:
        return jsonify({"error": "Cámara no encontrada"}), 404

    try:
        db.session.delete(camara)
        db.session.commit()
        return jsonify({"mensaje": "Cámara eliminada"}), 200

    except Exception as e:
        print("Error:", e)
        db.session.rollback()
        return jsonify({"error": "No se pudo eliminar"}), 500
