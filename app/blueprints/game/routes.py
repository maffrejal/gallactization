from flask import Blueprint, jsonify, redirect, url_for, render_template
from flask_login import current_user, login_required

from app.models import JobQueue
from app.services.job_queue import (
    enqueue_generate_universe_job,
    get_job_status
)

game_bp = Blueprint("game", __name__, url_prefix="/game")


# --------------------------------------------------------
# 1) Generate New Universe  (formerly "Start Playing")
# --------------------------------------------------------
@game_bp.post("/generate-universe")
@login_required
def generate_universe_route():
    """
    User clicked “Generate New Universe”.
    → Create job
    → Redirect to job status page
    """
    job_id = enqueue_generate_universe_job(current_user.id)
    return redirect(url_for("game.job_status_page", job_id=job_id))



# --------------------------------------------------------
# 2) Job Status HTML page (shows progress)
# --------------------------------------------------------
@game_bp.get("/job/<int:job_id>")
@login_required
def job_status_page(job_id):
    job = JobQueue.query.get(job_id)
    if not job:
        return "Job not found", 404

    # Pass BOTH job and job_id to template
    return render_template("game/job_status.html", job=job, job_id=job_id)


# --------------------------------------------------------
# 3) Job Status JSON for AJAX polling
# --------------------------------------------------------
@game_bp.get("/job-status/<int:job_id>")
@login_required
def job_status(job_id):
    status = get_job_status(job_id)
    if not status:
        return jsonify({"error": "Job not found"}), 404

    # When job is DONE → redirect user to /universe
    if status["status"] == "done":
        status["redirect"] = url_for("universe.index")

    return jsonify(status)



# --------------------------------------------------------
# 4) Start Game SESSION  (load/save game)
# --------------------------------------------------------
@game_bp.get("/session/<int:save_id>")
@login_required
def start_session(save_id):
    """
    Load a saved game or start new one.
    """
    return f"Starting gameplay session for save {save_id} (TODO)"
