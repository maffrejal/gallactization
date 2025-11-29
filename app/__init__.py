from flask import Flask, render_template
from app.extensions import db
from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.viewer import viewer_bp
from app.blueprints.api.routes import api_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'dev-gallactization'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:abc123@localhost:5432/gallactization"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(viewer_bp)
    app.register_blueprint(api_bp)

    @app.route('/')
    def home():
        return render_template('login.html')

    return app
