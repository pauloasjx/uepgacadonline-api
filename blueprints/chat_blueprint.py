from flask import Blueprint
from flask_socketio import emit, join_room

from blueprints import socketio
from models.user import User

chat_blueprint = Blueprint("chat", __name__)


@socketio.on('message', namespace='/chat')
def message(json):
    user = User.query.filter_by(token=json['token']).first()

    if user is not None:
        emit('message', {
            'academic_register': user['academic_register'],
            'name': user['name'],
            'message': json['message']
        })
