from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class JobQueue(db.Model):
    __tablename__ = "job_queue"

    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="queued")  # queued, running, completed, failed
    progress = db.Column(db.Float, default=0.0)

    meta = db.Column(JSONB, default={})

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
