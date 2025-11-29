from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login_get'))
    session['user_id'] = user.id
    session['username'] = user.username
    flash('Logged in', 'success')
    return redirect(url_for('dashboard.index'))

@auth_bp.route('/register', methods=['POST'])
def do_register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Provide username and password', 'danger')
        return redirect(url_for('auth.login_get'))
    if User.query.filter_by(username=username).first():
        flash('username already exists', 'danger')
        return redirect(url_for('auth.login_get'))
    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    flash('Registered — please login', 'success')
    return redirect(url_for('auth.login_get'))
