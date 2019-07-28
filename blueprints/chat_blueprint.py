from flask import Blueprint, request
from flask_socketio import emit, join_room

from blueprints import socketio
from database import db
from models.message import Message
from models.user import User

import json

from utils.response import success, error

chat_blueprint = Blueprint("chat", __name__, url_prefix='/chat')


@chat_blueprint.route("/room", methods=["GET"])
def room():
    token = request.headers.get("x-api-token")
    room = request.form.get('room')

    user = User.query.filter_by(token=token).first()

    if user is not None:
        messages = Message.query.filter_by(
            academic_register=user.academic_register[:-2]).all() if room else Message.query.all()

        messages = [_message.dumps() for _message in messages]

        return success(message="Sala retornada com sucesso", messages=messages)

    else:
        return error(
            message="Token inválido"
        )


@socketio.on('message', namespace='/chat')
def message(data):
    data = json.loads(data)

    user = User.query.filter_by(token=data['token']).first()
    room = data.get('room')

    if user is not None:
        _message = Message(
            text=data['message'],
            name=user.name,
            room=room,
            academic_register=user.academic_register
        )

        db.session.add(_message)

        overflow = Message.query.count() - 5
        if overflow > 0:
            Message.query.filter_by(room=room) \
                .order_by(Message.id.asc()) \
                .limit(overflow) \
                .delete()

        db.session.commit()

        emit('message', {
            'academic_register': user.academic_register,
            'name': user.name,
            'message': data['message'],
            'room': room
        }, room=user.academic_register[:-2] if data.get('room') else None)
