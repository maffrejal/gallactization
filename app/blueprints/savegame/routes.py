from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.models.save_game import SaveGame
from app.models.universe import Universe
from app.extensions import db
from datetime import datetime

savegame_bp = Blueprint("savegame", __name__, url_prefix="/save")


@savegame_bp.post("/new/<int:universe_id>")
@login_required
def new_game(universe_id):
    # Create initial new save
    save = SaveGame(
        user_id=current_user.id,
        universe_id=universe_id,
        name=f"Save {datetime.utcnow().strftime('%Y%m%d_%H%M')}",
        snapshot={}
    )
    db.session.add(save)
    db.session.commit()

    return redirect(url_for("game.start_session", save_id=save.id))


@savegame_bp.get("/load/<int:save_id>")
@login_required
def load_game(save_id):
    save = SaveGame.query.get_or_404(save_id)

    # Mark last played
    save.last_played = datetime.utcnow()
    db.session.commit()

    return redirect(url_for("game.start_session", save_id=save.id))
    
@savegame_bp.get("/universe/<int:universe_id>/saves")
@login_required
def list_for_universe(universe_id):
    # Get universe (optional sanity check)
    universe = Universe.query.filter_by(id=universe_id, user_id=current_user.id).first_or_404()

    # Load all saves for this universe
    saves = SaveGame.query.filter_by(
        universe_id=universe_id,
        user_id=current_user.id
    ).order_by(SaveGame.created_at.desc()).all()

    return render_template(
        "savegame/list.html",
        universe=universe,
        saves=saves,
    )