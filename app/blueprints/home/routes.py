from flask import Blueprint, render_template, session, redirect, url_for
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # if logged in -> galaxy list, else show themed login page
    if session.get('user_id'):
        return redirect(url_for('galaxy.list_galaxies'))
    return render_template('login.html')
