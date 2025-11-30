from flask import Blueprint, render_template, jsonify, request, url_for, redirect
from app.services.biome_generator import list_biomes, generate_and_persist_biome, get_biome
from app.services.lifeform_generator import list_lifeforms, generate_and_persist_lifeform, get_lifeform

biomes_bp = Blueprint("biomes", __name__, template_folder="../../template", url_prefix="/biomes")

@biomes_bp.route("/")
def biomes_index():
    biomes = list_biomes(100)
    return render_template("biomes/index.html", biomes=biomes)

@biomes_bp.route("/api")
def biomes_api():
    b = list_biomes(500)
    return jsonify([{
        "id": x.id,
        "name": x.name,
        "base_type": x.base_type,
        "rarity": x.rarity
    } for x in b])

@biomes_bp.route("/generate", methods=["POST"])
def biomes_generate():
    seed = request.json.get("seed") if request.is_json else None
    b = generate_and_persist_biome(seed)
    return jsonify({"id": b.id, "name": b.name})

@biomes_bp.route("/<bid>")
def biome_detail(bid):
    b = get_biome(bid)
    if not b:
        return "Biome not found", 404
    # optionally list lifeforms linked by biome in meta or separate table - we'll show lifeforms that mention the biome
    lf = []  # you can implement a proper query if you persist biome link in lifeform.meta
    return render_template("biomes/detail.html", biome=b, lifeforms=lf)

# Lifeform endpoints
life_bp = Blueprint("lifeforms", __name__, template_folder="../../template", url_prefix="/lifeform")

@life_bp.route("/<lid>")
def life_detail(lid):
    l = get_lifeform(lid)
    if not l:
        return "Lifeform not found", 404
    return render_template("biomes/life_detail.html", lifeform=l)
