from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    with app.app_context():
        db.app = app
        db.init_app(app)
