from app.extensions import db
from datetime import datetime

class StarSystem(db.Model):
    __tablename__ = "star_systems"

    id = db.Column(db.Integer, primary_key=True)
    galaxy_id = db.Column(db.Integer, db.ForeignKey("galaxies.id"))
    name = db.Column(db.String(120), nullable=False)
    star_type = db.Column(db.String(50))
    position_x = db.Column(db.Integer)
    position_y = db.Column(db.Integer)
    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    galaxy = db.relationship("Galaxy", back_populates="systems")
    planets = db.relationship("Planet", back_populates="system", lazy=True)
