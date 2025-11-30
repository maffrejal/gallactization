import time
import traceback
from app import create_app
from app.extensions import db
from app.models import JobQueue
from app.services.world_generator import generate_universe

# How often the worker checks for jobs (seconds)
POLL_INTERVAL = 2


def run_worker():
    from app import create_app
    app = create_app()

    with app.app_context():
        print("🛰  Universe Worker Started")

        while True:
            try:
                job = JobQueue.query.filter_by(status="queued").order_by(JobQueue.id.asc()).first()

                if not job:
                    print("🌀 Waiting for jobs...")
                    time.sleep(2)
                    continue

                print(f"🚀 Starting Job #{job.id} for user {job.user_id}")

                job.status = "running"
                db.session.commit()

                # ----- Actual universe generation -----
                try:
                    generate_universe(job.user_id, job)
                    job.status = "done"
                    job.progress = 100
                    job.message = "Universe generation complete"
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    job.status = "error"
                    job.message = str(e)
                    db.session.commit()
                    print(f"❌ Job {job.id} failed: {e}")
                # --------------------------------------

            except Exception as e:
                print(f"💥 Worker crashed: {e}")
                db.session.rollback()
                time.sleep(2)


if __name__ == "__main__":
    run_worker()
