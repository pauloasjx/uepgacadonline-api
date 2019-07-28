from database import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cod = db.Column(db.Integer, nullable=False)
