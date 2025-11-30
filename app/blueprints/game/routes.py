from flask import Blueprint, jsonify, redirect, url_for, render_template
from flask_login import current_user, login_required

from app.models import JobQueue
from app.services.job_queue import (
    enqueue_generate_universe_job,
    get_job_status
)

game_bp = Blueprint("game", __name__, url_prefix="/game")


# -------------------------
# START GAME → enqueue job
# -------------------------
@game_bp.post("/start")
@login_required
def start_game():
    job_id = enqueue_generate_universe_job(current_user.id)
    return redirect(url_for("game.job_status_page", job_id=job_id))


# -------------------------
# Job status HTML page
# -------------------------
@game_bp.get("/job/<int:job_id>")
@login_required
def job_status_page(job_id):
    job = JobQueue.query.get(job_id)
    if not job:
        return "Job not found", 404

    return render_template("game/job_status.html", job=job)


# -------------------------
# Job status JSON API (AJAX polling)
# -------------------------
@game_bp.get("/job-status/<int:job_id>")
@login_required
def job_status(job_id):
    status = get_job_status(job_id)
    if not status:
        return jsonify({"error": "Job not found"}), 404

    return jsonify(status)
