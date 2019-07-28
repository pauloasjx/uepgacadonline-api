from database import db
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    room = db.Column(db.Boolean, nullable=False)
    academic_register = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def dumps(self):
        return {
            'id': self.id,
            'text': self.text,
            'name': self.name,
            'room': self.room,
            'academic_register': self.academic_register,
            'created_at': self.created_at
        }

