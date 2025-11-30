from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.universe import Universe
from app.models.save_game import SaveGame
from app.models.galaxy import Galaxy
from app.extensions import db

universe_bp = Blueprint("universe", __name__, url_prefix="/universe")


@universe_bp.get("/")
@login_required
def index():
    universes = (
        Universe.query.filter_by(user_id=current_user.id)
        .order_by(Universe.created_at.desc())
        .all()
    )
    return render_template("universe/list.html", universes=universes)


@universe_bp.get("/<int:universe_id>/choose")
@login_required
def choose_universe(universe_id):
    universe = Universe.query.get_or_404(universe_id)
    saves = (
        SaveGame.query.filter_by(universe_id=universe_id)
        .order_by(SaveGame.last_played.desc())
        .all()
    )
    return render_template("universe/saves.html", universe=universe, saves=saves)
