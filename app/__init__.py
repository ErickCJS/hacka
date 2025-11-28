from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(
        __name__
    )

    # CONFIGURACIÓN BASE DE DATOS
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/seguridad"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)

    db.init_app(app)

    # Importar modelos
    from app.models import Camara, Deteccion
    
    # Importar y registrar rutas
    from app.routes import deteccion_bp
    app.register_blueprint(deteccion_bp, url_prefix="/deteccion")
    
    from app.routes.camaras import camaras_bp
    app.register_blueprint(camaras_bp)
    
    
    from app.routes.views import views_bp
    app.register_blueprint(views_bp)    

    from app.routes.deteccion_vehicular import detector_bp
    app.register_blueprint(detector_bp)


    # Tus rutas principales
    @app.route("/")
    def home():
        return "hombres trabajando"

    @app.route("/denuncias", methods=["GET", "POST"])
    def denuncias():
        from flask import render_template
        return render_template("contenido/denuncias.html")

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app
