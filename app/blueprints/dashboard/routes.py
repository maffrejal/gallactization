from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.galaxy import Galaxy
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    # Fetch all galaxies created for this user
    galaxies = Galaxy.query.filter(
        Galaxy.meta['created_for_user'].as_integer() == current_user.id
    ).all()

    return render_template(
        'dashboard.html',
        user=current_user,
        galaxies=galaxies
    )

