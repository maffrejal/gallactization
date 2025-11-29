from app.extensions import db
from datetime import datetime

class Planet(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    system_id = db.Column(db.Integer, db.ForeignKey("systems.id"))
    size = db.Column(db.Integer, default=1)
    position = db.Column(db.Integer, default=1)
    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    system = db.relationship("System", back_populates="planets")

    # FIXED — NO backref, NO duplicate attribute
    biomes = db.relationship("PlanetBiome", back_populates="planet", lazy=True)
