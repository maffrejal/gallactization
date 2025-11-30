from app.extensions import db
from datetime import datetime

class SaveGame(db.Model):
    __tablename__ = "save_games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    universe_id = db.Column(db.Integer, db.ForeignKey("universes.id"), nullable=False)

    name = db.Column(db.String(120))
    progress = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIXED: Add relationship to Universe
    universe = db.relationship("Universe", back_populates="saves")

    def save(self):
        db.session.add(self)
        db.session.commit()
