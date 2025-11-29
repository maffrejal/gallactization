from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
    print('DB ready — admin/password')
