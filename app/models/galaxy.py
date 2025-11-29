from app.extensions import db
from datetime import datetime

class Galaxy(db.Model):
    __tablename__ = "galaxies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    seed = db.Column(db.Integer, nullable=False)
    num_stars = db.Column(db.Integer, default=0)
    type = db.Column(db.String(50))
    meta = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIX: this relationship MUST exist
    systems = db.relationship("StarSystem", back_populates="galaxy", lazy=True)

