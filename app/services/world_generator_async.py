from app.services.world_generator import generate_universe
from app.services.job_queue import update_job_status, update_job_progress
from app.extensions import db

def generate_universe_async(job_id: int, user_id: int):
    """Runs the full generator but updates progress and does not block Flask."""
    try:
        update_job_status(job_id, "running", "Starting universe generation…")

        # We override generate_universe() internal printouts using a callback
        def progress_callback(stage: str, done: int, total: int):
            pct = done / total if total else 0
            update_job_progress(job_id, pct, f"{stage}: {done}/{total}")

        result = generate_universe(
            user_id=user_id,
            force=True,
            progress_callback=progress_callback
        )

        update_job_status(job_id, "completed", "Universe generation completed.")
        update_job_progress(job_id, 1.0)

        return result

    except Exception as ex:
        update_job_status(job_id, "failed", f"Error: {str(ex)}")
        db.session.rollback()
        raise
