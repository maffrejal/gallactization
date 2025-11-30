from app.extensions import db
from app.models import JobQueue
from datetime import datetime

def enqueue_generate_universe_job(user_id: int) -> int:
    """Adds a universe generation job to the DB queue."""
    job = JobQueue(
        job_type="universe_generation",
        user_id=user_id,
        status="queued",
        progress=0.0,
        meta={"message": "Waiting to start"},
        created_at=datetime.utcnow(),
    )
    db.session.add(job)
    db.session.commit()
    return job.id

def update_job_progress(job_id: int, progress: float, message: str = None):
    """Sets job progress (0.0–1.0)"""
    job = JobQueue.query.get(job_id)
    if not job:
        return
    job.progress = progress
    if message:
        meta = job.meta
        meta["message"] = message
        job.meta = meta
    db.session.commit()

def update_job_status(job_id: int, status: str, message: str = None):
    """Update job status: queued → running → completed/failed"""
    job = JobQueue.query.get(job_id)
    if not job:
        return
    job.status = status
    if message:
        meta = job.meta
        meta["message"] = message
        job.meta = meta
    db.session.commit()

def get_job_status(job_id: int):
    job = JobQueue.query.get(job_id)
    if not job:
        return None
    return {
        "id": job_id,
        "status": job.status,
        "progress": job.progress,
        "meta": job.meta.get("message", "")
    }
