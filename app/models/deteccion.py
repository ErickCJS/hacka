from app import db
from datetime import datetime

class Deteccion(db.Model):
    __tablename__ = "deteccion"

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(20))
    color = db.Column(db.String(20))
    tipo = db.Column(db.String(20))
    id_camara = db.Column(db.Integer, db.ForeignKey("camara.id"))
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    camara = db.relationship("Camara")
