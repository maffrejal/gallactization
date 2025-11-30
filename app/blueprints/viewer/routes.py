from flask import Blueprint, render_template
from app.models.galaxy import Galaxy
from app.services.system_generator import generate_star_systems_for_galaxy
from app.models.system import StarSystem

viewer_bp = Blueprint("viewer", __name__, url_prefix="/viewer")

@viewer_bp.route("/galaxy-map")
def galaxy_map():
    return render_template("galaxy_map/index.html")
@viewer_bp.route("/galaxy/<int:gid>")
@viewer_bp.route("/galaxy/<int:gid>")
def galaxy_detail(gid):
    galaxy = Galaxy.query.get_or_404(gid)

    # Auto-generate star systems if missing
    #systems = generate_star_systems_for_galaxy(galaxy, n=10)
    systems = StarSystem.query.filter_by(galaxy_id=gid).all()

    return render_template("galaxy_map/galaxy_detail.html",
                           galaxy=galaxy,
                           systems=systems)
