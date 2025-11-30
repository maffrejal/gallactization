import time
import traceback
from app import create_app
from app.extensions import db
from app.models import JobQueue
from app.services.world_generator import generate_universe

# How often the worker checks for jobs (seconds)
POLL_INTERVAL = 2


def run_worker():
    app = create_app()
    app.app_context().push()

    print("🛰  Universe Worker Started")
    print("🌀 Waiting for jobs...")

    while True:
        try:
            # get next pending job
            job = JobQueue.query.filter_by(status="queued").order_by(JobQueue.id.asc()).first()

            if not job:
                time.sleep(POLL_INTERVAL)
                continue

            print(f"🚀 Starting Job #{job.id} for user {job.user_id}")

            job.status = "running"
            job.progress = 0
            job.message = "Universe generation started"
            db.session.commit()

            try:
                # run universe generator
                generate_universe(job.user_id, job)

                job.status = "done"
                job.progress = 100
                job.message = "Universe generation completed!"
                db.session.commit()

                print(f"✅ Job #{job.id} completed successfully")

            except Exception as e:
                job.status = "error"
                job.message = str(e)
                job.progress = 0
                db.session.commit()

                print(f"❌ Job #{job.id} failed:")
                traceback.print_exc()

        except Exception as worker_err:
            print("🔥 Worker internal error:")
            traceback.print_exc()

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_worker()
