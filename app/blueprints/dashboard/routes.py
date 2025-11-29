from flask import Blueprint, render_template, session, redirect, url_for
from app.models import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('auth.login_get'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)
