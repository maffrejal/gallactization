from flask import Blueprint, render_template, session, redirect, url_for
from ...models.galaxy import Galaxy
galaxy_bp = Blueprint('galaxy', __name__)

@galaxy_bp.route('/')
def list_galaxies():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    galaxies = Galaxy.query.limit(200).all()
    return render_template('galaxies.html', galaxies=galaxies)

@galaxy_bp.route('/view/<int:gid>')
def view_galaxy(gid):
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    g = Galaxy.query.get_or_404(gid)
    return render_template('galaxy_viewer.html', galaxy=g)
