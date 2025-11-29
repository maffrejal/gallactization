from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime


class PlanetBiome(db.Model):
    __tablename__ = "planet_biomes"

    id = db.Column(db.Integer, primary_key=True)

    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    biome_id = db.Column(db.String(64), db.ForeignKey("biomes.id"))

    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIXED
    planet = db.relationship("Planet", back_populates="biomes")
    biome = db.relationship("Biome", back_populates="planet_links")