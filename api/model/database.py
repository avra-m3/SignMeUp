from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup(app):
    print("Initializing App")
    db.init_app(app)
    print("Creating Tables")
    db.create_all()
    db.session.commit()
    print("Done")
