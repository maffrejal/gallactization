from flask import Blueprint, render_template
from app.models.galaxy import Galaxy

viewer_bp = Blueprint("viewer", __name__, url_prefix="/viewer")

@viewer_bp.route("/galaxy-map")
def galaxy_map():
    return render_template("galaxy_map/index.html")
@viewer_bp.route("/galaxy/<int:gid>")
def galaxy_detail(gid):
    g = Galaxy.query.get_or_404(gid)
    return render_template("galaxy_map/detail.html", galaxy=g)
