import time
from app import create_app
from app.extensions import db
from app.models import JobQueue
from app.services.world_generator_async import generate_universe_async

app = create_app()

def run_job_queue_worker():
    with app.app_context():
        while True:
            job = JobQueue.query.filter_by(status="queued").order_by(JobQueue.created_at.asc()).first()
            if job:
                print(f"[WORKER] Running job {job.id} for user {job.user_id}")
                try:
                    generate_universe_async(job.id, job.user_id)
                except Exception as ex:
                    print(f"[WORKER] Job failed: {ex}")
            time.sleep(2)   # poll interval

if __name__ == "__main__":
    run_job_queue_worker()
