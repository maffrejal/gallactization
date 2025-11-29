from flask import Blueprint, request, jsonify, current_app, abort
from app.models import Biome, Lifeform
from app.extensions import db

biomes_bp = Blueprint('biomes_api', __name__)

def serialize_biome(b: Biome):
    d = b.to_dict()
    # don't include huge nested objects twice; they are JSON already
    return d

@biomes_bp.route('/', methods=['GET'])
def list_biomes():
    # pagination
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except ValueError:
        return jsonify({'error': 'invalid pagination parameters'}), 400

    # filters
    base_type = request.args.get('base_type')
    min_rarity = request.args.get('min_rarity', type=float)
    max_rarity = request.args.get('max_rarity', type=float)

    q = Biome.query
    if base_type:
        q = q.filter_by(base_type=base_type)
    if min_rarity is not None:
        q = q.filter(Biome.rarity >= min_rarity)
    if max_rarity is not None:
        q = q.filter(Biome.rarity <= max_rarity)

    pag = q.order_by(Biome.name).paginate(page=page, per_page=per_page, error_out=False)
    items = [serialize_biome(b) for b in pag.items]

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': pag.total,
        'pages': pag.pages,
        'items': items
    })

@biomes_bp.route('/<biome_id>', methods=['GET'])
def get_biome(biome_id):
    b = Biome.query.get(biome_id)
    if not b:
        return jsonify({'error': 'biome not found'}), 404

    # attach lifeforms (summaries)
    life_q = Lifeform.query.filter_by(biome_id=b.id).limit(200).all()
    life_summaries = [{'id': l.id, 'name': l.name, 'trophic_level': l.trophic_level, 'domain': l.domain} for l in life_q]

    data = b.to_dict()
    data['lifeforms'] = life_summaries

    return jsonify(data)
