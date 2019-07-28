from flask import Blueprint
from flask_socketio import emit, join_room

from blueprints import socketio
# from database import db

chat_blueprint = Blueprint("chat", __name__)


@socketio.on('message', namespace='/chat')
def message(json):
    pass
    # user = db.get(json['token'])

    # if user is not None:
    #     emit('message', {
    #         'academic_register': user['academic_register'],
    #         'complete_name': user['complete_name'],
    #         'message': json['message']
    #     })
