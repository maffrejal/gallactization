from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user, login_required
from app.models import User
from app.models.universe import Universe

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    universes = (
        Universe.query
        .filter_by(user_id=current_user.id)
        .order_by(Universe.created_at.desc())
        .all()
    )

    return render_template(
        'dashboard.html',
        user=current_user,
        universes=universes
    )
