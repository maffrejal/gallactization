from app.extensions import db
from datetime import datetime

class Universe(db.Model):
    __tablename__ = "universes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(120))
    seed = db.Column(db.BigInteger, nullable=False)  # <-- FIX ADDED HERE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    meta = db.Column(db.JSON, default={})

    galaxies = db.relationship("Galaxy", back_populates="universe", lazy=True)
    saves = db.relationship("SaveGame", back_populates="universe", lazy=True)
