from app import db

class Camara(db.Model):
    __tablename__ = "camara"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60))
    rtsp_url = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    estado = db.Column(db.String(20), default="activa")
