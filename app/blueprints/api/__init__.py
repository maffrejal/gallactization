# API package initializer
from flask import Blueprint, jsonify
from app.models import Galaxy

api_bp = Blueprint("api", __name__, url_prefix="/api")

from flask import Blueprint, jsonify
from app.models import Galaxy

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/galaxies")
def api_galaxies():
    import os
    print(">>> USING ROUTES FILE:", os.path.abspath(__file__))  # DEBUG

    galaxies = Galaxy.query.limit(2000).all()

    data = []
    for g in galaxies:

        gid = int(g.id)

        # 100% safe coordinate generator – no seed used anywhere
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




# Register sub-blueprints in your app.create_app:
# from app.blueprints.api.biomes import biomes_bp
# from app.blueprints.api.lifeforms import lifeforms_bp
# app.register_blueprint(biomes_bp, url_prefix='/api/biomes')
# app.register_blueprint(lifeforms_bp, url_prefix='/api/lifeforms')
