from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JobSeeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume = db.Column(db.String(120), nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
