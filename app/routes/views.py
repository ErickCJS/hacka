from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

# Ruta para mostrar el mapa de cámaras
@views_bp.route("/camaras")
def vista_camaras():
    return render_template("contenido/camaras.html")

