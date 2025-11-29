from app.extensions import db
from datetime import datetime

class System(db.Model):
    __tablename__ = "systems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    galaxy_id = db.Column(db.Integer, db.ForeignKey("galaxies.id"))
    position = db.Column(db.Integer, default=1)
    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    planets = db.relationship("Planet", back_populates="system", lazy=True)
    galaxy = db.relationship("Galaxy", back_populates="systems")
