from app.extensions import db
from datetime import datetime

class Galaxy(db.Model):
    __tablename__ = "galaxies"

    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey("universes.id"), nullable=False)

    name = db.Column(db.String(120))
    seed = db.Column(db.BigInteger, nullable=False)
    num_stars = db.Column(db.BigInteger)
    type = db.Column(db.String(50))
    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    universe = db.relationship("Universe", back_populates="galaxies")

    systems = db.relationship("StarSystem", back_populates="galaxy", lazy=True)
