"""
routes/api/central.py
API para panel administrativo central
"""
from flask import Blueprint, request, jsonify, current_app, session, render_template
from werkzeug.utils import secure_filename


import controladores.controlador_camara as controlador_camara
from services.file_service import FileService
from utils.constants import *

camaras_bp = Blueprint('camaras', __name__)

# ==========================================



@camaras_bp.route('/listar', methods=['GET'])
def obtener_camaras():
    try:
        camaras = controlador_camara.listar_camaras()
        camaras_list = []
        for camara in camaras:
            camaras_list.append({
                "id_camara": camara[0],
                "nombre_camara": camara[1],
                "url_camara": camara[2],
                "latitud": camara[3],
                "longitud": camara[4],
                "calle": camara[5],
                "estado": camara[6]
            })
        return jsonify(camaras_list), 200
    except Exception as e:
        current_app.logger.error(f"Error al obtener cámaras: {e}")
        return jsonify({"error": "Error al obtener cámaras"}), 500
    
# ==========================================
@camaras_bp.route('/actualizar/<string:id_camara>', methods=['PUT'])
def actualizar_camara(id_camara):
    try:
        data = request.json
        estado = data.get('estado', 'A')
        if estado is not None:
            estado = 'A' if estado == True else 'I'
        else:
            estado = 'A'
        print(estado)
        controlador_camara.actualizar_camara(
            id_camara,
            data.get('nombre_camara'),
            data.get('url_camara'),
            data.get('latitud'),
            data.get('longitud'),
            data.get('calle'),
            estado
        )
        return jsonify({"code": 1,"message": "Cámara actualizada correctamente"}), 200
    except Exception as e:
        current_app.logger.error(f"Error al actualizar cámara: {e}")
        return jsonify({"code": 0,"error": "Error al actualizar cámara"}), 500
    
    
# ==========================================
@camaras_bp.route('/actualizar_estado/<int:id_camara>', methods=['PATCH'])
def actualizar_estado_camara(id_camara):
    try:
        data = request.json
        nuevo_estado = data.get('estado')
        controlador_camara.actualizar_estado_camara(id_camara, nuevo_estado)
        return jsonify({"message": "Estado de cámara actualizado correctamente"}), 200
    except Exception as e:
        current_app.logger.error(f"Error al actualizar estado de cámara: {e}")
        return jsonify({"error": "Error al actualizar estado de cámara"}), 500

# ==========================================
@camaras_bp.route('/crear', methods=['POST'])
def crear():
    try:
        data = request.json
        estado = data.get('estado', 'A')
        if estado is not None:
            estado = 'A' if estado == True else 'I'
        else:
            estado = 'A'
        controlador_camara.crear_camara(
            data.get('id_camara'),
            data.get('nombre_camara'),
            data.get('url_camara'),
            data.get('latitud'),
            data.get('longitud'),
            data.get('calle'),
            estado
        )
        return jsonify({"code": 1, "message": "Cámara creada correctamente"}), 201
    except Exception as e:
        current_app.logger.error(f"Error al crear cámara: {e}")
        return jsonify({"code": 0, "error": "Error al crear cámara"}), 500