import os
from flask_sqlalchemy import SQLAlchemy
import json
import flask


database_name = "bookshelf"
database_path = "postgresql://{}:{}@{}/{}".format(
    "student", "student", "localhost:5432", database_name)

db = SQLAlchemy()

"""
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)
    with app.app_context():
        db.create_all()


"""
Book

"""
class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    rating = db.Column(db.Integer)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
        }


