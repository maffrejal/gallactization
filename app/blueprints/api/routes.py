from flask import Blueprint, jsonify
from app.models import Galaxy

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/galaxies")
def api_galaxies():
    galaxies = Galaxy.query.limit(2000).all()  # reduce load for testing

    data = []
    for g in galaxies:

        # Convert ID to int (always safe)
        gid = int(g.id)

        # Generate deterministic coordinates from ID only
        x = ((gid * 7919) % 50000) - 25000
        y = ((gid * 15401) % 50000) - 25000

        data.append({
            "id": g.id,
            "name": g.name,
            "cluster": g.type,
            "x": x,
            "y": y
        })

    return jsonify(data)

