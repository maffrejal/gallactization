from flask import Blueprint, jsonify, request
from app.models import Lifeform

lifeforms_bp = Blueprint('lifeforms_api', __name__)

@lifeforms_bp.route('/<life_id>', methods=['GET'])
def get_lifeform(life_id):
    lf = Lifeform.query.get(life_id)
    if not lf:
        return jsonify({'error': 'lifeform not found'}), 404

    return jsonify(lf.to_dict())
